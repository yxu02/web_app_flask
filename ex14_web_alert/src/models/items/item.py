class Item:
    def __init__(self, name, price, url, **kwargs):
        self.name = name
        self.price = price
        self.url = url
        pass

    def __repr__(self):
        return f"<Item {self.name} with URL {self.url}>"
