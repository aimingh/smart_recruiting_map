from pymongo import MongoClient

# 몽고DB에 대한 database를 다른 몽고 서버로 이동

# 한쪽 몽고db read
with MongoClient('mongodb://192.168.0.225:27017') as client1:
    db = client1.Jobinfo
    # alljob = list(db.alljob.find())
    # Joblist = list(db.Joblist.find())
    # Joblist2 = list(db.Joblist2.find())
    # keyword = list(db.keyword.find())
    db = client1.Mountain
    # mountain_info = list(db.mountain_info.find())
    # mountainList = list(db.mountainList.find())
    # placelist = list(db.placelist.find())
    # weatherlist = list(db.weatherlist.find())

# 다른 몽고db save
with MongoClient('mongodb://192.168.0.134:8088') as serverclient:
    db = serverclient.Jobinfo
    # db.alljob.insert_many(alljob)
    # db.Joblist.insert_many(Joblist)
    # db.Joblist2.insert_many(Joblist2)
    # db.keyword.insert_many(keyword)
    db = serverclient.Mountain
    # db.mountain_info.insert_many(mountain_info)
    # db.mountainList.insert_many(mountainList)
    # db.placelist.insert_many(placelist)
    # db.weatherlist.insert_many(weatherlist)
    