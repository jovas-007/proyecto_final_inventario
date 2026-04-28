import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8080/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/* ── Productos ── */
export const getProductos = () => api.get('/productos/');
export const getProducto = (id) => api.get(`/productos/${id}`);
export const crearProducto = (data) => api.post('/productos/', data);
export const actualizarProducto = (id, data) => api.put(`/productos/${id}`, data);
export const eliminarProducto = (id) => api.delete(`/productos/${id}`);
export const getProductosBajoStock = () => api.get('/productos/bajo-stock');
export const getProductosStats = () => api.get('/productos/stats');

/* ── Categorías ── */
export const getCategorias = () => api.get('/categorias/');
export const getCategoria = (id) => api.get(`/categorias/${id}`);
export const crearCategoria = (data) => api.post('/categorias/', data);
export const actualizarCategoria = (id, data) => api.put(`/categorias/${id}`, data);
export const eliminarCategoria = (id) => api.delete(`/categorias/${id}`);
export const getCategoriasStats = () => api.get('/categorias/stats');

/* ── Proveedores ── */
export const getProveedores = () => api.get('/proveedores/');
export const getProveedor = (id) => api.get(`/proveedores/${id}`);
export const crearProveedor = (data) => api.post('/proveedores/', data);
export const actualizarProveedor = (id, data) => api.put(`/proveedores/${id}`, data);
export const eliminarProveedor = (id) => api.delete(`/proveedores/${id}`);
export const getProveedoresStats = () => api.get('/proveedores/stats');

/* ── Notificaciones ── */
export const getAlertasActivas = () => api.get('/notificaciones/alertas-activas');

export default api;
