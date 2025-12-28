from app.audit.checks.security_headers import SecurityHeadersCheck

CHECK_REGISTRY = [
    SecurityHeadersCheck(),
]
