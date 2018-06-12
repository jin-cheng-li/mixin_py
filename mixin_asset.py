# -*- coding: utf-8 -*-
import uuid


class URI(object):
    assets = "assets"
    transfers = "transfers"
    payments = "payments"

    @staticmethod
    def snapshots(assetId):
        return "%s/%s/snapshots" % (URI.assets, assetId)

    @staticmethod
    def fee(assetId):
        return "%s/%s/fee" % (URI.assets, assetId)

    @staticmethod
    def trace(trace_id):
        return "transfers/trace/%s" % trace_id


def assets(self, assetId=None):
    uri = URI.assets
    if assetId:
        uri = "%s/%s" % (uri, assetId)
    return self.jwtGetRequest(uri)


def trace(self, trace_id):
    return self.jwtGetRequest(URI.trace(trace_id))


def transfer(self, counter_user_id, asset_id, amount, memo=""):
    encrypted_pin = self.genEncrypedPin()
    trace_id = str(uuid.uuid1())
    body = {'asset_id': asset_id, 'counter_user_id': counter_user_id, 'amount': str(
        amount), 'pin': encrypted_pin, 'trace_id': trace_id}

    if memo and memo != "":
        body['meno'] = memo

    return self.jwtRequest(URI.transfers, body)

# verify_payments
# status "paid" OR "pending"


def payments(self, counter_user_id, asset_id, amount, trace_id=None):
    trace_id = trace_id or str(uuid.uuid1())
    encrypted_pin = self.genEncrypedPin()
    body = {'asset_id': asset_id, 'counter_user_id': counter_user_id, 'amount': str(
        amount), 'pin': encrypted_pin, 'trace_id': trace_id}

    return self.jwtRequest(URI.payments, body)


def snapshots(self, assetId):
    return self.jwtGetRequest(URI.snapshots(assetId))


def fee(self, assetId):
    return self.jwtGetRequest(URI.fee(assetId))


def listAssets(self):
    assets = []
    assets_lst = self.assets()
    if not assets_lst:
        return assets
    assets_info = assets_lst["data"]
    for singleAsset in assets_info:
        if singleAsset["balance"] != "0":
            assets.append((singleAsset["symbol"], singleAsset["balance"]))
    return assets
