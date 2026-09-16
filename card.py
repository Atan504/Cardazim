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
        return f"name: {self.name}\ncreator: {self.creator}\nimage: {self.image}\nriddle: {self.riddle}\nsolution: {self.solution}"

    @classmethod
    def create_card(
        cls, name: str, creator: str, path: PathLike, riddle: str, solution: str
    ):
        return Card(name, creator, CryptImage.create_from_path(path), riddle, solution)

    def serialize(self) -> bytes:  # TODO isolate length + data into another func
        name = len(self.name).to_bytes(4) + self.name.encode()
        creator = len(self.creator).to_bytes(4) + self.creator.encode()
        imageb = CryptImage.img_to_bytes(self.image.image)
        image = len(imageb).to_bytes(4) + imageb
        # TODO prob need to adress the case of encrpyt image by either fixing storing encrypted image or by adding an case
        hash = self.image.get_hash()
        riddle = len(self.riddle).to_bytes(4) + self.riddle.encode()
        return name + creator + image + hash + riddle

    @classmethod
    def deserialize(
        cls, byts: bytes
    ):  # TODO asap turn into for loop over a format instead of this
        p = 0
        namel = int.from_bytes(byts[p : p + 4])
        p += 4
        name = byts[p : p + namel].decode()
        p += namel
        creatorl = int.from_bytes(byts[p : p + 4])
        p += 4
        creator = byts[p : p + creatorl].decode()
        p += creatorl
        imagel = int.from_bytes(byts[p : p + 4])
        p += 4
        image = CryptImage.bytes_to_img(byts[p : p + imagel])
        p += imagel
        hash = byts[p : p + 32]
        p += 32
        riddlel = int.from_bytes(byts[p : p + 4])
        p += 4
        riddle = byts[p : p + riddlel].decode()
        crypt = CryptImage(image)
        crypt.set_hash(hash)
        return Card(name, creator, crypt, riddle, None)

    @property
    def cryptimage(self) -> CryptImage:
        return self.image
