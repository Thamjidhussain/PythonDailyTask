# Design Notes

- Separate transport, business validation, report writing, and orchestration.
- Retry only timeouts, connection failures, and server errors; 4xx usually needs correction, not retry.
- Reject malformed rows individually and preserve valid records.
- First valid occurrence of an ID wins; later duplicates are rejected.
- Use atomic replacement for report writing to reduce partial files.
- Logs include error type and processing counts, not credentials or full payloads.
- Tests mock network calls and use temporary directories for repeatability.
