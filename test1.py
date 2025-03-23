from tango.server import Device, attribute, command, device_property
import tango
import time
import numpy as np
import threading
import inspect

class nmdev(Device):
    num_of_attr = 20
    attrlist = []
    for i in range(num_of_attr):
        attrlist.append("temp_{:02d}".format(i+1))
    #attrlist = ['t01', 't02', 't03', 't04']
    N = len(attrlist)
    hvar = [0.0]*N
    hlist = [0]*N
    def hread(self, id):
        return self.hvar[id]
    def hwrite(self, v, id):
        self.hvar[id] = v
    for i in range(N):
        exec(f'def hread{i}(self): return self.hread({i})')
        exec(f'def hwrite{i}(self, v): self.hwrite(v,{i})')
        exec(f"h{i} = attribute(name='{attrlist[i]}', dtype='float', access=tango.READ_WRITE, fget='hread{i}', fset='hwrite{i}')")

    def init_device(self):
        super().init_device()
        #for attr in self.attr_list:
        #    self.set_change_event(attr,True,False)
        self.set_state(tango.DevState.ON)

if __name__ == "__main__":
    nmdev.run_server()
    print("ok")