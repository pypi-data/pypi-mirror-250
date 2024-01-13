import copy
from openai_api_utils.api.util import pprint_response_choices, pprint_assistant_message, pprint_raw_completion_response
from openai_api_utils.function_call import functions_acts
from operator import itemgetter


def chain_response(_completion_api):
    """
    1. `Completion` API 호출
    2. API 응답을 `messages`에 append
    3. 그 응답에 function_call 이 있다면..  함수를 실행후 결과 값을 `messages` 에 append 하고 재호출
    """

    def _execute(messages, resp):
        """ function_call 함수 실행 후, append 한 `messages` 반환. """

        funcs_found = [(f[0]['name_for_model'], f[1]) for f in functions_acts
                       if f[0]['name_for_model'] == resp.choices[0].message.function_call.name]

        if not funcs_found: # 마지막 assistant message 가 function_call 이 정의되지 않은 call 이라면
            raise Exception("No func found")
        else:
            func_name, func = funcs_found[0]
            data = func(resp)
            messages = append_function_message(messages, str(data), name=func_name)
        return messages

    def wrapper(client, messages, functions=None, verbose=False, silence=False):

        # 1. `Completion` API 호출
        completion, messages = _completion_api(client, messages, functions=functions, verbose=verbose, silence=silence)

        # 2. API 응답을 `messages`에 append
        content = completion.choices[0].message.content  # 어차피 서버에서 한개만 처리함..
        function_call = dict(completion.choices[0].message.function_call) if completion.choices[0].message.function_call else None
        messages = append_assistant_message(messages, content, function_call)

        # 3. 그 응답에 function_call 이 있다면..  함수를 실행후 결과 값을 `messages` 에 append 하고 재호출
        response_message = messages[-1]
        role, function_call = itemgetter('role', 'function_call')(response_message)

        if role == "assistant" and function_call is not None:
            messages = _execute(messages, completion)
            completion, messages = _completion_api(client, messages, functions=functions, verbose=verbose, silence=silence)

        return completion, messages

    return wrapper

@chain_response
def call_completion_api(client, messages, functions=None, verbose=False, silence=False):

    if functions:
        resp = client.chat.completions.create(
            model="Qwen-72B-Chat", messages=messages, functions=functions)
    else:
        resp = client.chat.completions.create(
            model="Qwen-72B-Chat", messages=messages)


    if not resp.choices:  ## choice 가 없으면 pass.
        raise Exception(f"No Completion Choices for message. {messages[-1]}")
    # elif resp.choices[0].message.function_call is None:
    #     print("No Function Call Defined")
    else:
        messages = append_message(messages, resp.choices[0].message.content, role=resp.choices[0].message.role)
        if verbose:
            pprint_raw_completion_response(resp)
            pprint_response_choices(resp.choices)
            pass

        if not resp.choices[0].message.function_call and not silence:
            pprint_assistant_message(resp.choices[0].message)

    return resp, messages


def append_message(messages, content, role='user', **kwargs):
    _messages = copy.deepcopy(messages)
    _messages.append({
        'role': role,
        'content': content,
        **kwargs
    })
    return _messages

def append_user_message(messages, content):
    return append_message(messages, content, role='user')

def append_assistant_message(messages, content, function_call=None):
    # if function_call:
    return append_message(messages, content, role='assistant', function_call=function_call)
    # else:
    #     return append_message(messages, content, role='assistant')

def append_function_message(messages, content, name):
    return append_message(messages, content, role='function', name=name)


