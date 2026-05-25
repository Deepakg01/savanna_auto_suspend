import time
import pytest


def wait_until_status(client, expected_statuses, timeout=120, interval=10):
    end_time = time.time() + timeout

    while time.time() < end_time:
        status = client.get_status_value()
        print(f"Current workspace status: {status}")

        if status is None:
            pytest.skip("Workspace status not available in API response")

        if status in expected_statuses:
            return status

        time.sleep(interval)

    pytest.skip(f"Workspace did not reach expected status {expected_statuses}")