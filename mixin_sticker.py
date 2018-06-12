# -*- coding: utf-8 -*-


class URI(object):

    @staticmethod
    def albums(id=None):
        return id and "stickers/albums/%s" % id or "stickers/albums"


def albums(self):
    return self.jwtGetRequest(URI.albums())


def stickers(self, id):
    return self.jwtGetRequest(URI.albums(id))
