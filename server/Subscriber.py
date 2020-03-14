from uuid import uuid4

class Subscriber:
    def __init__(self, uuid: uuid4, name, balance, hold, status):
        self.uuid = uuid
        self.name = str(name)
        self.balance = int(balance)
        self.hold = int(hold)
        self.status = bool(status)

def load_user(uuid: uuid4, name, balance, hold, status):
    return Subscriber(uuid, name, balance, hold, status)

def generate_user(balance, hold, status):
    return Subscriber(uuid4(), "generated", balance, hold, status)

if __name__ == "__main__":
    a = generate_user(122,0,False)
    print(a)