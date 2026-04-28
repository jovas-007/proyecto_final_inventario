"""Modelos SQLAlchemy para lectura de datos (solo lectura, sin escritura)."""

from app import db


class ProductoModel(db.Model):
    __tablename__ = 'productos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    descripcion = db.Column(db.Text)
    codigo_barras = db.Column(db.String(50))
    precio_compra = db.Column(db.Float)
    precio_venta = db.Column(db.Float)
    stock_actual = db.Column(db.Integer)
    stock_minimo = db.Column(db.Integer)
    unidad_medida = db.Column(db.String(30))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    fecha_registro = db.Column(db.DateTime)
    activo = db.Column(db.Boolean)

    categoria = db.relationship('CategoriaModel', backref='productos', lazy=True)
    proveedor = db.relationship('ProveedorModel', backref='productos', lazy=True)


class CategoriaModel(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    descripcion = db.Column(db.Text)


class ProveedorModel(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200))
    contacto = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(150))
    direccion = db.Column(db.Text)
    activo = db.Column(db.Boolean)
