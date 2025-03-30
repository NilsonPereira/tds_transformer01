def get_template_float(name):
    tlp = f'''
_{name} = 0.0
def read_{name}(self): return self._{name}
def write_{name}(self, val):
    self._{name} = val
    self.push_change_event('{name}', self._{name})
h_{name} = attribute(name='{name}', dtype='float', access=tango.READ_WRITE, fget=read_{name}, fset=write_{name})
    '''
    return tlp

def get_template_array(name, dim):
    tlp = f'''
_{name} = []
def read_{name}(self): return self._{name}
def write_{name}(self, val):
    self._{name} = val
    self.push_change_event('{name}', self._{name})
h_{name} = attribute(name='{name}', dtype=('float',), max_dim_x={dim}, access=tango.READ_WRITE, fget=read_{name}, fset=write_{name})
    '''
    return tlp
