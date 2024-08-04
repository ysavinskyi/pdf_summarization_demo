from typing import List, Optional, Union, Dict
from openai import OpenAI, ChatCompletion

from utils.response_validator import ResponseValidator


class OpenAiClient:
    """
    Handles the requests to Open AI servers using its API
    """

    def __init__(self, api_key: str) -> None:
        """
        Initializes the class
        :param api_key: the API token from Open AI account (https://platform.openai.com/api-keys)
        """
        self._client = OpenAI(
            api_key=api_key,
        )

    def send_request(self, prompt: Union[str, List], model: Optional[str] = 'gpt-3.5-turbo',
                     max_tokens: Optional[int] = 150, n_answers: Optional[int] = 1,
                     validator_name: Optional[str] = 'cosine_similarity', temperature: Optional[float] = 0.5
                     ) -> Dict[str, str]:
        """
        Handles the request to LLM model and validates its response accuracy. Accepts several inputs for prompts:
        - single string
        - list of strings (considered as all User role input)
        - list of dictionaries with corresponding roles for message e.g. {'role': 'assistant', 'content': 'response'}
        :return:
        """
        validator = ResponseValidator(validator_name)
        params = {
            'model': model,
            'max_tokens': max_tokens,
            'n': n_answers,
            'temperature': temperature
        }
        prompt_list = []

        prompt = [prompt] if type(prompt) is str else prompt
        for message in prompt:
            if type(message) is str:
                prompt_list.append({'role': 'user', 'content': message})

            elif type(message) is dict:
                prompt_list.append(message)

            else:
                raise TypeError('Prompt input type could by only string, list of string or list of dicts')

        response = self._make_query(prompt_list, **params)
        best_response = validator.validate_responses(response, prompt_list)

        return best_response

    def _make_query(self, prompt_list: List, **kwargs) -> ChatCompletion:
        """
        Sends the API query to LLM model and returns its response as an object of ChatCompletion
        :return: language model response
        """
        response = self._client.chat.completions.create(messages=prompt_list, **kwargs)

        return response
