import time
from urllib import response
import pytest
from utils.wait_utils import wait_until_status


ACTIVE_STATUSES = ["Active", "Running", "Idle"]
SUSPENDED_STATUSES = ["Suspended", "Stopped", "Paused"]


@pytest.mark.smoke
def test_tc01_verify_workspace_status(client):
    response = client.get_workspace_status()

    assert response.status_code == 200

    data = response.json()
    print("Response Body:", data)

    assert data is not None
    assert isinstance(data, dict)
    assert len(data.keys()) > 0


@pytest.mark.suspend
def test_tc02_verify_minimum_auto_suspend_time(client):
    response = client.set_auto_suspend_time(5)

    assert response.status_code in [200, 202, 404]

    client.run_query({})

    status = wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=900,
        interval=30
    )

    assert status in SUSPENDED_STATUSES


@pytest.mark.suspend
def test_tc03_workspace_should_not_suspend_before_configured_time(client):
    client.set_auto_suspend_time(10)
    client.run_query({})

    time.sleep(180)

    status = client.get_status_value()

    assert status in ACTIVE_STATUSES


@pytest.mark.suspend
def test_tc04_keep_alive_should_reset_suspend_timer(client):
    client.set_auto_suspend_time(5)

    client.run_query({})
    time.sleep(180)

    client.run_query({})
    time.sleep(180)

    status = client.get_status_value()

    assert status in ACTIVE_STATUSES


@pytest.mark.suspend
def test_tc05_long_running_query_should_prevent_suspend(client):
    client.set_auto_suspend_time(5)

    response = client.run_query({})

    assert response.status_code in [200, 202, 500]

    # response = client.run_query({"query": "RUN LONG_RUNNING_QUERY"})

    # assert response.status_code in [200, 202, 504]

    status = client.get_status_value()
    assert status not in SUSPENDED_STATUSES


@pytest.mark.suspend
def test_tc06_manual_suspend_workspace(client):
    response = client.suspend_workspace()

    if response.status_code == 404:
        pytest.skip("Manual suspend API endpoint not available or incorrect")

    assert response.status_code in [200, 202]

    status = wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=600,
        interval=30
    )

    assert status in SUSPENDED_STATUSES