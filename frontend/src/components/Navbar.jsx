import { NavLink } from 'react-router-dom';
import {
  FiGrid, FiPackage, FiLayers, FiTruck,
  FiClipboard, FiMenu, FiX
} from 'react-icons/fi';
import { useState } from 'react';
import './Navbar.css';

const navItems = [
  { to: '/', icon: <FiGrid />, label: 'Dashboard' },
  { to: '/productos', icon: <FiPackage />, label: 'Productos' },
  { to: '/categorias', icon: <FiLayers />, label: 'Categorías' },
  { to: '/proveedores', icon: <FiTruck />, label: 'Proveedores' },
  { to: '/inventario', icon: <FiClipboard />, label: 'Inventario' },
];

export default function Navbar() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <nav className={`sidebar ${collapsed ? 'collapsed' : ''}`}>
      <div className="sidebar-header">
        {!collapsed && <span className="sidebar-logo">StockPro</span>}
        <button className="sidebar-toggle" onClick={() => setCollapsed(!collapsed)}>
          {collapsed ? <FiMenu /> : <FiX />}
        </button>
      </div>

      <ul className="sidebar-nav">
        {navItems.map((item) => (
          <li key={item.to}>
            <NavLink
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
            >
              <span className="sidebar-icon">{item.icon}</span>
              {!collapsed && <span className="sidebar-label">{item.label}</span>}
            </NavLink>
          </li>
        ))}
      </ul>

      <div className="sidebar-footer">
        {!collapsed && <span className="sidebar-version">v1.0.0</span>}
      </div>
    </nav>
  );
}
