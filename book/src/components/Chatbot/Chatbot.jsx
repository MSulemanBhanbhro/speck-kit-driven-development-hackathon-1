import React, { useState, useRef, useEffect } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: 'Hello! I\'m your AI Robotics assistant. How can I help you with robotics today?', sender: 'bot', timestamp: new Date() }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
    if (!isOpen && inputRef.current) {
      setTimeout(() => inputRef.current.focus(), 100);
    }
  };

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (inputMessage.trim() === '') return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate bot response after delay
    setTimeout(() => {
      const botResponse = generateBotResponse(inputMessage);
      const botMessage = {
        id: Date.now() + 1,
        text: botResponse,
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
    }, 1000);
  };

  const generateBotResponse = (userMessage) => {
    const lowerCaseMessage = userMessage.toLowerCase();

    if (lowerCaseMessage.includes('hello') || lowerCaseMessage.includes('hi') || lowerCaseMessage.includes('hey')) {
      return 'Hello there! I\'m here to help you with AI Robotics topics. What would you like to know about robotics?';
    } else if (lowerCaseMessage.includes('ros') || lowerCaseMessage.includes('ros 2')) {
      return 'ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software. It provides libraries and tools to help software developers create robot applications. Would you like to know more about ROS 2 concepts?';
    } else if (lowerCaseMessage.includes('gazebo')) {
      return 'Gazebo is a robot simulation environment that provides realistic physics, high-quality graphics, and convenient programmatic interfaces. It\'s perfect for testing robotics algorithms before deploying to real robots.';
    } else if (lowerCaseMessage.includes('nvidia') || lowerCaseMessage.includes('isaac')) {
      return 'NVIDIA Isaac is a robotics platform that provides tools and libraries for developing AI-powered robots. It includes Isaac Sim for simulation and Isaac ROS for perception and navigation.';
    } else if (lowerCaseMessage.includes('humanoid') || lowerCaseMessage.includes('humanoid robot')) {
      return 'Humanoid robots are robots with human-like features and capabilities. They often use advanced control systems, AI, and perception to interact with humans and environments.';
    } else if (lowerCaseMessage.includes('physical ai') || lowerCaseMessage.includes('embodied ai')) {
      return 'Physical AI, also known as Embodied AI, focuses on AI systems that interact with the physical world through robotic bodies. This combines AI with robotics to create intelligent agents.';
    } else if (lowerCaseMessage.includes('vision') || lowerCaseMessage.includes('perception')) {
      return 'Vision and perception systems in robotics involve computer vision, sensor fusion, and machine learning to help robots understand and navigate their environment.';
    } else if (lowerCaseMessage.includes('thank')) {
      return 'You\'re welcome! Is there anything else I can help you with regarding robotics?';
    } else if (lowerCaseMessage.includes('help')) {
      return 'I can help you with topics related to: ROS 2, Gazebo simulation, NVIDIA Isaac, Humanoid Robotics, Physical AI, Vision-Language-Action systems, and more. What specific topic would you like to explore?';
    } else {
      return 'That\'s an interesting question about robotics! I\'m here to help you learn about AI Robotics concepts. Would you like to know more about ROS 2, Gazebo, NVIDIA Isaac, or Humanoid Robotics?';
    }
  };

  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chatbot">
      {/* Chatbot Toggle Button */}
      {isOpen ? null : (
        <button className="chatbot-toggle" onClick={toggleChat} aria-label="Open AI Robotics Assistant">
          <div className="chatbot-icon">🤖</div>
        </button>
      )}

      {/* Chatbot Window */}
      {isOpen && (
        <div className="chatbot-window">
          <div className="chatbot-header">
            <div className="chatbot-header-content">
              <div className="chatbot-icon">🤖</div>
              <div className="chatbot-info">
                <h4>AI Robotics Assistant</h4>
                <p>Ask me anything about robotics!</p>
              </div>
            </div>
            <button className="chatbot-close" onClick={toggleChat}>
              ×
            </button>
          </div>

          <div className="chatbot-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`chatbot-message ${message.sender}`}
              >
                <div className="message-content">
                  <p>{message.text}</p>
                  <span className="message-time">
                    {formatTime(message.timestamp)}
                  </span>
                </div>
              </div>
            ))}

            {isTyping && (
              <div className="chatbot-message bot typing-indicator">
                <div className="message-content">
                  <div className="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          <form className="chatbot-input-form" onSubmit={handleSendMessage}>
            <input
              ref={inputRef}
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your robotics question..."
              className="chatbot-input"
            />
            <button type="submit" className="chatbot-send-button">
              <span>➤</span>
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default Chatbot;