class Store:
    def __init__(self, name, url_prefix):
        self.name = name
        self.url_prefix = url_prefix

    def __repr__(self):
        return f"<Store {self.name}>"
