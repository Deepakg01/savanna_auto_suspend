import pytest
from utils.wait_utils import wait_until_status


ACTIVE_STATUSES = ["Active", "Running", "Idle"]
SUSPENDED_STATUSES = ["Suspended", "Stopped", "Paused"]


@pytest.mark.state
def test_tc16_active_to_suspended_transition(client):
    client.set_auto_suspend_time(5)
    client.run_query("SELECT 1")

    status = wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=900,
        interval=30
    )

    assert status in SUSPENDED_STATUSES


@pytest.mark.state
def test_tc17_suspended_to_active_transition(client):
    client.suspend_workspace()

    wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=600,
        interval=30
    )

    client.resume_workspace()

    status = wait_until_status(
        client,
        expected_statuses=ACTIVE_STATUSES,
        timeout=900,
        interval=30
    )

    assert status in ACTIVE_STATUSES


@pytest.mark.state
def test_tc18_resume_request_during_suspended_state(client):
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