import unittest

from Subscriber import Subscriber, generate_user
import helpers.exceptions as e


class TestSimple(unittest.TestCase):
    def test_add(self):
        before = 10
        addition = 10
        expected = before+addition
        user = generate_user(before, 0, True)
        user.add(addition)
        actual = user.balance
        self.assertTrue(expected == actual)

    def test_substract(self):
        balance_before = 20
        hold_before = 0
        substaction = 10
        expected_balance = balance_before
        expected_hold = hold_before+substaction
        user = generate_user(balance_before, hold_before, True)
        user.substract(substaction)
        actual_balance = user.balance
        actual_hold = user.hold
        self.assertTrue(expected_balance == actual_balance)
        self.assertTrue(expected_hold == actual_hold)

    def test_substract_hold(self):
        before = 20
        hold = 10
        expected = before-hold
        user = generate_user(before, hold, True)
        user.substract_hold()
        actual = user.balance
        self.assertTrue(expected == actual)

    def test_closed(self):
        user = generate_user(0, 0, False)
        with self.assertRaises(e.ClosedAccountException):
            user.add(10)
