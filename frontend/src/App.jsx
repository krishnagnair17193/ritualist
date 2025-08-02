// src/App.jsx
import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import Navbar from './components/Navbar';
import HabitDashboard from './components/DashboardView';
// import HabitsView from './components/HabitsView';
// import AnalyticsView from './components/AnalyticsView';

const App = () => {
  const [activeView, setActiveView] = useState('dashboard');

  // Optional: apply background theme directly
  useEffect(() => {
    document.body.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
    document.body.style.fontFamily = "'Inter', sans-serif";
    return () => {
      document.body.style.background = '';
      document.body.style.fontFamily = '';
    };
  }, []);

  return (
    <div className="min-h-screen text-white">
      <Header />
      <Navbar activeView={activeView} setActiveView={setActiveView} />

      <main className="max-w-6xl mx-auto mt-8 px-6 pb-24">
        {activeView === 'dashboard' && <DashboardView />}
        {/* {activeView === 'habits' && <HabitsView />} */}
        {/* {activeView === 'analytics' && <AnalyticsView />} */}
      </main>

      {/* Optional Floating Action Button */}
      <div className="fixed bottom-8 right-8 z-50">
        <button
          className="floating-button"
          title="Add New Habit"
          onClick={() => alert('Open New Habit Modal')}
        >
          <svg
            width="24"
            height="24"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 6v6m0 0v6m0-6h6m-6 0H6"
            />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default App;