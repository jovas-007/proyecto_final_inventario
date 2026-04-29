import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FiBell, FiAlertTriangle, FiAlertOctagon, FiPackage,
  FiRefreshCw, FiTruck
} from 'react-icons/fi';
import { getAlertasActivas } from '../../services/api';
import '../dashboard/Dashboard.css';

const severidadConfig = {
  agotado: {
    label: 'AGOTADO',
    color: '#ef4444',
    bg: 'rgba(239,68,68,0.1)',
    icon: FiAlertOctagon,
  },
  critico: {
    label: 'CRÍTICO',
    color: '#f97316',
    bg: 'rgba(249,115,22,0.1)',
    icon: FiAlertTriangle,
  },
  bajo: {
    label: 'BAJO',
    color: '#eab308',
    bg: 'rgba(234,179,8,0.1)',
    icon: FiAlertTriangle,
  },
};

export default function Notificaciones() {
  const [alertas, setAlertas] = useState([]);
  const [resumen, setResumen] = useState({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => { loadAlertas(); }, []);

  async function loadAlertas() {
    try {
      const res = await getAlertasActivas();
      setAlertas(res.data.data);
      setResumen(res.data.resumen);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }

  function handleRefresh() {
    setRefreshing(true);
    loadAlertas();
  }

  if (loading) return <div className="page-loading">Cargando alertas...</div>;

  return (
    <div className="dashboard">
      <div className="page-header-row">
        <div>
          <h1 className="page-title">Notificaciones</h1>
          <p className="page-subtitle">
            {resumen.total_alertas || 0} alertas activas de stock bajo
          </p>
        </div>
        <button
          className="btn btn--primary"
          onClick={handleRefresh}
          disabled={refreshing}
          style={{ display: 'flex', alignItems: 'center', gap: 6 }}
        >
          <FiRefreshCw className={refreshing ? 'spin' : ''} />
          Actualizar
        </button>
      </div>

      {/* ── Tarjetas Resumen ── */}
      <div className="stats-grid" style={{ marginBottom: 28 }}>
        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0 }}
          style={{ borderLeft: '4px solid #ef4444' }}
        >
          <div className="stat-icon" style={{ background: 'rgba(239,68,68,0.15)', color: '#ef4444' }}>
            <FiAlertOctagon />
          </div>
          <div className="stat-info">
            <span className="stat-value">{resumen.agotados || 0}</span>
            <span className="stat-label">Agotados</span>
          </div>
        </motion.div>

        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          style={{ borderLeft: '4px solid #f97316' }}
        >
          <div className="stat-icon" style={{ background: 'rgba(249,115,22,0.15)', color: '#f97316' }}>
            <FiAlertTriangle />
          </div>
          <div className="stat-info">
            <span className="stat-value">{resumen.criticos || 0}</span>
            <span className="stat-label">Críticos</span>
          </div>
        </motion.div>

        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          style={{ borderLeft: '4px solid #eab308' }}
        >
          <div className="stat-icon" style={{ background: 'rgba(234,179,8,0.15)', color: '#eab308' }}>
            <FiBell />
          </div>
          <div className="stat-info">
            <span className="stat-value">{resumen.bajos || 0}</span>
            <span className="stat-label">Stock Bajo</span>
          </div>
        </motion.div>

        <motion.div
          className="stat-card"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          style={{ borderLeft: '4px solid #a78bfa' }}
        >
          <div className="stat-icon" style={{ background: 'rgba(167,139,250,0.15)', color: '#a78bfa' }}>
            <FiPackage />
          </div>
          <div className="stat-info">
            <span className="stat-value">{resumen.total_alertas || 0}</span>
            <span className="stat-label">Total Alertas</span>
          </div>
        </motion.div>
      </div>

      {/* ── Tabla de Alertas ── */}
      <div
        className="table-container"
        style={{
          background: 'var(--surface)',
          borderRadius: 16,
          border: '1px solid var(--border)',
        }}
      >
        <table className="data-table">
          <thead>
            <tr>
              <th>Severidad</th>
              <th>Producto</th>
              <th>Stock Actual</th>
              <th>Stock Mínimo</th>
              <th>Precio</th>
              <th>Proveedor</th>
            </tr>
          </thead>
          <tbody>
            <AnimatePresence>
              {alertas.map((a) => {
                const config = severidadConfig[a.severidad] || severidadConfig.bajo;
                const Icon = config.icon;
                return (
                  <motion.tr
                    key={a.id}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                  >
                    <td data-label="Severidad">
                      <span
                        className="stock-badge"
                        style={{
                          background: config.bg,
                          color: config.color,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: 4,
                          fontWeight: 700,
                          fontSize: '0.75rem',
                        }}
                      >
                        <Icon size={13} />
                        {config.label}
                      </span>
                    </td>
                    <td className="td-name" data-label="Producto">
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        <FiPackage style={{ color: 'var(--primary)', flexShrink: 0 }} />
                        <div>
                          <div>{a.nombre}</div>
                          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
                            {a.codigo_barras || '—'}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td data-label="Stock Actual">
                      <span
                        style={{
                          fontSize: '1.2rem',
                          fontWeight: 800,
                          color: config.color,
                        }}
                      >
                        {a.stock_actual}
                      </span>
                    </td>
                    <td data-label="Stock Mínimo" style={{ color: 'var(--text-muted)' }}>{a.stock_minimo}</td>
                    <td data-label="Precio" style={{ fontWeight: 600 }}>${a.precio_venta?.toFixed(2)}</td>
                    <td data-label="Proveedor">
                      <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                        <FiTruck style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }} />
                        {a.proveedor_nombre || '—'}
                      </div>
                    </td>
                  </motion.tr>
                );
              })}
            </AnimatePresence>
          </tbody>
        </table>
        {alertas.length === 0 && (
          <div
            style={{
              textAlign: 'center',
              padding: 60,
              color: 'var(--text-muted)',
            }}
          >
            <FiBell size={40} style={{ marginBottom: 12, opacity: 0.3 }} />
            <div style={{ fontSize: '1.1rem', fontWeight: 500 }}>Todo en orden</div>
            <div style={{ fontSize: '0.85rem', marginTop: 4 }}>
              No hay productos con stock bajo en este momento
            </div>
          </div>
        )}
      </div>

      <style>{`
        .spin {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
