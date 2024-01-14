import time, colorama, inspect
from types import NoneType
from typing import Any

colvals = {
    int      : colorama.Fore.YELLOW,
    float    : colorama.Fore.YELLOW,
    str      : colorama.Fore.WHITE,
    complex  : colorama.Fore.CYAN,
    NoneType : colorama.Fore.MAGENTA
}

timestamps : bool = False

def log(*values, end : str = '\n', indent : int = 0) -> None:
    """
    Logs values to stdout, in a nice format.
    """
    indentblock = ''.join(['\t' for _ in range(indent + 1)])
    sub = ''.join(['\t' for _ in range(indent)])
    
    for value in values:
        if (type(value)) == bool:
            print(f'{colorama.Fore.MAGENTA}{value}{colorama.Style.RESET_ALL}', end = '')
            return
        elif value in [None, [], '', {}]:
            if value == None:
                print(f'{colorama.Fore.MAGENTA}None{colorama.Style.RESET_ALL}', end = '')
            if value == []:
                print(f'{colorama.Fore.MAGENTA}[]{colorama.Style.RESET_ALL}', end = '')
            if value == '':
                print(f"{colorama.Fore.MAGENTA}''{colorama.Style.RESET_ALL}", end = '')
            if value == {}:
                print(f"{colorama.Fore.MAGENTA}", '{}', f"{colorama.Style.RESET_ALL}", end = '')
            return
        elif type(value) == dict:
            print(colorama.Fore.LIGHTBLACK_EX, end = '')
            print('{')
            print(colorama.Style.RESET_ALL, end = '')
            for i, each in enumerate(value.keys()):
                print(indentblock, end = '')
                log(f'{colorama.Fore.LIGHTGREEN_EX}{each}{colorama.Style.RESET_ALL}', end = ' : ', indent = indent + 1)
                log(value[each], end = ',\n' if i != (len(value.keys()) - 1) else '\n', indent = indent + (1 if type(value[each]) == dict else 0))
            print(sub, end = '')
            print(colorama.Fore.LIGHTBLACK_EX, end = '')
            print('}', end = end)
            print(colorama.Style.RESET_ALL, end = '')
        elif type(value) in [tuple, list]:
            print(colorama.Fore.LIGHTBLACK_EX, end = '')
            print('(' if (type(value) == tuple) else '[', end = '')
            print(colorama.Style.RESET_ALL, end = '')
            for i, each in enumerate(value):
                log(each, end = f'{colorama.Fore.LIGHTBLACK_EX},{colorama.Style.RESET_ALL} ' if i < (len(value) - 1) else '', indent=indent)
            print(colorama.Fore.LIGHTBLACK_EX, end = '')
            print(')' if (type(value) == tuple) else ']')
            print(colorama.Style.RESET_ALL, end = '')
        else:
            if type(value) in colvals.keys():
                print(f'{colvals[type(value)]}{value}{colorama.Style.RESET_ALL}', end = '')
            else:
                print(f'{colorama.Fore.BLUE}{value}{colorama.Style.RESET_ALL}', end = '')
    print(end, end = '')


def dblog(*values, end : str = '\n') -> Any:
    """
    Logs the variable to stdout.
    """
    localitems = inspect.currentframe().f_back.f_locals.items()
    for value in values:
        varstring = [var_name for var_name, var_val in localitems if var_val is value]
        if len(varstring) > 0: varstring = varstring[0]
        else : varstring = None
        message = (time.strftime('[%d/%m/%Y %H:%M:%S]'))
        if timestamps : print(message, end = ' ')
        if varstring: log(varstring, end = ' -> ')
        log(value, end = '')
    print(end, end = '')
    return values

def error(*values, end : str = '\n') -> Any:
    original = colvals[str]
    colvals[str] = colorama.Fore.RED + colorama.Style.BRIGHT
    vals = dblog(*values, end)
    colvals[str] = original
    return vals

def warning(*values, end : str = '\n') -> Any:
    original = colvals[str]
    colvals[str] = colorama.Fore.YELLOW + colorama.Style.BRIGHT
    vals = dblog(*values, end)
    colvals[str] = original
    return vals

def ok(*values, end : str = '\n') -> Any:
    original = colvals[str]
    colvals[str] = colorama.Fore.GREEN + colorama.Style.BRIGHT
    vals = dblog(*values, end)
    colvals[str] = original
    return vals


def getln() -> int:
    """
    Returns the line number in source code wherever this function is called.
    """
    return inspect.currentframe().f_back.f_lineno