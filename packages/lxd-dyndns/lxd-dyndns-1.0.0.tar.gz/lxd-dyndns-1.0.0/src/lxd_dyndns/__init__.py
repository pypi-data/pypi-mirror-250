import logging

import asyncio

try:
    import uvloop  # type: ignore

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass

logger = logging.getLogger("lxd-dyndns")

handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s]   \t%(name)s: %(message)s")
)

logger.addHandler(handler)

logger.setLevel(logging.DEBUG)
