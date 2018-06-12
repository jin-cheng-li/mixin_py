# -*- coding: utf-8 -*-
import md5
import uuid


class URI(object):
    contacts = "friends"

    @staticmethod
    def conversations(id=None):
        return id and 'conversations/%s' % id or 'conversations'

    @staticmethod
    def participants(id, action):
        return 'conversations/%s/participants/%s' % (id, action)

    @staticmethod
    def exit(id):
        return 'conversations/%s/exit' % id

    @staticmethod
    def join(codeId):
        return 'conversations/%s/join' % codeId

    @staticmethod
    def mute(conversationId):
        return 'conversations/%s/mute' % conversationId

    @staticmethod
    def reset(conversationId):
        return 'conversations/%s/reset' % conversationId


class ConversationCategory(object):
    GROUP = "GROUP"
    CONTACT = "CONTACT"


class ParticipantAction(object):
    ADD = "ADD"
    REMOVE = "REMOVE"
    JOIN = "JOIN"
    EXIT = "EXIT"
    ROLE = "ROLE"


class ParticipantRole(object):
    OWNER = "OWNER"
    ADMIN = "ADMIN"


def genConversationId(self, user_id, client_id=None):
    n = md5.new()
    n.update(user_id)
    n.update(client_id or self.client_id)
    result = n.digest()
    result_6 = chr((ord(result[6]) & 0x0f) | 0x30)
    result_8 = chr((ord(result[8]) & 0x3f) | 0x80)
    result_new = result[:6] + result_6 + result[7] + result_8 + result[9:]
    conver_id = uuid.UUID(bytes=result_new)
    return str(conver_id)


"""
participants: action|role|user_id
category: GROUP|CONTACT
"""


def createConversation(self, conversation_id, participants, category):
    parameters = {"conversation_id": conversation_id, "participants": participants, "category": category}
    return self.jwtRequest(URI.conversations(), parameters)


def getConversation(self, id):
    return self.jwtGetRequest(URI.conversations(id))


def exitConversation(self, id):
    return self.jwtRequest(URI.exit(id))


def joinConversation(self, codeId):
    return self.jwtRequest(URI.join(codeId))


def addParticipant(self, conversationId, participants):
    return self.jwtRequest(URI.participants(conversationId, ParticipantAction.ADD), participants)


def removeParticipant(self, conversationId, userId):
    parameters = [{"user_id": userId, "role": ""}]
    return self.jwtRequest(URI.participants(conversationId, ParticipantAction.REMOVE), parameters)


def adminParticipant(self, conversationId, userId):
    parameters = [{"user_id": userId, "role": ParticipantRole.ADMIN}]
    return self.jwtRequest(URI.participants(conversationId, ParticipantAction.ROLE), parameters)


def updateGroupInfo(self, conversationId, name=None, announcement=None, duration=None):
    parameters = {"conversationId": conversationId}
    if name:
        parameters["name"] = name
    if announcement:
        parameters["announcement"] = announcement
    if duration:
        parameters["duration"] = announcement
    return self.jwtRequest(URI.conversations(conversationId), parameters)


def updateCodeId(self, conversationId):
    return self.jwtRequest(URI.reset(conversationId))
