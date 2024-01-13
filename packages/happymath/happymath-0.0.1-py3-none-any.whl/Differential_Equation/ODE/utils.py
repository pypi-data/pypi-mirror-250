from sympy import dsolve
from IPython.display import display
from ...latex_trans import tex2sympy
from ..utils import is_linear_de,de_var_order,de_func
import re



def is_ode(ode_sympy):
    var_list, _ = de_var_order(ode_sympy)

    if not de_func(ode_sympy):
        return False
    if len(var_list) == 1:
        return True
    elif len(var_list) > 1:
        return False
    else:
        return False


def ode_analyzer(ode_object):
    if type(ode_object) == str:
        ode_object = tex2sympy(ode_object)

    bool_ode = is_ode(ode_object)
    bool_linear = is_linear_de(ode_object)
    _, older_ode = de_var_order(ode_object)

    if not bool_ode:
        raise ValueError("这似乎并不是一个常微分方程，请仔细检查输入表达式！")

    if bool_linear:
        linear = "线性"
    else:
        linear = "非线性"

    try:
        res_solve = dsolve(ode_object)
        bool_solve = True
    except Exception as e:
        bool_solve = False

    if bool_solve:
        print(f"这是一个{older_ode}阶{linear}常微分方程，方程具有解析解，为:")
        display(res_solve)
        return res_solve
    else:
        print(f"这是一个{older_ode}阶{linear}常微分方程，方程不具有解析解，考虑数值方法求解！")
        return None