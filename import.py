import sys
import os

from gtfsrt.reader import GTFSRtReader
from importer.database import Database

def main(argv):
    db = Database()
    gt = GTFSRtReader(argv[0], GTFSRtReader.READ_VEHICLE_POSITION)
    
    data_gen = gt.read_batch(100)
    cnt = 0
    for d in data_gen:
        db.insert_many(d)
        cnt = cnt + 1
        print('Processed ', cnt, ' batch(es)')

if __name__ == '__main__':
    main(argv = sys.argv[1:])
