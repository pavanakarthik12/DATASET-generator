import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <ul className="footer-links">
          <li><a href="#about">About</a></li>
          <li><a href="#docs">Documentation</a></li>
          <li><a href="#api">API</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
        <p>&copy; 2024 Smart Dataset Generator. All rights reserved.</p>
      </div>
    </footer>
  );
};

export default Footer;
