def serialize_mongo(doc):
    doc["_id"] = str(doc["_id"])
    return doc