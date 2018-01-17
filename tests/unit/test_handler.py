# -*- coding: utf-8 -*-
from evenflow.Config import Config
from evenflow.Containers import Containers
from evenflow.Handler import Handler
from evenflow.Lexicon import Lexicon
from evenflow.models import db

from playhouse import db_url

from pytest import fixture

from storyscript import resolver


@fixture
def config(mocker):
    mocker.patch.object(Config, 'get')


@fixture
def resolve_obj(mocker):
    mocker.patch.object(resolver, 'resolve_obj')


@fixture
def line():
    line = {'ln': '1', 'container': 'hello-world', 'args': 'args',
            'method': None}
    return line


def test_handler_init_db(mocker, config):
    mocker.patch.object(db, 'init')
    mocker.patch.object(db_url, 'parse')
    Handler.init_db()
    Config.get.assert_called_with('database')
    db_url.parse.assert_called_with(Config.get())
    db.init.assert_called_with(db_url.parse())


def test_build_story(mocker, config):
    story = mocker.MagicMock()
    Handler.build_story(story)
    story.provider.assert_called_with(Config.get(), Config.get())
    assert story.build_tree.call_count == 1


def test_handler_run(mocker, resolve_obj, line):
    mocker.patch.object(Containers, 'run')
    mocker.patch.object(Containers, 'result')
    mocker.patch.object(Containers, '__init__', return_value=None)
    context = {}
    result = Handler.run(line, {'data': 'data'}, context)
    resolver.resolve_obj.assert_called_with({'data': 'data'}, line['args'])
    Containers.__init__.assert_called_with('hello-world')
    Containers.run.assert_called_with(*resolver.resolve_obj())
    assert context['result'] == Containers.result()
    assert result == '1'


def test_handler_run_if(mocker, resolve_obj, line):
    mocker.patch.object(Lexicon, 'if_condition')
    line['method'] = 'if'
    result = Handler.run(line, {'data': 'data'}, {})
    assert result == Lexicon.if_condition()