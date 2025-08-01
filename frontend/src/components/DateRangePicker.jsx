import React from 'react';

const DateRangePicker = ({ dateRange, setDateRange }) => {
  const handleChange = (e) => {
    const { name, value } = e.target;
    setDateRange((prev) => ({
      ...prev,
      [name]: new Date(value),
    }));
  };

  return (
    <div className="space-x-4">
      <input
        type="date"
        name="start"
        value={dateRange.start?.toISOString().split('T')[0] || ''}
        onChange={handleChange}
        className="border p-2 rounded"
      />
      <input
        type="date"
        name="end"
        value={dateRange.end?.toISOString().split('T')[0] || ''}
        onChange={handleChange}
        className="border p-2 rounded"
      />
    </div>
  );
};

export default DateRangePicker;