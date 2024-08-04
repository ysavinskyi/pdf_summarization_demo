from flask import Flask
from api.summarize_pdf import bp as summarize_pdf
from api.generic_message import bp as generic_message

# Initialize Flask app
app = Flask(__name__)

# Register the blueprint
app.register_blueprint(summarize_pdf)
app.register_blueprint(generic_message)

if __name__ == '__main__':
    app.run(debug=True)
