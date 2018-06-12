# -*- coding: utf-8 -*-


class URI(object):
    me = "me"
    session = "session"
    preferences = "me/preferences"
    verifyPin = "pin/verify"
    updatePin = "pin/update"
    pinToken = "pin/token"


def me(self):
    return self.jwtGetRequest(URI.me)


def updateProfile(self, full_name=None, avatar_base64=None):
    body = {}
    if full_name:
        body["full_name"] = full_name
    if avatar_base64:
        body["avatar_base64"] = avatar_base64
    return self.jwtRequest(URI.me, body)


def updateSession(self, deviceToken):
    body = {"notification_token": deviceToken, "platform": "IOS"}
    return self.jwtRequest(URI.me, body)


def preferences(self, receive_message_source="CONTACTS"):
    body = {"receive_message_source": receive_message_source}
    return self.jwtRequest(URI.preferences, body)


def verify(self, pin=None):
    body = {"pin": self.genEncrypedPin(pin)}
    return self.jwtRequest(URI.verifyPin, body)


def updatePin(self, new_pin, old=None):
    old_encrypted_pin = self.genEncrypedPin()
    new_encrypted_pin = self.genEncrypedPin(new_pin)
    body = {"old_pin": old_encrypted_pin, "pin": new_encrypted_pin}
    return self.jwtRequest(URI.updatePin, body)


def getPinToken(self):
    return self.jwtGetRequest(URI.pinToken)
