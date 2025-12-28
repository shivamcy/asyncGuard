import requests
from app.audit.checks.base import BaseCheck

class ErrorHandlingConsistencyCheck(BaseCheck):
    name = "error_handling_consistency"
    severity = "high"

    def execute(self, api):
        try:
            r = requests.get(f"{api.url}/non-existent-path", timeout=5)

            body = r.text.lower()

            leaked_keywords = ["traceback", "exception", "stack trace", "sqlalchemy"]

            leaks = [k for k in leaked_keywords if k in body]

            if leaks:
                return {
                    "passed": False,
                    "details": {
                        "leaked_information": leaks,
                        "response_snippet": body[:300],
                    },
                }

            return {
                "passed": True,
                "details": {
                    "message": "Error responses do not leak internal details",
                    "status_code": r.status_code,
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
