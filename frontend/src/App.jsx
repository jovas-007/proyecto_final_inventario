import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/dashboard/Dashboard';
import Productos from './pages/productos/Productos';
import Categorias from './pages/categorias/Categorias';
import Proveedores from './pages/proveedores/Proveedores';
import Inventario from './pages/inventario/Inventario';
import Notificaciones from './pages/notificaciones/Notificaciones';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/productos" element={<Productos />} />
          <Route path="/categorias" element={<Categorias />} />
          <Route path="/proveedores" element={<Proveedores />} />
          <Route path="/inventario" element={<Inventario />} />
          <Route path="/notificaciones" element={<Notificaciones />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
