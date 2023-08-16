from configger import configger
from nornir_utils.plugins.functions import print_result


template_string_for_pe1_eqam7 = """
This template is a string.

task.host is actually a nested dict:
  'task_host.name':     {{ task_host.name }}
  'task_host.data':     {{ task_host.extended_data() }}
  'task_host.hostname': {{ task_host.hostname }}

"""


parameter_dict = {
	 # default (global) parameters
	 'defaults': {
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
		'template_str': template_string_for_pe1_eqam7,
		'host_parm32':  'test',
		'host_parm42':  'test'
	},
	'br1.gs': {}
	
}


results = configger(parameter_dict)
print_result(results)


