import requests
from app.audit.checks.base import BaseCheck

class IdempotencySafetyCheck(BaseCheck):
    name = "idempotency_safety"
    severity = "high"

    def execute(self, api):
        try:
            payload = {"test": "idempotency"}

            r1 = requests.post(api.url, json=payload, timeout=5)
            r2 = requests.post(api.url, json=payload, timeout=5)

            if r1.status_code < 400 and r2.status_code < 400:
                return {
                    "passed": False,
                    "details": {
                        "issue": "Repeated POST requests accepted",
                        "first_status": r1.status_code,
                        "second_status": r2.status_code,
                    },
                }

            return {
                "passed": True,
                "details": {
                    "message": "API protects against duplicate POSTs",
                    "first_status": r1.status_code,
                    "second_status": r2.status_code,
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
