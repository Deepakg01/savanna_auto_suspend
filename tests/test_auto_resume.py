import pytest
from concurrent.futures import ThreadPoolExecutor
from utils.wait_utils import wait_until_status


ACTIVE_STATUSES = ["Active", "Running", "Idle"]
SUSPENDED_STATUSES = ["Suspended", "Stopped", "Paused"]


@pytest.mark.resume
def test_tc07_auto_resume_from_api_request(client):
    client.enable_auto_resume(True)
    client.suspend_workspace()

    wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=600,
        interval=30
    )

    response = client.run_query("SELECT 1")

    assert response.status_code in [200, 202, 503]

    status = wait_until_status(
        client,
        expected_statuses=ACTIVE_STATUSES,
        timeout=900,
        interval=30
    )

    assert status in ACTIVE_STATUSES


@pytest.mark.resume
def test_tc08_auto_resume_disabled_should_not_resume(client):
    client.enable_auto_resume(False)
    client.suspend_workspace()

    wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=600,
        interval=30
    )

    response = client.run_query("SELECT 1")

    assert response.status_code in [400, 409, 423, 503]

    status = client.get_status_value()

    assert status in SUSPENDED_STATUSES


@pytest.mark.resume
def test_tc09_manual_resume_workspace(client):
    client.suspend_workspace()

    wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=600,
        interval=30
    )

    response = client.resume_workspace()

    assert response.status_code in [200, 202]

    status = wait_until_status(
        client,
        expected_statuses=ACTIVE_STATUSES,
        timeout=900,
        interval=30
    )

    assert status in ACTIVE_STATUSES


@pytest.mark.resume
def test_tc10_concurrent_resume_requests(client):
    client.enable_auto_resume(True)
    client.suspend_workspace()

    wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=600,
        interval=30
    )

    def trigger_query():
        return client.run_query("SELECT 1").status_code

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda _: trigger_query(), range(5)))

    print("Concurrent response codes:", results)

    assert all(code in [200, 202, 409, 503] for code in results)

    status = wait_until_status(
        client,
        expected_statuses=ACTIVE_STATUSES,
        timeout=900,
        interval=30
    )

    assert status in ACTIVE_STATUSES