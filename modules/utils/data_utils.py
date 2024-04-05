def encrypt_data(data, key):
    """
    根据key作凯撒加密, key长度小于data，因此key循环使用
    """
    return "".join([chr(ord(data[i]) ^ ord(key[i % len(key)])) for i in range(len(data))])

def decrypt_data(data, key):
    """
    根据key作凯撒解密, key长度小于data，因此key循环使用
    """
    return "".join([chr(ord(data[i]) ^ ord(key[i % len(key)])) for i in range(len(data))])