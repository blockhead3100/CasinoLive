import React, { useState } from 'react';
import LoginForm from './components/auth/LoginForm';
import SignUpForm from './components/auth/SignUpForm';
import ChatContainer from './components/chat/ChatContainer';

const App: React.FC = () => {
  const [isAuthenticated] = useState(true);
  const [isLogin, setIsLogin] = useState(true);

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background p-4">
        {isLogin ? (
          <div>
            <LoginForm />
            <p className="text-center mt-4">
              Don't have an account?{' '}
              <button
                onClick={() => setIsLogin(false)}
                className="text-primary hover:underline"
              >
                Sign up
              </button>
            </p>
          </div>
        ) : (
          <div>
            <SignUpForm />
            <p className="text-center mt-4">
              Already have an account?{' '}
              <button
                onClick={() => setIsLogin(true)}
                className="text-primary hover:underline"
              >
                Log in
              </button>
            </p>
          </div>
        )}
      </div>
    );
  }

  return <ChatContainer />;
};

export default App;
