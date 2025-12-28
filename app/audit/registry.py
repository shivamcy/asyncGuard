from app.audit.checks.security_headers import SecurityHeadersCheck
from app.audit.checks.cors import CORSCheck
from app.audit.checks.rate_limit import RateLimitingCheck
from app.audit.checks.authentication import AuthenticationRequiredCheck
from app.audit.checks.input_validation import InputValidationCheck
from app.audit.checks.rbac import RBACCheck
from app.audit.checks.http import HTTPMethodRestrictionCheck
from app.audit.checks.header_leakage import SensitiveHeaderLeakageCheck
from app.audit.checks.idempotency import IdempotencyCheck
from app.audit.checks.errors import ErrorHandlingConsistencyCheck

CHECK_REGISTRY = [
    SecurityHeadersCheck(),
    CORSCheck(),
    RateLimitingCheck(),
    AuthenticationRequiredCheck(),
    InputValidationCheck(),
    RBACCheck(),
    HTTPMethodRestrictionCheck(),
    SensitiveHeaderLeakageCheck(),
    IdempotencyCheck(),
    ErrorHandlingConsistencyCheck(),
]
