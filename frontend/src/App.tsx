import React, { useState } from 'react';
import LandingPage from './components/LandingPage';
import ChatInterface from './components/ChatInterface';

function App() {
  const [currentView, setCurrentView] = useState<'landing' | 'chat'>('landing');

  return (
    <>
      {currentView === 'landing' ? (
        <LandingPage onLaunchApp={() => setCurrentView('chat')} />
      ) : (
        <ChatInterface onBackToLanding={() => setCurrentView('landing')} />
      )}
    </>
  );
}

export default App;
