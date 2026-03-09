import asyncio
import logging

import docker

from .server import run_stdio
from .settings import ServerSettings


def main():
    """Run the server sourcing configuration from environment variables."""
    settings = ServerSettings()
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.WARNING),
        format="%(levelname)s: %(message)s",
    )
    asyncio.run(run_stdio(settings, docker.from_env()))


# Optionally expose other important items at package level
__all__ = ["main", "run_stdio", "ServerSettings"]

