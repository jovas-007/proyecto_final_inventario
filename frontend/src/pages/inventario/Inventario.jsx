import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FiSearch, FiPackage, FiFilter } from 'react-icons/fi';
import { getProductos, getCategorias } from '../../services/api';
import '../dashboard/Dashboard.css';

export default function Inventario() {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [search, setSearch] = useState('');
  const [catFilter, setCatFilter] = useState('');
  const [stockFilter, setStockFilter] = useState('todos');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const [p, c] = await Promise.all([getProductos(), getCategorias()]);
        setProductos(p.data.data);
        setCategorias(c.data.data);
      } catch (err) { console.error(err); }
      finally { setLoading(false); }
    }
    load();
  }, []);

  const filtered = productos.filter((p) => {
    const matchSearch =
      p.nombre.toLowerCase().includes(search.toLowerCase()) ||
      (p.codigo_barras && p.codigo_barras.includes(search));
    const matchCat = !catFilter || p.categoria_id === parseInt(catFilter);
    const matchStock =
      stockFilter === 'todos' ? true :
      stockFilter === 'bajo' ? p.stock_actual <= p.stock_minimo :
      stockFilter === 'normal' ? p.stock_actual > p.stock_minimo :
      true;
    return matchSearch && matchCat && matchStock;
  });

  const totalUnidades = filtered.reduce((s, p) => s + p.stock_actual, 0);
  const totalValor = filtered.reduce((s, p) => s + p.precio_venta * p.stock_actual, 0);

  if (loading) return <div className="page-loading">Cargando inventario...</div>;

  return (
    <div className="dashboard">
      <motion.div className="page-header" initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="page-title">Inventario General</h1>
        <p className="page-subtitle">Vista completa de todos los productos en stock</p>
      </motion.div>

      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 16 }}>
        <div className="search-box" style={{ marginBottom: 0, flex: 1, minWidth: 220 }}>
          <FiSearch />
          <input placeholder="Buscar producto..." value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>

        <div className="search-box" style={{ marginBottom: 0, maxWidth: 200 }}>
          <FiFilter />
          <select
            style={{ background: 'none', border: 'none', color: 'var(--text)', fontSize: '0.88rem', width: '100%', outline: 'none' }}
            value={catFilter}
            onChange={(e) => setCatFilter(e.target.value)}
          >
            <option value="">Todas las categorías</option>
            {categorias.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
          </select>
        </div>

        <div className="search-box" style={{ marginBottom: 0, maxWidth: 180 }}>
          <FiFilter />
          <select
            style={{ background: 'none', border: 'none', color: 'var(--text)', fontSize: '0.88rem', width: '100%', outline: 'none' }}
            value={stockFilter}
            onChange={(e) => setStockFilter(e.target.value)}
          >
            <option value="todos">Todo stock</option>
            <option value="bajo">Bajo stock</option>
            <option value="normal">Stock normal</option>
          </select>
        </div>
      </div>

      {/* Summary bar */}
      <div style={{
        display: 'flex', gap: 24, padding: '12px 20px', background: 'var(--surface)',
        borderRadius: 12, border: '1px solid var(--border)', marginBottom: 16,
        fontSize: '0.85rem', color: 'var(--text-secondary)'
      }}>
        <span>Mostrando <strong style={{ color: 'var(--text)' }}>{filtered.length}</strong> de {productos.length} productos</span>
        <span>Total unidades: <strong style={{ color: 'var(--text)' }}>{totalUnidades.toLocaleString()}</strong></span>
        <span>Valor total: <strong style={{ color: 'var(--primary)' }}>${totalValor.toLocaleString('es-MX', { minimumFractionDigits: 2 })}</strong></span>
      </div>

      <div className="table-container" style={{ background: 'var(--surface)', borderRadius: 16, border: '1px solid var(--border)' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Código</th>
              <th>Categoría</th>
              <th>Proveedor</th>
              <th>P. Compra</th>
              <th>P. Venta</th>
              <th>Stock</th>
              <th>Mínimo</th>
              <th>Unidad</th>
              <th>Valor Total</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((p) => (
              <tr key={p.id}>
                <td className="td-name" data-label="Producto">
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <FiPackage style={{ color: 'var(--primary)', flexShrink: 0 }} />
                    {p.nombre}
                  </div>
                </td>
                <td data-label="Código" style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{p.codigo_barras || '—'}</td>
                <td data-label="Categoría">{p.categoria_nombre || '—'}</td>
                <td data-label="Proveedor">{p.proveedor_nombre || '—'}</td>
                <td data-label="P. Compra">${p.precio_compra.toFixed(2)}</td>
                <td data-label="P. Venta" style={{ fontWeight: 600 }}>${p.precio_venta.toFixed(2)}</td>
                <td data-label="Stock">
                  <span className={`stock-badge ${
                    p.stock_actual <= p.stock_minimo
                      ? p.stock_actual === 0 ? 'stock-badge--danger' : 'stock-badge--warning'
                      : ''
                  }`} style={p.stock_actual > p.stock_minimo ? { background: 'rgba(34,197,94,0.1)', color: 'var(--success)' } : {}}>
                    {p.stock_actual}
                  </span>
                </td>
                <td data-label="Mínimo">{p.stock_minimo}</td>
                <td data-label="Unidad" style={{ textTransform: 'capitalize' }}>{p.unidad_medida}</td>
                <td data-label="Valor Total" style={{ fontWeight: 600 }}>${(p.precio_venta * p.stock_actual).toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && (
          <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
            No se encontraron productos con los filtros seleccionados
          </div>
        )}
      </div>
    </div>
  );
}
