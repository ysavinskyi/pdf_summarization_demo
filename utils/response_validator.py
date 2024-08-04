from typing import Dict, List
from rouge import Rouge
from sentence_transformers import SentenceTransformer, util
from openai import ChatCompletion


class ResponseValidator:
    """
    Validate the LLM response basing on chosen approach
    """

    def __init__(self, algorithm: str) -> None:
        """
        Initializes the class
        :param algorithm: the algorithm on which the validation will be performed
        """
        algorithm_methods_map = {'rouge': self._rouge_metrics_val,
                                 'cosine_similarity': self._cosine_similarity_val}
        self._validation_algorithm = [
            algorithm_methods_map[name] for name in algorithm_methods_map.keys() if algorithm.lower() in name
        ][0]

    def validate_responses(
            self, model_response: ChatCompletion, init_request_list: List[Dict[str, str]]
    ) -> Dict[str, str]:
        """
        Initializes the class
        :param model_response: model response distributed as ChatCompletion object
        :param init_request_list: initial request(s) for which responses generated
        :return: dict with the best response text and the metric score used to validate
        """
        request_context = ""
        for request in init_request_list:
            request_context += f"{request['role']}: {request['content']}\n\n"

        responses_list = [response.message.content for response in model_response.choices]

        best_result = self._validation_algorithm(request_context, responses_list)

        return best_result

    @staticmethod
    def _cosine_similarity_val(request_context: str, responses_list: List[str]) -> Dict[str, str]:
        """
        Validates prompt and response(s) accuracy using similarity of their embeddings
        :param request_context: string of the user request sent to LLM
        :param responses_list: list of the model responses for user's request
        :return: dict with the best response text and the score of cosine similarity
        """
        model = SentenceTransformer('all-MiniLM-L6-v2')

        best_response_dict = {'text': None, 'metrics': {'cosine_similarity_score': 0.0}}
        for response in responses_list:
            reference_embedding = model.encode(request_context, convert_to_tensor=True)
            generated_embedding = model.encode(response, convert_to_tensor=True)

            cosine_similarity = float(util.pytorch_cos_sim(reference_embedding, generated_embedding))
            if cosine_similarity > best_response_dict['metrics']['cosine_similarity_score']:
                best_response_dict['metrics']['cosine_similarity_score'] = cosine_similarity
                best_response_dict['text'] = response

        return best_response_dict

    @staticmethod
    def _rouge_metrics_val(request_context: str, responses_list: List[str]) -> Dict[str, str]:
        """
        Validates prompt and response(s) standard ML metrics using ROUGE algorithm
        :param request_context: string of the user request sent to LLM
        :param responses_list: list of the model responses for user's request
        :return: dict with the best response text and the metric scores
        """
        rouge = Rouge()

        best_response_dict = {'text': None, 'metrics': {'ROUGE_metrics': None}}
        best_summary_score = 0
        for response in responses_list:
            rogue_scores = rouge.get_scores(response, request_context, avg=True)
            summary_score = 0
            for metric_set, scores in rogue_scores.items():
                summary_score += sum(scores.values())

            if summary_score > best_summary_score:
                best_summary_score = summary_score
                best_response_dict['text'] = response
                best_response_dict['metrics']['ROUGE_metrics'] = rogue_scores

        return best_response_dict
