import React from 'react';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-content">
        <a href="#" className="navbar-brand">
          Smart Dataset Generator
        </a>
        <ul className="navbar-links">
          <li><a href="#weather">Weather</a></li>
          <li><a href="#stocks">Stocks</a></li>
          <li><a href="#news">News</a></li>
          <li><a href="#images">Images</a></li>
          <li><a href="#chat">AI Assistant</a></li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
