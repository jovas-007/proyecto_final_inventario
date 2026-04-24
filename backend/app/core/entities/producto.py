from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Producto:
    id: Optional[int] = None
    nombre: str = ''
    descripcion: str = ''
    codigo_barras: str = ''
    precio_compra: float = 0.0
    precio_venta: float = 0.0
    stock_actual: int = 0
    stock_minimo: int = 5
    unidad_medida: str = 'pieza'
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    activo: bool = True

    # Relaciones (para serialización)
    categoria_nombre: Optional[str] = None
    proveedor_nombre: Optional[str] = None

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'codigo_barras': self.codigo_barras,
            'precio_compra': self.precio_compra,
            'precio_venta': self.precio_venta,
            'stock_actual': self.stock_actual,
            'stock_minimo': self.stock_minimo,
            'unidad_medida': self.unidad_medida,
            'categoria_id': self.categoria_id,
            'proveedor_id': self.proveedor_id,
            'categoria_nombre': self.categoria_nombre,
            'proveedor_nombre': self.proveedor_nombre,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None,
            'activo': self.activo,
        }

    @property
    def stock_bajo(self) -> bool:
        return self.stock_actual <= self.stock_minimo

    @property
    def ganancia(self) -> float:
        return self.precio_venta - self.precio_compra
