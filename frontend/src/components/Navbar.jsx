import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import {
  FiGrid, FiPackage, FiLayers, FiTruck,
  FiClipboard, FiBell, FiFileText, FiMenu, FiX
} from 'react-icons/fi';
import './Navbar.css';

const navItems = [
  { to: '/',               icon: <FiGrid />,      label: 'Dashboard'   },
  { to: '/productos',      icon: <FiPackage />,   label: 'Productos'   },
  { to: '/categorias',     icon: <FiLayers />,    label: 'Categorías'  },
  { to: '/proveedores',    icon: <FiTruck />,     label: 'Proveedores' },
  { to: '/inventario',     icon: <FiClipboard />, label: 'Inventario'  },
  { to: '/notificaciones', icon: <FiBell />,      label: 'Alertas'     },
  { to: '/reportes',       icon: <FiFileText />,  label: 'Reportes'    },
];

export default function Navbar() {
  const [collapsed, setCollapsed]   = useState(false);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [isMobile, setIsMobile]     = useState(window.innerWidth <= 900);

  useEffect(() => {
    const handler = () => setIsMobile(window.innerWidth <= 900);
    window.addEventListener('resize', handler);
    return () => window.removeEventListener('resize', handler);
  }, []);

  // Close mobile menu on route change
  const handleLinkClick = () => {
    if (isMobile) setMobileOpen(false);
  };

  const sidebarClass = [
    'sidebar',
    !isMobile && collapsed ? 'collapsed' : '',
    isMobile && mobileOpen ? 'mobile-open' : '',
  ].filter(Boolean).join(' ');

  return (
    <>
      {/* ── Mobile top bar ── */}
      {isMobile && (
        <div className="mobile-topbar">
          <button className="mobile-menu-btn" onClick={() => setMobileOpen(true)}>
            <FiMenu />
          </button>
          <span className="mobile-topbar-logo">StockPro</span>
        </div>
      )}

      {/* ── Backdrop ── */}
      {isMobile && mobileOpen && (
        <div className="mobile-overlay" onClick={() => setMobileOpen(false)} />
      )}

      {/* ── Sidebar ── */}
      <nav className={sidebarClass}>
        <div className="sidebar-header">
          {(!isMobile && !collapsed) || isMobile ? (
            <span className="sidebar-logo">StockPro</span>
          ) : null}
          <button
            className="sidebar-toggle"
            onClick={() => isMobile ? setMobileOpen(false) : setCollapsed(!collapsed)}
          >
            {(isMobile || !collapsed) ? <FiX /> : <FiMenu />}
          </button>
        </div>

        <ul className="sidebar-nav">
          {navItems.map((item) => (
            <li key={item.to}>
              <NavLink
                to={item.to}
                end={item.to === '/'}
                className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
                onClick={handleLinkClick}
              >
                <span className="sidebar-icon">{item.icon}</span>
                {(!collapsed || isMobile) && (
                  <span className="sidebar-label">{item.label}</span>
                )}
              </NavLink>
            </li>
          ))}
        </ul>

        <div className="sidebar-footer">
          {(!collapsed || isMobile) && (
            <span className="sidebar-version">v1.0.0</span>
          )}
        </div>
      </nav>
    </>
  );
}
