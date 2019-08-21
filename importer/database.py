from pymongo import MongoClient

URL = '127.0.0.1:27017'

class Database:
    def __init__(self):
        self.client = MongoClient(port=27017)
        self.db = self.client.gtfsrt

        #self.db.vehicle_position.create_index('position')
    
    def insert_many(self, gtfs):
        if not isinstance(gtfs, dict):
            print('gtfs not instance of dict')
            return
        if 'vehicle' in gtfs.keys():
            d = gtfs['vehicle']
            try:
                self.db.vehicle_position.insert_many(d, ordered = False)
            except Exception as e:
                print('Some write errors')
                #print('Write exception: ', e.details)
    
    def aggregate(self, collection, pipeline):
        return self.db[collection].aggregate(pipeline)
