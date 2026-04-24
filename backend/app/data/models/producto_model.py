from datetime import datetime
from app.data.database import db
from app.core.entities.producto import Producto


class ProductoModel(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text, default='')
    codigo_barras = db.Column(db.String(50), unique=True, nullable=True)
    precio_compra = db.Column(db.Float, default=0.0)
    precio_venta = db.Column(db.Float, nullable=False)
    stock_actual = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=5)
    unidad_medida = db.Column(db.String(30), default='pieza')
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'), nullable=True)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    categoria = db.relationship('CategoriaModel', backref='productos', lazy=True)
    proveedor = db.relationship('ProveedorModel', backref='productos', lazy=True)

    def to_entity(self) -> Producto:
        return Producto(
            id=self.id,
            nombre=self.nombre,
            descripcion=self.descripcion or '',
            codigo_barras=self.codigo_barras or '',
            precio_compra=self.precio_compra or 0.0,
            precio_venta=self.precio_venta,
            stock_actual=self.stock_actual or 0,
            stock_minimo=self.stock_minimo or 5,
            unidad_medida=self.unidad_medida or 'pieza',
            categoria_id=self.categoria_id,
            proveedor_id=self.proveedor_id,
            categoria_nombre=self.categoria.nombre if self.categoria else None,
            proveedor_nombre=self.proveedor.nombre if self.proveedor else None,
            fecha_registro=self.fecha_registro,
            fecha_actualizacion=self.fecha_actualizacion,
            activo=self.activo,
        )

    @staticmethod
    def from_entity(entity: Producto) -> 'ProductoModel':
        return ProductoModel(
            nombre=entity.nombre,
            descripcion=entity.descripcion,
            codigo_barras=entity.codigo_barras or None,
            precio_compra=entity.precio_compra,
            precio_venta=entity.precio_venta,
            stock_actual=entity.stock_actual,
            stock_minimo=entity.stock_minimo,
            unidad_medida=entity.unidad_medida,
            categoria_id=entity.categoria_id,
            proveedor_id=entity.proveedor_id,
            activo=entity.activo,
        )
