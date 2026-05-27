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

    def build_url(self, path_template):
        path = path_template.format(
            workgroup_id=self.workgroup_id,
            workspace_id=self.workspace_id
        )
        return f"{self.base_url}{path}"

    def _request(self, method, url, headers=None, **kwargs):
        print(f"\n{method.upper()} URL:", url)

        if "json" in kwargs:
            print("Payload:", kwargs["json"])

        response = requests.request(
            method=method,
            url=url,
            headers=headers or self.headers,
            timeout=kwargs.pop("timeout", 60),
            **kwargs
        )

        print("Status Code:", response.status_code)
        print("Response Body:", response.text)

        return response

    def workspace_url(self):
        path = os.getenv(
            "WORKSPACE_STATUS_PATH",
            "/workgroups/{workgroup_id}/workspaces/{workspace_id}"
        )
        return self.build_url(path)

    def get_workspace_status(self):
        return self._request("get", self.workspace_url(), timeout=30)

    def set_auto_suspend_time(self, minutes):
        path = os.getenv(
            "AUTO_SUSPEND_PATH",
            "/workgroups/{workgroup_id}/workspaces/{workspace_id}"
        )

        payload = {
            "auto_stop_minutes": minutes
        }

        return self._request(
            "put",
            self.build_url(path),
            json=payload,
            timeout=30
        )

    def enable_auto_resume(self, enabled=True):
        path = os.getenv(
            "AUTO_RESUME_PATH",
            "/workgroups/{workgroup_id}/workspaces/{workspace_id}"
        )

        payload = {
            "autoResume": enabled,
            "auto_resume": enabled
        }

        return self._request(
            "put",
            self.build_url(path),
            json=payload,
            timeout=30
        )

    def suspend_workspace(self):
        path = os.getenv(
            "SUSPEND_PATH",
            "/workgroups/{workgroup_id}/workspaces/{workspace_id}/pause"
        )
        

        return self._request(
            "post",
            self.build_url(path),
            timeout=60
        )

    def resume_workspace(self):
        path = os.getenv(
            "RESUME_PATH",
            "/workgroups/{workgroup_id}/workspaces/{workspace_id}/resume"
        )

        return self._request(
            "post",
            self.build_url(path),
            timeout=60
        )

    def run_query(self, params=None):
        if self.graph_name and self.query_name:
            url = f"{self.restpp_url}/query/{self.graph_name}/{self.query_name}"

            return self._request(
                "post",
                url,
                json=params or {},
                timeout=60
            )

        url = f"{self.restpp_url}/echo"

        return self._request(
            "get",
            url,
            timeout=60
        )

    def get_status_value(self):
        response = self.get_workspace_status()
        response.raise_for_status()

        data = response.json()
        print("Full JSON:", data)

        result = data.get("Result")

        if isinstance(result, dict):
            return (
            result.get("status")
            or result.get("state")
            or result.get("workspace_status")
            or result.get("workspaceState")
            or result.get("desired_status")
            or result.get("current_status")
            or result.get("health")
        )

        return (
        data.get("status")
        or data.get("state")
        or data.get("workspace_status")
        or data.get("workspaceState")
    )

    def invalid_api_key_request(self):
        headers = {
            "x-api-key": "invalid_api_key",
            "Content-Type": "application/json"
        }

        return self._request(
            "get",
            self.workspace_url(),
            headers=headers,
            timeout=30
        )

    def invalid_workspace_request(self):
        fake_workspace_id = os.getenv(
            "INVALID_WORKSPACE_ID",
            "00000000-0000-0000-0000-000000000000"
        )

        path = os.getenv(
            "WORKSPACE_STATUS_PATH",
            "/workgroups/{workgroup_id}/workspaces/{workspace_id}"
        )

        url = f"{self.base_url}{path.format(workgroup_id=self.workgroup_id, workspace_id=fake_workspace_id)}"

        return self._request(
            "get",
            url,
            timeout=30
        )