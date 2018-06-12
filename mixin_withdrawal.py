# -*- coding: utf-8 -*-
import uuid


class URI(object):
    addresses_uri = "addresses"
    withdrawals = "withdrawals"

    @staticmethod
    def addresses(assetId):
        return "assets/%s/addresses" % assetId

    @staticmethod
    def delete(assetId):
        return "assets/%s/delete" % assetId


def addresses(self, assetId):
    return self.jwtGetRequest(URI.addresses(assetId))


def save(self, assetId, publicKey, pin_token=None, label=""):
    encrypted_pin = self.genEncrypedPin(pin_token)
    body = {
        "pin": encrypted_pin,
        "label": label,
        "publicKey": publicKey,
        "assetId": assetId,
    }
    return self.jwtRequest(URI.addresses(assetId), body)


def withdrawal(self, addressId, amount, pin_token=None, traceId=None, memo=""):
    encrypted_pin = self.genEncrypedPin(pin_token)
    traceId = traceId or str(uuid.uuid1())
    body = {
        "addressId": addressId,
        "amount": amount,
        "traceId": traceId,
        "pin": encrypted_pin,
        "memo": memo,
    }
    return self.jwtRequest(URI.withdrawals, body)


def delete(self, addressId, pin_token=None):
    encrypted_pin = self.genEncrypedPin(pin_token)
    body = {
        "PIN": encrypted_pin,
    }
    return self.jwtRequest(URI.delete(addressId), body)
