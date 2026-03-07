import { useState } from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import './styles/globals.css';
import Header from './components/Common/Header';
import Sidebar from './components/Common/Sidebar';
import ErrorBoundary from './components/Common/ErrorBoundary';

// Pages
import Dashboard from './pages/index';
import ContentPage from './pages/content';
import TrendsPage from './pages/trends';
import ScriptsPage from './pages/scripts';
import SettingsPage from './pages/settings';

export default function App() {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  return (
    <ErrorBoundary>
      <div className="app">
        <Header />
        <div className="app-container">
          <Sidebar 
            collapsed={sidebarCollapsed}
            onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
          />
          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/content" element={<ContentPage />} />
              <Route path="/trends" element={<TrendsPage />} />
              <Route path="/scripts" element={<ScriptsPage />} />
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      </div>
    </ErrorBoundary>
  );
}
