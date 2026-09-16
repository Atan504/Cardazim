import sys

sys.path.append("../Cardazim")
from card import Card

if __name__ == "__main__":
    c = Card.create_card(
        "name",
        "me",
        "31-facts-about-monkey-1743611277-3496435490.png",
        "what 123?",
        "123",
    )
    b = c.serialize()
    l = Card.deserialize(b)
    print(str(l))
    l.cryptimage.save("./tests/cardTest.png")
