import React from "react";
import "./ChatMessage.css";

const ChatMessage = ({ text, sender }) => {
  if (!text) {
    console.warn("ChatMessage received empty text:", { text, sender });
  }

  return (
    <div className={`chat-message ${sender === "user" ? "user-message" : "bot-message"}`}>
      <p>{text || "Empty message received!"}</p>
    </div>
  );
};

export default ChatMessage;
