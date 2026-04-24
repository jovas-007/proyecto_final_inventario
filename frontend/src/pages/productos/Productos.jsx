import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  FiPlus, FiEdit2, FiTrash2, FiSearch, FiPackage
} from 'react-icons/fi';
import Modal from '../../components/Modal';
import {
  getProductos, crearProducto, actualizarProducto, eliminarProducto,
  getCategorias, getProveedores
} from '../../services/api';
import '../dashboard/Dashboard.css';

const emptyForm = {
  nombre: '', descripcion: '', codigo_barras: '',
  precio_compra: '', precio_venta: '',
  stock_actual: '', stock_minimo: '5',
  unidad_medida: 'pieza',
  categoria_id: '', proveedor_id: '', activo: true,
};

export default function Productos() {
  const [productos, setProductos] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [proveedores, setProveedores] = useState([]);
  const [search, setSearch] = useState('');
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [errors, setErrors] = useState({});
  const [editId, setEditId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { loadAll(); }, []);

  async function loadAll() {
    try {
      const [p, c, prov] = await Promise.all([
        getProductos(), getCategorias(), getProveedores(),
      ]);
      setProductos(p.data.data);
      setCategorias(c.data.data);
      setProveedores(prov.data.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  function validateForm() {
    const newErrors = {};
    if (!form.nombre.trim() || form.nombre.trim().length < 3 || form.nombre.trim().length > 100) {
      newErrors.nombre = 'El nombre es obligatorio (3-100 caracteres)';
    }
    if (!form.descripcion.trim() || form.descripcion.trim().length < 10 || form.descripcion.trim().length > 255) {
      newErrors.descripcion = 'La descripción es obligatoria (10-255 caracteres)';
    }
    if (!form.precio_venta || parseFloat(form.precio_venta) <= 0) {
      newErrors.precio_venta = 'El precio de venta debe ser mayor a 0';
    }
    if (form.precio_compra === '' || parseFloat(form.precio_compra) < 0) {
      newErrors.precio_compra = 'El precio de compra es obligatorio (min 0)';
    }
    if (form.stock_actual === '' || parseInt(form.stock_actual) < 0) {
      newErrors.stock_actual = 'El stock es obligatorio (min 0)';
    }
    if (!form.codigo_barras || !/^\d{8,15}$/.test(form.codigo_barras.trim())) {
      newErrors.codigo_barras = 'El código de barras es obligatorio (8-15 dígitos numéricos)';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }

  function openCreate() {
    setForm(emptyForm);
    setErrors({});
    setEditId(null);
    setModal(true);
  }

  function openEdit(prod) {
    setForm({
      nombre: prod.nombre,
      descripcion: prod.descripcion,
      codigo_barras: prod.codigo_barras,
      precio_compra: prod.precio_compra,
      precio_venta: prod.precio_venta,
      stock_actual: prod.stock_actual,
      stock_minimo: prod.stock_minimo,
      unidad_medida: prod.unidad_medida,
      categoria_id: prod.categoria_id || '',
      proveedor_id: prod.proveedor_id || '',
      activo: prod.activo,
    });
    setErrors({});
    setEditId(prod.id);
    setModal(true);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const payload = {
        ...form,
        nombre: form.nombre.trim(),
        precio_compra: parseFloat(form.precio_compra) || 0,
        precio_venta: parseFloat(form.precio_venta) || 0,
        stock_actual: parseInt(form.stock_actual) || 0,
        stock_minimo: parseInt(form.stock_minimo) || 5,
        categoria_id: form.categoria_id ? parseInt(form.categoria_id) : null,
        proveedor_id: form.proveedor_id ? parseInt(form.proveedor_id) : null,
      };

      if (editId) {
        await actualizarProducto(editId, payload);
      } else {
        await crearProducto(payload);
      }
      setModal(false);
      loadAll();
    } catch (err) {
      alert(err.response?.data?.error || 'Error al guardar');
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('¿Eliminar este producto?')) return;
    try {
      await eliminarProducto(id);
      loadAll();
    } catch (err) {
      alert('Error al eliminar');
    }
  }

  const filtered = productos.filter((p) =>
    p.nombre.toLowerCase().includes(search.toLowerCase()) ||
    (p.codigo_barras && p.codigo_barras.includes(search))
  );

  if (loading) return <div className="page-loading">Cargando productos...</div>;

  return (
    <div className="dashboard">
      <div className="page-header-row">
        <div>
          <h1 className="page-title">Productos</h1>
          <p className="page-subtitle">{productos.length} productos registrados</p>
        </div>
        <button className="btn btn--primary" onClick={openCreate}>
          <FiPlus /> Agregar Producto
        </button>
      </div>

      <div className="search-box">
        <FiSearch />
        <input
          placeholder="Buscar por nombre o código de barras..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="table-container" style={{ background: 'var(--surface)', borderRadius: 16, border: '1px solid var(--border)' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Producto</th>
              <th>Código</th>
              <th>Compra</th>
              <th>Venta</th>
              <th>Stock</th>
              <th>Categoría</th>
              <th>Proveedor</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <AnimatePresence>
              {filtered.map((p) => (
                <motion.tr
                  key={p.id}
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                >
                  <td className="td-name">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <FiPackage style={{ color: 'var(--primary)', flexShrink: 0 }} />
                      {p.nombre}
                    </div>
                  </td>
                  <td style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}>{p.codigo_barras || '—'}</td>
                  <td>${p.precio_compra.toFixed(2)}</td>
                  <td style={{ fontWeight: 600 }}>${p.precio_venta.toFixed(2)}</td>
                  <td>
                    <span className={`stock-badge ${
                      p.stock_actual <= p.stock_minimo
                        ? p.stock_actual === 0 ? 'stock-badge--danger' : 'stock-badge--warning'
                        : ''
                    }`} style={p.stock_actual > p.stock_minimo ? { background: 'rgba(34,197,94,0.1)', color: 'var(--success)' } : {}}>
                      {p.stock_actual}
                    </span>
                  </td>
                  <td>{p.categoria_nombre || '—'}</td>
                  <td>{p.proveedor_nombre || '—'}</td>
                  <td>
                    <div className="actions-cell">
                      <button className="btn btn--ghost btn--icon btn--sm" onClick={() => openEdit(p)} title="Editar">
                        <FiEdit2 />
                      </button>
                      <button className="btn btn--danger btn--icon btn--sm" onClick={() => handleDelete(p.id)} title="Eliminar">
                        <FiTrash2 />
                      </button>
                    </div>
                  </td>
                </motion.tr>
              ))}
            </AnimatePresence>
          </tbody>
        </table>
        {filtered.length === 0 && (
          <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
            No se encontraron productos
          </div>
        )}
      </div>

      {/* ── Modal CRUD ── */}
      <Modal isOpen={modal} onClose={() => setModal(false)} title={editId ? 'Editar Producto' : 'Nuevo Producto'} width="600px">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Nombre *</label>
            <input 
              className={`form-input ${errors.nombre ? 'error' : ''}`}
              required 
              value={form.nombre} 
              onChange={(e) => setForm({ ...form, nombre: e.target.value })} 
            />
            {errors.nombre && <span className="field-error">{errors.nombre}</span>}
          </div>

          <div className="form-group">
            <label className="form-label">Descripción *</label>
            <textarea 
              className={`form-textarea ${errors.descripcion ? 'error' : ''}`}
              required
              value={form.descripcion} 
              onChange={(e) => setForm({ ...form, descripcion: e.target.value })} 
            />
            {errors.descripcion && <span className="field-error">{errors.descripcion}</span>}
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Código de Barras *</label>
              <input 
                className={`form-input ${errors.codigo_barras ? 'error' : ''}`}
                required
                value={form.codigo_barras} 
                onChange={(e) => setForm({ ...form, codigo_barras: e.target.value })} 
              />
              {errors.codigo_barras && <span className="field-error">{errors.codigo_barras}</span>}
            </div>
            <div className="form-group">
              <label className="form-label">Unidad de Medida</label>
              <select className="form-select" value={form.unidad_medida} onChange={(e) => setForm({ ...form, unidad_medida: e.target.value })}>
                <option value="pieza">Pieza</option>
                <option value="kilo">Kilo</option>
                <option value="litro">Litro</option>
                <option value="paquete">Paquete</option>
                <option value="caja">Caja</option>
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Precio Compra *</label>
              <input 
                className={`form-input ${errors.precio_compra ? 'error' : ''}`}
                type="number" step="0.01" min="0" required
                value={form.precio_compra} 
                onChange={(e) => setForm({ ...form, precio_compra: e.target.value })} 
              />
              {errors.precio_compra && <span className="field-error">{errors.precio_compra}</span>}
            </div>
            <div className="form-group">
              <label className="form-label">Precio Venta *</label>
              <input 
                className={`form-input ${errors.precio_venta ? 'error' : ''}`}
                type="number" step="0.01" min="0.01" required 
                value={form.precio_venta} 
                onChange={(e) => setForm({ ...form, precio_venta: e.target.value })} 
              />
              {errors.precio_venta && <span className="field-error">{errors.precio_venta}</span>}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Stock Actual *</label>
              <input 
                className={`form-input ${errors.stock_actual ? 'error' : ''}`}
                type="number" min="0" required
                value={form.stock_actual} 
                onChange={(e) => setForm({ ...form, stock_actual: e.target.value })} 
              />
              {errors.stock_actual && <span className="field-error">{errors.stock_actual}</span>}
            </div>
            <div className="form-group">
              <label className="form-label">Stock Mínimo</label>
              <input className="form-input" type="number" min="0" value={form.stock_minimo} onChange={(e) => setForm({ ...form, stock_minimo: e.target.value })} />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Categoría</label>
              <select className="form-select" value={form.categoria_id} onChange={(e) => setForm({ ...form, categoria_id: e.target.value })}>
                <option value="">Sin categoría</option>
                {categorias.map((c) => <option key={c.id} value={c.id}>{c.nombre}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">Proveedor</label>
              <select className="form-select" value={form.proveedor_id} onChange={(e) => setForm({ ...form, proveedor_id: e.target.value })}>
                <option value="">Sin proveedor</option>
                {proveedores.map((p) => <option key={p.id} value={p.id}>{p.nombre}</option>)}
              </select>
            </div>
          </div>

          <div className="form-actions">
            <button type="button" className="btn btn--ghost" onClick={() => setModal(false)}>Cancelar</button>
            <button type="submit" className="btn btn--primary">{editId ? 'Guardar Cambios' : 'Crear Producto'}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
