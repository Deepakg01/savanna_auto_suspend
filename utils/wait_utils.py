import time


def wait_until_status(client, expected_statuses, timeout=600, interval=30):
    end_time = time.time() + timeout

    while time.time() < end_time:
        status = client.get_status_value()
        print(f"Current workspace status: {status}")

        if status in expected_statuses:
            return status

        time.sleep(interval)

    raise TimeoutError(
        f"Workspace did not reach expected status {expected_statuses} within {timeout} seconds"
    )