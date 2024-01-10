import argparse
import asyncio
import os
import tomllib

from pylxd import Client as LXDClient
import urllib3

from . import asyncio, logger
from .config import setup_config
from .dyndns_client import DDNSClient, DDNSClientOptions

# Disable warnings about insecure requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser(description="LXD dynamic DNS client")
parser.add_argument(
    "-f",
    metavar="file",
    type=str,
    help="config file, see `man 5 lxd-dyndns.conf` for details",
    default="/etc/lxd-dyndns.conf",
)
parser.add_argument("-n", action="store_true", help="configtest mode")
parser.add_argument(
    "-d",
    help="debug level",
    choices=["debug", "info", "warn", "error", "critical"],
    default="info",
)


def run() -> int:
    args = parser.parse_args()
    logger.setLevel(args.d.upper())

    loop = asyncio.get_event_loop()
    clients: list[DDNSClient] = []

    with open(args.f, "rb") as f:
        config = tomllib.load(f)

        if not setup_config(config):
            logger.error("Invalid config file")
            return 1

        logger.info("Config file is valid")
        if args.n:
            return 0

        cache_dir = config["cache_dir"]

        for project, options in config["projects"].items():
            logger.info("Creating handlers for project: %s", project)

            lxd_client = LXDClient(
                endpoint=options["lxd_server"],
                cert=(options["lxd_client_cert"], options["lxd_client_key"]),
                verify=options["lxd_verify"],
                project=project,
            )

            ddns_options = DDNSClientOptions(
                ipv4_prefixes=options["ipv4_prefixes"],
                ipv6_prefixes=options["ipv6_prefixes"],
                dns_server=options["dns_server"],
                dns_port=options["dns_port"],
                dns_zone=options["dns_zone"],
                dns_transport=options["dns_transport"],
                dns_key_name=options["dns_key_name"],
                dns_key_secret=options["dns_key_secret"],
                cache_dir=os.path.join(cache_dir, project),
                client=lxd_client,
                refresh_interval=options["refresh_interval"],
            )
            ddns_client = DDNSClient(ddns_options)

            clients.append(ddns_client)

    tasks = asyncio.gather(
        *[loop.create_task(ddns_client.run()) for ddns_client in clients]
    )
    loop.run_until_complete(tasks)

    return 0
