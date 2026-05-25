import pytest
from concurrent.futures import ThreadPoolExecutor
from utils.savanna_client import SavannaClient
from utils.wait_utils import wait_until_status


ACTIVE_STATUSES = ["Active", "Running", "Idle"]
SUSPENDED_STATUSES = ["Suspended", "Stopped", "Paused"]


def skip_if_api_not_available(response, api_name):
    print(f"{api_name} Status:", response.status_code)
    print(f"{api_name} Body:", response.text)

    if response.status_code in [403, 404]:
        pytest.skip(f"{api_name} API not available or permission denied")


@pytest.mark.resume
def test_tc07_auto_resume_from_api_request(client: SavannaClient):
    auto_resume_response = client.enable_auto_resume(True)
    skip_if_api_not_available(auto_resume_response, "Auto Resume")

    assert auto_resume_response.status_code in [200, 202]

    suspend_response = client.suspend_workspace()
    skip_if_api_not_available(suspend_response, "Suspend")

    assert suspend_response.status_code in [200, 202]

    wait_until_status(client, SUSPENDED_STATUSES, timeout=120, interval=10)

    response = client.run_query({})
    print("Query Status:", response.status_code)
    print("Query Body:", response.text)

    assert response.status_code in [200, 202, 503]

    status = wait_until_status(client, ACTIVE_STATUSES, timeout=180, interval=10)

    assert status in ACTIVE_STATUSES


@pytest.mark.resume
def test_tc08_auto_resume_disabled_should_not_resume(client: SavannaClient):
    auto_resume_response = client.enable_auto_resume(False)
    skip_if_api_not_available(auto_resume_response, "Auto Resume Disable")

    assert auto_resume_response.status_code in [200, 202]

    suspend_response = client.suspend_workspace()
    skip_if_api_not_available(suspend_response, "Suspend")

    assert suspend_response.status_code in [200, 202]

    wait_until_status(client, SUSPENDED_STATUSES, timeout=120, interval=10)

    response = client.run_query({"query": "ls"})
    print("Query Status:", response.status_code)
    print("Query Body:", response.text)

    assert response.status_code in [400, 409, 423, 503]

    status = client.get_status_value()

    if status is None:
        pytest.skip("Workspace status not available in API response")

    assert status in SUSPENDED_STATUSES


@pytest.mark.resume
def test_tc09_manual_resume_workspace(client: SavannaClient):
    suspend_response = client.suspend_workspace()
    skip_if_api_not_available(suspend_response, "Suspend")

    assert suspend_response.status_code in [200, 202]

    wait_until_status(client, SUSPENDED_STATUSES, timeout=120, interval=10)

    response = client.resume_workspace()
    skip_if_api_not_available(response, "Resume")

    assert response.status_code in [200, 202]

    status = wait_until_status(client, ACTIVE_STATUSES, timeout=180, interval=10)

    assert status in ACTIVE_STATUSES


@pytest.mark.resume
def test_tc10_concurrent_resume_requests(client: SavannaClient):
    auto_resume_response = client.enable_auto_resume(True)
    skip_if_api_not_available(auto_resume_response, "Auto Resume")

    assert auto_resume_response.status_code in [200, 202]

    suspend_response = client.suspend_workspace()
    skip_if_api_not_available(suspend_response, "Suspend")

    assert suspend_response.status_code in [200, 202]

    wait_until_status(client, SUSPENDED_STATUSES, timeout=120, interval=10)

    def trigger_query():
        return client.run_query({}).status_code

    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(lambda _: trigger_query(), range(5)))

    print("Concurrent response codes:", results)

    assert all(code in [200, 202, 409, 503] for code in results)

    status = wait_until_status(client, ACTIVE_STATUSES, timeout=180, interval=10)

    assert status in ACTIVE_STATUSES