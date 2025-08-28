from OpenSSL import crypto

key = crypto.PKey()
key.generate_key(crypto.TYPE_RSA, 2048)

private_pem = crypto.dump_privatekey(crypto.FILETYPE_PEM, key)
with open("private.pem", "wb") as f:
    f.write(private_pem)

public_pem = crypto.dump_publickey(crypto.FILETYPE_PEM, key)
with open("public.pem", "wb") as f:
    f.write(public_pem)

