import React from "react";
import ChatWindow from "../components/ChatWindow/ChatWindow";
import "./ChatPage.css";

const ChatPage = () => {
  return (
    <div className="chat-page">
      <h2 className="chat-title">Chat with AI Assistant</h2>
      <ChatWindow />
    </div>
  );
};

export default ChatPage;
