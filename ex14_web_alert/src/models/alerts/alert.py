class Alert:
    def __init__(self, user, price_limit, item, **kwargs):
        self.user = user
        self.price_limit = price_limit
        self.item = item
        pass

    def __repr__(self):
        return f"<Alert for user {self.user} on item {self.item} " \
            f"with price limit {self.price_limit}>"

