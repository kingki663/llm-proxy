import os
import logging
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
default_openai_model = os.getenv('DEFAULT_OPENAI_MODEL')
openai_api_url = os.getenv('OPENAI_API_URL')
gemini_api_key = os.getenv('GEMINI_API_KEY')
gemini_api_url = os.getenv('GEMINI_API_URL')
default_gemini_model = os.getenv('DEFAULT_GEMINI_MODEL')
api_access_key = os.getenv('API_ACCESS_KEY')
port = int(os.getenv('PORT', 5000))

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log"),   # Logs to a file
                        logging.StreamHandler()          # Logs to console
                    ])
logger = logging.getLogger(__name__)

# API key validation middleware
def api_key_required(f):
    def decorator(*args, **kwargs):
        api_key = request.headers.get('X-API-KEY')
        if api_key != api_access_key:
            logger.warning(f"Unauthorized access attempt from IP: {request.remote_addr}")
            return jsonify(error='Forbidden', message='Invalid or missing API key'), 403
        return f(*args, **kwargs)
    decorator.__name__ = f.__name__
    return decorator

# OpenAI API endpoint
@app.route('/api/openai', methods=['POST'])
@app.route('/api/openai/chat/completions', methods=['POST']) # 支持使用openai库进行请求
@api_key_required
def openai_proxy():
    model = request.json.get('model', default_openai_model)
    url = f'{openai_api_url}/chat/completions' if model.startswith('gpt-') else f'{openai_api_url}/engines/{model}/completions'
    
    logger.info(f"Received request for OpenAI model: {model} from IP: {request.remote_addr}")

    try:
        response = requests.post(
            url,
            json={**request.json, 'model': model},
            headers={
                'Authorization': f'Bearer {openai_api_key}',
                'Content-Type': 'application/json'
            }
        )
        response.raise_for_status()
        logger.info(f"Request to OpenAI API successful with status: {response.status_code}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return jsonify(error='HTTP Error', message=str(http_err)), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        return jsonify(error='Service Unavailable', message=str(req_err)), 503
    except Exception as err:
        logger.critical(f"Unhandled exception occurred: {err}")
        return jsonify(error='Internal Server Error', message=str(err)), 500
      
# Gemini API endpoint
@app.route('/v1/generate', methods=['POST'])
@api_key_required
def gemini_proxy():
    try:
        model_name = request.json.get('model', default_gemini_model)
        api_url = f"{gemini_api_url}{model_name}:generateContent?key={gemini_api_key}"
        
        request_body = {
            "contents": [
                {
                    "parts": [
                        {"text": request.json.get('input', '')}
                    ]
                }
            ]
        }

        logger.info(f"Received request for Gemini model: {model_name} from IP: {request.remote_addr}")

        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, json=request_body, headers=headers)
        response.raise_for_status()
        logger.info(f"Request to Gemini API successful with status: {response.status_code}")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return jsonify(error='HTTP Error', message=str(http_err)), response.status_code
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request exception occurred: {req_err}")
        return jsonify(error='Service Unavailable', message=str(req_err)), 503
    except Exception as err:
        logger.critical(f"Unhandled exception occurred: {err}")
        return jsonify(error='Internal Server Error', message=str(err)), 500

# Handle all other routes
@app.errorhandler(404)
def not_found(error):
    logger.warning(f"404 Not Found: {request.path} from IP: {request.remote_addr}")
    return jsonify(error='Not Found', message='The requested resource was not found'), 404

# Handle all other exceptions
@app.errorhandler(Exception)
def handle_exception(e):
    response = e.get_response()
    logger.critical(f"Unhandled server error: {e}")
    response.data = jsonify(error='Internal Server Error', message=str(e)).data
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=port)
