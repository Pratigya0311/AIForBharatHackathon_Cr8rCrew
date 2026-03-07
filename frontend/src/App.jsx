import { useState } from 'react';
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
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'content':
        return <ContentPage />;
      case 'trends':
        return <TrendsPage />;
      case 'scripts':
        return <ScriptsPage />;
      case 'settings':
        return <SettingsPage />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <ErrorBoundary>
      <div className="app">
        <Header />
        <div className="app-container">
          <Sidebar 
            currentPage={currentPage} 
            onNavigate={setCurrentPage}
            collapsed={sidebarCollapsed}
            onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
          />
          <main className="main-content">
            {renderPage()}
          </main>
        </div>
      </div>
    </ErrorBoundary>
  );
}