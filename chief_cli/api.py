"""Chief API client — thin wrapper around httpx."""

import json
import os
import time
from typing import Any, Dict, Optional

import httpx

from chief_cli.config import get_api_key, get_api_url, load_config
from chief_cli.log import logger

MAX_RETRIES = int(os.getenv("CHIEF_MAX_RETRIES", "3"))
RETRY_BACKOFF_BASE = 1.0
RETRY_BACKOFF_MAX = 30.0
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}
RETRYABLE_EXCEPTIONS = (httpx.ConnectError, httpx.TimeoutException)


_ERROR_HINTS = {
    401: ["Run: chief login", "Or set CHIEF_API_KEY env var"],
    403: ["You may not have access to this resource."],
    404: ["The resource was not found.", "Run: chief orgs list"],
    422: ["The request data is invalid."],
    429: ["Rate limit exceeded."],
    500: ["Server error. Try again in a few minutes."],
}


def format_error_hint(status_code: int) -> str:
    hints = _ERROR_HINTS.get(status_code, [])
    if not hints:
        return ""
    return "\n".join(f"  {h}" for h in hints)


class AuthError(Exception):
    pass


class APIError(Exception):
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class ChiefClient:
    """HTTP client for the Chief API."""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        self.api_key = api_key or get_api_key()
        self.api_url = api_url or get_api_url()

        if not self.api_key:
            raise AuthError("Not authenticated.\n  Run: chief login")

        config = load_config()
        self._timeout = float(os.getenv("CHIEF_TIMEOUT", config.get("timeout", 60)))
        self._client = httpx.Client(base_url=self.api_url, timeout=self._timeout)

    def _headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/json", "Authorization": f"ApiKey {self.api_key}"}

    def _request_with_retry(self, method: str, path: str, **kwargs) -> httpx.Response:
        last_exc = None
        for attempt in range(MAX_RETRIES + 1):
            try:
                resp = getattr(self._client, method)(path, headers=self._headers(), **kwargs)
                if resp.status_code not in RETRYABLE_STATUS_CODES or attempt == MAX_RETRIES:
                    return resp
                delay = min(RETRY_BACKOFF_BASE * (2 ** attempt), RETRY_BACKOFF_MAX)
                time.sleep(delay)
            except RETRYABLE_EXCEPTIONS as exc:
                last_exc = exc
                if attempt == MAX_RETRIES:
                    raise
                time.sleep(min(RETRY_BACKOFF_BASE * (2 ** attempt), RETRY_BACKOFF_MAX))
        raise last_exc or APIError("Request failed after retries")

    def get(self, path: str, params: Optional[Dict] = None) -> Any:
        resp = self._request_with_retry("get", path, params=params)
        return self._handle_response(resp)

    def post(self, path: str, data: Optional[Dict] = None) -> Any:
        resp = self._request_with_retry("post", path, json=data)
        return self._handle_response(resp)

    def put(self, path: str, data: Optional[Dict] = None) -> Any:
        resp = self._request_with_retry("put", path, json=data)
        return self._handle_response(resp)

    def delete(self, path: str) -> Any:
        resp = self._request_with_retry("delete", path)
        if resp.status_code == 204:
            return None
        return self._handle_response(resp)

    def _handle_response(self, resp: httpx.Response) -> Any:
        if resp.status_code == 401:
            raise AuthError("Not authenticated.")
        if resp.status_code >= 400:
            detail = ""
            try:
                body = resp.json()
                detail = body.get("detail", resp.text)
            except Exception:
                detail = resp.text
            hint = format_error_hint(resp.status_code)
            msg = f"API error {resp.status_code}: {detail}"
            if hint:
                msg += f"\n{hint}"
            raise APIError(msg, status_code=resp.status_code)
        return resp.json()

    # Organization operations
    def list_orgs(self, params: Optional[Dict] = None) -> list:
        data = self.get("/organizations", params=params)
        return data.get("data", data) if isinstance(data, dict) else data

    def get_org(self, org_id: str) -> dict:
        return self.get(f"/organizations/{org_id}")

    def create_org(self, data: dict) -> dict:
        return self.post("/organizations", data)

    def update_org(self, org_id: str, data: dict) -> dict:
        return self.put(f"/organizations/{org_id}", data)

    # Applet operations
    def list_applets(self, params: Optional[Dict] = None) -> list:
        data = self.get("/applets", params=params)
        return data.get("data", data) if isinstance(data, dict) else data

    def get_applet(self, applet_id: str) -> dict:
        return self.get(f"/applets/{applet_id}")

    # Release operations
    def get_latest_release(self, platform: Optional[str] = None) -> dict:
        path = f"/releases/latest/{platform}" if platform else "/releases/latest"
        return self.get(path)

    def check_update(self) -> dict:
        return self.get("/releases/check-update")

    # Metrics operations
    def get_portfolio_metrics(self) -> dict:
        return self.get("/metrics/portfolio")
