from app.audit.checks.base import BaseCheck
import requests

class RBACCheck(BaseCheck):
    name = "rbac"
    severity = "high"
    def execute(self, api):
        try:
            headers = {
                "Authorization": "Bearer invalid_token_or_lower_privilege"
            }
            r = requests.get(api.url, headers=headers, timeout=5)

            if r.status_code in [200, 201]:
                return {
                    "passed": False,
                    "details": {
                        "issue": "Endpoint accessible without proper role",
                        "status_code": r.status_code,
                    },
                }
            return {
                "passed": True,
                "details": {
                    "message": "RBAC enforced properly",
                    "status_code": r.status_code,
                },
            }
        
        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }

