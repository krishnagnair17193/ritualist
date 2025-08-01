import React, { useState } from 'react';
import Heatmap from '../components/Heatmap';
import HabitSelector from '../components/HabitSelector';
import DateRangePicker from '../components/DateRangePicker';

const HomePage = () => {
  const [selectedHabit, setSelectedHabit] = useState(null);
//   const [dateRange, setDateRange] = useState({ start: null, end: null });

  const today = new Date();
  const lastWeek = new Date();
  lastWeek.setDate(today.getDate() - 6);

const [dateRange, setDateRange] = useState({
  start: lastWeek,
  end: today,
});

  // Dummy habit list for now
  const habits = [
    { id: 1, name: 'Exercise' },
    { id: 2, name: 'Meditation' },
    { id: 3, name: 'Reading' },
  ];

  return (
      <div>
    <div className="p-6 space-y-6">
      <DateRangePicker dateRange={dateRange} setDateRange={setDateRange} />
      <HabitSelector habits={habits} onSelect={setSelectedHabit} />
      {selectedHabit && (
        <Heatmap habit={selectedHabit} dateRange={dateRange} />
      )}
    </div>
    <div className="text-2xl text-green-600 font-bold">Tailwind is working ✅</div>
    </div>
  );
};

export default HomePage;