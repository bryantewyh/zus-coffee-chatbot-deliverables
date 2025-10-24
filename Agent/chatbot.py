"""Chatbot wrapper"""

from agent import create_agent
from typing import Dict, Any, List
import uuid

class ZUSChatbot:
    """
    Chatbot wrapper for ZUS Coffee assistant.
    Manages multiple user sessions.
    """
    
    def __init__(self):
        """Initialize the chatbot with session management."""
        self.sessions = {}  
    
    def get_or_create_session(self, session_id: str = None):
        """Get existing session or create a new one."""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        if session_id not in self.sessions:
            self.sessions[session_id] = create_agent(session_id)
        
        return session_id, self.sessions[session_id]
    
    def chat(self, message: str, session_id: str = None) -> Dict[str, Any]:
        """
        Process a chat message.
        
        Args:
            message: User's message
            session_id: Optional session ID (creates new if not provided)
        
        Returns:
            Dict with response and session info
        """
        session_id, agent = self.get_or_create_session(session_id)
        
        result = agent.execute(message)
        return {
            "session_id": session_id,
            "message": result["response"],
            "requires_input": result.get("requires_input", False),
            "success": result["success"]
        }
    
    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history for a session."""
        if session_id in self.sessions:
            return self.sessions[session_id].get_conversation_history()
        return []
    
    def clear_session(self, session_id: str):
        """Clear a session's history."""
        if session_id in self.sessions:
            self.sessions[session_id].clear_history()
            del self.sessions[session_id]
