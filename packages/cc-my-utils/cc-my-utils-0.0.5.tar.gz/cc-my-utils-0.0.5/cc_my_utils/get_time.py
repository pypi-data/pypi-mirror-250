#!/usr/bin/env python3

import datetime


def get_time(app):
    if app == 'notion':
        return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    