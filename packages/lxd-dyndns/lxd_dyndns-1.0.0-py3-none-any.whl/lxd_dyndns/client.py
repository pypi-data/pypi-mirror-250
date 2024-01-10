import asyncio
import json
import ssl
import tomllib

import urllib.parse
import aiohttp
import websockets

from . import logger


_EVENTS_PATH = "/1.0/events?type=lifecycle&project={0}"
_STATE_PATH = "/1.0/instances/{0}/state?project={1}"
_INTERESTING_EVENTS = [
    "instance-created",
    "instance-deleted",
    "instance-ready",
    "instance-renamed",
    "instance-restarted",
    "instance-shutdown",
    "instance-started",
    "instance-stopped",
    "instance-updated",
]


class LXDDynDNSClient:
    def __init__(self, config_file: str):
        logger.info("Parsing config file: %s", config_file)
        with open(config_file, "rb") as f:
            self.config = tomllib.load(f)
        if not self.setup_config():
            raise RuntimeError("Invalid config file")

    def setup_config(self) -> bool:
        if not "projects" in self.config:
            logger.error("Missing section [projects]")
            return False
        for project in self.config["projects"]:
            project_info = self.config["projects"][project]
            if not isinstance(project_info, dict):
                raise RuntimeError("Invalid project definition")
            if not "url" in project_info:
                raise RuntimeError("Missing option 'url' for project")

            logger.info("Parsing config for project: %s", project)

            url = project_info["url"]
            parsed_url = urllib.parse.urlparse(url)
            project_info["parsed_url"] = parsed_url

            project_info["unix_socket"] = False
            if parsed_url.scheme not in ["ws", "wss"]:
                raise RuntimeError("Invalid scheme for project")
            if parsed_url.hostname is None:
                if parsed_url.path is None:
                    raise RuntimeError("Missing hostname or path for project")
                elif parsed_url.path.startswith("/"):
                    project_info["unix_socket"] = True
                else:
                    raise RuntimeError(f"Invalid path for project: {parsed_url.path}")
                # TODO - support unix sockets
                raise NotImplementedError("No unix socket support yet")
            else:
                logger.debug(f"Hostname: {parsed_url.hostname}")
                project_info["hostname"] = parsed_url.hostname
                if parsed_url.port is None:
                    project_info["port"] = 8443
                else:
                    project_info["port"] = parsed_url.port

            # check if we need to use ssl
            ssl_context = None
            if parsed_url.scheme == "wss":
                logger.info("Using SSL")
                ssl_context = ssl.create_default_context()
                if "noverify" in project_info and project_info["noverify"]:
                    logger.warning("Disabling SSL verification")
                    ssl_context.check_hostname = False
                    ssl_context.verify_mode = ssl.CERT_NONE
                elif "cafile" in project_info:
                    # FIXME - doesn't seem to be working!?
                    logger.debug(f"Loading CA file: {project_info['cafile']}")
                    ssl_context = ssl.create_default_context(
                        cafile=project_info["cafile"]
                    )

                if "certfile" in project_info and "keyfile" in project_info:
                    logger.debug(
                        f"Loading client side certificates - certfile: {project_info['certfile']}, keyfile: {project_info['keyfile']}"
                    )
                    ssl_context.load_cert_chain(
                        certfile=project_info["certfile"],
                        keyfile=project_info["keyfile"],
                    )
                events_path = _EVENTS_PATH.format(project)
                project_info[
                    "websocket_url"
                ] = f"wss://{project_info['hostname']}:{project_info['port']}{events_path}"
                project_info[
                    "request_url"
                ] = f"https://{project_info['hostname']}:{project_info['port']}"
            else:
                # TODO - support non-SSL connections
                raise NotImplementedError("No non-SSL support yet")
            project_info["ssl_context"] = ssl_context

        return True

    async def start(self):
        logger.info("Starting LXD Dynaminc DNS client")
        async with aiohttp.ClientSession() as self.client_session:
            await asyncio.gather(
                *map(
                    self.start_project,
                    [
                        (project, self.config["projects"][project])
                        for project in self.config["projects"]
                    ],
                )
            )

    async def start_project(self, data: tuple[str, dict]):
        name = data[0]
        project_info = data[1]

        logger.info(f"Starting to monitor project {name}")

        # check if socket or not
        if project_info["unix_socket"]:
            logger.info(
                f"Connecting to unix websocket {project_info['parsed_url'].path}"
            )
            async for websocket in websockets.unix_connect(
                project_info["parsed_url"].path,
                logger=logger,
                ssl=project_info["ssl_context"],
            ):
                await self.handle_websocket(websocket, name, project_info)
        else:
            logger.info(f"Connecting to socket {project_info['websocket_url']}")
            async for websocket in websockets.connect(
                project_info["websocket_url"],
                logger=logger,
                ssl=project_info["ssl_context"],
            ):
                await self.handle_websocket(websocket, name, project_info)

    async def handle_websocket(
        self,
        websocket: websockets.WebSocketClientProtocol,
        name: str,
        project_info: dict,
    ):
        async for raw_message in websocket:
            logger.debug(f"Received message: {raw_message}")
            # location: worker01
            # metadata:
            #   action: instance-created
            #   context:
            #     location: worker01
            #     storage-pool: local
            #     type: container
            #   name: epsilon2
            #   project: homelab
            #   source: /1.0/instances/epsilon2?project=homelab
            # project: homelab
            # timestamp: "2023-12-25T00:19:53.821687129-05:00"
            # type: lifecycle
            await websocket.recv()
            message = json.loads(raw_message)
            logger.debug(f"Message: {message}")
            if message["metadata"]["action"] not in _INTERESTING_EVENTS:
                logger.debug(
                    "Ignoring message with action: %s", message["metadata"]["action"]
                )
            else:
                logger.info("Processing message")
                for instance in [message["metadata"]["source"]]:
                    # get instance information
                    logger.info(f"Processing instance: {instance}")
                    instance_url = f"{project_info['request_url']}{instance}"
                    logger.info(f"Getting instance information from {instance_url}")
                    async with self.client_session.get(
                        instance_url, ssl=project_info["ssl_context"]
                    ) as instance_info:
                        instance_json = await instance_info.json()
                        logger.info(f"Got instance information: {instance_info}")
                        instance_pretty = json.dumps(instance_json, indent=4)
                        print(instance_pretty)
                        instance_name = instance_json["metadata"]["name"]
                    state_url = f"{project_info['request_url']}{_STATE_PATH.format(instance_name, name)}"
                    async with self.client_session.get(
                        state_url, ssl=project_info["ssl_context"]
                    ) as state_info:
                        state_json = await state_info.json()
                        logger.info(f"Got instance state information: \n{state_info}")
                        state_pretty = json.dumps(state_json, indent=4)
                        print(state_pretty)
