"""Test cases for successful conversation flows.
   Assumptions is that each test succeeds without error in getting the data.
"""
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent import create_agent


@pytest.fixture
def agent():
    """Fixture to provide a fresh agent for each test."""
    return create_agent("test_session")


def test_three_turn_conversation(agent):
    """Test the main example flow with three related turns."""
    
    # Turn 1: Ask about outlet in Petaling Jaya
    result1 = agent.execute("Is there an outlet in Petaling Jaya?")
    response1 = result1['response']
    
    assert result1['success'] is True
    assert response1 is not None
    assert len(response1) > 0
    assert any(word in response1.lower() for word in ["yes", "outlet", "ss 2", "damansara", "petaling jaya"])
    
    # Turn 2: Ask about SS 2 opening time
    result2 = agent.execute("SS 2, what's the opening time?")
    response2 = result2['response']
    
    assert result2['success'] is True
    assert any(time in response2.lower() for time in ["am", "open", "closes", "pm"])
    
    # Turn 3: Ask about closing time (should understand context)
    result3 = agent.execute("And when does it close?")
    response3 = result3['response']
    
    assert result3['success'] is True
    assert any(time in response3.lower() for time in ["am", "open", "closes", "pm"])
    
    # Verify conversation history has 6 messages (3 user + 3 assistant)
    history = agent.get_conversation_history()
    assert len(history) >= 6


def test_product_search(agent):
    """Test product search functionality."""
    
    # Ask about mugs
    result = agent.execute("What mugs do you have?")
    response = result['response']
    
    assert result['success'] is True
    assert response is not None
    assert any(word in response.lower() for word in ["mug", "tumbler", "product", "price"])


def test_context_retention(agent):
    """Test that the bot retains context across multiple turns."""
    
    # Establish context
    result1 = agent.execute("I want to visit the SS 2 outlet")
    assert result1['success'] is True
    
    # Ask follow-up that relies on context
    result2 = agent.execute("What time does it open?")
    response2 = result2['response']
    
    assert result2['success'] is True
    assert any(time in response2.lower() for time in ["am", "open", "closes", "pm"])
    
    # Another follow-up
    result3 = agent.execute("Where is it located?")
    response3 = result3['response']
    
    assert result3['success'] is True
    assert any(location in response3.lower() for location in ["ss 2", "address"])
    
    # Verify history
    history = agent.get_conversation_history()
    assert len(history) >= 6


def test_nearest_outlets_with_location(agent):
    """Test nearest outlet search with GPS coordinates."""
    
    # Set user location 
    agent.update_context('user_location', {
        'latitude': 3.1191791750227895,
        'longitude': 101.63313809936191
    })
    
    # Ask for nearest outlets
    result = agent.execute("Show me the nearest outlets")
    response = result['response']
    
    assert result['success'] is True
    assert response is not None
    assert any(word in response.lower() for word in ["nearest", "closest", "distance", "km", "away"])


def test_calculator_tool(agent):
    """Test calculator functionality."""
    
    # Ask a calculation question
    result = agent.execute("What is 15% of 50?")
    response = result['response']
    
    assert result['success'] is True
    assert "7.5" in response or "7.50" in response


def test_greeting(agent):
    """Test simple greeting."""
    
    result = agent.execute("Hello")
    response = result['response']
    
    assert result['success'] is True
    assert response is not None
    assert any(word in response.lower() for word in ["hello", "hi", "help", "zus", "coffee"])


def test_off_topic_redirect(agent):
    """Test that off-topic questions are redirected politely."""
    
    result = agent.execute("What's the weather today?")
    response = result['response']
    
    assert result['success'] is True
    assert any(word in response.lower() for word in ["zus", "coffee", "help", "assist"])


def test_session_isolation():
    """Test that different sessions maintain separate histories."""
    
    agent1 = create_agent("session_1")
    agent2 = create_agent("session_2")
    
    # Agent 1 conversation
    agent1.execute("I want to visit SS 2 outlet")
    result1 = agent1.execute("What time does it open?")
    
    # Agent 2 conversation (should not have SS 2 context)
    result2 = agent2.execute("What time does it open?")
    
    # Agent 1 should have context, Agent 2 should ask for clarification
    assert result1['success'] is True
    assert result2['success'] is True
    
    # Check histories are different
    history1 = agent1.get_conversation_history()
    history2 = agent2.get_conversation_history()
    
    assert len(history1) >= 4  # 2 turns
    assert len(history2) >= 2  # 1 turn
    assert history1 != history2


def test_clear_history(agent):
    """Test that clearing history works correctly."""
    
    # Build up some history
    agent.execute("Show me outlets in KL")
    agent.execute("What mugs do you have?")
    
    # Verify history exists
    history_before = agent.get_conversation_history()
    assert len(history_before) > 0
    
    # Clear history
    agent.clear_history()
    
    # Verify history is cleared
    history_after = agent.get_conversation_history()
    assert len(history_after) == 0
    
    # Verify context is also cleared
    assert agent.context == {}
