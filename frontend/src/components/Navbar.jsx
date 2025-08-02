import React from 'react';

const Navbar = ({ activeView, setActiveView }) => {
  const navItems = [
    { name: 'Dashboard', key: 'dashboard' },
    { name: 'My Habits', key: 'habits' },
    { name: 'Analytics', key: 'analytics' },
  ];

  return (
    <nav className="flex justify-center gap-2 mt-6 px-6">
      {navItems.map((item) => (
        <button
          key={item.key}
          className={`nav-button px-6 py-3 rounded-full text-sm font-medium ${
            activeView === item.key ? 'active' : 'text-white/70'
          }`}
          onClick={() => setActiveView(item.key)}
        >
          {item.name}
        </button>
      ))}
    </nav>
  );
};

export default Navbar;
