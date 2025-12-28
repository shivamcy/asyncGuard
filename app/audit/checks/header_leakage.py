import requests
from app.audit.checks.base import BaseCheck

class SensitiveHeaderLeakageCheck(BaseCheck):
    name = "sensitive_header_leakage"
    severity = "medium"

    def execute(self, api):
        try:
            r = requests.get(api.url, timeout=5)

            sensitive_headers = [
                "server",
                "x-powered-by",
                "x-aspnet-version",
            ]

            leaked = [
                h for h in sensitive_headers if h in r.headers
            ]

            if leaked:
                return {
                    "passed": False,
                    "details": {
                        "leaked_headers": leaked,
                        "headers": dict(r.headers),
                    },
                }

            return {
                "passed": True,
                "details": {
                    "message": "No sensitive headers exposed",
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
