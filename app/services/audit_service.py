from datetime import datetime
from app.models.audit_run import AuditRun
from app.models.api_endpoint import ApiEndpoints
from app.audit.runner import AuditRunner

class AuditService:
    @staticmethod
    def run_audit_sync(api_id: int, db):
        api = db.get(ApiEndpoints, api_id)
        if not api:
            raise ValueError("API not found")

        audit_run = AuditRun(
            api_id=api.id,
            score=0,
            time_window=datetime.utcnow(),
        )

        db.add(audit_run)
        db.commit()
        db.refresh(audit_run)

        AuditRunner.run(api, audit_run, db)
