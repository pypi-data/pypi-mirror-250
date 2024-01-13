from openai_api_utils.function_call.acts import get_current_weather


functions_acts = [
    (
      {
          "name_for_human": "get current weather",
          "name_for_model": "get_current_weather",
          "description_for_model": "this api searches weather of a location",
          "parameters": [
              {
                  "name": "location",
                  "type": "string",
                  "description": "The city and state.",
                  "required": True,
              }
          ],

      },
      get_current_weather

    ),
]




