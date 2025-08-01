import React from 'react';

const HabitSelector = ({ habits = [], onSelect }) => {
  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-2">Select Habit</h2>
      <ul className="space-y-2">
        {habits.map((habit) => (
          <li key={habit.id}>
            <button
              onClick={() => onSelect(habit)}
              className="bg-blue-500 hover:bg-blue-600 text-white py-1 px-3 rounded"
            >
              {habit.name}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HabitSelector;