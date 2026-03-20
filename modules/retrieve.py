from modules.db import get_collection

def retrieve(query, collection_name="human_db"):

    collection = get_collection(collection_name)

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    return results["documents"][0]