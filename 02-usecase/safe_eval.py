import ast
import operator as op
import re
import signal
from typing import Callable, Dict, Iterable, List, Union


def AVG(*values):  # noqa
    if not isinstance(values, Iterable):
        values = [values]
    return sum(values) / len(values) if values else 0


def IF(*values) -> Union[float, int, str]:  # noqa
    condition, value1, value2 = values
    return value1 if condition else value2


FunctionEvaluator = Callable[[List[Union[float, int]]], Union[float, int, str]]

FUNCTIONS_MAP: Dict[str, FunctionEvaluator] = {
    'SUM': sum,
    'MIN': min,
    'MAX': max,
    'AVG': AVG,
    'IF': IF,
}

OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg,
    ast.Gt: op.gt,
    ast.GtE: op.ge,
    ast.LtE: op.le,
    ast.Lt: op.lt,
}


def custom_eval(node, value_map=None):
    """
    for safely using `eval`
    """
    if isinstance(node, ast.Call):
        values = [custom_eval(v) for v in node.args]
        func_name = node.func.id
        if func_name in {'AVG', 'IF'}:
            return FUNCTIONS_MAP[func_name](*values)
        elif func_name in FUNCTIONS_MAP:
            return FUNCTIONS_MAP[func_name](values)
        else:
            raise NotImplementedError(func_name)
    elif isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.Str):
        return node.s
    elif isinstance(node, ast.BinOp):
        return OPERATORS[type(node.op)](
            custom_eval(node.left, value_map=value_map),
            custom_eval(node.right, value_map=value_map),
        )
    elif isinstance(node, ast.UnaryOp):
        return OPERATORS[type(node.op)](custom_eval(node.operand, value_map=value_map))
    elif isinstance(node, ast.Compare):
        return OPERATORS[type(node.ops[0])](
            custom_eval(node.left, value_map=value_map),
            custom_eval(node.comparators[0], value_map=value_map),
        )
    elif isinstance(node, ast.Name):
        name = node.id
        if value_map is None:
            raise ValueError('value_map must not be None')
        if name not in value_map:
            raise KeyError()
        try:
            return value_map[name]
        except KeyError as e:
            raise e
    else:
        raise ArithmeticError()


def handle_special_char(expr: str):
    """
    handler for '^' to '**', 10% to 0.1
    """

    def handle_percent_sign(matched):
        span = matched.group('number')
        span = float(span[:-1])
        return str(span / 100)

    expr = expr.replace('^', '**')
    res = re.sub('(?P<number>[0-9]+%)', handle_percent_sign, expr)
    return res


def calculate(expr, value_map=None, millisecond=100):
    """
    calculate expression, each expression only have 100 millisecond to execute
    """

    def signal_handler(_, __):
        raise TimeoutError()

    signal.signal(signal.SIGALRM, signal_handler)
    seconds = millisecond / 10 ** 3
    signal.setitimer(signal.ITIMER_REAL, seconds, seconds)

    expr = handle_special_char(expr)
    try:
        res = custom_eval(ast.parse(expr, mode='eval').body, value_map=value_map)
    except TimeoutError as e:
        raise e
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)

    return res


if __name__ == '__main__':
    a = {'122': 1122}
    b = '(2*id_122 + 1)*2 * SUM(2,3) + IF(1>2,1,3)'
    print(calculate(b, value_map={'id_122': 2}))
    a = calculate('5*(2+3)')
    print(a)
    b = calculate('-40*1+2*6-2')
    print(b)
    c = calculate('9**9**9**9**9**9**9**9')
    print(c)
    d = calculate("__import__('os').remove('docker.md')")
    print('--', d)
