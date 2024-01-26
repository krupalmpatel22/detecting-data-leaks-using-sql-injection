import React from 'react';
import '../assets/css/Dashboard.css'; // Import your CSS file
import { Link } from 'react-router-dom'; // Make sure to import Link if using React Router

function Dashboard() {
  return (
    <div className="dashboard-container">
      <nav className="dashboard-navbar">
        <div className="navbar-left">
          <img
            src="/path-to-your-logo.png" // Replace with your company logo path
            alt="Company Logo"
            className="navbar-logo"
          />
        </div>
        <div className="navbar-right">
          <Link to="/" className="nav-link">
            Home
          </Link>
          <Link to="/profile" className="nav-link">
            Profile
          </Link>
          <Link to="/sign-out" className="nav-link">
            Sign-out
          </Link>
        </div>
      </nav>
      <div className="dashboard-content">
        <h2>Welcome to Your Dashboard!</h2>
        {/* Your dashboard content goes here */}
      </div>
    </div>
  );
}

export default Dashboard;
