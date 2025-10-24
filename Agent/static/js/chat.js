        const chatMessages = document.getElementById('chatMessages');
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        let userLocation = null;
        let locationAttempted = false;

        // Focus input on load
        messageInput.focus();
        // Request user location on page load
        function getUserLocation() {
            if (navigator.geolocation && !locationAttempted) {
                locationAttempted = true;
                console.log('Requesting user location...');
                
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        userLocation = {
                            latitude: position.coords.latitude,
                            longitude: position.coords.longitude
                        };
                        console.log('Location obtained:', userLocation);
                    },
                    (error) => {
                        console.log('Location access denied or unavailable:', error.message);
                        userLocation = null;
                    },
                    {
                        enableHighAccuracy: false,
                        timeout: 5000,
                        maximumAge: 300000 // Cache for 5 minutes
                    }
                );
            }
        }
        
        // Try to get location when page loads
        getUserLocation();

        function handleKeyPress(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                sendMessage();
            }
        }

        function addMessage(content, isUser) {
            // Remove welcome message if present
            const welcomeMsg = chatMessages.querySelector('.welcome-message');
            if (welcomeMsg) {
                welcomeMsg.remove();
            }

            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            
            if (isUser) {
                // User messages: plain text
                contentDiv.textContent = content;
            } else {
                // Bot messages: format markdown and preserve line breaks
                let formatted = content
                    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\n/g, '<br>');
                contentDiv.innerHTML = formatted;
            }
            
            messageDiv.appendChild(contentDiv);
            chatMessages.appendChild(messageDiv);
            
            // Scroll to bottom
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function showTypingIndicator() {
            const indicator = document.createElement('div');
            indicator.className = 'message bot';
            indicator.id = 'typingIndicator';
            indicator.innerHTML = '<div class="typing-indicator active"><span></span><span></span><span></span></div>';
            chatMessages.appendChild(indicator);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

        function hideTypingIndicator() {
            const indicator = document.getElementById('typingIndicator');
            if (indicator) {
                indicator.remove();
            }
        }

        async function sendMessage() {
            const message = messageInput.value.trim();
            
            if (!message) return;
            
            // Add user message
            addMessage(message, true);
            messageInput.value = '';
            
            // Disable input
            messageInput.disabled = true;
            sendBtn.disabled = true;
            
            // Show typing indicator
            showTypingIndicator();
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        message: message,
                        location: userLocation
                    })
                });
                
                const data = await response.json();
                
                hideTypingIndicator();
                
                if (data.success) {
                    addMessage(data.message, false);
                } else {
                    addMessage('Sorry, something went wrong. Please try again.', false);
                }
                
            } catch (error) {
                hideTypingIndicator();
                addMessage('Connection error. Please check your internet and try again.', false);
                console.error('Error:', error);
            } finally {
                // Re-enable input
                messageInput.disabled = false;
                sendBtn.disabled = false;
                messageInput.focus();
            }
        }

        async function clearConversation() {
            if (!confirm('Are you sure you want to clear the conversation?')) {
                return;
            }
            
            try {
                const response = await fetch('/api/clear', {
                    method: 'POST'
                });
                
                const data = await response.json();
                
                if (data.success) {
                    chatMessages.innerHTML = `
                        <div class="welcome-message">
                            <h2>Welcome to ZUS Coffee!</h2>
                            <p>I'm your virtual assistant. I can help you find outlets, browse products, and answer questions about our services.</p>
                            <p style="margin-top: 12px; color: #999;">Try asking: "What mugs do you have?" or "Show me outlets in KL"</p>
                        </div>
                    `;
                    messageInput.focus();
                }
                
            } catch (error) {
                alert('Could not clear conversation. Please try again.');
                console.error('Error:', error);
            }
        }