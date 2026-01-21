class Request
    """Defining what a person needs from IT"""
    def __init__ 
    import heapq


#Request Class

class Request:
    def __init__(self, status, location, priority):
        self.status = status
        self.location = location
        self.priority = priority

    def __str__(self):
        return f"Status: {self.status}, Location: {self.location}, Priority: {self.priority}"


#Request Queue
class RequestQueue:
    def __init__(self):
        self.queue = []
        self.counter = 0  # Ensures FIFO for same priority

    def add_request(self, request):
        # Negative priority because heapq is a min-heap
        heapq.heappush(self.queue, (-request.priority, self.counter, request))
        self.counter += 1

    def process_request(self):
        if not self.queue:
            return None
        return heapq.heappop(self.queue)[2]

    def display_queue(self):
        if not self.queue:
            print("Queue is empty.")
            return

        for item in sorted(self.queue, reverse=True):
            print(item[2])


#driver code

def main():
    request_queue = RequestQueue()

    request_queue.add_request(Request("Open", "New York", 3))
    request_queue.add_request(Request("In Progress", "Chicago", 5))
    request_queue.add_request(Request("Open", "Los Angeles", 2))
    request_queue.add_request(Request("Open", "Houston", 5))

    print("Current Queue:")
    request_queue.display_queue()

    print("\nProcessing Requests:")
    while True:
        request = request_queue.process_request()
        if not request:
            break
        print("Processing ->", request)


if __name__ == "__main__":
    main()
