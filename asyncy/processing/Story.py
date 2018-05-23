# -*- coding: utf-8 -*-
from .Handler import Handler
from ..Stories import Stories
from ..constants import ContextConstants


class Story:

    @staticmethod
    def story(app, logger, story_name):
        return Stories(app, story_name, logger)

    @staticmethod
    def save(logger, story, start):
        """
        Saves the narration and the results for each line.
        """
        logger.log('story-save', story.name, story.app_id)

    @staticmethod
    def execute(app, logger, story, skip_server_finish=False):
        """
        Executes each line in the story
        """
        line_number = story.first_line()
        while line_number:
            line_number = Handler.run(logger, line_number, story)
            logger.log('story-execution', line_number)
            if line_number:
                if line_number.endswith('.story'):
                    line_number = Story.run(app, logger, line_number,
                                            skip_server_finish=True)

        if skip_server_finish is False:
            # If we're running in an http context, then we need to call finish
            # on Tornado's response object.
            server_request = story.context.get(ContextConstants.server_request)
            if server_request:
                if server_request.is_not_finished():
                    story.logger.log_raw('debug',
                                         'Closing Tornado\'s response')
                    story.context[ContextConstants.server_io_loop] \
                        .add_callback(server_request.finish)

    @classmethod
    def run(cls, app, logger, story_name, *, story_id=None,
            start=None, block=None, context=None, skip_server_finish=False):
        logger.log('story-start', story_name, story_id)
        story = cls.story(app, logger, story_name)
        story.prepare(context, start, block)
        cls.execute(app, logger, story, skip_server_finish=skip_server_finish)
        logger.log('story-end', story_name, story_id)
