# 检查是否存在logs文件夹
import os
from module.tools.config import debug
from sys import stderr
from datetime import datetime

from loguru import logger

logs = os.path.join('logs')
if not os.path.exists(logs):
    os.mkdir(logs)

if not debug:
    logger.remove()
    logger.add(stderr, level="INFO")
logger.add(f"./logs/output_{datetime.strftime(datetime.now(), '%Y-%m-%d')}.log", format="[{time:MM-DD HH:mm:ss}] - {level}: {message}", rotation="00:00")
