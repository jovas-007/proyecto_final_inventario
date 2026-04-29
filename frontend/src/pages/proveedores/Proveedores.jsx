import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiPlus, FiEdit2, FiTrash2, FiSearch, FiTruck, FiPhone, FiMail, FiMapPin } from 'react-icons/fi';
import Modal from '../../components/Modal';
import { getProveedores, crearProveedor, actualizarProveedor, eliminarProveedor } from '../../services/api';
import '../dashboard/Dashboard.css';

const emptyForm = {
  nombre: '', contacto: '', telefono: '',
  email: '', direccion: '', activo: true,
};

export default function Proveedores() {
  const [proveedores, setProveedores] = useState([]);
  const [search, setSearch] = useState('');
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [errors, setErrors] = useState({});
  const [editId, setEditId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  async function load() {
    try {
      const res = await getProveedores();
      setProveedores(res.data.data);
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  }

  function validateForm() {
    const newErrors = {};
    if (!form.nombre.trim() || form.nombre.trim().length < 3 || form.nombre.trim().length > 100) {
      newErrors.nombre = 'Obligatorio (3-100 chars)';
    }
    if (!form.contacto.trim() || form.contacto.trim().length < 3 || form.contacto.trim().length > 100) {
      newErrors.contacto = 'Obligatorio (3-100 chars)';
    }
    if (!form.telefono.trim() || !/^\d{10}$/.test(form.telefono.trim())) {
      newErrors.telefono = 'Obligatorio (10 dígitos exactos)';
    }
    if (!form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.trim())) {
      newErrors.email = 'El correo electrónico es obligatorio y debe ser válido';
    }
    if (!form.direccion.trim() || form.direccion.trim().length < 10 || form.direccion.trim().length > 255) {
      newErrors.direccion = 'La dirección es obligatoria (10-255 chars)';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }

  function openCreate() { setForm(emptyForm); setErrors({}); setEditId(null); setModal(true); }

  function openEdit(prov) {
    setForm({
      nombre: prov.nombre, contacto: prov.contacto,
      telefono: prov.telefono, email: prov.email,
      direccion: prov.direccion, activo: prov.activo,
    });
    setErrors({});
    setEditId(prov.id);
    setModal(true);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const payload = {
        ...form,
        nombre: form.nombre.trim(),
        telefono: form.telefono.trim(),
        email: form.email.trim(),
      };
      if (editId) await actualizarProveedor(editId, payload);
      else await crearProveedor(payload);
      setModal(false);
      load();
    } catch (err) { alert(err.response?.data?.error || 'Error al guardar'); }
  }

  async function handleDelete(id) {
    if (!window.confirm('¿Eliminar este proveedor?')) return;
    try { await eliminarProveedor(id); load(); }
    catch { alert('Error al eliminar. Puede tener productos asociados.'); }
  }

  const filtered = proveedores.filter((p) =>
    p.nombre.toLowerCase().includes(search.toLowerCase()) ||
    p.contacto.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <div className="page-loading">Cargando proveedores...</div>;

  return (
    <div className="dashboard">
      <div className="page-header-row">
        <div>
          <h1 className="page-title">Proveedores</h1>
          <p className="page-subtitle">{proveedores.length} proveedores registrados</p>
        </div>
        <button className="btn btn--primary" onClick={openCreate}>
          <FiPlus /> Agregar Proveedor
        </button>
      </div>

      <div className="search-box">
        <FiSearch />
        <input placeholder="Buscar proveedor..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <div className="table-container" style={{ background: 'var(--surface)', borderRadius: 16, border: '1px solid var(--border)' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Proveedor</th>
              <th>Contacto</th>
              <th>Teléfono</th>
              <th>Email</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <AnimatePresence>
              {filtered.map((p) => (
                <motion.tr key={p.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                  <td className="td-name" data-label="Proveedor">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <FiTruck style={{ color: 'var(--success)', flexShrink: 0 }} />
                      {p.nombre}
                    </div>
                  </td>
                  <td data-label="Contacto">{p.contacto || '—'}</td>
                  <td data-label="Teléfono">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                      <FiPhone style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }} />
                      {p.telefono}
                    </div>
                  </td>
                  <td data-label="Email">
                    {p.email ? (
                      <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                        <FiMail style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }} />
                        {p.email}
                      </div>
                    ) : '—'}
                  </td>
                  <td data-label="Estado">
                    <span className={`stock-badge ${p.activo ? '' : 'stock-badge--danger'}`}
                      style={p.activo ? { background: 'rgba(34,197,94,0.1)', color: 'var(--success)' } : {}}>
                      {p.activo ? 'Activo' : 'Inactivo'}
                    </span>
                  </td>
                  <td data-label="Acciones">
                    <div className="actions-cell">
                      <button className="btn btn--ghost btn--icon btn--sm" onClick={() => openEdit(p)}><FiEdit2 /></button>
                      <button className="btn btn--danger btn--icon btn--sm" onClick={() => handleDelete(p.id)}><FiTrash2 /></button>
                    </div>
                  </td>
                </motion.tr>
              ))}
            </AnimatePresence>
          </tbody>
        </table>
        {filtered.length === 0 && <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>No se encontraron proveedores</div>}
      </div>

      <Modal isOpen={modal} onClose={() => setModal(false)} title={editId ? 'Editar Proveedor' : 'Nuevo Proveedor'} width="560px">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Nombre de la Empresa *</label>
            <input 
              className={`form-input ${errors.nombre ? 'error' : ''}`}
              required 
              value={form.nombre} 
              onChange={(e) => setForm({ ...form, nombre: e.target.value })} 
            />
            {errors.nombre && <span className="field-error">{errors.nombre}</span>}
          </div>
          <div className="form-row">
            <div className="form-group">
              <label className="form-label">Persona de Contacto *</label>
              <input 
                className={`form-input ${errors.contacto ? 'error' : ''}`}
                required
                value={form.contacto} 
                onChange={(e) => setForm({ ...form, contacto: e.target.value })} 
              />
              {errors.contacto && <span className="field-error">{errors.contacto}</span>}
            </div>
            <div className="form-group">
              <label className="form-label">Teléfono *</label>
              <input 
                className={`form-input ${errors.telefono ? 'error' : ''}`}
                required 
                value={form.telefono} 
                onChange={(e) => setForm({ ...form, telefono: e.target.value })} 
              />
              {errors.telefono && <span className="field-error">{errors.telefono}</span>}
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Email *</label>
            <input 
              className={`form-input ${errors.email ? 'error' : ''}`}
              type="email" required
              value={form.email} 
              onChange={(e) => setForm({ ...form, email: e.target.value })} 
            />
            {errors.email && <span className="field-error">{errors.email}</span>}
          </div>
          <div className="form-group">
            <label className="form-label">Dirección *</label>
            <textarea 
              className={`form-textarea ${errors.direccion ? 'error' : ''}`}
              required
              value={form.direccion} 
              onChange={(e) => setForm({ ...form, direccion: e.target.value })} 
            />
            {errors.direccion && <span className="field-error">{errors.direccion}</span>}
          </div>
          <div className="form-group">
            <label className="form-label" style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}>
              <input 
                type="checkbox" 
                checked={form.activo} 
                onChange={(e) => setForm({ ...form, activo: e.target.checked })} 
                style={{ width: 16, height: 16, cursor: 'pointer' }}
              />
              Proveedor Activo (puede hacer pedidos)
            </label>
          </div>
          <div className="form-actions">
            <button type="button" className="btn btn--ghost" onClick={() => setModal(false)}>Cancelar</button>
            <button type="submit" className="btn btn--primary">{editId ? 'Guardar' : 'Crear'}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
