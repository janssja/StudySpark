from flask import Blueprint, render_template, jsonify, request
from app.advisor import StudyAdvisor

main = Blueprint('main', __name__)
advisor = StudyAdvisor()

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    response = advisor.process_message(data['message'])
    return jsonify(response)

@main.route('/api/restart', methods=['POST'])
def restart():
    global advisor
    # Maak een nieuwe advisor instantie
    advisor = StudyAdvisor()
    return jsonify({'status': 'success'})