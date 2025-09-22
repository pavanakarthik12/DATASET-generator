import React, { useState, useRef, useEffect } from 'react';
import { chatbotAPI } from '../api/api';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(true);
  const [messages, setMessages] = useState([
    {
      type: 'assistant',
      content: 'Hello! I\'m your AI assistant for the Smart Dataset Generator. I can help you with suggestions for data collection, analysis strategies, and export formats. How can I assist you today?'
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      type: 'user',
      content: inputValue.trim()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await chatbotAPI.getSuggestion(inputValue.trim());
      
      if (response.success && response.data) {
        const assistantMessage = {
          type: 'assistant',
          content: response.data.suggestion || response.data.recommendations || 'I received your message but couldn\'t generate a proper response.'
        };
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        throw new Error(response.error || response.detail || 'Failed to get AI response');
      }
    } catch (error) {
      console.error('Chatbot error:', error);
      const errorMessage = {
        type: 'assistant',
        content: `Sorry, I encountered an error: ${error.message}. Please try again or check if the backend is running.`
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className={`chat-widget ${isOpen ? '' : 'hidden'}`} id="chat">
      <div className="chat-header">
        <h4>AI Assistant</h4>
        <button className="chat-toggle" onClick={toggleChat}>
          {isOpen ? '−' : '+'}
        </button>
      </div>
      
      {isOpen && (
        <>
          <div className="chat-messages">
            {messages.map((message, index) => (
              <div key={index} className={`chat-message ${message.type}`}>
                {message.content}
              </div>
            ))}
            {isLoading && (
              <div className="chat-message assistant">
                Thinking...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          
          <form className="chat-input" onSubmit={handleSubmit}>
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask me about dataset generation..."
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading || !inputValue.trim()}>
              Send
            </button>
          </form>
        </>
      )}
    </div>
  );
};

export default ChatWidget;
