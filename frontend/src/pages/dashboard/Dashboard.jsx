import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import {
  FiPackage, FiAlertTriangle, FiLayers, FiTruck, FiDollarSign, FiTrendingDown
} from 'react-icons/fi';
import StatsCard from '../../components/StatsCard';
import { getProductosStats, getCategoriasStats, getProveedoresStats, getProductosBajoStock } from '../../services/api';
import './Dashboard.css';

export default function Dashboard() {
  const [stats, setStats] = useState({});
  const [bajoStock, setBajoStock] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  async function loadData() {
    try {
      const [prodStats, catStats, provStats, bajo] = await Promise.all([
        getProductosStats(),
        getCategoriasStats(),
        getProveedoresStats(),
        getProductosBajoStock(),
      ]);
      setStats({
        ...prodStats.data.data,
        ...catStats.data.data,
        ...provStats.data.data,
      });
      setBajoStock(bajo.data.data);
    } catch (err) {
      console.error('Error loading dashboard:', err);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return <div className="page-loading">Cargando dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <motion.div
        className="page-header"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="page-title">Dashboard</h1>
        <p className="page-subtitle">Resumen general de tu inventario</p>
      </motion.div>

      <div className="stats-grid">
        <StatsCard
          icon={<FiPackage />}
          label="Total Productos"
          value={stats.total_productos || 0}
          color="primary"
        />
        <StatsCard
          icon={<FiAlertTriangle />}
          label="Bajo Stock"
          value={stats.bajo_stock || 0}
          color="warning"
        />
        <StatsCard
          icon={<FiLayers />}
          label="Categorías"
          value={stats.total_categorias || 0}
          color="info"
        />
        <StatsCard
          icon={<FiTruck />}
          label="Proveedores"
          value={stats.total_proveedores || 0}
          color="success"
        />
        <StatsCard
          icon={<FiDollarSign />}
          label="Valor del Inventario"
          value={`$${(stats.valor_inventario || 0).toLocaleString('es-MX', {
            minimumFractionDigits: 2,
          })}`}
          color="primary"
          sub="Precio de venta × stock"
        />
      </div>

      {bajoStock.length > 0 && (
        <motion.div
          className="bajo-stock-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="section-header">
            <FiTrendingDown className="section-icon warning-icon" />
            <h2 className="section-title">Productos con Bajo Stock</h2>
            <span className="badge badge--warning">{bajoStock.length}</span>
          </div>

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Categoría</th>
                  <th>Stock Actual</th>
                  <th>Stock Mínimo</th>
                  <th>Proveedor</th>
                </tr>
              </thead>
              <tbody>
                {bajoStock.map((p) => (
                  <tr key={p.id}>
                    <td className="td-name">{p.nombre}</td>
                    <td>{p.categoria_nombre || '—'}</td>
                    <td>
                      <span className={`stock-badge ${p.stock_actual === 0 ? 'stock-badge--danger' : 'stock-badge--warning'}`}>
                        {p.stock_actual}
                      </span>
                    </td>
                    <td>{p.stock_minimo}</td>
                    <td>{p.proveedor_nombre || '—'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </motion.div>
      )}
    </div>
  );
}
