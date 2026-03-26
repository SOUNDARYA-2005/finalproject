import json
from jsonschema import validate, ValidationError

# Load schema once
with open("schemas/log_schema.json", "r") as f:
    schema = json.load(f)

def parse_log(log):
    try:
        structured_log = {
            "@timestamp": log.get("timestamp"),
            "level": log.get("level"),
            "service": log.get("service"),
            "message": log.get("message"),
            "ip": log.get("ip")
        }

        # Validate against schema
        validate(instance=structured_log, schema=schema)

        # Safe enrichment
        message = structured_log.get("message", "")
        structured_log["message_length"] = len(message)

        return structured_log

    except (ValidationError, KeyError, TypeError):
        return None