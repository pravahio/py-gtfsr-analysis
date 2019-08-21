import os
import hashlib
import json
from datetime import datetime

from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict

GL_unique = {}

class GTFSRtReader:
    READ_TRIP_UPDATES = 0
    READ_VEHICLE_POSITION = 1
    READ_SERVICE_ALERTS = 3

    SAmode = False
    VPmode = False
    TUmode = False

    def __init__(self, path, read_mode):
        self.path = path

        a = []

        if isinstance(read_mode, int):
            a.append(read_mode)
        else:
            a.extend(read_mode)

        for i in a:
            if i == self.READ_SERVICE_ALERTS:
                self.SAmode = True
            if i == self.READ_VEHICLE_POSITION:
                self.VPmode = True
            if i == self.READ_TRIP_UPDATES:
                self.TUmode = True
    
    def read_file(self, f_name, tu, sa, vp):
        gtfs_msg = self.read_gtfs_rt_file(f_name)
        if gtfs_msg is None:
            return
        #print(f_name, ' Len: ', len(gtfs_msg.entity))
        
        for feed in gtfs_msg.entity:
            if self.TUmode and feed.HasField('trip_update'):
                tu.append(MessageToDict(feed.trip_update))
            if self.SAmode and feed.HasField('alert'):
                sa.append(MessageToDict(feed.alert))
            if self.VPmode and feed.HasField('vehicle'):
                mgg = MessageToDict(feed.vehicle)

                # check if timestamp, pos->lat, pos->long exist.
                cl_txt = (str(mgg['timestamp']) + str(mgg['position']['latitude']) + str(mgg['position']['longitude'])).encode('utf-8')

                dt = datetime.fromtimestamp(int(mgg['timestamp'][:10]))
                mgg['timestamp'] = dt

                mgg['_id'] = hashlib.md5(cl_txt).hexdigest()

                if mgg['_id'] in GL_unique:
                    continue
                GL_unique[mgg['_id']] = 1
                vp.append(mgg)
        
    def compute_res(self, tu, sa, vp):
        res = {}

        if len(sa) != 0:
            res['alert'] = sa
        if len(vp) != 0:
            res['vehicle'] = vp
        if len(tu) != 0:
            res['trip_update'] = tu
        
        return res
    
    def read(self):
        tu = []
        sa = []
        vp = []
        
        for r, d, f in os.walk(self.path):
            for file in f:
                f_name = os.path.join(r, file)
                self.read_file(f_name)
        
        return self.compute_res(tu, sa, vp)
    
    def read_batch(self, batch_size):
        tu = []
        sa = []
        vp = []
        
        cnt = 0
        for r, d, f in os.walk(self.path):
            for file in f:
                f_name = os.path.join(r, file)
                self.read_file(f_name, tu, sa, vp)
                if cnt % batch_size == 0:
                    yield self.compute_res(tu, sa, vp)
                    tu = []
                    sa = []
                    vp = []
        
        yield self.compute_res(tu, sa, vp)

    def read_gtfs_rt_file(self, fullpath):
        feed = gtfs_realtime_pb2.FeedMessage()
        with open(fullpath, 'rb') as f:
            data = f.read()
            try:
                feed.ParseFromString(data)
            except:
                print('Error parsing GTFS-RT')
                return None
            return feed