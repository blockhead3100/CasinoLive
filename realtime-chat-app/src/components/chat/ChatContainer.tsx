import React, { useState } from 'react';
import ChatHeader from './ChatHeader';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import { Message } from '../../types/message';
import { User } from '../../types/user';

const mockUser: User = {
  id: '1',
  username: 'John Doe',
  email: 'john@example.com',
  isOnline: true,
};

const mockMessages: Message[] = [
  {
    id: '1',
    content: 'Hey there!',
    senderId: '1',
    receiverId: '2',
    timestamp: new Date(),
  },
  {
    id: '2',
    content: 'Hi! How are you?',
    senderId: '2',
    receiverId: '1',
    timestamp: new Date(),
  },
];

const ChatContainer: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>(mockMessages);

  const handleSendMessage = (content: string) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      content,
      senderId: '1',
      receiverId: '2',
      timestamp: new Date(),
    };
    setMessages([...messages, newMessage]);
  };

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto bg-white shadow-lg">
      <ChatHeader user={mockUser} />
      <MessageList messages={messages} currentUserId="1" />
      <MessageInput onSendMessage={handleSendMessage} />
    </div>
  );
};

export default ChatContainer;
