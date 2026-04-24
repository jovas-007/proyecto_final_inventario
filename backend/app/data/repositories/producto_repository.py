from typing import List, Optional
from app.data.database import db
from app.data.models.producto_model import ProductoModel
from app.core.entities.producto import Producto
from app.core.interfaces.producto_repository import ProductoRepositoryInterface


class ProductoRepository(ProductoRepositoryInterface):

    def obtener_todos(self) -> List[Producto]:
        modelos = ProductoModel.query.order_by(ProductoModel.nombre).all()
        return [m.to_entity() for m in modelos]

    def obtener_por_id(self, producto_id: int) -> Optional[Producto]:
        modelo = ProductoModel.query.get(producto_id)
        return modelo.to_entity() if modelo else None

    def crear(self, producto: Producto) -> Producto:
        modelo = ProductoModel.from_entity(producto)
        db.session.add(modelo)
        db.session.commit()
        return modelo.to_entity()

    def actualizar(self, producto: Producto) -> Producto:
        modelo = ProductoModel.query.get(producto.id)
        if not modelo:
            raise ValueError('Producto no encontrado')

        modelo.nombre = producto.nombre
        modelo.descripcion = producto.descripcion
        modelo.codigo_barras = producto.codigo_barras or None
        modelo.precio_compra = producto.precio_compra
        modelo.precio_venta = producto.precio_venta
        modelo.stock_actual = producto.stock_actual
        modelo.stock_minimo = producto.stock_minimo
        modelo.unidad_medida = producto.unidad_medida
        modelo.categoria_id = producto.categoria_id
        modelo.proveedor_id = producto.proveedor_id
        modelo.activo = producto.activo

        db.session.commit()
        return modelo.to_entity()

    def eliminar(self, producto_id: int) -> bool:
        modelo = ProductoModel.query.get(producto_id)
        if not modelo:
            return False
        db.session.delete(modelo)
        db.session.commit()
        return True

    def obtener_bajo_stock(self) -> List[Producto]:
        modelos = ProductoModel.query.filter(
            ProductoModel.stock_actual <= ProductoModel.stock_minimo,
            ProductoModel.activo == True
        ).order_by(ProductoModel.stock_actual).all()
        return [m.to_entity() for m in modelos]

    def contar_todos(self) -> int:
        return ProductoModel.query.filter_by(activo=True).count()

    def contar_bajo_stock(self) -> int:
        return ProductoModel.query.filter(
            ProductoModel.stock_actual <= ProductoModel.stock_minimo,
            ProductoModel.activo == True
        ).count()

    def valor_total_inventario(self) -> float:
        from sqlalchemy import func
        result = db.session.query(
            func.sum(ProductoModel.precio_venta * ProductoModel.stock_actual)
        ).filter(ProductoModel.activo == True).scalar()
        return float(result) if result else 0.0
