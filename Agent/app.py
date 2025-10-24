"""Flask web application for ZUS Coffee Chatbot."""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from chatbot import ZUSChatbot
import os
import uuid
from datetime import timedelta

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)

# Enable CORS for API endpoints
CORS(app)

# Initialize chatbot
chatbot = ZUSChatbot()

@app.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        user_location = data.get('location') 
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            session.permanent = True
        
        session_id = session['session_id']
        if user_location:
            _, agent = chatbot.get_or_create_session(session_id)
            agent.update_context('user_location', user_location)

        # Get response from chatbot
        response = chatbot.chat(user_message, session_id)
        
        return jsonify({
            'success': True,
            'message': response['message'],
            'session_id': session_id,
            'requires_input': response.get('requires_input', False)
        })
        
    except Exception as e:
        app.logger.error(f"Chat error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Sorry, something went wrong. Please try again.'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history for current session."""
    try:
        session_id = session.get('session_id')
        
        if not session_id:
            return jsonify({'history': []})
        
        history = chatbot.get_history(session_id)
        return jsonify({
            'success': True,
            'history': history,
            'session_id': session_id
        })
        
    except Exception as e:
        app.logger.error(f"History error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Could not retrieve history'
        }), 500

@app.route('/api/clear', methods=['POST'])
def clear_session():
    """Clear current conversation."""
    try:
        session_id = session.get('session_id')
        
        if session_id:
            chatbot.clear_session(session_id)
        
        # Create new session
        session['session_id'] = str(uuid.uuid4())
        
        return jsonify({
            'success': True,
            'message': 'Conversation cleared',
            'session_id': session['session_id']
        })
        
    except Exception as e:
        app.logger.error(f"Clear error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Could not clear conversation'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint for cloud deployment."""
    return jsonify({
        'status': 'healthy',
        'active_sessions': len(chatbot.sessions)
    })

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )