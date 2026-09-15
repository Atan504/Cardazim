from os import PathLike

from CryptImage import CryptImage


class Card:
    def __init__(
        self, name: str, creator: str, image: CryptImage, riddle: str, solution: str
    ):
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self):
        return f"<Card name:{self.name}, creator:{self.creator}>"

    def __str__(self):
        pass

    @classmethod
    def create_card(
        name: str, creator: str, path: PathLike, riddle: str, solution: str
    ):
        return Card(name, creator, CryptImage.create_from_path(path), riddle, solution)

    def serialize(self) -> bytes:
        name = len(self.name).to_bytes(4) + self.name.encode()
        creator = len(self.creator).to_bytes(4) + self.creator.encode()
        w = self.image.get_image().width().to_bytes(4)
        h = self.image.get_image().height().to_bytes(4)
        image = h + w + CryptImage.img_to_bytes(self.image)
        hash = self.image.get_hash().digest()
        riddle = len(self.riddle).to_bytes(4) + self.riddle.encode()
        return name + creator + image + hash + riddle

    @classmethod
    def deserialize(byts: bytes):
        p = 0
        namel = int.from_bytes(byts[p : p + 4])
        p += 4
        name = byts[p, p + namel].decode()
        p += namel
        creatorl = int.from_bytes(byts[p : p + 4])
        p += 4
        creator = byts[p, p + creatorl].decode()
        p += creatorl
        w = int.from_bytes(byts[p : p + 4])
        p += 4
        h = int.from_bytes(byts[p : p + 4])
        p += 4
        imagel = w * h * 3
        image = CryptImage.bytes_to_img(byts[p, p + imagel])
        p += imagel
        hash = byts[p, p + 32]
        p += 32
        riddlel = int.from_bytes(byts[p : p + 4])
        p += 4
        riddle = byts[p, p + riddlel]
        crypt = CryptImage(image)
        crypt.set_hash(hash)
        return Card(name, creator, crypt, riddle, None)
