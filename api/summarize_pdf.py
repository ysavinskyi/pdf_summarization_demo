import os
from datetime import datetime
from flask import Blueprint, request, jsonify

from constants.location import PDF_CACHE_DIR
from utils.pdf_parser import PdfParser
from utils.open_ai_client import OpenAiClient

bp = Blueprint('summarize_pdf', __name__)


@bp.route('/summarize_pdf', methods=['POST'])
def summarize_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file provided'}), 400

    api_key = request.form.get('api_key')
    if not api_key:
        return jsonify({'error': 'No API token provided'}), 400

    saved_file_name = _save_file(file)

    pdf = PdfParser(saved_file_name)
    open_ai_client = OpenAiClient(api_key=api_key)

    response = open_ai_client.send_request(
        f'Summarize the text\n\n {pdf.text}',
        n_answers=3, validator_name='rouge',
        max_tokens=300, model='gpt-4', temperature=0.2,
    )
    model_response, metrics = list(response.values())
    response_data = {
        'model_response': model_response,
        'metrics': metrics
    }

    return jsonify(response_data)


def _save_file(file):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    saved_file_name = f'{timestamp}_{file.filename}'
    file_path = os.path.join(PDF_CACHE_DIR, saved_file_name)

    file.save(file_path)

    return saved_file_name
