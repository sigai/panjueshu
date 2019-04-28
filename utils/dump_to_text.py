import json
from time import sleep
from datetime import datetime

from redis import Redis
import pymongo
from bson import ObjectId

r = Redis()
client = pymongo.MongoClient()
db = client.panjueshu
coll = db.case


def dump_mongo():
    docs = coll.find({})
    for doc in docs:
        oid = doc["_id"]
        doc.pop("_id")
        item = json.dumps(doc, ensure_ascii=False)
        try:
            with open("case.jl", mode="a", encoding="utf-8") as f:
                f.write(item + "\n")
            res = coll.delete_one({"_id": oid})
            if res.deleted_count:
                print(doc["CaseId"])
        except Exception as e:
            coll.update_one(doc, upsert=True)
            print(e)
        
def dump_redis():
    while True:
        items = r.spop("panjueshu:case", 1000)
        if not items:
            sleep(60)
            continue
        try:
            for item in items:
                doc = str(item, encoding="utf-8")
                with open("case_redis.jl", mode="a", encoding="utf-8") as f:
                    f.write(doc +"\n")
        except Exception as e:
            print(e)
            r.sadd("panjueshu:case", *items)
        now = datetime.now().isoformat(timespec="seconds")
        print(f"{now}[+] dumped {len(items)} item")
            

if __name__ == '__main__':
    dump_redis()
    
