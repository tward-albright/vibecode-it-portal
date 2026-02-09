import json
from dataclasses import asdict, dataclass
from typing import List


# -------------------------
# User
# -------------------------
@dataclass(frozen=True)
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

    def key(self):
        return (self.issue.lower(), self.location.lower(), self.requester)

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
    def __init__(self, done_file="done_tickets.json"):
        self._tickets: List[Ticket] = []
        self._keys = set()
        self._done: List[Ticket] = []
        self.done_file = done_file
        self._load_done_tickets()

    def add_ticket(self, ticket: Ticket):
        key = ticket.key()
        if key in self._keys:
            print("⚠️  Duplicate ticket ignored.")
            return

        self._tickets.append(ticket)
        self._keys.add(key)

    def remove_ticket(self, index: int):
        if index < 0 or index >= len(self._tickets):
            print("\nInvalid ticket number.\n")
            return

        ticket = self._tickets.pop(index)
        self._keys.remove(ticket.key())

        self._done.append(ticket)
        self._save_done_tickets()

        print(f"\n✅ Ticket marked as done:\n{ticket}\n")

    def _save_done_tickets(self):
        with open(self.done_file, "w", encoding="utf-8") as f:
            json.dump(
                [{**asdict(t), "requester": asdict(t.requester)} for t in self._done],
                f,
                indent=2,
            )

    def _load_done_tickets(self):
        try:
            with open(self.done_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    user = User(**item["requester"])
                    ticket = Ticket(
                        issue=item["issue"],
                        location=item["location"],
                        urgency=item["urgency"],
                        requester=user,
                    )
                    self._done.append(ticket)
        except FileNotFoundError:
            pass

    def get_done_tickets(self) -> List[Ticket]:
        return self._done

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

    def queue_menu(self):
        print("Queue options:")
        print("1. Sort by urgency")
        print("2. Sort by location")
        print("3. Mark ticket as done")
        print("4. Exit")
        choice = input("Choose an option (1–4): ")

        if choice == "1":
            self.queue.sort_by_urgency()
            print("\nQueue sorted by urgency.\n")

        elif choice == "2":
            self.queue.sort_by_location()
            print("\nQueue sorted by location.\n")

        elif choice == "3":
            if not self.queue.get_tickets():
                print("\nNo tickets to mark as done.\n")
                return

            try:
                num = int(input("Enter ticket number to mark done: "))
                self.queue.remove_ticket(num - 1)
            except ValueError:
                print("\nPlease enter a valid number.\n")

        elif choice == "4":
            print("\nGoodbye!\n")
            exit()

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

    queue.add_ticket(Ticket("Access badge not working", "Main Entrance", 2, carol))
    queue.add_ticket(Ticket("Database backup failed", "Data Center", 5, bob))

    ui = TextUI(queue)

    while True:
        ui.display_queue()
        ui.queue_menu()
