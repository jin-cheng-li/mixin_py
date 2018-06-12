# -*- coding: utf-8 -*-
class Scope(object):
    PROFILE = "PROFILE:READ"
    PHONE = "PHONE:READ"
    ASSETS = "ASSETS:READ"
    APPS_READ = "APPS:READ"
    APPS_WRITE = "APPS:WRITE"
    CONTACTS_READ = "CONTACTS:READ"


class URI(object):
    authorize = "oauth/authorize"


def authorize(self):
    pass
