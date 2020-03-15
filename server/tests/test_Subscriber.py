import unittest

from Subscriber import Subscriber, generate_user

class TestSimple(unittest.TestCase):
    def test_add(self):
        before = 10
        addition = 10
        expected = before+addition
        user = generate_user(before,0,True)
        user.add(addition)
        actual = user.balance
        return self.assertTrue(expected == actual)
    
    def test_substract(self):
        before = 20
        substaction = 10
        expected = before-substaction
        user = generate_user(before,0,True)
        user.substract(substaction)
        actual = user.balance
        return self.assertTrue(expected == actual)
    
    def test_substract_hold(self):
        before = 20
        hold = 10
        expected = before-hold
        user = generate_user(before,hold,True)
        user.substract_hold()
        actual = user.balance
        return self.assertTrue(expected == actual)

