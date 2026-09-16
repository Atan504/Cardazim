import builtins
from os import PathLike

import PIL
from CryptImage import CryptImage
from PIL import Image


class Card:
    def __init__(self, name: str, creator: str, image: CryptImage, riddle: str, solution: str):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self):
        return f"<Card name:{self.name}, creator:{self.creator}>"

    def __str__(self):
        return f"name: {self.name}\ncreator: {self.creator}\nimage: {self.image}\nriddle: {self.riddle}\nsolution: {'unsolved' if self.solution is None else self.solution}"

    @classmethod
    def create_card(cls, name: str, creator: str, path: PathLike, riddle: str, solution: str):
        return Card(name, creator, CryptImage.create_from_path(path), riddle, solution)

    @classmethod
    def _length_and_data(cls, data: str | bytes, length_size: int) -> bytes:
        return len(data).to_bytes(length_size) + (data.encode() if isinstance(data, str) else data)

    serialize_format = [  # noqa: RUF012
        # name of value, if its dynamically sized, length of value(not dynamic)\ length of length of value, type
        ("name", True, 4, str),
        ("creator", True, 4, str),
        ("image", True, 4, Image),
        ("hash", False, 32, bytes),
        ("riddle", True, 4, str),
    ]

    @classmethod
    def handle_serialize_types(cls, data: bytes, type: type):
        match type:
            case builtins.str:
                return data.decode()
            case builtins.bytes:
                return data
            case PIL.Image:
                return CryptImage.bytes_to_img(data)
            case builtins.int:
                return int.from_bytes(data)

    def serialize(self) -> bytes:
        format_dict = {
            "name": self.name,
            "creator": self.creator,
            "image": CryptImage.img_to_bytes(self.image.image),
            "hash": self.image.get_hash(),
            "riddle": self.riddle,
        }

        byts = b""
        for field in self.serialize_format:
            if field[1]:
                byts += self._length_and_data(format_dict.get(field[0]), field[2])
            else:
                byts += format_dict.get(field[0])
        return byts

    @classmethod
    def deserialize(cls, byts: bytes):
        p = 0
        values = {}
        for field in cls.serialize_format:
            if field[1]:
                l = int.from_bytes(byts[p : p + field[2]])
                p += field[2]
                values[field[0]] = cls.handle_serialize_types(byts[p : p + l], field[3])
                p += l
            else:
                values[field[0]] = cls.handle_serialize_types(byts[p : p + field[2]], field[3])
                p += field[2]

        crypt = CryptImage(values.get("image"))
        crypt.set_hash(values.get("hash"))
        return Card(values.get("name"), values.get("creator"), crypt, values.get("riddle"), None)

    @property
    def cryptimage(self) -> CryptImage:
        return self.image
