

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  // API call function
  const apiCall = async (endpoint, options = {}) => {
    try {
      const baseUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const fullUrl = `${baseUrl}${endpoint}`;

      console.log('Making API call to:', fullUrl);

      const response = await fetch(fullUrl, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        },
        ...options
      });

      const contentType = response.headers.get('content-type');

      if (!response.ok) {
        // Try to get error message from response
        let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

        if (contentType && contentType.includes('application/json')) {
          const errorData = await response.json();
          errorMessage = errorData.detail || errorData.message || errorMessage;
        }

        throw new Error(errorMessage);
      }

      // Check if the response is JSON
      if (contentType && contentType.includes('application/json')) {
        return await response.json();
      }

      return { success: true };
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    try {
      // Basic validation
      if (!email || !password) {
        throw new Error("Please fill in all fields");
      }

      if (!email.includes("@")) {
        throw new Error("Please enter a valid email address");
      }

      if (password.length < 6) {
        throw new Error("Password must be at least 6 characters long");
      }

      // Prepare login data
      const loginData = {
        email: email,
        password: password
      };

      let response;

      if (isSignUp) {
        // Call sign up API
        response = await apiCall('/auth/register', {
          method: 'POST',
          body: JSON.stringify(loginData)
        });
      } else {
        // Call login API
        response = await apiCall('/auth/login', {
          method: 'POST',
          body: JSON.stringify(loginData)
        });
      }

      // Store authentication data
      if (response.access_token) {
        localStorage.setItem("authToken", response.access_token);
        localStorage.setItem("refreshToken", response.refresh_token || "");
      }

      localStorage.setItem("isLoggedIn", "true");
      localStorage.setItem("userEmail", email);
      localStorage.setItem("userName", response.user?.name || email.split("@")[0]);
      localStorage.setItem("userId", response.user?.id || "");

      // Navigate to dashboard
      navigate("/");

    } catch (err) {
      console.error('Login error:', err);

      // Handle specific error cases
      if (err.message.includes('401') || err.message.includes('Unauthorized')) {
        setError("Invalid email or password");
      } else if (err.message.includes('404') || err.message.includes('not found')) {
        setError("Authentication service unavailable. Using demo mode.");
        // Fall back to demo login
        localStorage.setItem("isLoggedIn", "true");
        localStorage.setItem("userEmail", email);
        localStorage.setItem("userName", email.split("@")[0]);
        navigate("/");
      } else if (err.message.includes('Failed to fetch') || err.message.includes('NetworkError')) {
        setError("Cannot connect to server. Using demo mode.");
        // Fall back to demo login
        localStorage.setItem("isLoggedIn", "true");
        localStorage.setItem("userEmail", email);
        localStorage.setItem("userName", email.split("@")[0]);
        navigate("/");
      } else {
        setError(err.message);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const toggleMode = () => {
    setIsSignUp(!isSignUp);
    setError("");
  };

  const clearError = () => {
    if (error) setError("");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#121212] text-white">
      <div className="bg-[#1e1e1e] p-8 rounded-2xl shadow-xl w-96 border border-gray-700">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-emerald-400 mb-2">🎯 Ritualist</h1>
          <h2 className="text-xl font-semibold mb-2">
            {isSignUp ? "Create Account" : "Welcome Back"}
          </h2>
          <p className="text-gray-400 text-sm">
            {isSignUp ? "Start your habit journey" : "Sign in to continue"}
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-900/50 border border-red-500 text-red-300 px-4 py-3 rounded-lg mb-6 text-sm">
            <div className="flex items-center">
              <span className="mr-2">⚠️</span>
              {error}
            </div>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Email Field */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Email Address
            </label>
            <input
              type="email"
              required
              className="w-full px-4 py-3 rounded-lg bg-[#2a2a2a] border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                clearError();
              }}
            />
          </div>

          {/* Password Field */}
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Password
            </label>
            <div className="relative">
              <input
                type={showPassword ? "text" : "password"}
                required
                className="w-full px-4 py-3 rounded-lg bg-[#2a2a2a] border border-gray-600 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all pr-12"
                placeholder={isSignUp ? "Create a password (6+ characters)" : "Enter your password"}
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  clearError();
                }}
              />
              <button
                type="button"
                className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-300"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "👁️" : "👁️‍🗨️"}
              </button>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-emerald-500/50 disabled:cursor-not-allowed text-white font-semibold py-3 rounded-lg transition-all duration-200 transform hover:scale-[1.02] active:scale-[0.98] mt-6"
          >
            {isLoading ? (
              <div className="flex items-center justify-center">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                {isSignUp ? "Creating Account..." : "Signing In..."}
              </div>
            ) : (
              isSignUp ? "Create Account" : "Sign In"
            )}
          </button>
        </form>

        {/* Toggle Mode */}
        <div className="mt-6 text-center">
          <p className="text-gray-400 text-sm">
            {isSignUp ? "Already have an account?" : "Don't have an account?"}
            <button
              type="button"
              onClick={toggleMode}
              className="text-emerald-400 hover:text-emerald-300 font-medium ml-2 transition-colors"
            >
              {isSignUp ? "Sign In" : "Sign Up"}
            </button>
          </p>
        </div>

        {/* Demo Credentials */}
        <div className="mt-6 p-4 bg-gray-800/50 rounded-lg border border-gray-600">
          <p className="text-xs text-gray-400 mb-2">Demo Credentials:</p>
          <div className="text-xs text-gray-300 space-y-1">
            <div>📧 Email: demo@example.com</div>
            <div>🔒 Password: demo123</div>
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center">
          <p className="text-xs text-gray-500">
            Build better habits, one day at a time
          </p>
        </div>
      </div>
    </div>
  );
}