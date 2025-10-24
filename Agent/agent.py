"""Agent using LangChain chains with memory."""

from langchain_openai import ChatOpenAI
from openai import RateLimitError
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from typing import Dict, Any, List
import json
import re
import os
from tools import AVAILABLE_TOOLS, get_tool


class AgentPlanner:
    """
    Agent that plans and executes actions based on user intent.
    Uses LangChain chains with conversation memory.
    """
    
    def __init__(self, session_id: str = "default"):
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0, api_key=os.getenv("OPENAI_API_KEY"))
        self.session_id = session_id
        
        # Memory stores
        self.chat_history_store = {}
        self.context = {} 
        
        # Build the planning chain with memory
        self._build_chain()
    
    def _build_chain(self):
        """Build LangChain with conversation memory."""
        
        # System prompt for planning
        tools_description = "\n".join([
            f"- {name}: {tool.description}" 
            for name, tool in AVAILABLE_TOOLS.items()
        ])
        
        # Use raw string to avoid f-string interpretation issues
        system_template = """
        You are an AI agent planner for ZUS Coffee assistant. Your job is to decide what action to take.
        AVAILABLE TOOLS:
        """ + tools_description + """

        CONTEXT ABOUT ZUS COFFEE:
        - ZUS Coffee has multiple outlets across Malaysia with names like "IOI City Mall", "Sunway Pyramid", etc.
        - When users mention outlet names or areas (like Subang Jaya, Petaling Jaya), they are asking about ZUS Coffee outlets.
        - Use the outlet_query tool to search for outlet information when users ask about locations, outlet names, or areas.

        SAFETY & RESTRICTIONS:
        - You must NEVER perform or plan any destructive, irreversible, or system-level actions.
        Examples include: "drop database", "delete files", "shutdown system", "format drive", or anything similar.
        - If the user requests such an action, do not confirm or attempt it — simply refuse and provide a safe, friendly response.
        - Your responses should stay within the scope of a friendly, helpful chatbot that answers questions and uses available tools.
        - You are not allowed to modify, destroy, or affect external systems, data, or configurations.

        SCOPE & BOUNDARIES:
        - Your PRIMARY focus is ZUS Coffee related queries: products, outlets, and general coffee shop information.
        - You can use ANY of your AVAILABLE TOOLS to help users. If a tool exists for a task, you are allowed and encouraged to use it.
        - Examples of what you CAN do: answer product questions, search outlets, perform calculations (discounts, percentages, tips), and use any other available tool.
        - If the user asks about topics completely unrelated to ZUS Coffee AND you have no relevant tool (e.g., weather, news, politics, other businesses), politely redirect them.
        - Examples of OFF-TOPIC requests: "What's the weather?", "Tell me a joke", "Who is the president?", "Tell me about Starbucks"
        - For off-topic requests WITHOUT relevant tools, use ACTION: answer and provide a polite redirect to ZUS Coffee
        
        DATA LIMITATIONS IMPORTANT!:
        - You ONLY have access to data about:
        * ZUS Coffee outlets (locations, addresses, operating hours, phone numbers)
        * Physical products: drinkware accessories, mugs, and tumblers
        - You DO NOT have data about:
        * Coffee drinks/beverages (lattes, cold brews, etc.)
        * Food items (pastries, sandwiches, etc.)  
        * Prices for drinks
        * Menu items
        * Promotions or discounts
        * Online ordering
        - If users ask about drinks, food, or menu items, politely inform them you can only help with outlet locations and merchandise products.
        - DO NOT make up information or pretend you can search for data you don't have.

        RESPONSE QUALITY:
        - Avoid repeating the same phrases multiple times in your responses
        - Use varied language to keep responses natural and engaging
        - Exception: When listing search results, it's okay to use consistent formatting

        Analyze the user's input and decide:
        1. What is the user's INTENT?
        2. What information is MISSING?
        3. What ACTION should you take?

        Respond in this EXACT format (DO NOT deviate from this format):

        INTENT: describe the user's intent
        MISSING: list missing information, or "none" if you have everything
        ACTION: MUST BE EXACTLY ONE OF: use_tool OR ask_user OR answer (no other values allowed!)
        TOOL: tool name from AVAILABLE TOOLS if ACTION is use_tool, otherwise write "none"
        PARAMS: JSON parameters for the tool like {{"query": "mugs"}}, or {{}} if none needed
        QUESTION: your question if ACTION is ask_user, otherwise write "none"
        ANSWER: your answer if ACTION is answer, otherwise write "none"
        REASONING: brief explanation of your decision
    
        CRITICAL FORMATTING RULES:
        - DO NOT write conversational responses outside this format
        - DO NOT skip any fields
        - ALWAYS include all 8 fields above, even if the value is "none"
        - Your response MUST start with "INTENT:" on the first line
        - ACTION must be EXACTLY "use_tool", "ask_user", or "answer" - nothing else!
        - Always provide ANSWER field even if empty - write a proper greeting or response!
        
        Be concise and follow the format exactly.   
        """

        # Create prompt with message history placeholder
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_template),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}")
        ])
        
        # Base chain
        base_chain = prompt | self.llm
        
        # Wrap with message history
        self.chain = RunnableWithMessageHistory(
            base_chain,
            self._get_session_history,
            input_messages_key="question",
            history_messages_key="history",
        )
    
    def _get_session_history(self, session_id: str) -> ChatMessageHistory:
        """Get or create chat history for a session."""
        if session_id not in self.chat_history_store:
            self.chat_history_store[session_id] = ChatMessageHistory()
        return self.chat_history_store[session_id]
    
    def execute(self, user_input: str) -> Dict[str, Any]:
        """
        Main execution: plan > execute > return result.
        
        Args:
            user_input: User's message
        
        Returns:
            Dict with execution result and bot response
        """
        try:
            # Plan using the chain (with memory)
            decision = self._plan(user_input)
            # Validate decision
            if decision["action"] == "use_tool" and not decision.get("tool"):
                decision["action"] = "answer"
                decision["answer"] = "I need to clarify what you're asking for."

            # Execute based on decision
            if decision["action"] == "use_tool":
                # Check if missing info
                if decision.get("missing") and decision["missing"].lower() != "none":
                    result = {
                        "success": True,
                        "response": decision.get(
                            "question",
                            "Could you please provide more details?"
                        ),
                        "requires_input": True
                    }
                else:
                    result = self._execute_tool(decision)
            
            elif decision["action"] == "ask_user":
                missing = decision.get("missing", "").lower()
                if "longitude" in missing or "latitude" in missing:
                    return {
                        "response": "Sorry, I can't find the nearest ZUS Coffee outlets near you without your location. Perhaps try giving an area instead. ",
                        "requires_input": False,
                        "success": False
                    }
                result = {
                    "success": True,
                    "response": decision.get("question", "Could you provide more details?"),
                    "requires_input": True
                }
            
            else:
                result = {
                    "success": True,
                    "response": decision.get("answer", "I'm here to help!"),
                    "requires_input": False
                }
                    
            # Add assistant response to history ONLY if it was a valid decision
            history = self._get_session_history(self.session_id)
            # Only add if we have a proper response
            if result.get("response"):  
                history.add_ai_message(result["response"])
                    
            # Include decision for transparency
            result["decision"] = decision
            
            return result
        
        except RateLimitError as e:
        # Gracefully handle rate limiting
            return {
                "success": False,
                "response": "I'm currently receiving too many requests. Please try again in a moment.",
                "error": "rate_limit",
                "error_message": str(e),
                "requires_input": False
            }
    
    def _plan(self, user_input: str) -> Dict[str, Any]:
        """Plan what action to take using the chain."""
        
        # Check if this is a location-related query
        location_keywords = ["near", "nearest", "closest", "nearby", "close to me", "around me", "outlet", "location", "branch", "store"]
        user_input_lower = user_input.lower()
        is_location_query = any(keyword in user_input_lower for keyword in location_keywords)
        
        context_info = ""
        # Populate context information ONLY for location queries
        if is_location_query and self.context.get('user_location'):
            loc = self.context['user_location']
            context_info = f"\nUser's GPS Location Available: (Latitude {loc['latitude']}, Longitude {loc['longitude']})"
        
        # Invoke chain with message history and context
        full_input = user_input + context_info
        
        response = self.chain.invoke(
            {"question": full_input},
            config={"configurable": {"session_id": self.session_id}}
        )
        
        decision_text = response.content
        decision = self._parse_decision(decision_text)
        
        user_input_lower = user_input.lower()
        
        if (decision.get("tool") == "outlet_query" and 
            any(keyword in user_input_lower for keyword in location_keywords) and 
            self.context.get('user_location')):
            
            location = self.context['user_location']
            # Add latitude/longitude to params
            decision['params']['latitude'] = location['latitude']
            decision['params']['longitude'] = location['longitude']
        
        print("DECISION TEXT:\n", decision_text)
        print("PARSED DECISION:\n", decision)
        
        return decision
    
    def _parse_decision(self, decision_text: str) -> Dict[str, Any]:
        """Parse the LLM's decision into a structured format."""
        
        decision = {
            "intent": "",
            "missing": "",
            "action": "answer",
            "tool": None,
            "params": {},
            "question": "",
            "answer": "",
            "reasoning": ""
        }

        # Check if response is in correct format
        if not decision_text.strip().startswith("INTENT:"):
            # Treat entire response as an answer
            print("WARNING: LLM didn't follow format. Using fallback parsing.")
            decision["intent"] = "unstructured response"
            decision["missing"] = "none"
            decision["action"] = "answer"
            decision["answer"] = decision_text.strip()
            decision["reasoning"] = "fallback parsing due to format violation"
            return decision
        
        patterns = {
            "intent": r"INTENT:\s*(.+?)(?=\n|$)",
            "missing": r"MISSING:\s*(.+?)(?=\n|$)",
            "action": r"ACTION:\s*(.+?)(?=\n|$)",
            "tool": r"TOOL:\s*(.+?)(?=\n|$)",
            "params": r"PARAMS:\s*(.+?)(?=\n|$)",
            "question": r"QUESTION:\s*(.+?)(?=\n|$)",
            "answer": r"ANSWER:\s*(.+?)(?=\n|$)",
            "reasoning": r"REASONING:\s*(.+?)(?=\n|$)"
        }
        
        for key, pattern in patterns.items():
            match = re.search(pattern, decision_text, re.IGNORECASE)
            if match:
                value = match.group(1).strip()
                # Remove any leading non-alphanumeric characters (*, [, etc.) and whitespace
                value = re.sub(r'^[^a-zA-Z0-9{]+', '', value)
                # Remove any trailing non-alphanumeric characters and whitespace  
                value = re.sub(r'[^a-zA-Z0-9}]+$', '', value)
                
                if key == "params" and value and value != "none":
                    try:
                        decision[key] = json.loads(value)
                    except:
                        decision[key] = {}
                else:
                    decision[key] = value

        if decision["action"] in AVAILABLE_TOOLS and not decision["action"] == "ask_user":
            # Action may have use_tool since llm hallucinates
            # Ensure that action is NEVER any tool call
            decision["action"] = "use_tool"
            

        return decision
    
    def _execute_tool(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool based on the decision."""
        
        tool_name = decision.get("tool")
        params = decision.get("params", {})
        
        if not tool_name or tool_name == "none":
            return {
                "success": True,
                "response": "I'm not sure how to help with that.",
                "requires_input": False
            }
        
        tool = get_tool(tool_name)
        if not tool:
            return {
                "success": True,
                "response": f"Tool '{tool_name}' not found.",
                "requires_input": False
            }
        
        # Execute the tool
        tool_result = tool.execute(**params)

        print("TOOL RESULT:", tool_result)
        print("SUCCESS:", tool_result.get("success"))
        print("MESSAGE:", tool_result.get("message"))
        print("RESULT:", tool_result.get("result"))

        # Update context if needed
        if tool_name == "outlet_lookup" and tool_result.get("success"):
            self.context["current_outlet"] = tool_result["result"]
        
        # Generate response
        if tool_result.get("success"):
            response = self._generate_response_from_tool(tool_name, tool_result)
        else:
            response = tool_result.get("message") or "An error occurred while using the tool."
        
        return {
            # Agent handled request so true
            "success": True,  
            "response": response,
            "tool_result": tool_result,
            "requires_input": False
        }
    
    def _generate_response_from_tool(self, tool_name: str, tool_result: Dict[str, Any]) -> str:
        """Generate natural language response from tool results."""
        
        if tool_name == "calculator":
            return f"The answer is {tool_result['result']}"
        
        elif tool_name == "product_search":
            data = tool_result["result"]
            products = data.get("products", [])
            
            if not products:
                return "I couldn't find any products matching your description."
            
            # Aggregate the data first
            product_list_text = ""
            for i, product in enumerate(products[:5], 1):
                product_list_text += (
                    f"{i}. {product['name']} ({product.get('category', 'Uncategorized')})\n"
                    f"   Price: {product.get('price', 'N/A')}\n"
                )
                if product.get("description"):
                    product_list_text += f"   Description: {product['description']}\n"
                product_list_text += "\n"
            
            summary_prompt = f"""
            You are a helpful assistant summarizing ZUS Coffee outlet data.

            Below is a list of our product search results:
            {product_list_text}

            Your task:
            1. Write a short, friendly summary (2–4 sentences) highlighting:
            - What kind of drinks or products were found (e.g., coffee blends, drinkware, cold brews).
            - The overall vibe (e.g., "refreshing options", "perfect for caffeine lovers").
            - Mention that the customer can explore or order them at our stores or online.
            - The product name(s) and their description(s) using the format:
                1.  product name and price
                    description
            2. Use a warm, brand-consistent tone like ZUS Coffee marketing copy.
            3. Avoid repeating exact product names and summarize naturally.
            4. Keep it concise and specific.
            """

            summary = self.llm.invoke(summary_prompt)

            return summary.content.strip()

        elif tool_name == "outlet_query":
            data = tool_result.get("result") or {}  
            outlets = data.get("results", [])
            # Check if this was a nearest query
            is_nearest = tool_result.get("is_nearest", False)  
            
            if not outlets:
                if is_nearest:
                    return "I couldn't find any outlets near your location. Please ensure location access is enabled."
                return "I couldn't find any outlets matching your description."
            
            # Build structured text
            outlet_texts = []

            # Just incase llm returned >3
            outlets = outlets[:3]
            for outlet in outlets:
                # Skip entries that only contain errors
                if "error" in outlet and not outlet.get("name"):
                    return f"Sorry, I couldn’t retrieve the information. Could you be more specific?"

                name = outlet.get("name", "Unknown Outlet")
                address = outlet.get("address", "Address unavailable")
                phone = outlet.get("phone", "Phone unavailable")
                operating_hours = outlet.get("operating_hours", "Operating hours unavailable")

                # Include distance for nearest queries
                if is_nearest:
                    distance = outlet.get("distance_km", "Distance unavailable")
                    text = (
                        f"Name: {name}\n"
                        f"Distance: {distance} km away\n"
                        f"Address: {address}\n"
                        f"Phone: {phone}\n"
                        f"Operating Hours: {operating_hours}\n"
                    )
                else:
                    text = (
                        f"Name: {name}\n"
                        f"Address: {address}\n"
                        f"Phone: {phone}\n"
                        f"Operating Hours: {operating_hours}\n"
                    )
                
                outlet_texts.append(text)
            
            # Check if we have any valid outlets after filtering
            if not outlet_texts:
                return "Sorry, I couldn't retrieve the outlet information. Could you be more specific?"
            
            combined_outlet_info = "\n\n".join(outlet_texts)
            
            # Different prompt for nearest vs regular search
            if is_nearest:
                summary_prompt = f"""
                You are a helpful assistant for ZUS Coffee customers.
                
                The user asked for the NEAREST outlets, and here are the results sorted by distance:
                {combined_outlet_info}
                
                Your task:
                1. Write a friendly summary (3-5 sentences) in first person (as ZUS Coffee).
                2. Emphasize these are the CLOSEST locations to the user.
                3. List outlets with: branch name, distance, address, and hours.
                4. ALWAYS Use format:
                1. **Branch Name**
                    Distance km away
                    Address
                    Operating hours
                5. Use an enthusiastic, welcoming tone.
                6. End with something friendly like "We look forward to serving you!"
                """
            else:
                summary_prompt = f"""
                You are a helpful assistant summarizing ZUS Coffee outlet data.

                Below is structured outlet data retrieved from the database:
                {combined_outlet_info}

                Your task:
                1. Write a short, human-friendly summary (3–5 sentences).
                2. Refer to ZUS Coffee in first person (e.g., "We" instead of "ZUS Coffee").
                3. Use format:
                    1. **Branch Name**
                        Address
                        Operating hours
                - Any consistent patterns (e.g., "We're open daily from 8AM to 8PM" or "You can reach us at 012-816 1340.")
                4. Use a professional but friendly tone suitable for a coffee brand.
                5. Avoid repeating the word "outlet" — vary with "branch", "location", or "store".
                6. Do not restate every detail like coordinates; summarize naturally.
                7. Keep the response concise and specific without too much added jargon.
                """
            
            summary = self.llm.invoke(summary_prompt)
            return summary.content.strip()

        
        else:
            return tool_result.get("message", "I processed your request.")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get conversation history for current session."""
        history = self._get_session_history(self.session_id)
        return [
            {"role": "user" if isinstance(msg, type(history.messages[0])) else "assistant", 
             "content": msg.content}
            for msg in history.messages
        ]
    
    def clear_history(self):
        """Clear conversation history for current session."""
        if self.session_id in self.chat_history_store:
            self.chat_history_store[self.session_id].clear()
        self.context = {}
    
    def update_context(self, key: str, value: Any):
        """Update context manually."""
        self.context[key] = value


# Factory function for creating agents with different sessions
def create_agent(session_id: str = "default") -> AgentPlanner:
    """Create a new agent instance for a session."""
    return AgentPlanner(session_id=session_id)
