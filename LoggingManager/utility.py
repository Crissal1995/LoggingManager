import inspect
from .logger import Levels


def retrieve_name(var):
    """
    Gets the name of var. Does it from the out most frame inner-wards.
    :param var: variable to get name from.
    :return: string
    """
    for fi in reversed(inspect.stack()):
        names = [var_name for var_name, var_val in fi.frame.f_locals.items() if var_val is var]
        if len(names) > 0:
            return names[0]


def check_parameter(obj, obj_name):
    types = {
        'filepath': str,
        'append': bool,
        'level': Levels,
    }
    if obj_name not in types:
        raise ValueError('{} not in valid parameters: {}'.format(obj_name, types.keys()))
    if not isinstance(obj, types.get(obj_name)):
        raise TypeError(
            'expected {e}, got {a} (parameter {p})'
            .format(p=obj_name, e=types.get(obj_name), a=type(obj))
        )
    print('everything ok!')


def get_level(string: str) -> Levels:
    values = {
        'notset':   Levels.NOTSET,
        'debug':    Levels.DEBUG,
        'info':     Levels.INFO,
        'warning':  Levels.WARNING,
        'error':    Levels.ERROR,
        'critical': Levels.CRITICAL
    }
    string = string.lower()
    if string not in values:
        raise ValueError('{p} not in {vs}'.format(p=string, vs=values.keys()))
    return values[string]
