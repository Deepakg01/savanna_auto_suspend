import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


class SavannaClient:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "").rstrip("/")
        self.api_key = os.getenv("API_KEY", "").strip()
        self.workgroup_id = os.getenv("WORKGROUP_ID", "").strip()
        self.workspace_id = os.getenv("WORKSPACE_ID", "").strip()
        self.restpp_url = os.getenv("RESTPP_URL", "").rstrip("/")
        self.graph_name = os.getenv("GRAPH_NAME", "").strip()
        self.query_name = os.getenv("QUERY_NAME", "").strip()

        self.headers = {
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }

    def workspace_url(self):
        return f"{self.base_url}/workgroups/{self.workgroup_id}/workspaces/{self.workspace_id}"

    def get_workspace_status(self):
        url = self.workspace_url()
        print("Final URL:", url)

        response = requests.get(url, headers=self.headers, timeout=30)

        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

        return response

    def set_auto_suspend_time(self, minutes):
        payload = {
            "autoSuspendMinutes": minutes
        }

        return requests.patch(
            self.workspace_url(),
            headers=self.headers,
            json=payload,
            timeout=30
        )

    def enable_auto_resume(self, enabled=True):
        payload = {
            "autoResume": enabled
        }

        return requests.patch(
            self.workspace_url(),
            headers=self.headers,
            json=payload,
            timeout=30
        )

    def suspend_workspace(self):
        return requests.post(
            f"{self.workspace_url()}/suspend",
            headers=self.headers,
            timeout=60
        )

    def resume_workspace(self):
        return requests.post(
            f"{self.workspace_url()}/resume",
            headers=self.headers,
            timeout=60
        )

    def run_query(self, params=None):
        if self.graph_name and self.query_name:
            url = f"{self.restpp_url}/query/{self.graph_name}/{self.query_name}"
            print("Query URL:", url)

            return requests.post(
                url,
                headers=self.headers,
                json=params or {},
                timeout=60
            )

        url = f"{self.restpp_url}/echo"
        print("Echo URL:", url)

        return requests.get(
            url,
            headers=self.headers,
            timeout=60
        )

    def get_status_value(self):
        response = self.get_workspace_status()
        response.raise_for_status()

        data = response.json()
        print("JSON Keys:", data.keys())

        return (
            data.get("status")
            or data.get("state")
            or data.get("workspaceStatus")
            or data.get("workspace_state")
            or data.get("phase")
            or data.get("health")
            or data.get("data", {}).get("status")
            or data.get("data", {}).get("state")
            or data.get("data", {}).get("phase")
            or data.get("workspace", {}).get("status")
            or data.get("workspace", {}).get("state")
        )

    def invalid_api_key_request(self):
        headers = {
            "x-api-key": "invalid_api_key",
            "Content-Type": "application/json"
        }

        return requests.get(
            self.workspace_url(),
            headers=headers,
            timeout=30
        )

    def invalid_workspace_request(self):
        fake_workspace_id = os.getenv(
            "INVALID_WORKSPACE_ID",
            "00000000-0000-0000-0000-000000000000"
        )

        url = f"{self.base_url}/workgroups/{self.workgroup_id}/workspaces/{fake_workspace_id}"

        return requests.get(
            url,
            headers=self.headers,
            timeout=30
        )