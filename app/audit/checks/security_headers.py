import httpx
from app.audit.checks.base import BaseCheck

REQUIRED_HEADERS = [
    "x-content-type-options",
    "x-frame-options",
    "content-security-policy",
    "strict-transport-security",
]

class SecurityHeadersCheck(BaseCheck):
    name = "security_headers"
    severity = "medium"

    def execute(self, api):
        response = httpx.get(api.url, timeout=5)

        headers = {k.lower(): v for k, v in response.headers.items()}
        missing = [h for h in REQUIRED_HEADERS if h not in headers]

        if missing:
            return {
                "passed": False,
                "details": {"missing_headers": missing},
            }

        return {
            "passed": True,
            "details": {"message": "All required security headers present"},
        }
