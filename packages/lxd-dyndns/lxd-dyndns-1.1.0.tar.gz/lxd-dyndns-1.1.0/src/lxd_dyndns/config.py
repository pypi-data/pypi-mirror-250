from ast import parse
import ipaddress
from typing import Any

import urllib.parse

from lxd_dyndns.dyndns_client import DNSConnectionTransport

from . import logger


CACHE_DIR = "/var/lib/lxd-dyndns"


def setup_config(config: dict[str, Any]) -> bool:
    config_valid = True

    if not "projects" in config:
        logger.error("Missing section [projects]")
        config_valid = False

    if not isinstance(config["projects"], dict):
        logger.error("Invalid projects section")
        config_valid = False

    for project, project_info in config["projects"].items():
        logger.debug("Parsing config for project: %s", project)

        if not isinstance(project_info, dict):
            logger.error(f"Invalid project definition for: {project}")
            config_valid = False
            continue

        if not "cache_dir" in project_info:
            if "cache_dir" in config:
                logger.debug(
                    f"Using global option for 'cache_dir' as option not specified for: {project}"
                )
                project_info["cache_dir"] = config["cache_dir"]
            else:
                project_info["cache_dir"] = CACHE_DIR
            logger.error(
                f"Using '{CACHE_DIR}' for caching as option 'cache_dir' is not specified"
            )

        if not "ipv4_prefixes" in project_info:
            if "ipv4_prefixes" in config:
                logger.debug(
                    f"Using global option for 'ipv4_prefixes' as option not specified for: {project}"
                )
                project_info["ipv4_prefixes"] = config["ipv4_prefixes"]
            else:
                logger.debug(
                    f"Will use all IPv4 addresses as option 'ipv4_prefixes' not specified for: {project}"
                )
                project_info["ipv4_prefixes"] = []
        if not isinstance(project_info["ipv4_prefixes"], list):
            logger.error(f"Invalid 'ipv4_prefixes' for: {project}")
            config_valid = False
        else:
            for prefix in project_info["ipv4_prefixes"]:
                try:
                    project_info["ipv4_prefixes"] = list(
                        map(ipaddress.IPv4Network, project_info["ipv4_prefixes"])
                    )
                except ValueError:
                    logger.error(f"Invalid 'ipv4_prefixes' for: {project}")
                    config_valid = False
                    break

        if not "ipv6_prefixes" in project_info:
            if "ipv6_prefixes" in config:
                logger.debug(
                    f"Using global option for 'ipv6_prefixes' as option not specified for: {project}"
                )
                project_info["ipv6_prefixes"] = config["ipv6_prefixes"]
            else:
                logger.debug(
                    f"Will use all IPv6 addresses as option 'ipv6_prefixes' not specified for: {project}"
                )
                project_info["ipv6_prefixes"] = []
        if not isinstance(project_info["ipv6_prefixes"], list):
            logger.error(f"Invalid 'ipv6_prefixes' for: {project}")
            config_valid = False
        else:
            for prefix in project_info["ipv6_prefixes"]:
                try:
                    project_info["ipv6_prefixes"] = list(
                        map(ipaddress.IPv6Network, project_info["ipv6_prefixes"])
                    )
                except ValueError:
                    logger.error(f"Invalid 'ipv6_prefixes' for: {project}")
                    config_valid = False
                    break

        if not "dns_server" in project_info:
            if "dns_server" in config:
                logger.debug(
                    f"Using global option for 'dns_server' as option not specified for: {project}"
                )
                project_info["dns_server"] = config["dns_server"]
            else:
                logger.error(f"Missing option 'dns_server' for: {project}")
                config_valid = False
        if "dns_server" in project_info and not isinstance(
            project_info["dns_server"], str
        ):
            logger.error(f"Invalid 'dns_server' for: {project}")
            config_valid = False

        if not "dns_port" in project_info:
            if "dns_port" in config:
                logger.debug(
                    f"Using global option for 'dns_port' as option not specified for: {project}"
                )
                project_info["dns_port"] = config["dns_port"]
            else:
                logger.debug(
                    f"Using DNS port 53 as option 'dns_port' not specified for: {project}"
                )
                project_info["dns_port"] = 53
        if "dns_port" in project_info and not isinstance(project_info["dns_port"], int):
            logger.error(f"Invalid 'dns_port' for: {project}")
            config_valid = False

        if not "dns_zone" in project_info:
            if "dns_zone" in config:
                logger.debug(
                    f"Using global option for 'dns_zone' as option not specified for: {project}"
                )
                project_info["dns_zone"] = config["dns_zone"]
            else:
                logger.error(f"Missing option 'dns_zone' for: {project}")
                config_valid = False
        if "dns_zone" in project_info and not isinstance(project_info["dns_zone"], str):
            logger.error(f"Invalid 'dns_zone' for: {project}")
            config_valid = False

        if not "dns_transport" in project_info:
            if "dns_transport" in config:
                logger.debug(
                    f"Using global option for 'dns_transport' as option not specified for: {project}"
                )
                project_info["dns_transport"] = config["dns_transport"]
            else:
                logger.debug(
                    f"Using 'udp' for DNS as option 'dns_transport' not specified for: {project}"
                )
                project_info["dns_transport"] = "udp"
        if not isinstance(project_info["dns_transport"], str):
            logger.error(f"Invalid 'dns_transport' for: {project}")
            config_valid = False
        else:
            project_info["dns_transport"] = DNSConnectionTransport.from_string(
                project_info["dns_transport"]
            )

        if not "dns_key_name" in project_info:
            if "dns_key_name" in config:
                logger.debug(
                    f"Using global option for 'dns_key_name' as option not specified for: {project}"
                )
                project_info["dns_key_name"] = config["dns_key_name"]
            else:
                logger.error(f"Missing option 'dns_key_name' for: {project}")
                config_valid = False
        if "dns_key_name" in project_info and not isinstance(
            project_info["dns_key_name"], str
        ):
            logger.error(f"Invalid 'dns_key_name' for: {project}")
            config_valid = False

        if not "dns_key_secret" in project_info:
            if "dns_key_secret" in config:
                logger.debug(
                    f"Using global option for 'dns_key_secret' as option not specified for: {project}"
                )
                project_info["dns_key_secret"] = config["dns_key_secret"]
            else:
                logger.error(f"Missing option 'dns_key_secret' for: {project}")
                config_valid = False
        if "dns_key_secret" in project_info and not isinstance(
            project_info["dns_key_secret"], str
        ):
            logger.error(f"Invalid 'dns_key_secret' for: {project}")
            config_valid = False

        if not "lxd_server" in project_info:
            if "lxd_server" in config:
                logger.debug(
                    f"Using global option for 'lxd_server' as option not specified for: {project}"
                )
                project_info["lxd_server"] = config["lxd_server"]
            else:
                logger.error(f"Missing option 'lxd_server' for: {project}")
                config_valid = False
        if "lxd_server" in project_info and not isinstance(
            project_info["lxd_server"], str
        ):
            logger.error(f"Invalid 'lxd_server' for: {project}")
            config_valid = False

        if not "lxd_client_cert" in project_info:
            if "lxd_client_cert" in config:
                logger.debug(
                    f"Using global option for 'lxd_client_cert' as option not specified for: {project}"
                )
                project_info["lxd_client_cert"] = config["lxd_client_cert"]
            else:
                logger.error(f"Missing option 'lxd_client_cert' for: {project}")
                config_valid = False
        if "lxd_client_cert" in project_info and not isinstance(
            project_info["lxd_client_cert"], str
        ):
            logger.error(f"Invalid 'lxd_client_cert' for: {project}")
            config_valid = False

        if not "lxd_client_key" in project_info:
            if "lxd_client_key" in config:
                logger.debug(
                    f"Using global option for 'lxd_client_key' as option not specified for: {project}"
                )
                project_info["lxd_client_key"] = config["lxd_client_key"]
            else:
                logger.error(f"Missing option 'lxd_client_key' for: {project}")
                config_valid = False
        if "lxd_client_key" in project_info and not isinstance(
            project_info["lxd_client_key"], str
        ):
            logger.error(f"Invalid 'lxd_client_key' for: {project}")
            config_valid = False

        if not "lxd_verify" in project_info:
            if "lxd_verify" in config:
                logger.debug(
                    f"Using global option for 'lxd_verify' as option not specified for: {project}"
                )
                project_info["lxd_verify"] = config["lxd_verify"]
            else:
                logger.debug(
                    f"Using 'true' for 'lxd_verify' as option not specified for: {project}"
                )
                project_info["lxd_verify"] = "true"
        if "lxd_verify" in project_info and not isinstance(
            project_info["lxd_verify"], bool
        ):
            logger.error(f"Invalid 'lxd_verify' for: {project}")
            config_valid = False

        if not "refresh_interval" in project_info:
            if "refresh_interval" in config:
                logger.debug(
                    f"Using global option for 'refresh_interval' as option not specified for: {project}"
                )
                project_info["refresh_interval"] = config["refresh_interval"]
            else:
                logger.debug(
                    f"Using 30 seconds for 'refresh_interval' as option not specified for: {project}"
                )
                project_info["refresh_interval"] = 30
        if "refresh_interval" in project_info and not isinstance(
            project_info["refresh_interval"], int
        ):
            logger.error(f"Invalid 'refresh_interval' for: {project}")
            config_valid = False

    return config_valid
