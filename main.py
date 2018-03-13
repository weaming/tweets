#!/usr/bin/env python
# coding: utf-8

from config import app_conf
from tweet import app
import fire

class Cmd(object):
    def run(self, user=None):
        if user:
            app_conf['twitter_id'] = user

        app.run(debug=False)

    def debug(self, user='instagram'):
        if user:
            app_conf['twitter_id'] = user

        app.run(debug=True)

fire.Fire(Cmd)

