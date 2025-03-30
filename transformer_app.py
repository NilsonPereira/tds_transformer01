import tango
import json
import time
import threading
import numpy as np
import os

class SENSOR():
    def __init__(self, source, params):
        self.source = source
        self.params = params
        self.name = source.split('/')[-1]
        self.ch_in = None
        self.ch_out = None
        self.ch_offset = None
        self.ch_outarray = None
        self.ch_timestamps = None
        self.ch_std = None
        self.ch_mean = None
        self.offset = 0.0
        self.std = 0.0
        self.mean = 0.0
        self.maxdim = 5000
        self.buf = np.array([], dtype='float')
        self.bufts = np.array([], dtype='float')
        self.outarray = np.array([], dtype='float')
        self.timestamps = np.array([], dtype='float')
        self.val = 0.0
        self.ts = 0.0
        self.eve = None
    def new_val(self, e):
        try:
            self.val = e.attr_value.value + self.offset
            self.ts = e.attr_value.time.tv_sec + (1e-6 * e.attr_value.time.tv_usec)
            self.ch_out.write(self.val)
            self.calcall()
        except Exception as err:
            print(err)
    def new_offset(self, e):
        newval = e.attr_value.value
        if newval != self.offset:
            self.offset = newval
            self.params[f"{self.name}_offset"] = self.offset
            self.eve.set()

    def calcall(self):
        self.buf = np.concatenate((self.buf, [self.val]))
        self.bufts = np.concatenate((self.bufts, [self.ts]))
        self.buf = self.buf[-self.maxdim:]
        self.bufts = self.bufts[-self.maxdim:]
        self.outarray = self.buf[self.bufts > (time.time() - np.abs(60*self.params['period']))]
        self.timestamps = self.bufts[self.bufts > (time.time() - np.abs(60*self.params['period']))]
        # if self.params['sma'] >= 2:
        #     window = int(np.round(self.params['sma']))
        #     weights = np.ones(window)/float(window)
        #     self.outarray = np.convolve(self.outarray, weights, 'same')
        self.ch_outarray.write(self.outarray)
        self.ch_timestamps.write(self.timestamps)
        self.std = 1000.0*np.std(self.outarray)
        self.mean = np.mean(self.outarray)
        self.ch_std.write(self.std)
        self.ch_mean.write(self.mean)
            
def main():
    ## load config file
    with open("config.json", 'r') as f:
        config = json.load(f)
    attrlist = config['attribute_list']
    device_out = config['device_out']

    ## parameter saving event
    eve = threading.Event()

    ## load parameters
    global params
    paramlist = ['period', 'sma']
    filename = config['param_file']
    if os.path.exists(filename) and os.path.isfile(filename):
        with open(filename, 'r') as f:
            params = json.load(f)
        print(f"[{time.asctime()}] Parameters loaded from: {filename}")
    else:
        params = {}
        for p in paramlist:
            params[p] = 1.0
        for a in attrlist:
            n = a.split('/')[-1] + '_offset'
            params[n] = 0.0
        eve.set()

    paramch = []
    def setparam(e):
        global params
        params[e.attr_value.name] = e.attr_value.value
        eve.set()
    for p in paramlist:
        ch = tango.AttributeProxy(f"{device_out[0]}/{p}")
        ch.write(params[p])
        ch.subscribe_event(tango.EventType.CHANGE_EVENT, setparam)
        paramch.append(ch)

    sensors = []
    for a in attrlist:
        sensors.append(SENSOR(a, params))
    for s in sensors:
        s.eve = eve
        s.ch_out = tango.AttributeProxy(f"{device_out[0]}/{s.name}")
        s.ch_offset = tango.AttributeProxy(f"{device_out[0]}/{s.name}_offset")
        s.ch_offset.write(params[f"{s.name}_offset"])
        s.offset = params[f"{s.name}_offset"]
        s.ch_outarray = tango.AttributeProxy(f"{device_out[0]}/{s.name}_outarray")
        s.ch_timestamps = tango.AttributeProxy(f"{device_out[0]}/{s.name}_timestamps")
        s.ch_std = tango.AttributeProxy(f"{device_out[0]}/{s.name}_std")
        s.ch_mean = tango.AttributeProxy(f"{device_out[0]}/{s.name}_mean")
        s.ch_offset.subscribe_event(tango.EventType.CHANGE_EVENT, s.new_offset)
        s.ch_in = tango.AttributeProxy(s.source)
        s.ch_in.subscribe_event(tango.EventType.CHANGE_EVENT, s.new_val)

    print("Listening...")
    while True:
        eve.wait()
        try:
            print(f"[{time.asctime()}] Saving parameters: {filename}")
            with open(filename, "w") as f:
                json.dump(params, f, indent=4)
        except Exception as err:
            print(err)
        eve.clear()
        time.sleep(1)

if __name__ == "__main__":
    main()
