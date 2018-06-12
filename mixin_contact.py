# -*- coding: utf-8 -*-
class URI(object):
    contacts = "friends"


def getContacts(self):
    return self.jwtGetRequest(URI.contacts)
