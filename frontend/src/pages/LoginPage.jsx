import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // Simulate login
    localStorage.setItem("isLoggedIn", "true");
    navigate("/");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#121212] text-white">
      <form
        onSubmit={handleLogin}
        className="bg-[#1e1e1e] p-8 rounded-2xl shadow-xl w-80"
      >
        <h2 className="text-2xl font-semibold mb-6 text-center">Login</h2>
        <label className="block mb-4">
          <span className="text-sm">Email</span>
          <input
            type="email"
            required
            className="mt-1 w-full px-3 py-2 rounded-md bg-[#2a2a2a] border border-gray-600 text-white"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <label className="block mb-6">
          <span className="text-sm">Password</span>
          <input
            type="password"
            required
            className="mt-1 w-full px-3 py-2 rounded-md bg-[#2a2a2a] border border-gray-600 text-white"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <button
          type="submit"
          className="w-full bg-emerald-500 hover:bg-emerald-600 text-white font-semibold py-2 rounded-md"
        >
          Sign In
        </button>
      </form>
    </div>
  );
}