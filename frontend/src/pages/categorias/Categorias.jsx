import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiPlus, FiEdit2, FiTrash2, FiSearch, FiLayers } from 'react-icons/fi';
import Modal from '../../components/Modal';
import { getCategorias, crearCategoria, actualizarCategoria, eliminarCategoria } from '../../services/api';
import '../dashboard/Dashboard.css';

const emptyForm = { nombre: '', descripcion: '' };

export default function Categorias() {
  const [categorias, setCategorias] = useState([]);
  const [search, setSearch] = useState('');
  const [modal, setModal] = useState(false);
  const [form, setForm] = useState(emptyForm);
  const [errors, setErrors] = useState({});
  const [editId, setEditId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => { load(); }, []);

  async function load() {
    try {
      const res = await getCategorias();
      setCategorias(res.data.data);
    } catch (err) { console.error(err); }
    finally { setLoading(false); }
  }

  function validateForm() {
    const newErrors = {};
    if (!form.nombre.trim() || form.nombre.trim().length < 3 || form.nombre.trim().length > 50) {
      newErrors.nombre = 'El nombre es obligatorio (3-50 caracteres)';
    }
    if (!form.descripcion.trim() || form.descripcion.trim().length < 10 || form.descripcion.trim().length > 255) {
      newErrors.descripcion = 'La descripción es obligatoria (10-255 caracteres)';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }

  function openCreate() { setForm(emptyForm); setErrors({}); setEditId(null); setModal(true); }

  function openEdit(cat) {
    setForm({ nombre: cat.nombre, descripcion: cat.descripcion });
    setErrors({});
    setEditId(cat.id);
    setModal(true);
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const payload = {
        nombre: form.nombre.trim(),
        descripcion: form.descripcion.trim(),
      };
      if (editId) await actualizarCategoria(editId, payload);
      else await crearCategoria(payload);
      setModal(false);
      load();
    } catch (err) { alert(err.response?.data?.error || 'Error al guardar'); }
  }

  async function handleDelete(id) {
    if (!window.confirm('¿Eliminar esta categoría?')) return;
    try { await eliminarCategoria(id); load(); }
    catch { alert('Error al eliminar. Puede tener productos asociados.'); }
  }

  const filtered = categorias.filter((c) =>
    c.nombre.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <div className="page-loading">Cargando categorías...</div>;

  return (
    <div className="dashboard">
      <div className="page-header-row">
        <div>
          <h1 className="page-title">Categorías</h1>
          <p className="page-subtitle">{categorias.length} categorías registradas</p>
        </div>
        <button className="btn btn--primary" onClick={openCreate}>
          <FiPlus /> Agregar Categoría
        </button>
      </div>

      <div className="search-box">
        <FiSearch />
        <input placeholder="Buscar categoría..." value={search} onChange={(e) => setSearch(e.target.value)} />
      </div>

      <div className="table-container" style={{ background: 'var(--surface)', borderRadius: 16, border: '1px solid var(--border)' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <AnimatePresence>
              {filtered.map((c) => (
                <motion.tr key={c.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
                  <td style={{ color: 'var(--text-muted)' }}>#{c.id}</td>
                  <td className="td-name">
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <FiLayers style={{ color: 'var(--info)', flexShrink: 0 }} />
                      {c.nombre}
                    </div>
                  </td>
                  <td>{c.descripcion || '—'}</td>
                  <td>
                    <div className="actions-cell">
                      <button className="btn btn--ghost btn--icon btn--sm" onClick={() => openEdit(c)}><FiEdit2 /></button>
                      <button className="btn btn--danger btn--icon btn--sm" onClick={() => handleDelete(c.id)}><FiTrash2 /></button>
                    </div>
                  </td>
                </motion.tr>
              ))}
            </AnimatePresence>
          </tbody>
        </table>
        {filtered.length === 0 && <div style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>No se encontraron categorías</div>}
      </div>

      <Modal isOpen={modal} onClose={() => setModal(false)} title={editId ? 'Editar Categoría' : 'Nueva Categoría'}>
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
          <div className="form-actions">
            <button type="button" className="btn btn--ghost" onClick={() => setModal(false)}>Cancelar</button>
            <button type="submit" className="btn btn--primary">{editId ? 'Guardar' : 'Crear'}</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}
