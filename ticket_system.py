from dataclasses import dataclass
from typing import List


# -------------------------
# User
# -------------------------
@dataclass
class User:
    name: str
    department: str

    def __str__(self):
        return f"{self.name} ({self.department})"


# -------------------------
# Ticket
# -------------------------
@dataclass
class Ticket:
    issue: str
    location: str
    urgency: int  # higher number = more urgent
    requester: User

    def __str__(self):
        return (
            f"[Urgency: {self.urgency}] "
            f"{self.issue} @ {self.location} "
            f"- Requested by {self.requester}"
        )


# -------------------------
# Queue
# -------------------------
class Queue:
    def __init__(self):
        self._tickets: List[Ticket] = []

    def add_ticket(self, ticket: Ticket):
        self._tickets.append(ticket)

    def get_tickets(self) -> List[Ticket]:
        return self._tickets

    def sort_by_urgency(self):
        self._tickets.sort(key=lambda t: t.urgency, reverse=True)

    def sort_by_location(self):
        self._tickets.sort(key=lambda t: t.location.lower())


# -------------------------
# TextUI
# -------------------------
class TextUI:
    def __init__(self, queue: Queue):
        self.queue = queue

    def display_queue(self):
        if not self.queue.get_tickets():
            print("The ticket queue is empty.\n")
            return

        print("\nCurrent Ticket Queue:")
        print("-" * 60)
        for i, ticket in enumerate(self.queue.get_tickets(), start=1):
            print(f"{i}. {ticket}")
        print("-" * 60 + "\n")

    def sort_menu(self):
        print("Sort tickets by:")
        print("1. Urgency")
        print("2. Location")
        choice = input("Choose an option (1 or 2): ")

        if choice == "1":
            self.queue.sort_by_urgency()
            print("\nQueue sorted by urgency.\n")
        elif choice == "2":
            self.queue.sort_by_location()
            print("\nQueue sorted by location.\n")
        else:
            print("\nInvalid choice.\n")


# -------------------------
# Demo / Example Usage
# -------------------------
if __name__ == "__main__":
    queue = Queue()

    # Create users
    alice = User("Alice", "Finance")
    bob = User("Bob", "Engineering")
    carol = User("Carol", "HR")

    # Add sample tickets
    queue.add_ticket(Ticket("Printer not working", "Office 2A", 2, alice))
    queue.add_ticket(Ticket("Server outage", "Data Center", 5, bob))
    queue.add_ticket(Ticket("Email access issue", "Office 1B", 3, carol))
    queue.add_ticket(Ticket("Wi-Fi down", "Office 3C", 4, alice))

    # Add more sample tickets
    queue.add_ticket(Ticket("Laptop overheating", "Office 4D", 1, bob))
    queue.add_ticket(Ticket("VPN connection failed", "Remote", 4, carol))
    queue.add_ticket(Ticket("Projector not displaying", "Conference Room A", 3, alice))
    queue.add_ticket(Ticket("Access badge not working", "Main Entrance", 2, carol))
    queue.add_ticket(Ticket("Database backup failed", "Data Center", 5, bob))

    ui = TextUI(queue)

    # Show initial queue
    ui.display_queue()

    # Let user sort and re-display
    ui.sort_menu()
    ui.display_queue()
