from app.audit.checks.headers import SecurityHeadersCheck

CHECK_REGISTRY = [
    SecurityHeadersCheck(),
]
