import requests
import openai
from openai_api_utils.function_call.resources import call_function


@call_function
def get_current_weather(location:str):
    print(f"run get_current_weather(location=`{location}`)")
    return {"result": "result"}
