from tango.server import Device, attribute, command
import tango
import time
import numpy as np

class nmdev(Device):
    # create attributes
    var01 = attribute(dtype='float', access=tango.READ)
    var01_offset = attribute(dtype='float', access=tango.READ_WRITE)
    var01_diff = attribute(dtype='float', access=tango.READ)
    var01_buf1h = attribute(dtype='DevVarFloatArray', max_dim_x=3600,access=tango.READ)
    var01_std1h = attribute(dtype='float', access=tango.READ)
    var01_buf6h = attribute(dtype='DevVarFloatArray', max_dim_x=21600, access=tango.READ)
    var01_std6h = attribute(dtype='float', access=tango.READ)

    ## tango attribute read functions
    def read_var01(self): return self._var01
    def read_var01_offset(self): return self._var01_offset
    def write_var01_offset(self, val): self._var01_offset = val
    def read_var01_diff(self): return self._var01_diff
    def read_var01_buf1h(self): return self._var01_buf1h
    def read_var01_std1h(self): return self._var01_std1h
    def read_var01_buf6h(self): return self._var01_buf6h
    def read_var01_std6h(self): return self._var01_std6h

def init_device(self):
        super().init_device()
        self.set_state(tango.DevState.ON)
        self.set_change_event("var01", True, False)

        # create device proxy
        self.plcdev = tango.DeviceProxy('test/Clock/1')

print("OK")