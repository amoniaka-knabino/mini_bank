from uuid import uuid4, UUID
import helpers.decorators as d
import helpers.exceptions as e
import json

class Subscriber:
    def __init__(self, uuid, name, balance, hold, status):
        if (type(uuid) is UUID):
            self.uuid = uuid
        elif (type(uuid) is str):
            self.uuid = UUID(uuid)
        else:
            raise ValueError
        self.name = str(name)
        self.balance = int(balance)
        self.hold = int(hold)
        self.status = bool(status)
    
    def substract_hold(self):
        self.balance -= self.hold
        self.hold = 0
    
    @d.check_status
    def add(self, delta):
        self.check_param(delta)
        self.balance += delta
    
    @d.check_status
    def substract(self, delta):
        self.check_param(delta)
        if (self.check_substract(delta)):
            self.hold += delta
    
    @d.check_status
    def check_substract(self, substraction):
        result = self.balance - self.hold - substraction
        if result < 0:
            return False
        else:
            return True
    def check_param(self, sum):
        if sum < 0:
            raise e.InvalidSumException
    
    def __str__(self):
        return (f"uuid: {self.uuid}, name: {self.name}, "
                f"balance: {self.balance}, hold: {self.hold}, "
                f"status: {'opened' if self.status else 'closed'}") 
    
    def __eq__(self, other):
        return ( self.uuid == other.uuid and self.name == other.name
                and self.balance == other.balance and self.hold == other.hold
                and self.status == other.status)
    
    def __hash__(self):
        """
        Гарантируется, что uuid уникален в пределах множества абонентов => использовать его хэш эффективней, чем хэш имени или другого поля
        """
        return self.uuid.__hash__()
    
    def dict_for_json(self):
        return {"uuid":self.uuid, "name":self.name, "balance":self.balance, "hold":self.hold, "status":str(self.status)}


def generate_user(balance, hold, status):
    return Subscriber(uuid4(), "generated", balance, hold, status)

def get_subs_set_from_json_file(filename):
    with open(filename) as f:
        subs_from_json = json.loads(f.read())
        return get_subs_set_from_json(subs_from_json)

def get_subs_set_from_json(subs_from_json):
    subscribers = set()
    for u in subs_from_json:
        sub = Subscriber(u["uuid"], u["name"], u["balance"], u["hold"], u["status"]=='True')
        subscribers.add(sub)
    return subscribers