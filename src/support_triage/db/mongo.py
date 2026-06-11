from pymongo import MongoClient

from support_triage.core.config import settings


client: MongoClient = MongoClient(settings.mongo_url)
database = client[settings.mongo_database]
raw_tickets = database["raw_tickets"]
llm_outputs = database["llm_outputs"]


def store_raw_ticket(ticket_id: int, body: str) -> None:
    raw_tickets.update_one(
        {"ticket_id": ticket_id},
        {"$set": {"ticket_id": ticket_id, "body": body}},
        upsert=True,
    )


def get_raw_ticket_body(ticket_id: int) -> str | None:
    document = raw_tickets.find_one({"ticket_id": ticket_id})
    if not document:
        return None
    return str(document.get("body", ""))


def store_llm_output(ticket_id: int, payload: dict) -> None:
    llm_outputs.update_one(
        {"ticket_id": ticket_id},
        {"$set": {"ticket_id": ticket_id, "payload": payload}},
        upsert=True,
    )
