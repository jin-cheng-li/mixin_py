# -*- coding: utf-8 -*-

ERRCODES = {
    202: {
        400: "The request body can’t be pasred as valid data.",
        401: "Unauthorized, maybe invalid token.",
        403: "Forbidden.",
        404: "The endpoint is not found.",
        409: "Too Many Requests.",
        10002: "The request data has invalid field.",
        10003: "Failed to deliver SMS to +8613800138000.",
        20110: "Invalid phone number +8613800138000",
        20111: "Insufficient identity numbers.",
        20112: "Invalid invitation code.",
        20113: "Invalid phone verification code.",
        20114: "Expired phone verification code.",
        20115: "Invalid QR code.",
        20116: "The group chat is full.",
        20117: "Insufficient balance.",
        20118: "Invalid PIN format.",
        20119: "PIN incorrect.",
        20120: "Transfer amount too small.",
        20121: "Authorization code expired.",
        20122: "Phone number used by someone else.",
        20123: "You have created too many apps, the maximum is 10.",
        30100: "Chain not in sync.",
        30101: "Private key for XYZ missing.",
        30102: "Invalid address format.",
        30103: "Insufficient %asset_id% pool",
    },
    500: {
        500: "Internal Server Error.",
        7000: "Blaze server error.",
        7001: "The blaze operation timeout.",
    }
}
