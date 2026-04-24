from typing import List, Optional
from app.core.entities.producto import Producto
from app.core.interfaces.producto_repository import ProductoRepositoryInterface


class ProductoUseCases:

    def __init__(self, repository: ProductoRepositoryInterface):
        self.repository = repository

    def listar_productos(self) -> List[Producto]:
        return self.repository.obtener_todos()

    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        return self.repository.obtener_por_id(producto_id)

    def crear_producto(self, data: dict) -> Producto:
        nombre = data.get('nombre', '').strip()
        if not nombre or len(nombre) < 3 or len(nombre) > 100:
            raise ValueError('El nombre del producto debe tener entre 3 y 100 caracteres')
            
        descripcion = data.get('descripcion', '').strip()
        if not descripcion or len(descripcion) < 10 or len(descripcion) > 255:
            raise ValueError('La descripción debe tener entre 10 y 255 caracteres')
            
        codigo_barras = data.get('codigo_barras', '').strip()
        if not codigo_barras or len(codigo_barras) < 8 or len(codigo_barras) > 15:
            raise ValueError('El código de barras es obligatorio y debe tener entre 8 y 15 caracteres')
        
        precio_venta = float(data.get('precio_venta', 0))
        if precio_venta <= 0:
            raise ValueError('El precio de venta debe ser mayor a 0')
            
        precio_compra = float(data.get('precio_compra', -1))
        if precio_compra < 0:
            raise ValueError('El precio de compra es obligatorio y no puede ser negativo')
            
        stock_actual = int(data.get('stock_actual', -1))
        if stock_actual < 0:
            raise ValueError('El stock actual es obligatorio y no puede ser negativo')

        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            codigo_barras=codigo_barras,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock_actual=stock_actual,
            stock_minimo=int(data.get('stock_minimo', 5)),
            unidad_medida=data.get('unidad_medida', 'pieza'),
            categoria_id=data.get('categoria_id'),
            proveedor_id=data.get('proveedor_id'),
            activo=data.get('activo', True),
        )
        return self.repository.crear(producto)

    def actualizar_producto(self, producto_id: int, data: dict) -> Producto:
        producto = self.repository.obtener_por_id(producto_id)
        if not producto:
            raise ValueError('Producto no encontrado')

        if 'nombre' in data:
            nombre = data['nombre'].strip()
            if not nombre or len(nombre) < 3 or len(nombre) > 100:
                raise ValueError('El nombre del producto debe tener entre 3 y 100 caracteres')
            producto.nombre = nombre

        if 'descripcion' in data:
            descripcion = data['descripcion'].strip()
            if not descripcion or len(descripcion) < 10 or len(descripcion) > 255:
                raise ValueError('La descripción debe tener entre 10 y 255 caracteres')
            producto.descripcion = descripcion

        if 'codigo_barras' in data:
            codigo_barras = data['codigo_barras'].strip()
            if not codigo_barras or len(codigo_barras) < 8 or len(codigo_barras) > 15:
                raise ValueError('El código de barras debe tener entre 8 y 15 caracteres')
            producto.codigo_barras = codigo_barras

        if 'precio_venta' in data:
            precio_venta = float(data['precio_venta'])
            if precio_venta <= 0:
                raise ValueError('El precio de venta debe ser mayor a 0')
            producto.precio_venta = precio_venta
            
        if 'precio_compra' in data:
            precio_compra = float(data['precio_compra'])
            if precio_compra < 0:
                raise ValueError('El precio de compra no puede ser negativo')
            producto.precio_compra = precio_compra

        if 'stock_actual' in data:
            stock_actual = int(data['stock_actual'])
            if stock_actual < 0:
                raise ValueError('El stock actual no puede ser negativo')
            producto.stock_actual = stock_actual

        producto.stock_minimo = int(data.get('stock_minimo', producto.stock_minimo))
        producto.unidad_medida = data.get('unidad_medida', producto.unidad_medida)
        producto.categoria_id = data.get('categoria_id', producto.categoria_id)
        producto.proveedor_id = data.get('proveedor_id', producto.proveedor_id)
        producto.activo = data.get('activo', producto.activo)

        return self.repository.actualizar(producto)

    def eliminar_producto(self, producto_id: int) -> bool:
        return self.repository.eliminar(producto_id)

    def obtener_bajo_stock(self) -> List[Producto]:
        return self.repository.obtener_bajo_stock()

    def contar_productos(self) -> int:
        return self.repository.contar_todos()

    def contar_bajo_stock(self) -> int:
        return self.repository.contar_bajo_stock()

    def valor_total_inventario(self) -> float:
        return self.repository.valor_total_inventario()
