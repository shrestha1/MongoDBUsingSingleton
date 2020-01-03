from pymongo import MongoClient

class Singleton:

    def __init__(self,singleton_class):
        self._singleton_class = singleton_class

    def __call__(self):
        raise TypeError('Singletons are not callable')

    def instance(self):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._singleton_class()
            return self._instance
        
@Singleton
class SingletonLogger:

    def __init__(self):
        self.enabled = True
        print("Logger created")

    def __call__(self, function):
        print("inside logger")
        def log_function(*args, **kwargs):
            if self.enabled:
                print("\n{} is executed".format(function.__name__))
            return function(*args, **kwargs)
        return log_function

    def log_info_message(self, message):
        print("INFO: {}".format(message))
 
logger = SingletonLogger.instance()
# logger.log_info_message("from singleton logger") 


@Singleton
class MongoModule:

    def __init__(self):
        self.enabled = True

        self.connection = MongoClient("mongodb://localhost:27017/", username="", password="", authSource="sudhhalekha")
        self.db = self.connection["sudhhalekha"]
        self.col = self.db["TotalWords"]
        dbnames = self.connection.list_database_names()
        if "sudhhalekha" in dbnames:
            print("Accessing Database......")
            if "TotalWords" in self.db.list_collection_names():
                print("Accessing Collection...")
        else:
            print("Establishing Database, Please wait")
            self.db = self.connection["sudhhalekha"]
            self.col = self.db["TotalWords"]
            self.col.insert({"_id": 0, 'WORD': 'क', 'FREQUENCY': 23, 'INCORRECT_LIST': 'NAN',
                             'DEFINITION': 'प्राचीन लिपि देवनागरीबाट लिइएको प्रथम अक्षर।'})
            print("Database has been successfully established. Thank you !!!")

    # def __call__(self,function):
    #     print("Done")
    #     print("inside logger")
    #     def log_function(*args, **kwargs):
    #         if self.enabled:
    #             print("\n{} is executed".format(function.__name__))
    #         return function(*args, **kwargs)
    #     return log_function


    def load_wordDictionary(self):
        dfdata = pd.DataFrame(list(self.col.find()))
        # print(dfdata)
        WORDS = pd.Series(dfdata.FREQUENCY.values, index=dfdata.WORD).to_dict()

        return WORDS

    def mongo_read_last_data(self):
        d = self.col.find().sort([('_id', -1)]).limit(1)
        return [_ for _ in d]

    def message(self, message):
        print("INFO: {}".format(message))

# mongoModule = MongoModule.instance()
# @mongoModule
# def singleton_check():
#     mongoModule = MongoModule.instance()
#     print(mongoModule.mongo_read_last_data())

