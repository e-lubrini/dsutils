
import inspect
from tqdm import tqdm
from inspect import getmembers, isfunction
from humanfriendly import format_timespan

def get_var_name(var):
    try:
        callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
        var = [var_name for var_name, var_val in callers_local_vars if var_val is var][0]
    except IndexError:
        callers_local_vars = inspect.currentframe().f_back.f_locals.items()
        var = [var_name for var_name, var_val in callers_local_vars if var_val is var][0] 
    return str(var)

def dbg(mess, title=''):
    #subprocess.Popen(['echo', str('\033[35m'+ str(title)+'\033[32m'+ str(get_var_name(mess)+': '+'\033[0m'+str(mess)))])
    print(str('\033[35m'+ str(title)+'\033[32m'+ str(get_var_name(mess)+': '+'\033[0m'+str(mess))))
    return

def verbose_mess(mess, verbose):
    if verbose:
        mess_col(mess, verbose)

colours = dict(black = "30m",
                red = "31m",
                green = "32m",
                yellow = "33m",
                blue = "34m",
                magenta = "35m",
                cyan = "36m",
                white = "37m",
                grey = "38m",
                )

def mess_col(mess, col_tag):
    print('\033[0;{0} {1}. \033[0m'.format(col_tag, mess))
    return


def hr_size(num, suffix="B"):
    for unit in ["", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"]:
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"

def hr_time(num):
    value = format_timespan(num)
    return value

def get_funs_from_module(module):
    funs_raw = getmembers(module,isfunction)
    funs = dict()
    for n,t in funs_raw:
        funs[n] = t
    return funs

def true_counter(funcQ, elems, **kwargs):
    c = sum([funcQ(e,**kwargs) for e in tqdm(elems, get_var_name(elems), leave=False)])
    return c

