#!/usr/bin/python

from ansible.utils.display import Display
from ansible import constants as C
from collections import OrderedDict
import os

display = Display()

def k8s_filter(k8s_objects):
    resource_order = [
        'Secret',
        'ServiceAccount',
        'Group',
        'Role',
        'RoleBinding',
        'PersistentVolumeClaim',
        'ImageStream',
        'BuildConfig',
        'DeploymentConfig'
    ]
    no_log_true = ['Secret']

    resource_files = OrderedDict()
    # order the resources according to what's in resource_order
    for res in resource_order:
        for k8s_res in k8s_objects:
            if selected_object(res, k8s_res):
                if res in no_log_true:
                    resource_files[k8s_res] = True
                else:
                    resource_files[k8s_res] = False

    # append objects that might have been missed to the end
    for k8s_res in k8s_objects:
        if k8s_res not in resource_files.keys():
            resource_files[k8s_res] = False
    return resource_files

def selected_object(selector, k8s_object):
    playbook_dir = C.config.get_config_value("PLAYBOOK_DIR")

    if playbook_dir:
        k8s_file = open("%s/%s" % (playbook_dir, k8s_object))
    else:
        k8s_file = open(k8s_object)

    lines = k8s_file.readlines()
    k8s_file.close()

    for line in lines:
        line_sep = line.strip().split(':')
        if line_sep[0].strip() == 'kind':
            if line_sep[-1].strip() == selector:
                return True

def absolute_path(file_path):
    file_name = os.path.basename(file_path)
    return os.path.realpath(file_name)


class FilterModule(object):
    def filters(self):
        return {
            'k8s_filter': k8s_filter
        }

