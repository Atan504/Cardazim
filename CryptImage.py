import hashlib
import io
from os import PathLike
from typing import Union

from PIL import Image
from Crypto.Cipher import AES


class CryptImage:
    def __init__(self, img: Image):
        self.img = img
        self.key_hash = None

    @classmethod
    def create_from_path(cls, path: Union[str, PathLike]):
        return CryptImage(Image.open(path))

    def img_to_bytes(self, img: Image):
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format=img.format)
        return img_byte_array.getvalue()

    def bytes_to_img(self, byts: bytes):
        # add this and implement it in encrypt and deencrypt TODO!!!!
        return Image.open(io.BytesIO(byts))

    def encrypt(self, key: str) -> None:
        aes_key = hashlib.sha256(key.encode()).digest()
        self.key_hash = hashlib.sha256(aes_key)
        cipher = AES.new(aes_key, AES.MODE_EAX, nonce=b"arazim")
        self.img = cipher.encrypt(
            self.img_to_bytes(self.img)
        )  # converitng back to img instead of bytes

    def dencrypt(self, key: str):
        bkey = hashlib.sha256(key.encode()).digest()
        if hashlib.sha256(bkey).digest() != self.key_hash.digest():
            print(hashlib.sha256(bkey).digest())
            print(self.key_hash.digest())
            return False
        cipher = AES.new(bkey, AES.MODE_EAX, nonce=b"arazim")
        self.img = self.bytes_to_img(cipher.decrypt(self.img))
        self.key_hash = None
        return True

    def save(self):
        self.img.save("output1.jpg")
