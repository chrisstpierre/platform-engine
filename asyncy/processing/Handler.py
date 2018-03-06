# -*- coding: utf-8 -*-
from .Lexicon import Lexicon
from ..models import Mongo


class Handler:
    """
    Handles various task-related things.
    """

    @staticmethod
    def init_mongo(mongo_url):
        return Mongo(mongo_url)

    @staticmethod
    def make_environment(logger, story, application):
        """
        Makes the environment from story and application.
        """
        environment = story.environment()
        application_environment = application.environment(story.filename)
        for key, value in environment.items():
            if key in application_environment:
                environment[key] = application_environment[key]
        logger.log('container-environment', environment)
        return environment

    @staticmethod
    def run(logger, line_number, story, environment):
        """
        Run the story
        """
        story.start_line(line_number)
        line = story.line(line_number)

        if line['method'] == 'if':
            return Lexicon.if_condition(logger, story, line)
        elif line['method'] == 'next':
            return Lexicon.next(logger, story, line)
        elif line['method'] == 'run':
            Lexicon.run(logger, story, line, environment)