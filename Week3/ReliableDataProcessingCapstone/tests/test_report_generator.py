import json
from report_generator import write_report

def test_report_summary_and_parent_directory(tmp_path):
    path = tmp_path / "nested" / "report.json"
    write_report([{"id": 1}], [{"index": 1, "reason": "bad"}], path)
    report = json.loads(path.read_text(encoding="utf-8"))
    assert report["summary"] == {"received": 2, "processed": 1, "rejected": 1}
    assert not path.with_suffix(".json.tmp").exists()
