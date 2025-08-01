import React from 'react';
import { format, eachDayOfInterval } from 'date-fns';

const Heatmap = ({ habit, dateRange }) => {
  if (!habit || !dateRange.start || !dateRange.end) return null;

  // Generate days in range
  const days = eachDayOfInterval({ start: dateRange.start, end: dateRange.end });

  // Simulate data: random completion
  const completions = days.map((date) => ({
    date,
    completed: Math.random() > 0.5,
  }));

  return (
    <div>
      <h3 className="text-xl font-bold mb-2">{habit.name} Heatmap</h3>
      <div className="grid grid-cols-7 gap-2">
        {completions.map(({ date, completed }) => (
          <div
            key={date.toISOString()}
            className={`w-8 h-8 rounded ${
              completed ? 'bg-green-500' : 'bg-gray-300'
            } flex items-center justify-center text-xs`}
            title={format(date, 'yyyy-MM-dd')}
          >
            {format(date, 'd')}
          </div>
        ))}
      </div>
    </div>
  );
};

export default Heatmap;