from uuid import uuid4
import decorators as d

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
    
    @d.check_status
    def add(self, delta):
        self.balance += delta
    
    @d.check_status
    def substract(self, delta):
        if (self.check_substract(delta)):
            self.balance -= delta
    
    @d.check_status
    def check_substract(self, substraction):
        result = self.balance - self.hold - substraction
        if result < 0:
            return False
        else:
            return True
    
    
    def __str__(self):
        return (f"uuid: {self.uuid}, name: {self.name}, "
                f"balance: {self.balance}, hold: {self.hold}, "
                f"status: {'opened' if self.status else 'closed'}") 


def load_user(uuid: uuid4, name, balance, hold, status):
    return Subscriber(uuid, name, balance, hold, status)

def generate_user(balance, hold, status):
    return Subscriber(uuid4(), "generated", balance, hold, status)
