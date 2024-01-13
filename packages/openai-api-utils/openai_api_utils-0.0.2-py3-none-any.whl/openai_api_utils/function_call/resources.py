import inspect, json
from typing import Callable

def call_function(func):
    def wrapper(resp):

        if func.__name__ == "python":
            kwargs = {"tool_input": str(resp.choices[0].message.function_call.arguments)}
        else:
            kwargs = eval(resp.choices[0].message.function_call.arguments)

        try:
            output = func(**kwargs)
        except Exception:
            raise Exception("""Error from parsing function call arguments:
            {func}({kwargs})
            """.format(func=func.__name__, kwargs=kwargs))

        return output
    wrapper._inner = func

    return wrapper

def validate_function_arguments(func, fdesc):

    _ptostr: Callable[[str, type], str] = lambda name, _type: f"{name}: {_type.__name__}"
    def _stotype(s: str) -> type:
        _defines = {
            "string": str,
            "str": str,
            "int": int,
        }

        if s in _defines.keys():
            return _defines[s]
        elif type(eval(s)) == type:
            return eval(s)
        else:
            raise Exception(f"Unknown Type: {s}")

    params = fdesc['parameters']
    kwargs = {}

    for attr in ['name_for_human', 'name_for_model', 'description_for_model', 'parameters']:
        if not attr in fdesc:
            raise Exception(f"Function Description, `{func.__name__}` has missing information, `{{ .parameters.{attr} }}`: \n {json.dumps(fdesc, indent=2)}")

    for p in params:
        try:
            if not "description" in p.keys():
                raise KeyError('description')

            kwargs[p['name']] = _stotype(p['type'])
        except KeyError as e:
            raise Exception(f"Function Description, `{func.__name__}` has missing information,`{{ .parameters.{','.join(e.args)} }}`: \n {json.dumps(fdesc, indent=2)}")
        except Exception:
            raise Exception("Unknown")


    sig = inspect.signature(func)

    kwargs_matches = True
    kwargs_type_matches = True

    for k in kwargs.keys():
        if not k in sig.parameters.keys():
            print(f" Warning: Parameter, `{k}` is not mapped in actual function, `{func.__name__}({', '.join([f'{_ptostr(name, param)}' for name, param in signature.parameters.items()])}): \n  {json.dumps(fdesc, indent=2)}`")

    for name, param in sig.parameters.items():
        # Function 의 type(argument) 가  Desc.parameters에 명시가 되지 않은 경우.
        if not name in kwargs.keys():
            kwargs_matches = False
            raise Exception(f"Function, `{func.__name__}` has argument, `{name}`, but not defined in the description: \n{json.dumps(fdesc, indent=2)}")

        # Function 의 type(argument) 과  Desc.parameters.type 이 다른 경우.
        if param.annotation != kwargs[name]:
            kwargs_type_matches = False
            raise Exception(f"Function, `{func.__name__}` has argument, `{_ptostr(name, param.annotation)}`, but description has argument, `{_ptostr(name, kwargs[name])}`")

    # print(kwargs_matches, kwargs_type_matches)
    return kwargs_matches and  kwargs_type_matches



