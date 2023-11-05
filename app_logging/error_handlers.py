# error_handlers.py

from flask import jsonify

def handle_404(error):
    response = jsonify({'error': 'Not found', 'message': str(error)})
    response.status_code = 404
    return response

# Add more error handlers as needed...
