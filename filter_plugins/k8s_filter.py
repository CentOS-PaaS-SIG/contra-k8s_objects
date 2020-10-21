#!/usr/bin/python

from collections import OrderedDict
from ansible.utils.display import Display
from ansible import constants as C
import os

display = Display()

def k8s_filter(k8s_objects):
    resource_files = []
    resource_order = ['ServiceAccount', 'Group', 'RoleBinding', 'PersistentVolumeClaim', 'Secret', 'ImageStream', 'BuildConfig', 'DeploymentConfig']
    for res in resource_order:
        resource_files.extend([k8 for k8 in k8s_objects if selected_object(res, k8)])
    resource_files.extend(k8s_objects)
    return list(OrderedDict.fromkeys(resource_files))

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

