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
        return Image.open(io.BytesIO(byts))

    def encrypt(self, key: str) -> None:
        aes_key = hashlib.sha256(key.encode()).digest()
        self.key_hash = hashlib.sha256(aes_key).digest()
        cipher = AES.new(aes_key, AES.MODE_EAX, nonce=b"arazim")
        self.img = cipher.encrypt(
            self.img_to_bytes(self.img)
        )  # converitng back to img instead of bytes

    def dencrypt(self, key: str):
        bkey = hashlib.sha256(key.encode()).digest()
        if hashlib.sha256(bkey).digest() != self.key_hash:
            print(hashlib.sha256(bkey).digest())
            print(self.key_hash.digest())
            return False
        cipher = AES.new(bkey, AES.MODE_EAX, nonce=b"arazim")
        self.img = self.bytes_to_img(cipher.decrypt(self.img))
        self.key_hash = None
        return True

    def get_image(self):
        """
        return bytes if encrypted, else Image
        """
        return self.img

    def get_hash(self):
        return self.key_hash

    def set_hash(self, hash):
        self.key_hash = hash

    def save(self):
        self.img.save("output1.jpg")
