import json
from time import sleep

from redis import Redis
import pymongo

r = Redis()
client = pymongo.MongoClient()
db = client.panjueshu
coll = db.case


def load():
    while True:
        item = r.spop("panjueshu:case")
        if not item:
            sleep(60*10)
            continue
        try:
            doc = json.loads(item)
            case_id = doc["CaseId"]
            res = coll.update_one({"CaseId": case_id}, {"$set":doc}, upsert=True)
            if res.upserted_id:
                print(f"[+] {res.upserted_id}")
        except Exception as e:
            print(e)
            r.sadd("panjueshu:case", item)


if __name__ == '__main__':
    load()
    
