import React from 'react';
import { User } from '../../types/user';

interface ChatHeaderProps {
  user: User;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ user }) => {
  return (
    <div className="flex items-center px-6 py-3 bg-white border-b">
      <div className="relative">
        <img
          src={user.avatar || `https://ui-avatars.com/api/?name=${user.username}`}
          alt={user.username}
          className="w-10 h-10 rounded-full"
        />
        <div className={`absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-white ${user.isOnline ? 'bg-green-500' : 'bg-gray-400'}`} />
      </div>
      <div className="ml-3">
        <h3 className="font-semibold">{user.username}</h3>
        <p className="text-sm text-gray-500">
          {user.isOnline ? 'Online' : 'Offline'}
        </p>
      </div>
    </div>
  );
};

export default ChatHeader;
