from inventory import select_devices

params = {
   'defaults': {
     # default (global) parameters
    'template':      'templates/template.j2',
    'default_parm5': 'test',
    'default_parm6': 'test'
  },
  # parameters for group 'cli_junos_ssh'
  'cli_junos_ssh': {
    'group_parm1':   'test',
    'group_parm2':   'test'
  },
  'pe1.gs': {
     # parameters for group 'cli_junos_ssh'
    'host_parm31':  'test',
    'host_parm41':  'test'
  },
  'pe1.eqam7': {
     # parameters for group 'cli_junos_ssh'
    'template_string': 'template_string_for_pe1.eqam7.j2',
    'host_parm32':  'test',
    'host_parm42':  'test'
  },
  
}


selection = select_devices(params)

#hosts_list =  selection.inventory.hosts.keys()
#groups_list = selection.inventory.groups.keys()
#
#for name, params in params.items():
#  
#  if name in hosts_list:
#    selection.inventory.hosts[name].data = params
#    
#  elif name in groups_list:
#    selection.inventory.groups[name].data = params
#    
#  elif name == 'defaults':
#    selection.inventory.defaults.data = params
#
print('-'*30)  

print(selection.inventory.defaults.data)

print('-'*30)  

for g in selection.inventory.groups.values():
  print(g.name, g.extended_data())

print('-'*30)

for h in selection.inventory.hosts.values():
  print(h.name, h.extended_data())
