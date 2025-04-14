import React from 'react';
import { Message } from '../../types/message';

interface MessageListProps {
  messages: Message[];
  currentUserId: string;
}

const MessageList: React.FC<MessageListProps> = ({ messages, currentUserId }) => {
  return (
    <div className="flex-1 p-4 space-y-4 overflow-y-auto scrollbar-hide">
      {messages.map((message) => (
        <div
          key={message.id}
          className={`message-bubble ${
            message.senderId === currentUserId
              ? 'message-sent'
              : 'message-received'
          }`}
        >
          <p>{message.content}</p>
          <span className="text-xs opacity-75">
            {new Date(message.timestamp).toLocaleTimeString()}
          </span>
        </div>
      ))}
    </div>
  );
};

export default MessageList;
