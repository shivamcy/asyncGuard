import requests
from app.audit.checks.base import BaseCheck

class HTTPMethodRestrictionCheck(BaseCheck):
    name = "http_method_restriction"
    severity = "medium"

    def execute(self, api):
        results = {}

        try:
            methods = ["PUT", "DELETE", "PATCH"]

            for method in methods:
                r = requests.request(method, api.url, timeout=5)
                results[method] = r.status_code

            allowed = [
                m for m, code in results.items() if code < 400
            ]

            if allowed:
                return {
                    "passed": False,
                    "details": {
                        "unexpected_allowed_methods": allowed,
                        "results": results,
                    },
                }

            return {
                "passed": True,
                "details": {
                    "message": "HTTP methods restricted properly",
                    "results": results,
                },
            }

        except Exception as e:
            return {
                "passed": False,
                "details": {"error": str(e)},
            }
