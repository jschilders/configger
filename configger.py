from pathlib import Path
from nornir import InitNornir
from nornir.core.inventory import Inventory
from nornir.core.task import Task, Result
from nornir_jinja2.plugins.tasks import template_file, template_string

# Debug levels
DEBUG = 10
INFO =  20
WARN =  30
ERROR = 40
FATAL = 50

 
def config_cisco_ios(task: Task, template: str) -> Result:
    """Configure a Cisco IOS device

    Args:
        task (Task): Nornir Task object
        template (str): string containing changes to be made

    Returns:
        Result: Nornir Result object
    """
    return Result(
        #severity_level=DEBUG,
        host=task.host,
        result=f"Configured host {task.host.name}"
    )


def config_junos(task: Task, template: str) -> Result:
    """Configure a Junos device

    Args:
        task (Task): Nornir Task object
        template (str): string containing changes to be made

    Returns:
        Result: Nornir Result object
    """
    return Result(
        #severity_level=DEBUG,
        host=task.host,
        result=f"Configured host {task.host.name}"
    )


def select_devices(task_list: dict) -> Inventory:
    """Generate a filtered Nornir inventory containing only the needed devices
    (those mentioned in task_list) for this job and enhance this
    inventory with the data from the parameter
    Args:
        task_list (dict[hostname: str, parameters: dict]):
        Task list with a hostname as a key, and in the parameters dict,
        the template and the variables

    Returns:
        Inventory: Nornir Inventory object
    """
    
    inventory_dir = Path() / 'inventory' 
    host_file  =    str(inventory_dir / 'hosts.yaml')
    group_file =    str(inventory_dir / 'groups.yaml')
    defaults_file = str(inventory_dir / 'defaults.yaml')

    selection = InitNornir(
        inventory={
            'plugin': 'SimpleInventory',
            'options': {
                'host_file':     host_file,
                'group_file':    group_file,
                'defaults_file': defaults_file
            },
        },
        runner={
            'plugin': 'threaded',
            'options': {
                'num_workers': 10,
            },
        },
        logging={
            'enabled': True,
            'log_file': 'nornir.log',
            'level': 'DEBUG'
        }
    ).filter(filter_func=lambda host: host.name in task_list.keys())

    hosts_list =  selection.inventory.hosts.keys()
    groups_list = selection.inventory.groups.keys()
    
    for name, params in task_list.items():
        if name in hosts_list:
            selection.inventory.hosts[name].data.update(params)
        elif name in groups_list:
            selection.inventory.groups[name].data.update(params)
        elif name == 'defaults':
            selection.inventory.defaults.data.update(params)

    return selection


# Table of task names pointing to actual functions
task_table = {
    "junos":        config_junos,
    "cisco_ios":    config_cisco_ios
}


def run_tasks(task: Task) -> Result:
    """Perform configuration task for a specific host.

    Args:
        task (Task): Task object from Nornir

    Returns:    
        Result: Object containing result of this task
    """

    # generate the template
    params = task.host.extended_data()
    
    params['task_name'] = task.name
    params['task_host'] = task.host
       
    template_from_file     = params.pop('template', None)
    template_from_string   = params.pop('template_str', None)
    template_path          = params.pop('path', '')

    if template_from_string:
        result = task.run(task=template_string, template=template_from_string, **params)

    elif template_from_file:
        result = task.run(task=template_file, template=template_from_file, path=template_path, **params)

    # Config the device
    template = result[0].result
    job = task_table[task.host.platform]

    task.run(task=job, template=template)
    
    return Result(
        #severity_level=DEBUG,
        host=task.host,
        result=f">> Configger task {job.__name__!r} on host {task.host.name!r} with template {template!r}"
    )


def configger(task_list: dict[str, dict]) -> Result:
    """Perform configuration on hosts, as specified in joblist.
    'joblist' is a dict with the hostname as the key, and a
    dict of parameters as the value.

    Args:
        joblist dict[str, dict]: 
        Dictionary describing what jobs to run on what hosts.

    Returns:
        Result: Nornir Result object
    """
    selection = select_devices(task_list)
    return selection.run(task=run_tasks)

# ----------------------------------

def main():
    pass

if __name__ == '__main__':
    main()
