import React, { useState, useEffect, useRef } from "react";
import ChatInput from "../ChatInput/ChatInput";
import ChatMessage from "../ChatMessage/ChatMessage";
import { sendMessage } from "../../api/chatApi";
import "./ChatWindow.css";

const ChatWindow = () => {
  const [messages, setMessages] = useState([]);
  const messagesEndRef = useRef(null);

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    setMessages((prevMessages) => [...prevMessages, { text: message, sender: "user" }]);

    try {
      const response = await sendMessage(message);

      if (response && response.response) {
        setMessages((prevMessages) => [...prevMessages, { text: response.response, sender: "bot" }]);
      } else {
        setMessages((prevMessages) => [...prevMessages, { text: "No response from the AI.", sender: "bot" }]);
      }
    } catch (error) {
      console.error("Error sending message:", error);
      setMessages((prevMessages) => [...prevMessages, { text: "Something went wrong. Try again.", sender: "bot" }]);
    }
  };

 
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-window">
      <div className="messages">
        {messages.map((msg, index) => (
          <ChatMessage key={index} text={msg.text} sender={msg.sender} />
        ))}
        <div ref={messagesEndRef} /> {}
      </div>
      <ChatInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatWindow;
