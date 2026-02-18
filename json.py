import json
from datetime import datetime

ticket_data = {
    "ticket_id": "INC-2026-00421",
    "ticket_type": "Computer Request",
    "requester": {
        "student_id": "000543811",
        "name": "John Smith",
        "department": "Rossner"
    },
    "disc_details": {
        "asset_tag": "AST-SSD-7781",
        "disc_type": "SSD",
        "brand": "Samsung",
        "model": "870 EVO",
        "serial_number": "S3Z9NB0R123456X",
        "capacity_gb": 1000,
        "interface": "SATA",
        "encryption_enabled": True,
        "condition": "New"
    },
    "assignment": {
        "assigned_to": "IT Hardware Team",
        "assigned_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Pending Installation",
        "priority": "Medium"
    },
    "audit_trail": [
        {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "action": "Ticket Created",
            "performed_by": "John Connors"
        }
    ]
}

# Save JSON to file
with open("it_ticket_disc.json", "w") as file:
    json.dump(ticket_data, file, indent=4)

print("IT ticket disc record saved successfully!")
