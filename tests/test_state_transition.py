import pytest
from utils.wait_utils import wait_until_status


ACTIVE_STATUSES = ["Active", "Running", "Idle"]
SUSPENDED_STATUSES = ["Suspended", "Stopped", "Paused"]


def validate_api_response(response, api_name):
    print(f"{api_name} Status:", response.status_code)
    print(f"{api_name} Body:", response.text)

    if response.status_code in [403, 404]:
        pytest.skip(f"{api_name} API not available or permission denied")

    assert response.status_code in [200, 202, 204]


@pytest.mark.state
def test_tc16_active_to_suspended_transition(client):
    response = client.set_auto_suspend_time(5)
    validate_api_response(response, "Set Auto Suspend")

    query_response = client.run_query({})
    print("Query Status:", query_response.status_code)
    print("Query Body:", query_response.text)

    assert query_response.status_code in [200, 202, 503]

    status = wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=180,
        interval=10
    )

    assert status in SUSPENDED_STATUSES


@pytest.mark.state
def test_tc17_suspended_to_active_transition(client):
    suspend_response = client.suspend_workspace()
    validate_api_response(suspend_response, "Suspend Workspace")

    wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=180,
        interval=10
    )

    resume_response = client.resume_workspace()
    validate_api_response(resume_response, "Resume Workspace")

    status = wait_until_status(
        client,
        expected_statuses=ACTIVE_STATUSES,
        timeout=180,
        interval=10
    )

    assert status in ACTIVE_STATUSES


@pytest.mark.state
def test_tc18_resume_request_during_suspended_state(client):
    auto_resume_response = client.enable_auto_resume(True)
    validate_api_response(auto_resume_response, "Enable Auto Resume")

    suspend_response = client.suspend_workspace()
    validate_api_response(suspend_response, "Suspend Workspace")

    wait_until_status(
        client,
        expected_statuses=SUSPENDED_STATUSES,
        timeout=180,
        interval=10
    )

    response = client.run_query({})
    print("Query Status:", response.status_code)
    print("Query Body:", response.text)

    assert response.status_code in [200, 202, 503]

    status = wait_until_status(
        client,
        expected_statuses=ACTIVE_STATUSES,
        timeout=180,
        interval=10
    )

    assert status in ACTIVE_STATUSES