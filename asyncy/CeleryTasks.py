# -*- coding: utf-8 -*-
from .CeleryApp import CeleryApp
from .Config import Config
from .Logger import Logger
from .processing import Story


config = Config()
logger = Logger(config)
logger.start()

app = CeleryApp.start(config)


@app.task
def process_story(app_id, story_name, story_id=None):
    logger.log('task-received', app_id, story_name)
    Story.run(config, logger, app_id, story_name, story_id=story_id)
