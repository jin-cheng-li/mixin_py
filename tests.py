from mixin import MixinApi
import cfg

CNB_ASSET_ID = "965e5c6e-434c-3fa9-b780-c50f43cd955c"

if __name__ == "__main__":
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
