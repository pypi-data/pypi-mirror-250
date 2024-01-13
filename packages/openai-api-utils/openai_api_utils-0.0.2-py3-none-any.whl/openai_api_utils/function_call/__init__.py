from openai_api_utils.function_call.functions import functions_acts
from openai_api_utils.function_call.resources import validate_function_arguments
from openai_api_utils.api.util import pprint_tools


def load_functions_desc(verbose=True):
    function_desc = [f[0]for f in functions_acts]

    if verbose:
        pprint_tools(function_desc)

    return function_desc


# Function call Validation
for fdesc, func in [(a, f._inner) for (a, f) in functions_acts]:
    validate_function_arguments(func, fdesc)
