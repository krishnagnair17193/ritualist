import React from 'react';

const Header = () => {
  return (
    <header className="glass-effect px-6 py-4 flex justify-between items-center sticky top-0 z-40">
      <div className="flex items-center gap-3">
        <h1 className="text-3xl font-extrabold text-white">🧘 Ritualist</h1>
        <div className="text-sm text-white/80 hidden sm:block">Your journey to better habits</div>
      </div>
      <div className="flex items-center gap-4">
        <div className="streak-badge">🔥 5 day streak</div>
        <div className="flex items-center gap-3 text-white">
          <span className="text-sm font-medium hidden sm:block">Welcome back!</span>
          <img
            src="https://i.pravatar.cc/40"
            alt="avatar"
            className="w-10 h-10 rounded-full border-2 border-white/30"
          />
        </div>
      </div>
    </header>
  );
};

export default Header;