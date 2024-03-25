# encoding=utf-8
import binascii

from Crypto.Cipher import AES

def format_string(input_string):
    # 确保输入的字符串长度为16
    if len(input_string) != 16:
        return "Invalid input length"

    # 使用切片将字符串分割成四部分
    parts = [input_string[i:i + 4] for i in range(0, len(input_string), 4)]

    # 使用字符串连接操作将切片后的部分用 "-" 连接
    formatted_string = "-".join(parts)

    return formatted_string

# 加密函数
def encrypt_aes256gcm(key:bytes, ciphertext:bytes, iv:bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM, iv)
    # ed是密文部分，auth_tag是 digest部分有认证功能
    # ed = cipher.encrypt(ciphertext)
    ed, auth_tag = cipher.encrypt_and_digest(ciphertext)
    return ed + auth_tag


# 解密函数
def decrypt_aes256gcm(key:bytes, cipherBytes:bytes, iv:bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM, iv)

    auth_tag_length = 16  # 这个长度根据加密算法和模式来确定，AES-GCM通常为16字节
    auth_tag = cipherBytes[-auth_tag_length:]
    ciphertext = cipherBytes[:-auth_tag_length]

    # 解密并验证认证标签
    try:
        # plain_text = cipher.decrypt(ciphertext)
        plain_text = cipher.decrypt_and_verify(ciphertext, auth_tag)
        return plain_text
    except ValueError:
        print("Decryption failed: Invalid authentication tag")
        return None

# 加密 license.data
def license_data_encrypt(ciphertext:bytes):
    '在encrypt_aes256gcm之上封装,固定key和iv'
    key = binascii.unhexlify('fd2d9fb0bb4bc7a225d36e0cce8d26573950c4461c4d29afd46214e37e686197')
    iv = binascii.unhexlify('29cd7489b0a30e32fb589377')
    return encrypt_aes256gcm(key, ciphertext, iv)

# 解密 license.data
def license_data_decrypt(cipherBytes:bytes):
    '在decrypt_aes256gcm之上封装,固定key和iv'
    key = binascii.unhexlify('fd2d9fb0bb4bc7a225d36e0cce8d26573950c4461c4d29afd46214e37e686197')
    iv = binascii.unhexlify('29cd7489b0a30e32fb589377')
    return decrypt_aes256gcm(key, cipherBytes, iv)

