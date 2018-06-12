# -*- coding: utf-8 -*-
import websocket
import json
import uuid
import base64
import gzip
import ssl
import traceback
import types

from cStringIO import StringIO

try:
    import thread
except ImportError:
    import _thread as thread


class MixinWsApp(websocket.WebSocketApp):
    """docstring for MixinWsApp"""

    PRS_ASSET_ID = "3edb734c-6d6f-32ff-ab03-4eb43640c758"
    LY_ASSET_ID = "35f7a3a3-4335-3bf3-beca-685836602d72"
    BTCCash_ASSET_ID = "fd11b6e3-0b87-41f1-a41f-f0e9b49e5bf0"
    CNB_ASSET_ID = "965e5c6e-434c-3fa9-b780-c50f43cd955c"
    EOS_ASSET_ID = "f8127159-e473-389d-8e0c-9ac5a4dc8cc6"
    CANDY_ASSET_ID = "43b645fc-a52c-38a3-8d3b-705e7aaefa15"

    # actions
    ACKNOWLEDGE_MESSAGE_RECEIPT = "ACKNOWLEDGE_MESSAGE_RECEIPT"
    CREATE_MESSAGE = "CREATE_MESSAGE"
    LIST_PENDING_MESSAGES = "LIST_PENDING_MESSAGES"

    ACTIONS = [ACKNOWLEDGE_MESSAGE_RECEIPT, CREATE_MESSAGE, LIST_PENDING_MESSAGES]

    # categorys

    SYSTEM_ACCOUNT_SNAPSHOT = "SYSTEM_ACCOUNT_SNAPSHOT"
    PLAIN_TEXT = "PLAIN_TEXT"
    SYSTEM_CONVERSATION = "SYSTEM_CONVERSATION"
    PLAIN_STICKER = "PLAIN_STICKER"
    PLAIN_IMAGE = "PLAIN_IMAGE"
    PLAIN_CONTACT = "PLAIN_CONTACT"

    CATEGORYS = [
        SYSTEM_ACCOUNT_SNAPSHOT, PLAIN_TEXT, SYSTEM_CONVERSATION, PLAIN_STICKER,
        PLAIN_IMAGE, PLAIN_CONTACT
    ]

    def __init__(self, api_robot, url=None, header=None,
                 on_open=None, on_message=None, on_error=None,
                 on_close=None, on_ping=None, on_pong=None,
                 on_cont_message=None,
                 keep_running=True, get_mask_key=None, cookie=None,
                 subprotocols=None,
                 on_data=None):
        super(MixinWsApp, self).__init__(url, header,
                                         on_open, on_message, on_error,
                                         on_close, on_ping, on_pong,
                                         on_cont_message,
                                         keep_running, get_mask_key, cookie,
                                         subprotocols,
                                         on_data)
        self.api_robot = api_robot
        self.client_id = self.api_robot.client_id

        self.set_handler()
        self.check_params()

    def _callback(self, callback, *args):
        if callback:
            try:
                if isinstance(callback, types.MethodType):
                    callback(*args)
                else:
                    callback(self, *args)
            except Exception:
                print(traceback.format_exc())

    def set_handler(self):
        self.action_handler = {
            MixinWsApp.ACKNOWLEDGE_MESSAGE_RECEIPT: None,
            MixinWsApp.CREATE_MESSAGE: self.action_message
        }
        self.category_handler = {
            MixinWsApp.PLAIN_IMAGE: self.catePlainImage,
            MixinWsApp.SYSTEM_CONVERSATION: self.cateSysConversation,
            MixinWsApp.SYSTEM_ACCOUNT_SNAPSHOT: self.cateSysAccSnapshot,
            MixinWsApp.PLAIN_STICKER: self.cateplainSticker,
            MixinWsApp.PLAIN_TEXT: self.cateplainText,
        }

    def check_params(self):

        if not self.url:
            self.url = "wss://blaze.mixin.one/"
        # array is empty
        if not self.header:
            encoded = self.api_robot.genJwtToken('/', "", str(uuid.uuid4()), "GET")
            self.header = ["Authorization:Bearer " + encoded]

        if not self.subprotocols:
            self.subprotocols = ["Mixin-Blaze-1"]

        if not self.on_open:
            self.on_open = self.mixin_on_open
        if not self.on_message:
            self.on_message = self.mixin_on_message
        if not self.on_error:
            self.on_error = self.mixin_on_error
        if not self.on_close:
            self.on_close = self.mixin_on_close

    # categorys
    def catePlainImage(self, data, msgid, typeindata, category, dataindata, conversationid):
        pass

    def cateSysConversation(self, data, msgid, typeindata, category, dataindata, conversationid):
        pass

    def cateSysAccSnapshot(self, data, msgid, typeindata, category, dataindata, conversationid):
        pass

    def cateplainSticker(self, data, msgid, typeindata, category, dataindata, conversationid):
        pass

    def cateplainText(self, data, msgid, typeindata, category, dataindata, conversationid):
        pass
    # actions

    def action_message(self, rdata_obj):
        if 'error' in rdata_obj:
            msgid = rdata_obj["data"]["message_id"]
            data = rdata_obj["data"]
            self.replyMsg(msgid)
            print("error", data)
            return

        data = rdata_obj["data"]
        msgid = data["message_id"]
        typeindata = data["type"]
        category = data["category"]
        dataindata = data["data"]
        conversationid = data["conversation_id"]

        self.replyMsg(msgid)

        if category not in MixinWsApp.CATEGORYS:
            print("unknow category")
            print(rdata_obj)
            return

        handler = self.category_handler.get(category)
        if not handler:
            print("no handler category is: " + category)
            return
        handler(data, msgid, typeindata, category,
                dataindata, conversationid)

    # on event
    def mixin_on_message(self, message):
        inbuffer = StringIO(message)
        f = gzip.GzipFile(mode="rb", fileobj=inbuffer)
        rdata_injson = f.read()
        rdata_obj = json.loads(rdata_injson)
        action = rdata_obj["action"]
        print(rdata_obj)

        if action not in MixinWsApp.ACTIONS:
            print("unknow action")
            print(rdata_obj)
            return

        handler = self.action_handler.get(action)
        if not handler:
            print("no handler action is:" + action)
            # print(rdata_obj)
            return
        handler(rdata_obj)

    def mixin_on_error(self, error):
        print("### on_error###")
        print(error)

    def mixin_on_close(self):
        print("### closed ###")

    def mixin_on_open(self):

        def run(*args):
            print("### run ###")
            self.writeMessage(MixinWsApp.LIST_PENDING_MESSAGES)
            # while True:
            #     time.sleep(2)
        thread.start_new_thread(run, ())

    def start(self):
        websocket.enableTrace(True)
        self.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def writeMessage(self, action, params=None):
        Message = {"id": str(uuid.uuid1()), "action": action}
        if params:
            Message["params"] = params
        Message_instring = json.dumps(Message)
        fgz = StringIO()
        gzip_obj = gzip.GzipFile(mode='wb', fileobj=fgz)
        gzip_obj.write(Message_instring)
        gzip_obj.close()
        self.send(fgz.getvalue(), opcode=websocket.ABNF.OPCODE_BINARY)

    # messages

    def replyMsg(self, msgid):
        params = {"message_id": msgid, "status": "READ"}
        self.writeMessage("ACKNOWLEDGE_MESSAGE_RECEIPT", params)

    def sendUserContactCard(self, cid, to_user_id, to_share_userid):
        btnJson = json.dumps({"user_id": to_share_userid})
        params = {"conversation_id": cid, "recipient_id": to_user_id, "message_id": str(
            uuid.uuid4()), "category": "PLAIN_CONTACT", "data": base64.b64encode(btnJson)}
        return self.writeMessage("CREATE_MESSAGE", params)

    def sendText(self, cid, to_user_id, textContent):
        params = {"conversation_id": cid, "message_id": str(
            uuid.uuid4()), "category": "PLAIN_TEXT", "data": base64.b64encode(textContent)}
        if to_user_id:
            params["recipient_id"] = to_user_id

        return self.writeMessage("CREATE_MESSAGE", params)

    def sendSticker(self, cid, to_user_id, album_id, sticker_name):
        realStickerObj = {}
        realStickerObj['album_id'] = album_id
        realStickerObj['name'] = sticker_name

        btnJson = json.dumps(realStickerObj)
        params = {"conversation_id": cid, "recipient_id": to_user_id, "message_id": str(
            uuid.uuid4()), "category": "PLAIN_STICKER", "data": base64.b64encode(btnJson)}
        return self.writeMessage("CREATE_MESSAGE", params)

    def sendAppButton(self, cid, to_user_id, realLink, text4Link, colorOfLink="#d53120"):
        btn = '[{"label":"' + text4Link + '","action":"' + \
            realLink + '","color":"' + colorOfLink + '"}]'
        params = {"conversation_id": cid, "recipient_id": to_user_id, "message_id": str(
            uuid.uuid4()), "category": "APP_BUTTON_GROUP", "data": base64.b64encode(btn)}
        return self.writeMessage("CREATE_MESSAGE", params)

    # send pay button
    def sendPayAppButton(self, cid, to_user_id, inAssetName, inAssetID, inPayAmount, linkColor="#0CAAF5"):
        payLink = "https://mixin.one/pay?recipient=" + self.client_id + "&asset=" + \
            inAssetID + "&amount=" + \
            str(inPayAmount) + '&trace=' + str(uuid.uuid1()) + '&memo=PRS2CNB'
        self.sendAppButton(cid, to_user_id, payLink, inAssetName, linkColor)

    def showReceipt(self, inConversationID, reply_user_id, reply_snapShotID):
        payLink = "https://mixin.one/snapshots/" + reply_snapShotID
        shortSnapShort = reply_snapShotID[0:13] + "..."
        btn = '[{"label":"Your receipt:' + shortSnapShort + \
            '","action":"' + payLink + '","color":"#0CAAF5"}]'

        params = {"conversation_id": inConversationID, "recipient_id": reply_user_id, "message_id": str(
            uuid.uuid4()), "category": "APP_BUTTON_GROUP", "data": base64.b64encode(btn)}
        self.writeMessage("CREATE_MESSAGE", params)


if __name__ == "__main__":
    while True:
        ws = MixinWsApp()
        ws.start()
