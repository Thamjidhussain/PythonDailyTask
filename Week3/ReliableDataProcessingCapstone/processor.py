def process_records(payload):
    """Return (valid_records, rejected_records); first valid duplicate ID wins."""
    if not isinstance(payload, list):
        raise ValueError("Expected API payload to be a list")
    valid, rejected, seen = [], [], set()
    for index, row in enumerate(payload):
        reason = None
        if not isinstance(row, dict):
            reason = "record must be an object"
        elif not isinstance(row.get("id"), int) or isinstance(row.get("id"), bool):
            reason = "id must be an integer"
        elif not isinstance(row.get("name"), str) or not row["name"].strip():
            reason = "name is required"
        elif not isinstance(row.get("email"), str) or "@" not in row["email"]:
            reason = "email is invalid"
        elif row["id"] in seen:
            reason = "duplicate id"
        if reason:
            rejected.append({"index": index, "reason": reason, "record": row})
        else:
            seen.add(row["id"])
            valid.append({"id": row["id"], "name": row["name"].strip(),
                          "email": row["email"].strip().lower()})
    return valid, rejected
