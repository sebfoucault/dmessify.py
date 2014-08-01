import inspect
import os

def resource(resource_name):
    module = inspect.stack()[1][1]
    module_path = os.path.dirname(module)
    result = os.path.join(module_path, resource_name)
    return result

