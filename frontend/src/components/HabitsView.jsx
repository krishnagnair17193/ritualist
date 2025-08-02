import React from 'react';

const HabitsView = () => {
  return (
    <div className="view">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-white">My Habits</h2>
        <button className="bg-white/20 hover:bg-white/30 text-white px-6 py-3 rounded-full transition-all">
          ✨ New Habit
        </button>
      </div>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {[
          {
            emoji: "💧",
            streak: "5 days",
            title: "Drink Water",
            subtitle: "8 glasses per day",
            progress: 75,
            detail: "6/8 completed today",
          },
          {
            emoji: "🏃",
            streak: "12 days",
            title: "Exercise",
            subtitle: "30 minutes daily",
            progress: 100,
            detail: "Completed today! 🎉",
          },
          {
            emoji: "📚",
            streak: "3 days",
            title: "Reading",
            subtitle: "20 pages per day",
            progress: 40,
            detail: "8/20 pages completed",
          },
        ].map((habit, idx) => (
          <div
            key={idx}
            className="habit-card glass-effect rounded-2xl p-6 text-white"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="text-2xl">{habit.emoji}</div>
              <div className="streak-badge">{habit.streak}</div>
            </div>
            <h3 className="text-lg font-semibold mb-2">{habit.title}</h3>
            <p className="text-white/70 text-sm mb-4">{habit.subtitle}</p>
            <div className="w-full bg-white/20 rounded-full h-2">
              <div
                className="bg-green-400 h-2 rounded-full"
                style={{ width: `${habit.progress}%` }}
              ></div>
            </div>
            <p className="text-xs text-white/60 mt-2">{habit.detail}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HabitsView;