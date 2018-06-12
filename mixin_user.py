# -*- coding: utf-8 -*-


class URI(object):
    users = "users/fetch"
    relationships = "relationships"

    @staticmethod
    def search(keyword):
        return "search/%s" % keyword

    @staticmethod
    def codes(codeId):
        return "codes/%s" % codeId

    @staticmethod
    def users(id=None):
        return id and "users/%s" % id or "users"


class RelationshipAction(object):
    ADD = "ADD"
    REMOVE = "REMOVE"
    UPDATE = "UPDATE"
    BLOCK = "BLOCK"
    UNBLOCK = "UNBLOCK"


def codes(self, codeId):
    return self.jwtGetRequest(URI.codes(codeId))


def showUser(self, userId):
    return self.jwtGetRequest(URI.users(userId))


def showUsers(self, userIds):
    return self.jwtRequest(URI.users(), userIds)


def search(self, keyword):
    return self.jwtGetRequest(URI.search(keyword))


def addFriend(self, userId, full_name):
    body = {
        "userId": userId,
        "full_name": full_name,
        "action": RelationshipAction.ADD
    }
    return self.jwtRequest(URI.relationships, body)


def removeFriend(self, userId):
    body = {
        "userId": userId,
        "action": RelationshipAction.REMOVE
    }
    return self.jwtRequest(URI.relationships, body)


def remarkFriend(self, userId, full_name):
    body = {
        "userId": userId,
        "full_name": full_name,
        "action": RelationshipAction.UPDATE
    }
    return self.jwtRequest(URI.relationships, body)


def blockUser(self, userId):
    body = {
        "userId": userId,
        "action": RelationshipAction.BLOCK
    }
    return self.jwtRequest(URI.relationships, body)


def unblockUser(self, userId):
    body = {
        "userId": userId,
        "action": RelationshipAction.UNBLOCK
    }
    return self.jwtRequest(URI.relationships, body)
