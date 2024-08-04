from flask import Blueprint, request, jsonify

from utils.open_ai_client import OpenAiClient

bp = Blueprint('generic_message', __name__)


@bp.route('/generic_message', methods=['POST'])
def summarize_pdf():
    api_key = request.form.get('api_key')
    if not api_key:
        return jsonify({'error': 'No API token provided'}), 400

    message = request.form.get('message')
    if not message:
        return jsonify({'error': 'No message submit for model'}), 400

    open_ai_client = OpenAiClient(api_key=api_key)

    response = open_ai_client.send_request(
        prompt=message,
        n_answers=3,
    )
    model_response, metrics = list(response.values())
    response_data = {
        'model_response': model_response,
        'metrics': metrics
    }

    return jsonify(response_data)
