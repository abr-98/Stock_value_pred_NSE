from datetime import datetime


def parse_nse_annual_reports(resp_json):
    reports = []

    for item in resp_json.get("data", []):
        reports.append({
            "company": item.get("companyName"),
            "from_year": int(item["fromYr"]),
            "to_year": int(item["toYr"]),
            "submission_type": item.get("submission_type"),
            "broadcast_time": item.get("broadcast_dttm"),
            "dissemination_time": item.get("disseminationDateTime"),
            "file_url": item.get("fileName"),
            "file_type": "zip" if item.get("fileName", "").endswith(".zip") else "pdf"
        })

    return reports
