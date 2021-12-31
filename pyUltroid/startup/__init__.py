# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/pyUltroid/blob/main/LICENSE>.

import os
import platform
import sys
import time
from logging import INFO, WARNING, FileHandler, StreamHandler, basicConfig, getLogger

from safety.tools import *
from telethon import __version__

from ..version import __version__ as __pyUltroid__
from ..version import ultroid_version

file = f"ultroid{sys.argv[6]}.log" if len(sys.argv) > 6 else "ultroid.log"
if os.path.exists(file):
    os.remove(file)

LOGS = getLogger("pyUltLogs")
TelethonLogger = getLogger("Telethon")
TelethonLogger.setLevel(INFO)

_, v, __ = platform.python_version_tuple()

if int(v) < 10:
    from ._extra import _fix_logging

    _fix_logging(FileHandler)

basicConfig(
    format="%(asctime)s || %(name)s [%(levelname)s] : %(message)s",
    level=INFO,
    datefmt="%m/%d/%Y, %H:%M:%S",
    handlers=[FileHandler(file), StreamHandler()],
)

LOGS.info(
    """
                -----------------------------------
                        Starting Deployment
                -----------------------------------
"""
)

LOGS.info(f"Python version - {platform.python_version()}")
LOGS.info(f"py-Ultroid Version - {__pyUltroid__}")
LOGS.info(f"Telethon Version - {__version__}")
LOGS.info(f"Ultroid Version - {ultroid_version}")
