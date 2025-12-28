from app.audit.registry import CHECK_REGISTRY
from app.models.audit_result import AuditResult

class AuditRunner:
    @staticmethod
    def run(api, audit_run, db):
        score = 100

        for check in CHECK_REGISTRY:
            result = check.execute(api)

            if not result["passed"]:
                score -= 20

            db.add(
                AuditResult(
                    audit_run_id=audit_run.id,
                    check_name=check.name,
                    passed=result["passed"],
                    severity=check.severity,
                    details=result["details"],
                )
            )

        audit_run.score = max(score, 0)
        db.commit()
