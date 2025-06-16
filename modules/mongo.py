from pymongo import MongoClient

def get_city_counts(release, namespace):
    # Static Credentials for Dev Environment, Don't use it in Prod.
    client = MongoClient(f"mongodb://root:changeme@{release}-mongodb.{namespace}.svc.cluster.local:27017")
    db = client["weather_db"]
    collection = db["search_stats"]
    parser = collection.find({}, {"_id": 0, "city": 1, "count": 1}).sort("count", -1)
    return [(doc['city'], doc['count']) for doc in parser]
