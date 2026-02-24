# DEBUGGING EXERCISE: Find and fix the bug(s) in this implementation
"""
Event-Sourced Account Ledger
=============================

This module implements an event-sourced account system. Instead of storing
the current balance directly, all changes are stored as immutable events
(credits and debits). The account balance is reconstructed by replaying
all events in chronological order.

Event types:
    - "credit": Adds money to the account (balance increases)
    - "debit":  Removes money from the account (balance decreases)

Each event has a timestamp, and events must be replayed in timestamp order
to reconstruct the correct balance.

SYMPTOMS:
    Tests are failing because the reconstructed balance does not match the
    expected value. When replaying events, the final balance is incorrect.
    The events themselves appear to be recorded correctly, but the replay
    logic produces a wrong number. For example, crediting 100 then debiting
    30 should yield 70, but the system reports something different.
"""

import unittest
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass(frozen=True)
class Event:
    """An immutable ledger event."""
    event_type: str  # "credit" or "debit"
    amount: float
    timestamp: datetime
    description: str = ""

    def __post_init__(self):
        if self.event_type not in ("credit", "debit"):
            raise ValueError(f"Invalid event type: {self.event_type}")
        if self.amount < 0:
            raise ValueError(f"Amount must be non-negative, got {self.amount}")


@dataclass
class Account:
    """
    An event-sourced account that reconstructs its balance from events.

    Usage:
        account = Account(account_id="acc-001")
        account.credit(100.0, description="Initial deposit")
        account.debit(30.0, description="ATM withdrawal")
        print(account.balance)  # Should be 70.0
    """
    account_id: str
    _events: list[Event] = field(default_factory=list)
    _base_time: datetime = field(default_factory=datetime.now)
    _event_counter: int = field(default=0)

    def _next_timestamp(self) -> datetime:
        """Generate a monotonically increasing timestamp for event ordering."""
        self._event_counter += 1
        return self._base_time + timedelta(microseconds=self._event_counter)

    def credit(self, amount: float, description: str = "") -> None:
        """Record a credit event (money in)."""
        event = Event(
            event_type="credit",
            amount=amount,
            timestamp=self._next_timestamp(),
            description=description,
        )
        self._events.append(event)

    def debit(self, amount: float, description: str = "") -> None:
        """Record a debit event (money out)."""
        event = Event(
            event_type="debit",
            amount=amount,
            timestamp=self._next_timestamp(),
            description=description,
        )
        self._events.append(event)

    @property
    def balance(self) -> float:
        """Reconstruct the current balance by replaying all events in order."""
        # Sort events by timestamp to ensure correct order
        sorted_events = sorted(self._events, key=lambda e: e.timestamp)

        total = 0.0
        for event in sorted_events:
            if event.event_type == "credit":
                total += event.amount
            elif event.event_type == "debit":
                total -= event.amount
        return total

    def get_balance_at(self, point_in_time: datetime) -> float:
        """
        Reconstruct the balance at a specific point in time.

        Only events with timestamps <= point_in_time are included.
        """
        sorted_events = sorted(self._events, key=lambda e: e.timestamp)

        total = 0.0
        for event in sorted_events:
            if event.timestamp > point_in_time:
                break
            if event.event_type == "credit":
                total += event.amount
            elif event.event_type == "debit":
                total += event.amount
        return total

    @property
    def event_count(self) -> int:
        return len(self._events)

    def get_statement(self) -> list[dict]:
        """Return a chronological statement of all events with running balance."""
        sorted_events = sorted(self._events, key=lambda e: e.timestamp)

        statement = []
        running_balance = 0.0

        for event in sorted_events:
            if event.event_type == "credit":
                running_balance += event.amount
            elif event.event_type == "debit":
                running_balance -= event.amount

            statement.append({
                "type": event.event_type,
                "amount": event.amount,
                "balance": running_balance,
                "description": event.description,
                "timestamp": event.timestamp,
            })

        return statement


# ---------------------------------------------------------------------------
# Test Suite
# ---------------------------------------------------------------------------

class TestEventSourcedAccount(unittest.TestCase):
    """Tests for the event-sourced Account. These tests FAIL due to the bug."""

    def test_single_credit(self):
        account = Account(account_id="acc-001")
        account.credit(100.0, description="Deposit")
        self.assertAlmostEqual(account.balance, 100.0)

    def test_single_debit(self):
        account = Account(account_id="acc-001")
        account.credit(100.0)
        account.debit(30.0)
        self.assertAlmostEqual(account.balance, 70.0)

    def test_multiple_transactions(self):
        account = Account(account_id="acc-001")
        account.credit(500.0, description="Salary")
        account.debit(50.0, description="Groceries")
        account.debit(120.0, description="Electricity bill")
        account.credit(25.0, description="Refund")
        self.assertAlmostEqual(account.balance, 355.0)

    def test_balance_at_point_in_time(self):
        """Balance at a specific point in time should only include events up to that time."""
        account = Account(account_id="acc-001")

        account.credit(100.0, description="Day 1 deposit")
        after_first = account._events[-1].timestamp

        account.debit(30.0, description="Day 2 withdrawal")

        account.credit(50.0, description="Day 3 deposit")

        # Balance after just the first event should be 100
        balance_after_first = account.get_balance_at(after_first)
        self.assertAlmostEqual(balance_after_first, 100.0)

    def test_balance_at_includes_debit_correctly(self):
        """get_balance_at should subtract debits, not add them."""
        account = Account(account_id="acc-001")

        account.credit(200.0, description="Deposit")
        account.debit(75.0, description="Payment")
        final_time = account._events[-1].timestamp

        balance = account.get_balance_at(final_time)
        self.assertAlmostEqual(balance, 125.0,
                               msg="get_balance_at should subtract debits from the total")

    def test_empty_account(self):
        account = Account(account_id="acc-001")
        self.assertAlmostEqual(account.balance, 0.0)

    def test_event_count(self):
        account = Account(account_id="acc-001")
        account.credit(100.0)
        account.debit(50.0)
        account.credit(25.0)
        self.assertEqual(account.event_count, 3)

    def test_statement_running_balance(self):
        account = Account(account_id="acc-001")
        account.credit(100.0, description="Deposit")
        account.debit(40.0, description="Withdrawal")
        account.credit(20.0, description="Refund")

        statement = account.get_statement()
        balances = [entry["balance"] for entry in statement]
        self.assertEqual(balances, [100.0, 60.0, 80.0])

    def test_invalid_event_type(self):
        with self.assertRaises(ValueError):
            Event(event_type="transfer", amount=50.0, timestamp=datetime.now())

    def test_negative_amount_rejected(self):
        with self.assertRaises(ValueError):
            Event(event_type="credit", amount=-10.0, timestamp=datetime.now())


if __name__ == "__main__":
    unittest.main()
