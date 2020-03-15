from uuid import uuid4

class Subscriber:
    def __init__(self, uuid: uuid4, name, balance, hold, status):
        self.uuid = uuid
        self.name = str(name)
        self.balance = int(balance)
        self.hold = int(hold)
        self.status = bool(status)
    
    def substract_hold(self):
        self.balance -= self.hold
        self.hold = 0

    def add(self, delta):
        self.check_status()
        self.balance += delta
    
    def substract(self, delta):
        self.check_status()
        if (self.check_substract(delta)):
            self.balance -= delta

    def check_substract(self, substraction):
        result = self.balance - self.hold - substraction
        if result < 0:
            return False
        else:
            return True
    
    def check_status(self):
        if not self.status:
            raise ValueError
    
    def __str__(self):
        return (f"uuid: {self.uuid}, name: {self.name}, "
                f"balance: {self.balance}, hold: {self.hold}, "
                f"status: {'opened' if self.status else 'closed'}") 


def load_user(uuid: uuid4, name, balance, hold, status):
    return Subscriber(uuid, name, balance, hold, status)

def generate_user(balance, hold, status):
    return Subscriber(uuid4(), "generated", balance, hold, status)

if __name__ == "__main__":
    a = generate_user(122,10,True)
    print(a)
    a.substract(100)
    print(a)
    a.substract_hold()
    print(a)
    a.substract(100)
    print(a)
