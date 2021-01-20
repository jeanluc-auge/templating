import inspect
import functools
import cep
from munch import munchify
from argparse import ArgumentParser
from jinja2 import Environment, FileSystemLoader

def wrap(func):
    @functools.wraps(func)
    def wrapper(**kwargs):
        return func(**kwargs)

    return wrapper


def add_path(rest_method, api_path):
    """
    bypass decorator to modify the original function
    it replaces the original @api_request decorator
    Returns:
        function with additional attributs
        new attributs = decorator parmaeters
    The simplest option would have been to add args to the func kwargs,
    but the func is generic and it may not have **kwargs...
    """

    def outer_wrap(func):
        func.rest_method = rest_method
        func.api_path = api_path
        return wrap(func)

    return outer_wrap


def get_func_args(func):
    """
    retrieve function args and attributs
    :param
    func: string func signature
    func_name: string func name
    namespace: flask namespace corresponding to the code project or library
    :return: Dict of method args
    """
    func_args = {}
    # use inspect method to retrieve all args:
    func_args["all_args"] = [
        k for k in inspect.signature(func).parameters if k != "self"
    ]

    func_args['path_args'] = [
        arg
        for arg in func_args["all_args"]
        if (arg in func.api_path)
    ]

    func_args['free_args'] = [
        arg
        for arg in func_args["all_args"]
        if (arg not in func.api_path)
    ]

    print(f'func {func.__name__} args = {func_args}')
    return func_args


def get_class_name(func, namespace):
    """
    create flask class from function endpoint
    create a common flask class for all methods (get, put...) of an endpoint
    Args:
        str unformated_endpoint: the original endpoint defined in as '/...{}'
        str namespace
    Returns:
        str class_name: the common flask class for all methods
    """
    class_name = (
        func.api_path
        .strip("/")
        .replace("{", "")
        .replace("}", "")
        .replace("/", "_")
        .replace("-", "")
        .capitalize()
    )
    if class_name == "":
        class_name = (namespace + "_").capitalize()

    print(f'class_name: {class_name}')
    return class_name


def get_endpoint(func, func_args):
    """
    generate flask endpoint from decorator endpoint in list_func_args[1]
    Args:
        str api_path: the original endpoint defined in as '/...{}'
        list all_args: the function parameters
    Returns:
        formated endpoint for flask as '/...<int:>'
    """
    endpoint_args = {}
    for arg in func_args["path_args"]:
        if ("Id" in arg) or ("id" in arg):
            endpoint_args[arg] = f"<int:{arg}>"
        else:
            endpoint_args[arg] = f"<string:{arg}>"
    return func.api_path.format(**endpoint_args)


def record_endpoints(namespace):
    """
    generate a dict of all functions in a given namespace/class
    the searched namespace has to be a class in the module cep.py

    args:
        str namespace
    returns:
        dict endpoints

    """
    endpoints = {}
    cls = getattr(cep, namespace)
    for func_name in dir(cls):
        func = getattr(cls, func_name) # func object
        if callable(func) and "__" not in func_name:
            func_args = get_func_args(func)
            class_name = get_class_name(func, namespace)
            endpoint_name = get_endpoint(func, func_args)
            method = {
                'rest_method': func.rest_method,
                'func_name': func.__name__,
                'func_args': func_args,
            }
            if endpoint_name not in endpoints:
                endpoints[endpoint_name] = {
                    'class': class_name,
                    'methods': [method]
                }
            else:
                endpoints[endpoint_name]['methods'].append(method)
    print(f'endpoints: {endpoints}')
    return munchify(endpoints)

def record_namespace():
    output = ""
    exclude_list = ["__", "add_args", "add_path"]
    # {class_name=namespace: class_doc_string=client}
    namespaces = {
        namespace: getattr(cep, namespace).__doc__
        for namespace in dir(cep)
        if not any(x in namespace for x in exclude_list)
    }
    print(f'flask namespace: client: {namespaces}')
    return namespaces

def record_template_data():
    """
    render a namespace template
    generate all the flask endpoints for a namespace
    """
    namespaces = record_namespace()
    for namespace, client in namespaces.items():
        endpoints = record_endpoints(namespace)
        data_to_render = {"endpoints": endpoints, "namespace": namespace, "client": client}
        yield data_to_render


def render_code():
    """
    Final
    iterate over all namespace/class defined in cep.py module
    For each class <=> flask namespace
    concatenate the template output for each class by calling render namespace
    The resulting output needs to be copied manually in restplus.py flask module
    Returns:
        output template in file_for_flask
    """
    output = ""

    file_loader = FileSystemLoader("")
    env = Environment(loader=file_loader)
    # template = env.get_template('xtesting/template/Jenkinsfile_template.banc')
    template = env.get_template("template_endpoints")
    for data_to_render in record_template_data():
        print(f'rendering data: {data_to_render}')
        output += template.render(**data_to_render)
    print(f'template output:\n {output}')


if __name__ == "__main__":
    render_code()