# utils.py
import os
import json
from datetime import datetime

OUTPUTS_FOLDER = "outputs"

def save_report(summary: dict, user_requirement: str):
    """Save the final crew summary as a JSON report in the outputs folder."""
    
    os.makedirs(OUTPUTS_FOLDER, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.json"
    filepath = os.path.join(OUTPUTS_FOLDER, filename)
    
    report = {
        "timestamp": timestamp,
        "user_requirement": user_requirement,
        "status": summary["status"],
        "total_iterations": summary["total_iterations"],
        "final_code": summary["final_code"],
        "iterations": summary["iterations"]
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    
    return filepath


def format_status_badge(status: str) -> str:
    """Return a formatted status string for display."""
    if status == "SUCCESS":
        return "✅ SUCCESS"
    return "❌ FAILED"