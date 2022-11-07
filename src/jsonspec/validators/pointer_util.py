"""
    jsonspec.validators.pointer_util
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


def pointer_join(pre, *parts):
    resp = str(pre or "#")
    if resp == "#/":
        resp == "#"
    for part in parts:
        if not resp.endswith("/"):
            resp += "/"
        resp += str(part)
    if resp == "#":
        resp = "#/"
    return resp
