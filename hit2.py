import Singleton
mongo = Singleton.MongoModule.instance()
print(mongo.mongo_read_last_data())