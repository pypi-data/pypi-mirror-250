import threading
import time


class NetworkMonitor:
    """A class that monitors network activity and determines when a page has loaded."""

    def __init__(self):
        """Initialize the network monitor."""
        self.request_log = {}
        self.response_log = set()
        self.last_active_time = None
        self.multi_request_found = False
        self.start_time = time.time()
        self.lock_request = threading.Lock()
        self.lock_response = threading.Lock()

    def track_request(self, request):
        """Track a request and record its timestamp into the last_active_time.

        Parameters:

        request (requests.PreparedRequest): The request to track."""
        with self.lock_request:
            current_time = time.time()
            self.last_active_time = current_time
            # Check if there are multiple requests to the same destination
            if request.url in self.request_log:
                self.multi_request_found = True
            # Start logging urls after the first 6 seconds
            if current_time - self.start_time > 6:
                self.request_log[request.url] = current_time

    def track_response(self, response):
        """Track a response and mark it in the network log.

        Parameters:

        response (requests.Response): The response to track."""
        with self.lock_response:
            current_time = time.time()
            if current_time - self.start_time > 6:
                if response.url in self.request_log:
                    self.response_log.add(response.url)

    def check_conditions(self) -> bool:
        """Check if the conditions for Page Ready state have been met

        Returns:

        bool: True if the conditions for Page Ready State have been met, False otherwise."""
        with self.lock_response and self.lock_request:
            # Check for inactivity
            current_time = time.time()
            missing_responses = []
            if current_time - self.last_active_time > 0.5:
                # Check if all requests have been resolved
                for request in self.request_log:
                    if request not in self.response_log:
                        missing_responses.append(request)

                # If not all requests have been resolved, check if 1.5 seconds have passed since the last request. If so, treat the request as resolved
                missing_responses_count = len(missing_responses)
                for missing_response in missing_responses:
                    time_diff = current_time - self.request_log[missing_response]
                    if time_diff > 1.5:
                        missing_responses_count -= 1

                if missing_responses_count == 0:
                    return True

            # If multiple requests to the same destination are found, then the page is loaded
            if self.multi_request_found:
                return True

            return False
