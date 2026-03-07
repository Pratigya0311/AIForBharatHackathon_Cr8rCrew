import React from 'react';
import { NavLink } from 'react-router-dom';

import { Home, FolderOpen, TrendingUp, FileText, Settings, PanelLeftClose, PanelLeftOpen } from 'lucide-react';

const Sidebar = ({ collapsed, onToggleCollapse }) => {
  const menuItems = [
    { path: '/', label: 'Dashboard', icon: Home, end: true },
    { path: '/content', label: 'Content Library', icon: FolderOpen },
    { path: '/trends', label: 'Trending Topics', icon: TrendingUp },
    { path: '/scripts', label: 'My Scripts', icon: FileText },
    { path: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        {!collapsed && <h2>Workspace</h2>}
        <button className="sidebar-toggle" onClick={onToggleCollapse} title={collapsed ? 'Expand' : 'Collapse'}>
          {collapsed ? (
            <PanelLeftOpen size={18} strokeWidth={2} />
          ) : (
            <PanelLeftClose size={18} strokeWidth={2} />
          )}
        </button>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.end}
              className={({ isActive }) => `sidebar-item ${isActive ? 'active' : ''}`}
              title={item.label}
            >
              <Icon className="sidebar-icon" size={20} strokeWidth={2} />
              {!collapsed && <span className="sidebar-label">{item.label}</span>}
            </NavLink>
          );
        })}
      </nav>
    </aside>
  );
};

export default Sidebar;
