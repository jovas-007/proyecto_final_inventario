import { useState } from 'react';
import { motion } from 'framer-motion';
import {
  FiFileText, FiAlertTriangle, FiLayers, FiTruck,
  FiDownload, FiLoader
} from 'react-icons/fi';
import '../dashboard/Dashboard.css';

const REPORTES_API = import.meta.env.VITE_REPORTES_URL || 'http://127.0.0.1:8081/reportes';

const reportes = [
  {
    id: 'inventario',
    titulo: 'Inventario Completo',
    descripcion: 'Reporte detallado de todos los productos activos con precios, stock y estado.',
    icon: FiFileText,
    color: '#a78bfa',
    bg: 'rgba(167,139,250,0.12)',
    archivo: 'inventario_completo.pdf',
  },
  {
    id: 'stock-bajo',
    titulo: 'Stock Bajo',
    descripcion: 'Productos que necesitan resurtirse con datos de contacto del proveedor.',
    icon: FiAlertTriangle,
    color: '#ef4444',
    bg: 'rgba(239,68,68,0.12)',
    archivo: 'stock_bajo.pdf',
  },
  {
    id: 'categorias',
    titulo: 'Por Categorías',
    descripcion: 'Inventario organizado por categoría con totales y valores por sección.',
    icon: FiLayers,
    color: '#22c55e',
    bg: 'rgba(34,197,94,0.12)',
    archivo: 'reporte_categorias.pdf',
  },
  {
    id: 'proveedores',
    titulo: 'Proveedores',
    descripcion: 'Listado de proveedores con cantidad de productos y valor total asociado.',
    icon: FiTruck,
    color: '#f97316',
    bg: 'rgba(249,115,22,0.12)',
    archivo: 'reporte_proveedores.pdf',
  },
];

export default function Reportes() {
  const [downloading, setDownloading] = useState(null);

  async function handleDownload(reporte) {
    setDownloading(reporte.id);
    try {
      const response = await fetch(`${REPORTES_API}/${reporte.id}`);
      if (!response.ok) throw new Error('Error generando reporte');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = reporte.archivo;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    } catch (err) {
      alert('Error al generar el reporte. Intenta de nuevo.');
      console.error(err);
    } finally {
      setDownloading(null);
    }
  }

  return (
    <div className="dashboard">
      <div className="page-header-row">
        <div>
          <h1 className="page-title">Reportes</h1>
          <p className="page-subtitle">Genera y descarga reportes PDF profesionales</p>
        </div>
      </div>

      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
          gap: 20,
          marginTop: 8,
        }}
      >
        {reportes.map((r, idx) => {
          const Icon = r.icon;
          const isDownloading = downloading === r.id;
          return (
            <motion.div
              key={r.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1 }}
              style={{
                background: 'var(--surface)',
                border: '1px solid var(--border)',
                borderRadius: 16,
                padding: 28,
                display: 'flex',
                flexDirection: 'column',
                gap: 16,
                transition: 'border-color 0.2s, transform 0.2s',
                cursor: 'default',
              }}
              whileHover={{
                borderColor: r.color,
                y: -4,
              }}
            >
              <div
                style={{
                  width: 48,
                  height: 48,
                  borderRadius: 12,
                  background: r.bg,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: r.color,
                  fontSize: 22,
                }}
              >
                <Icon />
              </div>

              <div>
                <h3
                  style={{
                    fontSize: '1.1rem',
                    fontWeight: 700,
                    color: 'var(--text)',
                    margin: '0 0 6px 0',
                  }}
                >
                  {r.titulo}
                </h3>
                <p
                  style={{
                    fontSize: '0.82rem',
                    color: 'var(--text-muted)',
                    margin: 0,
                    lineHeight: 1.5,
                  }}
                >
                  {r.descripcion}
                </p>
              </div>

              <button
                className="btn btn--primary"
                onClick={() => handleDownload(r)}
                disabled={isDownloading}
                style={{
                  marginTop: 'auto',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  gap: 8,
                  background: isDownloading ? 'var(--border)' : undefined,
                }}
              >
                {isDownloading ? (
                  <>
                    <FiLoader className="spin" /> Generando...
                  </>
                ) : (
                  <>
                    <FiDownload /> Descargar PDF
                  </>
                )}
              </button>
            </motion.div>
          );
        })}
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
