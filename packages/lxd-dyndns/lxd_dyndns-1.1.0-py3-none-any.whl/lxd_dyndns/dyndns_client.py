import argparse
import asyncio
from calendar import c
from copy import deepcopy
import enum
import os
import pickle
import logging
from typing import TypedDict
from pylxd import Client

import ipaddress

import dns.asyncquery
import dns.tsigkeyring
import dns.update

from . import logger


class DNSConnectionTransport(enum.Enum):
    TCP = 0
    UDP = 1

    def __str__(self) -> str:
        return self.name

    @staticmethod
    def from_string(s: str):
        try:
            return DNSConnectionTransport[s]
        except KeyError:
            raise ValueError()


class DDNSContainerCache(TypedDict):
    ipv4_addrs: list[ipaddress.IPv4Address]
    ipv6_addrs: list[ipaddress.IPv6Address]


DDNSProjectCache = dict[str, DDNSContainerCache]


class DDNSClientOptions(TypedDict):
    ipv4_prefixes: list[ipaddress.IPv4Network]
    ipv6_prefixes: list[ipaddress.IPv6Network]
    dns_server: str
    dns_port: int
    dns_zone: str
    dns_transport: DNSConnectionTransport
    dns_key_name: str
    dns_key_secret: str
    cache_dir: str
    client: Client
    refresh_interval: int


class DDNSClient:
    def __init__(self, options: DDNSClientOptions):
        self.options = options
        self.load_cache()

    @property
    def project(self):
        return self.options["client"].project

    @property
    def cache(self):
        return os.path.join(self.options["cache_dir"], f"{self.project}.pkl")

    def save_cache(self):
        logger.info(f"[{self.project}] Saving cache")
        if not os.path.isdir(self.options["cache_dir"]):
            logger.info(f"[{self.project}] Creating cache directory")
            os.makedirs(self.options["cache_dir"])
        with open(
            self.cache,
            "wb",
        ) as f:
            pickle.dump(self.ddns_cache, f)
        logger.info(f"[{self.project}] Saved cache")

    def load_cache(self):
        logger.info(f"[{self.project}] Loading cache")
        try:
            with open(
                self.cache,
                "rb",
            ) as f:
                self.ddns_cache = pickle.load(f)
            logger.info(f"[{self.project}] Loaded cache")
        except FileNotFoundError:
            logger.warning(f"[{self.project}] Cache not found")
            self.ddns_cache = DDNSProjectCache()
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.save_cache()

    async def refresh(self):
        logger.debug(f"[{self.project}] Finding all containers and virtual machines")

        tasks = []

        containers = self.options["client"].containers.all()  # type: ignore
        for container in containers:
            if container.status == "Stopped":
                tasks.append(self.instance_remove(container))
            elif container.status == "Running":
                tasks.append(self.instance_add(container))

        virtual_machines = self.options["client"].virtual_machines.all()  # type: ignore
        for vm in virtual_machines:
            if vm.status == "Stopped":
                tasks.append(self.instance_remove(vm))
            if vm.status == "Running":
                tasks.append(self.instance_add(vm))

        await asyncio.gather(*tasks)

    async def instance_add(self, container):
        container_name = container.name
        logger.info(f"[{self.project} - {container_name}] Registering container")

        new_addresses = ([], [])

        networks = container.state().network
        for iface in networks:
            logger.debug(
                f"[{self.project} - {container_name}] Found interface: %s", iface
            )
            setting = networks[iface]
            addresses = setting["addresses"]
            for addr in addresses:
                if addr["scope"] == "global" and addr["family"] == "inet":
                    container_ip = ipaddress.IPv4Address(addr["address"])
                    if not self.options["ipv4_prefixes"] or any(
                        container_ip in prefix
                        for prefix in self.options["ipv4_prefixes"]
                    ):
                        new_addresses[0].append(container_ip)
                if addr["scope"] == "global" and addr["family"] == "inet6":
                    container_ip = ipaddress.IPv6Address(addr["address"])
                    if not self.options["ipv6_prefixes"] or any(
                        container_ip in prefix
                        for prefix in self.options["ipv6_prefixes"]
                    ):
                        new_addresses[1].append(container_ip)
        logger.debug(
            f"[{self.project} - {container_name}] Found valid addresses: %s",
            new_addresses,
        )
        await self.instance_update(container_name, new_addresses)

    async def instance_remove(self, container):
        container_name = container.name
        logger.info(
            f"[{self.project} - {container_name}] Removing all records for container"
        )
        await self.instance_update(container_name, ([], []))

    async def instance_update(
        self,
        container_name: str,
        addresses: tuple[list[ipaddress.IPv4Address], list[ipaddress.IPv6Address]],
    ):
        logger.info(f"[{self.project} - {container_name}] Updating container")

        logger.debug(f"[{self.project} - {container_name}] Creating keyring")
        keyring = dns.tsigkeyring.from_text(
            {self.options["dns_key_name"]: self.options["dns_key_secret"]}
        )
        logger.debug(f"[{self.project} - {container_name}] Creating DNS updater")
        dns_updater = dns.update.Update(self.options["dns_zone"], keyring=keyring)

        if container_name not in self.ddns_cache:
            logger.debug(f"[{self.project} - {container_name}] Adding to cache")
            self.ddns_cache[container_name] = DDNSContainerCache(
                ipv4_addrs=[], ipv6_addrs=[]
            )

        to_update = False
        new_addresses = deepcopy(self.ddns_cache[container_name])

        for ipv4 in self.ddns_cache[container_name]["ipv4_addrs"]:
            if ipv4 not in addresses[0]:
                logger.debug(
                    f"[{self.project} - {container_name}] Removing address %s",
                    ipv4,
                )
                dns_updater.delete(container_name, "A")
                new_addresses["ipv4_addrs"].remove(ipv4)
                to_update = True
        for ipv6 in self.ddns_cache[container_name]["ipv6_addrs"]:
            if ipv6 not in addresses[1]:
                logger.debug(
                    f"[{self.project} - {container_name}] Removing address %s",
                    ipv6,
                )
                dns_updater.delete(container_name, "AAAA")
                new_addresses["ipv6_addrs"].remove(ipv6)
                to_update = True

        for ipv4 in addresses[0]:
            if ipv4 not in self.ddns_cache[container_name]["ipv4_addrs"]:
                logger.debug(
                    f"[{self.project} - {container_name}] Adding address %s",
                    ipv4,
                )
                dns_updater.add(container_name, 300, "A", str(ipv4))
                new_addresses["ipv4_addrs"].append(ipv4)
                to_update = True
        for ipv6 in addresses[1]:
            if ipv6 not in self.ddns_cache[container_name]["ipv6_addrs"]:
                logger.debug(
                    f"[{self.project} - {container_name}] Adding address %s",
                    ipv6,
                )
                dns_updater.add(container_name, 300, "AAAA", str(ipv6))
                new_addresses["ipv6_addrs"].append(ipv6)
                to_update = True

        if to_update:
            logger.info(f"[{self.project} - {container_name}] Sending DNS update")
            if self.options["dns_transport"] == DNSConnectionTransport.TCP:
                response = await dns.asyncquery.tcp(
                    dns_updater,
                    self.options["dns_server"],
                    port=self.options["dns_port"],
                )
            else:
                response = await dns.asyncquery.udp(
                    dns_updater,
                    self.options["dns_server"],
                    port=self.options["dns_port"],
                )
            if response.rcode() != 0:
                logger.error(f"[{self.project} - {container_name}] DNS update failed: %s", dns.rcode.to_text(response.rcode()))  # type: ignore
                return
            logger.info(f"[{self.project} - {container_name}] DNS update successful")
            self.ddns_cache[container_name] = new_addresses
        else:
            logger.info(f"[{self.project} - {container_name}] No DNS update needed")

    async def run(self):
        while True:
            logger.debug(f"[{self.project}] Refreshing")
            await self.refresh()
            self.save_cache()
            await asyncio.sleep(int(self.options["refresh_interval"]))
