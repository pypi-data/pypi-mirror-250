import re
import sympy
from ..latex_trans import tex2sympy

def de_func(de_sympy):
    # 判断微分方程中未知函数
    str_de = str(de_sympy)
    pattern_func = "Derivative\((\S*), (\S*)"
    cnt_find = re.findall("Derivative", str_de)

    tmp_str = ""
    tmp_de = str_de

    for i in range(0, len(cnt_find)):
        find_num = tmp_de.find("Derivative")
        match_str = tmp_de[find_num + 10:]

        cnt = 0
        bool_str = []
        check_sign = False
        for check in list(match_str):
            cnt += 1
            if check == '(':
                bool_tmp = True
                bool_str.append(bool_tmp)
            elif check == ')':
                bool_str.pop()

            if len(bool_str) == 0:
                break

        content = "Derivative" + tmp_de[find_num + 10:find_num + 10 + cnt]
        match = re.search(pattern_func, content)

        if tmp_str != "" and tmp_str != match.group(1):
            return None

        else:
            tmp_str = match.group(1)
            tmp_de = tmp_de.replace(content, "")

    return tmp_str

def de_var_order(ode_sympy):
    tex_ode = str(ode_sympy)

    # 返回Derivative字段的起始和结束位置
    pattern = "Derivative"
    matches = re.finditer(pattern, tex_ode)
    pos_pattern_start = []
    pos_pattern_end = []
    for match in matches:
        start = match.start()
        end = match.end()
        pos_pattern_start.append(start)
        pos_pattern_end.append(end)

        # 存储完整的Derivative函数内容
    bool_str = []
    end_pos = []
    for i in pos_pattern_end:
        for j in range(i, len(tex_ode)):
            if tex_ode[j] == '(':
                bool_tmp = True
                bool_str.append(bool_tmp)
            elif tex_ode[j] == ')':
                bool_str.pop()

            if len(bool_str) == 0:
                end_pos.append(j + 1)
                break

    der_list = []
    for idx, k in enumerate(pos_pattern_start):
        der_list.append(tex_ode[k:end_pos[idx]])

    # 根据函数内容分情况输出ode的变量与阶数
    older_max = 0
    var_list = []
    for der in der_list:
        var_older_list = []
        split_res = der[11:-1].split(", ")
        var_older_list = [i.replace("(", "").replace(")", "") for i in split_res]

        if len(var_older_list) - 1 == 1:  ## 一阶单变量微分方程
            older_max = max(1, older_max)
            var_list.append(var_older_list[1])
        else:
            for var_oder in range(1, len(var_older_list)):
                if var_older_list[var_oder].isdigit():
                    older_max = max(int(var_older_list[var_oder]), older_max)
                else:
                    var_list.append(var_older_list[var_oder])

    return list(set(var_list)), older_max


def is_linear_de(de_sympy):
    str_de = str(de_sympy)
    fun_sym = de_func(de_sympy)

    if not fun_sym:
        raise ValueError("未知函数不存在，请检查方程定义是否正确！")

    pattern = fun_sym + "*Derivative"

    if str_de.find(pattern) == -1:
        return True
    else:
        return False


def apply_ics(res_od, ics: set, non_params: list = []):
    # 根据解析解和初始条件求得特殊解

    ics_pattern = r"(\S*)((\d+))"
    var = list(res_od.lhs.free_symbols)[0]
    trans_non = non_params

    var_ics = []
    trans_dic = {}
    keys_list = list(ics.keys())
    values_list = list(ics.values())

    for i in range(0, len(keys_list)):
        match = re.search(ics_pattern, str(keys_list[i]))
        if match:
            ics_value = match.group(2)

        if type(keys_list[i]) == str:
            tex_key = tex2sympy(keys_list[i])
        else:
            tex_key = keys_list[i]

        values = values_list[i]
        if type(values) == str:
            value_tex = tex2sympy(values)
            var_ics.append(value_tex)

        var_ics.append(values)
        trans_dic[tex_key] = values

    if non_params:
        trans_non = []
        for j in non_params:
            if type(j) == str:
                tmp_tex = tex2sympy(j)
            else:
                tmp_tex = j
            trans_non.append(tmp_tex)

    apply_symbols = res_od.free_symbols - set(trans_non)
    eqs = [(res_od.lhs.diff(var, n) - res_od.rhs.diff(var, n)).subs(var, ics_value).subs(trans_dic) for n in
           range(len(ics))]
    sol_params = sympy.solve(eqs, apply_symbols)
    return res_od.subs(sol_params)