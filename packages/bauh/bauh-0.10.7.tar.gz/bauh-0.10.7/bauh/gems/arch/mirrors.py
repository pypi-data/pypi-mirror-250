import logging
import os
import time
import traceback
from datetime import datetime
from logging import Logger
from pathlib import Path

from bauh.api.paths import CACHE_DIR

SYNC_FILE = f'{CACHE_DIR}/arch/mirrors_sync'


def should_sync(logger: logging.Logger):
    if os.path.exists(SYNC_FILE):
        with open(SYNC_FILE) as f:
            sync_file = f.read()

        try:
            sync_time = datetime.fromtimestamp(int(sync_file))
            now = datetime.now()

            if now > sync_time and now.day != sync_time.day:
                logger.info("Package databases synchronization out of date")
            else:
                msg = "Package databases already synchronized"
                logger.info(msg)
                return False
        except Exception:
            logger.warning("Could not convert the database synchronization time from '{}".format(SYNC_FILE))
            traceback.print_exc()
    return True


def register_sync(logger: Logger):
    try:
        Path('/'.join(SYNC_FILE.split('/')[0:-1])).mkdir(parents=True, exist_ok=True)
        with open(SYNC_FILE, 'w+') as f:
            f.write(str(int(time.time())))
    except Exception:
        logger.error("Could not write to mirrors sync file '{}'".format(SYNC_FILE))
        traceback.print_exc()
