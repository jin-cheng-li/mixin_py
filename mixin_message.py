# -*- coding: utf-8 -*-


class URI(object):
    acknowledge = "messages/acknowledge"

    @staticmethod
    def attachments(id=None):
        return id and "%s/%s" % ("attachments", id) or "attachments"

    @staticmethod
    def messageStatus(offset):
        return "messages/status/%s"


def messageStatus(self, offset):
    return self.jwtGetRequest(URI.messageStatus(offset))


def requestAttachment(self):
    return self.jwtRequest(URI.attachments())


def getAttachment(self, id):
    return self.jwtGetRequest(URI.attachments(id))
