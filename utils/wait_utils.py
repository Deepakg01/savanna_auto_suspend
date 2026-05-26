import time


def wait_until_status(client, expected_statuses, timeout=300, interval=15):
    end_time = time.time() + timeout
    last_status = None

    while time.time() < end_time:
        status = client.get_status_value()
        print(f"Current workspace status: {status}")

        last_status = status

        if status in expected_statuses:
            return status

        time.sleep(interval)

    assert False, (
        f"Workspace did not reach expected status {expected_statuses}. "
        f"Last observed status: {last_status}"
    )