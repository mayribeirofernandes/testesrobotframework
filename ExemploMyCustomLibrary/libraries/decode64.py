import base64

def decode_64_to_string(stringEncoded):
    print("Deconding [%s] to string." % stringEncoded)

    if not stringEncoded.endswith("=="):
        stringEncoded = stringEncoded + "=="

    stringDecoded = base64.b64decode(stringEncoded)

    return stringDecoded.decode('UTF-8')
