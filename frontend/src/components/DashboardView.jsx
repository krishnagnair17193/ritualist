import React, { useState, useEffect } from 'react';

const DashboardView = ({ onLogout }) => {
  const [habits, setHabits] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Debug environment variables
  console.log('Environment variables:', {
    REACT_APP_API_URL: process.env.REACT_APP_API_URL,
    NODE_ENV: process.env.NODE_ENV,
    allEnvVars: Object.keys(process.env).filter(key => key.startsWith('REACT_APP_'))
  });

  // API call function - replace with your actual API endpoint
  const apiCall = async (endpoint, options = {}) => {
    try {
      // Temporary hard-coded URL for testing
      const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const fullUrl = `${baseUrl}${endpoint}`;

      console.log('Making API call to:', fullUrl, 'with options:', options);

      const response = await fetch(fullUrl, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      // Check if the response is actually JSON
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Server returned non-JSON response (likely an error page)');
      }

      return await response.json();
    } catch (error) {
      if (error.name === 'SyntaxError') {
        throw new Error('Server returned invalid JSON (likely an HTML error page)');
      }
      throw error;
    }
  };

  // Fetch habit logs for a specific date
  const fetchHabitLogs = async (date) => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiCall(`/habits/logs/?date=${date}`);
      setHabits(data || []); // Ensure we have an array
    } catch (err) {
      setError(`Failed to fetch habits: ${err.message}`);
      console.error('Error fetching habit logs:', err);
      // Set mock data for development/testing
      setHabits([
        {
          id: 1,
          name: "Drink 8 glasses of water",
          description: "Stay hydrated throughout the day",
          completed: false,
          category: "Health",
          streak: 5
        },
        {
          id: 2,
          name: "30 minutes exercise",
          description: "Any form of physical activity",
          completed: true,
          category: "Fitness",
          streak: 12
        },
        {
          id: 3,
          name: "Read for 20 minutes",
          description: "Reading books or articles",
          completed: false,
          category: "Learning",
          streak: 3
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Fetch data when component mounts or date changes
  useEffect(() => {
    fetchHabitLogs(selectedDate);
  }, [selectedDate]);

  // Handle habit completion toggle
  const toggleHabit = async (habitId) => {
    try {
      await apiCall(`/habits/${habitId}/toggle`, {
        method: 'POST',
        body: JSON.stringify({
          date: selectedDate
        })
      });
      // Refresh the data
      fetchHabitLogs(selectedDate);
    } catch (err) {
      // For demo purposes, toggle locally if API fails
      setHabits(prevHabits =>
        prevHabits.map(habit =>
          habit.id === habitId
            ? { ...habit, completed: !habit.completed }
            : habit
        )
      );
      console.warn('API toggle failed, toggled locally:', err.message);
    }
  };

  // Handle date change
  const handleDateChange = (event) => {
    setSelectedDate(event.target.value);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p>Loading habits...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Habit Dashboard</h1>
            <p className="text-gray-600">Track your daily habits and build consistency</p>
          </div>
          {onLogout && (
            <button
              onClick={onLogout}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg transition-colors flex items-center gap-2"
            >
              <span>🚪</span>
              Logout
            </button>
          )}
        </div>
      </div>

      {/* Date Selector */}
      <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div className="flex items-center gap-4 flex-wrap">
          <span className="text-blue-600 text-lg">📅</span>
          <label htmlFor="date" className="text-sm font-medium text-gray-700 whitespace-nowrap">
            Select Date:
          </label>
          <input
            type="date"
            id="date"
            value={selectedDate}
            onChange={handleDateChange}
            className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 min-w-0 flex-shrink-0 text-gray-900 bg-white"
            style={{
              colorScheme: 'light',
              fontSize: '14px',
              minWidth: '150px'
            }}
          />
          <div className="text-sm text-gray-500">
            Selected: {new Date(selectedDate + 'T00:00:00').toLocaleDateString('en-US', {
              weekday: 'short',
              year: 'numeric',
              month: 'short',
              day: 'numeric'
            })}
          </div>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
          <div className="flex items-start">
            <span className="text-yellow-600 text-lg mr-2">⚠️</span>
            <div>
              <p className="text-yellow-800 font-medium">API Connection Issue</p>
              <p className="text-yellow-700 text-sm">{error}</p>
              <p className="text-yellow-600 text-xs mt-1">
                Showing demo data. Please check your API configuration.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Stats Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center">
            <span className="text-green-600 text-2xl mr-3">🎯</span>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Completed</h3>
              <p className="text-2xl font-bold text-green-600">
                {habits.filter(habit => habit.completed).length}
              </p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center">
            <span className="text-blue-600 text-2xl mr-3">📈</span>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Total Habits</h3>
              <p className="text-2xl font-bold text-blue-600">{habits.length}</p>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center">
            <span className="text-purple-600 text-2xl mr-3">📊</span>
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Completion Rate</h3>
              <p className="text-2xl font-bold text-purple-600">
                {habits.length > 0 ? Math.round((habits.filter(habit => habit.completed).length / habits.length) * 100) : 0}%
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Habits List */}
      <div className="bg-white rounded-lg shadow-sm">
        <div className="p-6 border-b border-gray-200">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-gray-900">Today's Habits</h2>
            <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors">
              <span className="text-lg">➕</span>
              Add Habit
            </button>
          </div>
        </div>

        <div className="p-6">
          {habits.length === 0 ? (
            <div className="text-center py-8">
              <span className="text-6xl text-gray-400 block mb-4">🎯</span>
              <p className="text-gray-500">No habits found for this date.</p>
              <p className="text-sm text-gray-400">Add some habits to get started!</p>
            </div>
          ) : (
            <div className="space-y-4">
              {habits.map((habit) => (
                <div
                  key={habit.id}
                  className={`flex items-center justify-between p-4 rounded-lg border ${
                    habit.completed
                      ? 'bg-green-50 border-green-200'
                      : 'bg-gray-50 border-gray-200'
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <button
                      onClick={() => toggleHabit(habit.id)}
                      className="text-2xl"
                    >
                      {habit.completed ? (
                        <span className="text-green-600">✅</span>
                      ) : (
                        <span className="text-gray-400">⭕</span>
                      )}
                    </button>
                    <div>
                      <h3 className={`font-medium ${
                        habit.completed ? 'text-green-800' : 'text-gray-900'
                      }`}>
                        {habit.name}
                      </h3>
                      {habit.description && (
                        <p className="text-sm text-gray-600">{habit.description}</p>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-2">
                    {habit.streak && (
                      <span className="bg-orange-100 text-orange-800 text-xs font-medium px-2 py-1 rounded">
                        {habit.streak} day streak
                      </span>
                    )}
                    {habit.category && (
                      <span className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded">
                        {habit.category}
                      </span>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardView;