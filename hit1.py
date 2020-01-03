# from Singleton import singleton_check
import Singleton
mongo = Singleton.MongoModule.instance()
mongo.message("inside File hit1")
# print("File hit1")
# singleton_check()
