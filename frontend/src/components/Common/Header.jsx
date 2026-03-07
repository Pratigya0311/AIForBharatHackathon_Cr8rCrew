import { mockUser } from '../../data/mockData';
import { Sun, Moon, Sparkles } from 'lucide-react';
import { useState, useEffect } from 'react';

const Header = () => {
  const [theme, setTheme] = useState(() => {
    // Initialize from localStorage or default to 'light'
    return localStorage.getItem('theme') || 'light';
  });

  useEffect(() => {
    // Apply theme on mount and when it changes
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  return (
    <header className="app-header">
      <div className="header-content">
        <div className="brand-block">
          <div className="brand-mark" aria-hidden="true">
            <Sparkles className="brand-glyph" size={20} strokeWidth={2.3} />
          </div>
          <div className="brand-text">
            <h1 className="brand-title">CreatorAI TrendScribe</h1>
            <p className="brand-subtitle">Ideas, trends, and scripts in one command center</p>
          </div>
        </div>
        <div className="header-right">
          <button 
            className="theme-toggle" 
            onClick={toggleTheme}
            title={`Switch to ${theme === 'light' ? 'dark' : 'light'} mode`}
          >
            {theme === 'light' ? <Moon size={20} /> : <Sun size={20} />}
          </button>
          <div className="user-info">
            <div className="user-details">
              <span className="user-name">{mockUser.name}</span>
              <span className="user-email">{mockUser.email}</span>
            </div>
            <div className="user-avatar">{mockUser.avatar}</div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
