import React, { useState, useEffect } from 'react';
import { Calendar, CheckCircle, Circle, TrendingUp, Target, Clock, Plus, Filter, RefreshCw } from 'lucide-react';

const HabitDashboard = () => {
  const [habits, setHabits] = useState([]);
  const [habitLogs, setHabitLogs] = useState([]);
  const [dashboardStats, setDashboardStats] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedPeriodicity, setSelectedPeriodicity] = useState('all');
  const [refreshing, setRefreshing] = useState(false);

  // API base URL - adjust this to match your FastAPI server
  const API_BASE_URL = 'http://localhost:8000'; // Change this to your API URL

  // API helper function
  const apiCall = async (endpoint, options = {}) => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
  };

  // Fetch habits with stats from API
  const fetchHabits = async () => {
    try {
      const data = await apiCall('/habits/with-stats/');
      setHabits(data);
    } catch (err) {
      console.error('Error fetching habits:', err);
      setError(err.message);
    }
  };

  // Fetch habit logs from API
  const fetchHabitLogs = async (date = selectedDate) => {
    try {
      const data = await apiCall(`/habits/logs/?date=${date}`);
      import React, { useState, useEffect } from 'react';
import { Calendar, CheckCircle, Circle, TrendingUp, Target, Clock, Plus, Filter } from 'lucide-react';

const HabitDashboard = () => {
  const [habits, setHabits] = useState([]);
  const [habitLogs, setHabitLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [selectedPeriodicity, setSelectedPeriodicity] = useState('all');

  // API base URL - adjust this to match your FastAPI server
  const API_BASE_URL = 'http://localhost:8000'; // Change this to your API URL

  // Fetch habits from API
  const fetchHabits = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/habits/`);
      if (!response.ok) throw new Error('Failed to fetch habits');
      const data = await response.json();
      setHabits(data);
    } catch (err) {
      setError(err.message);
    }
  };

  // Fetch habit logs from API
  const fetchHabitLogs = async (date = selectedDate) => {
    try {
      const response = await fetch(`${API_BASE_URL}/habits/logs?date=${date}`);
      if (!response.ok) throw new Error('Failed to fetch habit logs');
      const data = await response.json();
      setHabitLogs(data);
    } catch (err) {
      setError(err.message);
    }
  };

  // Toggle habit completion
  const toggleHabitCompletion = async (habitId, completed = true) => {
    try {
      const method = completed ? 'POST' : 'DELETE';
      const response = await fetch(`${API_BASE_URL}/habits/${habitId}/complete`, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          log_date: selectedDate,
          notes: completed ? 'Completed via dashboard' : ''
        })
      });

      if (!response.ok) throw new Error('Failed to update habit');
      
      // Refresh data
      await fetchHabitLogs(selectedDate);
    } catch (err) {
      setError(err.message);
    }
  };

  // Initial data fetch
  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchHabits(), fetchHabitLogs()]);
      setLoading(false);
    };

    loadData();
  }, []);

  // Refetch logs when date changes
  useEffect(() => {
    if (!loading) {
      fetchHabitLogs(selectedDate);
    }
  }, [selectedDate]);

  // Filter habits by periodicity
  const filteredHabits = habits.filter(habit => 
    selectedPeriodicity === 'all' || habit.periodicity === selectedPeriodicity
  );

  // Get habit log status for selected date
  const getHabitLogStatus = (habitId) => {
    const log = habitLogs.find(log => log.habit_id === habitId && log.log_date === selectedDate);
    return log?.completed || false;
  };

  // Calculate streak for a habit (mock calculation - you'd get this from API)
  const getHabitStreak = (habitId) => {
    // This would come from your API, but for demo purposes:
    return Math.floor(Math.random() * 15) + 1;
  };

  // Get habit completion rate (mock calculation)
  const getCompletionRate = (habitId) => {
    const habitLogsForHabit = habitLogs.filter(log => log.habit_id === habitId);
    if (habitLogsForHabit.length === 0) return 0;
    const completed = habitLogsForHabit.filter(log => log.completed).length;
    return Math.round((completed / habitLogsForHabit.length) * 100);
  };

  // Generate calendar days for current month
  const generateCalendarDays = () => {
    const date = new Date(selectedDate);
    const year = date.getFullYear();
    const month = date.getMonth();
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDayOfWeek = firstDay.getDay();
    
    const days = [];
    
    // Add empty cells for days before the first day of the month
    for (let i = 0; i < startingDayOfWeek; i++) {
      days.push(null);
    }
    
    // Add days of the month
    for (let day = 1; day <= daysInMonth; day++) {
      days.push(new Date(year, month, day));
    }
    
    return days;
  };

  const calendarDays = generateCalendarDays();
  const monthNames = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"];
  const currentMonth = new Date(selectedDate).getMonth();
  const currentYear = new Date(selectedDate).getFullYear();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 max-w-md">
          <h3 className="text-red-800 font-medium">Error Loading Data</h3>
          <p className="text-red-600 text-sm mt-1">{error}</p>
          <button 
            onClick={() => window.location.reload()} 
            className="mt-3 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 text-sm"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto p-6 bg-gray-50 min-h-screen">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Habit Tracker Dashboard</h1>
        <p className="text-gray-600">Track your daily habits and build lasting routines</p>
      </div>

      {/* Controls */}
      <div className="mb-6 flex flex-wrap gap-4 items-center justify-between">
        <div className="flex gap-4 items-center">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Filter</label>
            <select
              value={selectedPeriodicity}
              onChange={(e) => setSelectedPeriodicity(e.target.value)}
              className="border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Habits</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
            </select>
          </div>
        </div>

        <button className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors">
          <Plus className="w-4 h-4" />
          Add Habit
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Habits List */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Target className="w-5 h-5 text-blue-600" />
              Today's Habits ({new Date(selectedDate).toLocaleDateString()})
            </h2>
            
            {filteredHabits.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                <Circle className="w-12 h-12 mx-auto mb-3 text-gray-300" />
                <p>No habits found. Create your first habit to get started!</p>
              </div>
            ) : (
              <div className="space-y-3">
                {filteredHabits.map((habit) => {
                  const isCompleted = getHabitLogStatus(habit.id);
                  const streak = getHabitStreak(habit.id);
                  
                  return (
                    <div key={habit.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                      <div className="flex items-center gap-4">
                        <button
                          onClick={() => toggleHabitCompletion(habit.id, !isCompleted)}
                          className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-colors ${
                            isCompleted 
                              ? 'bg-green-500 border-green-500 text-white' 
                              : 'border-gray-300 hover:border-green-400'
                          }`}
                        >
                          {isCompleted && <CheckCircle className="w-4 h-4" />}
                        </button>
                        
                        <div className="flex items-center gap-3">
                          <span className="text-2xl">{habit.icon || '📝'}</span>
                          <div>
                            <h3 className={`font-medium ${isCompleted ? 'text-gray-500 line-through' : 'text-gray-900'}`}>
                              {habit.title}
                            </h3>
                            <p className="text-sm text-gray-600">{habit.description}</p>
                            <div className="flex items-center gap-4 mt-1">
                              <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                                {habit.periodicity}
                              </span>
                              {habit.frequency > 1 && (
                                <span className="text-xs text-gray-500">
                                  {habit.frequency}x {habit.periodicity === 'weekly' ? 'per week' : habit.periodicity === 'monthly' ? 'per month' : ''}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="text-right">
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <TrendingUp className="w-4 h-4" />
                          <span>{streak} day streak</span>
                        </div>
                        {habit.reminder && (
                          <div className="flex items-center gap-1 text-xs text-orange-600 mt-1">
                            <Clock className="w-3 h-3" />
                            <span>Reminder on</span>
                          </div>
                        )}
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Statistics */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Statistics</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{habits.length}</div>
                <div className="text-sm text-gray-600">Total Habits</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {habits.filter(h => getHabitLogStatus(h.id)).length}
                </div>
                <div className="text-sm text-gray-600">Completed Today</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {habits.length > 0 ? Math.round((habits.filter(h => getHabitLogStatus(h.id)).length / habits.length) * 100) : 0}%
                </div>
                <div className="text-sm text-gray-600">Completion Rate</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {Math.max(...habits.map(h => getHabitStreak(h.id)), 0)}
                </div>
                <div className="text-sm text-gray-600">Best Streak</div>
              </div>
            </div>
          </div>
        </div>

        {/* Calendar */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Calendar className="w-5 h-5 text-blue-600" />
            {monthNames[currentMonth]} {currentYear}
          </h2>
          
          <div className="grid grid-cols-7 gap-1 mb-2">
            {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
              <div key={day} className="text-center text-xs font-medium text-gray-500 p-2">
                {day}
              </div>
            ))}
          </div>
          
          <div className="grid grid-cols-7 gap-1">
            {calendarDays.map((day, index) => {
              if (!day) {
                return <div key={index} className="p-2"></div>;
              }
              
              const dayStr = day.toISOString().split('T')[0];
              const isSelected = dayStr === selectedDate;
              const isToday = dayStr === new Date().toISOString().split('T')[0];
              
              return (
                <button
                  key={index}
                  onClick={() => setSelectedDate(dayStr)}
                  className={`p-2 text-sm rounded-md transition-colors ${
                    isSelected 
                      ? 'bg-blue-600 text-white' 
                      : isToday 
                        ? 'bg-blue-100 text-blue-800 font-medium' 
                        : 'hover:bg-gray-100 text-gray-700'
                  }`}
                >
                  {day.getDate()}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HabitDashboard;