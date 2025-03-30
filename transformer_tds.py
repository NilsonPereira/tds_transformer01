from tango.server import Device, attribute, command, device_property
import tango
import json
from attribute_template import get_template_float, get_template_array

class nmdev(Device):
    xdim = 5000

    with open("config.json", 'r') as f:
        config = json.load(f)
    attrlist = config['attribute_list']
    
    attr_all = []
    attr_float = ['period', 'sma']
    attr_array = []
    for a in attrlist:
        n = a.split('/')[-1]
        attr_float = attr_float + [f"{n}", f"{n}_offset", f"{n}_std", f"{n}_mean" ]
        attr_array = attr_array + [f"{n}_outarray", f"{n}_timestamps"]
    attr_all = attr_all + attr_float + attr_array

    for a in attr_float:
        exec(get_template_float(a))
    for a in attr_array:
        exec(get_template_array(a, xdim))    

    def init_device(self):
        super().init_device()
        for attr in self.attr_all:
                self.set_change_event(attr,True,False)
        self.set_state(tango.DevState.ON)

if __name__ == "__main__":
    nmdev.run_server()
    print("ok")