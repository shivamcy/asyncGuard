async def verify_role(role: str):
    valid_roles = {"viewer", "auditor"}
    if role not in valid_roles:
        raise ValueError(f"Invalid role: {role}. Valid roles are: {', '.join(valid_roles)}")