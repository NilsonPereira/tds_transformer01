from tango.server import Device, attribute, command, device_property
import tango
import time
import numpy as np
import threading

class nmdev(Device):
    ## config
    buffer_size = 500000
    period_min = 1 # minute
    period_max = 10080 # 1 week

    # create attributes
    period = attribute(dtype='float', access=tango.READ_WRITE)
    t01 = attribute(dtype='float', access=tango.READ)
    t01_offset = attribute(dtype='float', access=tango.READ_WRITE)
    t01_std = attribute(dtype='float', access=tango.READ)
    t01_outarray = attribute(dtype=('float',), max_dim_x=500000, access=tango.READ)
    t01_buf = []
    t01_buf_ts = []

    

    ## list of attributes
    attr_list = ['t01', 't01_offset', 't01_std', 't01_outarray']

    def process_outarray(self):
        print(f"process_outarray all")

    ## tango attribute read functions
    def read_period(self): return self._period
    def write_period(self, v): 
         v = np.min([v, self.period_max])
         v = np.max([v, self.period_min])
         self._period = int(np.round(v))
    def read_t01(self): return self._t01
    def read_t01_offset(self): return self._t01_offset
    def write_t01_offset(self, val): 
         self._t01_offset = val
         self.process_outarray()
    def read_t01_std(self): return self._t01_std
    def read_t01_outarray(self): return self._t01_outarray

    ## init variables
    _period = 1.0
    _t01 = 0.0
    _t01_offset = 0.0
    _t01_std = 0.0
    _t01_outarray = []

    def monitor_thread(self):
        def updt(event_data):
            n = event_data.attr_name
            v = event_data.attr_value.value
            ts = event_data.attr_value.time
            self._t01 = v
            self.push_change_event('t01', self._t01)
            #print(f"name: {n}, v: {v}, TS: {ts}")
        labstat02 = tango.DeviceProxy('labstatus02/nmdev/labstatus')
        poll_event_id = labstat02.subscribe_event('var01', tango.EventType.CHANGE_EVENT, updt)
        while True:
            time.sleep(1)

    def init_device(self):
            t = threading.Thread(target=self.monitor_thread)
            t.start()
            super().init_device()
            for attr in self.attr_list:
                self.set_change_event(attr,True,False)
            self.set_state(tango.DevState.ON)

    
if __name__ == "__main__":
    nmdev.run_server()
    print("ok")
