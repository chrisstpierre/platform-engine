# -*- coding: utf-8 -*-
import docker


class Containers:

    def __init__(self, name):
        self.name = name

    def run(self, command=None):
        client = docker.from_env()
        self.result = client.containers.run(command=command)