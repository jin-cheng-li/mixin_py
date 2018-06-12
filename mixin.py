# -*- coding: utf-8 -*-

import base64
import time
import hashlib
import datetime
import jwt
import uuid
import json
import requests
import Crypto

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Signature import PKCS1_v1_5
from Crypto import Random
from Crypto.Cipher import AES

from util import do_patch_moudle


class MixinApi:
    def __init__(self, cfg):
        # calc
        self.keyForAES = ""
        # const
        self.mixin_uri = "https://api.mixin.one/"

        # ext
        self.client_id = cfg.client_id
        self.client_secret = cfg.client_secret
        self.session_id = cfg.session_id
        self.pin_code = cfg.pin_code
        self.pin_token = cfg.pin_token
        self.private_key = cfg.private_key
        self.admin_uuid = cfg.admin_uuid

        print("client_id:%s\nclient_secret:%s\nsession_id:%s\npin_code:%s\npin_token:%s\nprivat_key:%s\nadmin_uuid:%s\n" % (self.client_id, self.client_secret, self.session_id, self.pin_code, self.pin_token, self.private_key, self.admin_uuid))

    def genUri(self, uri):
        return "%s%s" % (self.mixin_uri, uri)

    def genSig(self, uri, body, method="POST"):
        return hashlib.sha256(method + uri + body).hexdigest()

    def genJwtToken(self, uri, body, jti, method="POST"):
        # print(uri, body, jti, method)
        jwtSig = self.genSig(uri, body, method)
        iat = datetime.datetime.utcnow()
        exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=200)
        jwtToken = jwt.encode({'uid': self.client_id, 'sid': self.session_id, 'iat': iat,
                               'exp': exp, 'jti': jti, 'sig': jwtSig}, self.private_key, algorithm='RS512')
        return jwtToken

    def genListenSignedToken(self, uri, body, jti, method):
        jwtToken = self.genJwtToken(self, uri, body, jti, method)
        privKeyObj = RSA.importKey(self.private_key)
        signer = PKCS1_v1_5.new(privKeyObj)
        signature = signer.sign(jwtToken)
        return signature

    def genEncrypedPin(self, pin_token=None):
        if self.keyForAES == "":
            privKeyObj = RSA.importKey(self.private_key)
            pin_token = pin_token or self.pin_token
            decoded_result = base64.b64decode(pin_token)
            # decoded_result_inhexString = ":".join("{:02x}".format(ord(c)) for c in decoded_result)
            # print("pin_token is:" + self.pin_token)
            # print("lenth of decoded pin_token is:" + str(len(decoded_result)))
            cipher = PKCS1_OAEP.new(
                key=privKeyObj, hashAlgo=Crypto.Hash.SHA256, label=self.session_id)

            decrypted_msg = cipher.decrypt(decoded_result)
            # decrypted_msg_inhexString = ":".join("{:02x}".format(ord(c)) for c in decrypted_msg)
            # print("lenth of AES key:" + str(len(decrypted_msg)))
            # print("content of AES key:")
            # print(decrypted_msg_inhexString)
            self.keyForAES = decrypted_msg

        ts = int(time.time())
        # print("ts"+ str(ts))
        tszero = ts % 0x100
        tsone = (ts % 0x10000) >> 8
        tstwo = (ts % 0x1000000) >> 16
        tsthree = (ts % 0x100000000) >> 24
        tsstring = chr(tszero) + chr(tsone) + chr(tstwo) + \
            chr(tsthree) + '\0\0\0\0'
        # counter = '\1\0\0\0\0\0\0\0'
        toEncryptContent = self.pin_code + tsstring + tsstring
        # print("before padding:" + str(len(toEncryptContent)))
        lenOfToEncryptContent = len(toEncryptContent)
        toPadCount = 16 - lenOfToEncryptContent % 16
        if toPadCount > 0:
            paddedContent = toEncryptContent + chr(toPadCount) * toPadCount
        else:
            paddedContent = toEncryptContent
        # print("after padding:" + str(len(paddedContent)))

        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.keyForAES, AES.MODE_CBC, iv)
        encrypted_result = cipher.encrypt(paddedContent)
        msg = iv + encrypted_result
        encrypted_pin = base64.b64encode(msg)
        # print("to encrypted content in hex is :" + ":".join("{:02x}".format(ord(c)) for c in paddedContent))
        # print("iv in hex is " + ":".join("{:02x}".format(ord(c)) for c in iv))
        # print("iv + encrypted result in hex is :" + ":".join("{:02x}".format(ord(c)) for c in (iv + encrypted_result)))
        # print("iv + encrypted_result in base64 :" + encrypted_pin)

        return encrypted_pin

    def _jwtRequest(self, uri, body="", jti=None, method="POST", headers={}):
        jti = jti or str(uuid.uuid1())
        is_post = (method == "POST")
        jwt_body = body

        if is_post:
            jwt_body = json.dumps(body)

        jwtToken = self.genJwtToken(('/%s' % uri), jwt_body, jti, method)
        headers["Authorization"] = "Bearer %s" % jwtToken
        url = self.genUri(uri)
        # print(url, body, jti, method, headers)
        if is_post:
            return requests.post(url, json=body, headers=headers)
        else:
            return requests.get(url, headers=headers)

    def jwtRequest(self, uri, body="", jti=None, method="POST", headers={}):
        r = self._jwtRequest(uri, body, jti, method, headers)
        result_obj = r.json()
        if r.status_code != 200:
            print(result_obj)
        return result_obj

    def jwtGetRequest(self, uri):
        return self.jwtRequest(uri, "", None, "GET")


# private function start with __
moduleNames = ["mixin_account", "mixin_asset", "mixin_authorize",
               "mixin_contact", "mixin_conversation", "mixin_message",
               "mixin_sticker", "mixin_user", "mixin_withdrawal"]

modules = map(__import__, moduleNames)
for module in modules:
    do_patch_moudle(MixinApi, module)

if __name__ == "__main__":
    CNB_ASSET_ID = "965e5c6e-434c-3fa9-b780-c50f43cd955c"
    import sys
    sys.path.append('..')
    import cfg

    api_robot = MixinApi(cfg)
    # print(api_robot.updateProfile("mini"))
    # print(api_robot.me())
    # print(api_robot.preferences("CONTACTS"))
    # print(api_robot.getPinToken())

    # print(api_robot.assets(CNB_ASSET_ID))
    # print(api_robot.payments(cfg.admin_uuid, CNB_ASSET_ID, 10))
    # api_robot.transfer(cfg.admin_uuid, CNB_ASSET_ID, 10)
    # print(api_robot.snapshots(CNB_ASSET_ID))
    # print(api_robot.fee(CNB_ASSET_ID))
    print(api_robot.listAssets())

    # print(api_robot.getContacts())
    # print(api_robot.albums())

    # print(api_robot.trace('25c46ba2-6b8a-11e8-8d5b-000c29bf7af6'))
