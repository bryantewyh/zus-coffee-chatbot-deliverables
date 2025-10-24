"""Test cases for interrupted, non-standard, and unhappy conversation flows."""
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import pytest
import sys
import os
# Mock api downtime
from unittest.mock import patch
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent import create_agent

@pytest.fixture
def agent():
    """Fixture to provide a fresh agent for each test."""
    return create_agent("test_session")

class TestConversationContext:
    """Tests for handling topic changes, context switches, and session behavior."""

    def test_topic_change_mid_conversation(self, agent):
        """User suddenly changes topic mid-conversation."""
        result1 = agent.execute("Tell me about SS 2 outlet")
        assert result1['success'] is True

        result2 = agent.execute("What about KLCC?")
        response2 = result2['response']
        assert result2['success'] is True
        assert "klcc" in response2.lower() or "klcc" in response2.lower()

        result3 = agent.execute("When does it open?")
        response3 = result3['response']
        assert result3['success'] is True
        assert any(word in response3.lower() for word in ["am", "open"])

        history = agent.get_conversation_history()
        assert len(history) >= 6

    def test_context_switch_without_clear(self, agent):
        """Switch topic without clearing context."""
        agent.execute("Tell me about SS 2 outlet")
        agent.execute("What time does it open?")
        result = agent.execute("What mugs do you have?")
        assert result['success'] is True
        assert any(w in result['response'].lower() for w in ["mug", "tumbler", "product"])

    def test_contradictory_requests(self, agent):
        """User corrects themselves mid-dialogue."""
        agent.execute("I want to visit SS 2")
        result = agent.execute("Actually, I meant KLCC")
        assert result['success'] is True
        assert "klcc" in result['response'].lower() or "klcc" in result['response'].lower()

    def test_partial_outlet_name(self, agent):
        """Partial or abbreviated outlet names should still match."""
        result = agent.execute("Tell me about SS2")
        assert result['success'] is True
        assert result['response'] is not None

    def test_case_insensitive_search(self, agent):
        """Ensure search is case-insensitive."""
        res1 = agent.execute("Show me outlets in petaling jaya")
        res2 = agent.execute("Show me outlets in PETALING JAYA")
        res3 = agent.execute("Show me outlets in Petaling Jaya")
        assert all(r['success'] for r in [res1, res2, res3])

class TestSessionState:
    """Tests related to history, session isolation, and persistence."""

    def test_session_isolation(self):
        agent1 = create_agent("session_1")
        agent2 = create_agent("session_2")
        agent1.execute("Tell me about SS 2")
        history1_before = len(agent1.get_conversation_history())
        agent2.execute("Tell me about KLCC")
        history2 = len(agent2.get_conversation_history())
        history1_after = len(agent1.get_conversation_history())
        assert history1_before == history1_after >= 2
        assert history2 >= 2

    def test_history_clearing(self, agent):
        agent.execute("Tell me about SS 2")
        agent.execute("What time does it open?")
        assert len(agent.get_conversation_history()) >= 4
        agent.clear_history()
        # Should have nothing
        assert len(agent.get_conversation_history()) == 0
        assert agent.context == {}

class TestInputRobustness:
    """Tests for malformed, empty, special, or extreme inputs."""

    def test_empty_message(self, agent):
        result = agent.execute("")
        assert result['success'] is True
        assert result['response'] is not None

    def test_very_long_message(self, agent):
        long_msg = "Tell me about outlets " * 100
        result = agent.execute(long_msg)
        assert result['success'] is True
        assert result['response'] is not None

    def test_special_characters(self, agent):
        result = agent.execute("What's é ss2??????? XDD LOL :)))) ? ☕")
        assert result['success'] is True
        assert result['response'] is not None

    def test_malformed_calculation(self, agent):
        result = agent.execute("Calculate abc + xyz")
        assert result['success'] is True
        assert result['response'] is not None

    def test_mixed_language_input(self, agent):
        result = agent.execute("Berapa harga coffee di SS 2?")
        assert result['success'] is True
        assert result['response'] is not None

class TestAmbiguityHandling:
    """Tests for ambiguous or unclear queries."""

    def test_ambiguous_query(self, agent):
        result = agent.execute("When does it open?")
        assert result['success'] is True
        assert len(result['response']) > 0

    def test_nearest_outlets_without_location(self, agent):
        result = agent.execute("Show me the nearest outlets")
        assert result['success'] is True
        assert any(w in result['response'].lower() for w in ["location", "where", "coordinates", "gps"])

class TestMissingData:
    """Tests for queries with nonexistent entities."""

    def test_nonexistent_outlet(self, agent):
        result = agent.execute("Is there an outlet in Antarctica?")
        assert result['success'] is True
        # Should return generic message saying how they only help in malaysia
        assert any(w in result['response'].lower() for w in ["couldn't find", "no outlet", "not found", "no results", "unable", "malaysia"])

    def test_nonexistent_product(self, agent):
        result = agent.execute("Do you sell unicorn-flavored coffee?")
        assert result['success'] is True
        assert any(w in result['response'].lower() for w in ["couldn't find", "no product", "not found", "don't have", "unable", "malaysia"])

class TestConversationFlow:
    """Stress tests for message order, repetition, and parallel queries."""

    def test_multiple_rapid_messages(self, agent):
        result1 = agent.execute("Show me outlets")
        result2 = agent.execute("What mugs do you have?")
        result3 = agent.execute("What's 10% of 50?")
        assert all(r['success'] for r in [result1, result2, result3])
        assert len(agent.get_conversation_history()) >= 6

    def test_repeated_same_question(self, agent):
        r1 = agent.execute("What time does SS 2 open?")
        r2 = agent.execute("What time does SS 2 open?")
        r3 = agent.execute("What time does SS 2 open?")
        assert all(r['success'] for r in [r1, r2, r3])
        assert all(r['response'] for r in [r1, r2, r3])

    def test_off_topic_questions(self, agent):
        off_topics = [
            "What's the weather today?",
            "Who is the president?",
            "Tell me a joke",
        ]
        for q in off_topics:
            result = agent.execute(q)
            assert result['success'] is True
            assert result['response'] is not None
            # Generic message
            assert any(w in result['response'].lower() for w in ["zus", "help"])

class TestMissingParameters:
    """Test handling of missing or incomplete parameters."""
    
    def test_vague_product_query(self, agent):
        """Test when user asks about products without specifying what."""
        result = agent.execute("Show me products")
        assert result['success'] is True
        assert result['response'] is not None
        # Should ask follow up
        assert len(result['response']) > 0
    
    def test_vague_outlet_query(self, agent):
        """Test when user asks about outlets without location."""
        result = agent.execute("Show me outlets")
        assert result['success'] is True
        assert result['response'] is not None
        # Should ask follow up
        assert len(result['response'].lower()) > 5
    
    def test_incomplete_calculation_request(self, agent):
        """Test when user asks to calculate without providing numbers."""
        result = agent.execute("Calculate something")
        assert result['success'] is True
        assert result['response'] is not None
        response_lower = result['response'].lower()
        # Should ask follow up
        assert any(word in response_lower for word in ['what', 'which', 'calculate', '?'])

    def test_outlet_nearest_no_available_latitude_longitude(self, agent):
        """Test when user does not allow location services."""
        result = agent.execute("Show me nearest outlets")
        assert result is not None
        response = result["response"].lower()
        assert "sorry" in response    

    def test_ambiguous_outlet_reference(self, agent):
        """Test when user references outlet ambiguously."""
        result = agent.execute("What time does the outlet open?")
        assert result['success'] is True
        response_lower = result['response'].lower()
        assert any(word in response_lower for word in ['which', 'specify', 'referring'])
    
    def test_empty_query(self, agent):
        """Test handling of empty or whitespace-only input."""
        result = agent.execute("   ")
        assert result is not None
        assert result['success'] is True
        assert result['response'] is not None

class TestAPIDowntime:
    """Test how the agent handles API downtime or failures gracefully."""

    def test_product_api_connection_error(self, agent):
        """Simulate product API being unreachable."""
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError("Server down")):
            result = agent.execute("What mugs do you have?")
            assert result is not None
            assert "response" in result
            response = result["response"].lower()
            assert any(word in response for word in ["connect", "unavailable", "server", "down"])

    def test_product_api_timeout(self, agent):
        """Simulate product API timeout."""
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            result = agent.execute("Show me tumblers")
            assert result is not None
            response = result["response"].lower()
            assert "timeout" in response or "try again" in response

    def test_product_api_http_error(self, agent):
        """Simulate product API returning 500 Internal Server Error."""
        mock_response = requests.Response()
        mock_response.status_code = 500
        with patch("requests.get", return_value=mock_response):
            with patch.object(mock_response, "raise_for_status", side_effect=requests.exceptions.HTTPError("500 error")):
                result = agent.execute("Show me mugs")
                assert result is not None
                response = result["response"].lower()
                assert "couldn't" in response or "try again later" in response

    def test_outlet_api_connection_error(self, agent):
        """Simulate outlet API being unreachable."""
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError("Connection refused")):
            result = agent.execute("Where are outlets in KL?")
            assert result is not None
            response = result["response"].lower()
            assert "connect" in response or "unavailable" in response

    def test_outlet_api_timeout(self, agent):
        """Simulate outlet API timing out."""
        with patch("requests.get", side_effect=requests.exceptions.Timeout):
            result = agent.execute("Find outlets in PJ")
            assert result is not None
            response = result["response"].lower()
            assert "timeout" in response or "try again" in response

    def test_outlet_nearest_api_connection_error(self, agent):
        """Simulate nearest outlet API POST endpoint connection failure."""
        with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Server unreachable")):
            
            # Set user location 
            agent.update_context('user_location', {
                'latitude': 3.1191791750227895,
                'longitude': 101.63313809936191
            })

            result = agent.execute("Show me nearest outlets")
            assert result is not None
            response = result["response"].lower()
            assert "connect" in response or "unavailable" in response

    def test_outlet_api_unexpected_exception(self, agent):
        """Simulate unexpected generic exception."""
        with patch("requests.get", side_effect=Exception("Unexpected crash")):
            result = agent.execute("Find outlets in Penang")
            assert result is not None
            response = result["response"].lower()
            assert "unexpected" in response or "error" in response

    def test_outlet_api_unexpected_exception_nearest(self, agent):
        """Simulate unexpected generic exception for nearest."""  

        with patch("requests.get", side_effect=Exception("Unexpected crash")):
            result = agent.execute("Show me nearest outlets")
            assert result is not None
            response = result["response"].lower()
            # Shouldnt return any outlets
            assert any(w in result['response'].lower() for w in ["zus coffee", "operating hours"])

    def test_calculator_api_connection_error(self, agent):
        """Simulate calculator API being unreachable."""
        with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Server down")):
            result = agent.execute("What is 15% of 100?")
            assert result is not None
            assert "response" in result
            response = result["response"].lower()
            assert any(word in response for word in ["connect", "service", "calculator"])

    def test_calculator_api_timeout(self, agent):
        """Simulate calculator API timeout."""
        with patch("requests.post", side_effect=requests.exceptions.Timeout):
            result = agent.execute("Calculate 50 * 20")
            assert result is not None
            response = result["response"].lower()
            assert "timeout" in response or "try again" in response

    def test_calculator_api_http_error(self, agent):
        """Simulate calculator API returning 500 Internal Server Error."""
        mock_response = requests.Response()
        mock_response.status_code = 500
        with patch("requests.post", return_value=mock_response):
            with patch.object(mock_response, "raise_for_status", side_effect=requests.exceptions.HTTPError("500 error")):
                result = agent.execute("What's 25% of 200?")
                assert result is not None
                response = result["response"].lower()
                assert "unable" in response or "products" in response or "outlets" in response

    def test_calculator_api_unexpected_exception(self, agent):
        """Simulate unexpected generic exception in calculator."""
        with patch("requests.post", side_effect=Exception("Unexpected crash")):
            result = agent.execute("Calculate 100 + 50")
            assert result is not None
            response = result["response"].lower()
            assert "unable" in response or "products" in response or "outlets" in response
            
class TestRecoveryAndRetry:
    """Test bot's ability to recover from errors."""
    
    def test_recovery_after_error(self, agent):
        """Test that bot can continue conversation after an error."""
        result1 = agent.execute("asdfghjkl")
        assert result1 is not None
        result2 = agent.execute("What mugs do you have?")
        assert result2 is not None
        assert 'response' in result2
        assert result2['response'] is not None
        assert len(agent.get_conversation_history()) > 0
    
    def test_multiple_failed_requests(self, agent):
        """Test handling of multiple consecutive failures."""
        agent.execute("...")
        agent.execute("")
        result = agent.execute("Show me something")
        assert result is not None
        assert result['response'] is not None
        assert len(agent.get_conversation_history()) > 0

class TestAgentRobustness:
    """Test overall agent robustness."""
    
    def test_agent_does_not_crash_on_any_input(self, agent):
        """Test that agent handles various edge cases without crashing."""
        test_inputs = ["", "   ", "!!@#$%", "a" * 1000, "Calculate", "Show", "valid"]
        for test_input in test_inputs:
            try:
                result = agent.execute(test_input)
                assert result is not None, f"Agent returned None for input: {test_input}"
                assert 'response' in result, f"No response for input: {test_input}"
            except Exception as e:
                pytest.fail(f"Agent crashed on input '{test_input}': {str(e)}")
    
    def test_agent_maintains_state_after_errors(self, agent):
        """Test that agent state remains consistent after errors."""
        agent.execute("Tell me about SS2 outlet")
        agent.execute("")
        assert isinstance(agent.get_conversation_history(), list)
        assert isinstance(agent.context, dict)
    
    def test_context_not_corrupted_by_bad_input(self, agent):
        """Test that bad input doesn't corrupt conversation context."""
        agent.execute("I'm looking at SS2")
        agent.execute("@#$%^&")
        assert agent.context is not None
        assert all(isinstance(k, str) for k in agent.context.keys())
