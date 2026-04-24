"""
Script para poblar la base de datos con datos de prueba.
Ejecutar: python init_db.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from run import create_app
from app.data.database import db
from app.data.models.categoria_model import CategoriaModel
from app.data.models.proveedor_model import ProveedorModel
from app.data.models.producto_model import ProductoModel


def seed():
    app = create_app()

    with app.app_context():
        print("Insertando datos de prueba...")

        # ── Categorías ──
        categorias_data = [
            ('Bebidas', 'Refrescos, jugos, agua, bebidas energéticas'),
            ('Botanas', 'Papas, cacahuates, chicharrones, dulces'),
            ('Lácteos', 'Leche, yogurt, queso, crema'),
            ('Panadería', 'Pan de caja, pan dulce, tortillas'),
            ('Abarrotes', 'Arroz, frijol, aceite, enlatados'),
            ('Higiene Personal', 'Jabón, shampoo, pasta dental, desodorante'),
            ('Limpieza', 'Detergente, cloro, escobas, trapeadores'),
            ('Farmacia', 'Medicamentos básicos, curitas, alcohol'),
            ('Congelados', 'Helados, pizzas congeladas, hielo'),
            ('Cigarros y Tabaco', 'Cigarros, encendedores'),
        ]

        categorias = {}
        for nombre, desc in categorias_data:
            existing = CategoriaModel.query.filter_by(nombre=nombre).first()
            if not existing:
                cat = CategoriaModel(nombre=nombre, descripcion=desc)
                db.session.add(cat)
                db.session.flush()
                categorias[nombre] = cat.id
            else:
                categorias[nombre] = existing.id

        # ── Proveedores ──
        proveedores_data = [
            ('Coca-Cola FEMSA', 'Juan Pérez', '3312345678', 'ventas@cocacola.mx', 'Av. Industria 100, Guadalajara'),
            ('Bimbo', 'María López', '5598765432', 'distribución@bimbo.mx', 'Calle Pan 50, CDMX'),
            ('Sabritas PepsiCo', 'Carlos García', '8187654321', 'pedidos@sabritas.mx', 'Blvd. Snacks 200, Monterrey'),
            ('Lala', 'Ana Martínez', '3345678901', 'ventas@lala.mx', 'Av. Lácteos 75, Torreón'),
            ('La Costeña', 'Roberto Sánchez', '5523456789', 'ventas@lacostena.mx', 'Calle Conserva 30, Ecatepec'),
            ('Procter & Gamble', 'Laura Díaz', '5534567890', 'dist@pg.mx', 'Av. Limpieza 400, CDMX'),
        ]

        proveedores = {}
        for nombre, contacto, tel, email, dir_ in proveedores_data:
            existing = ProveedorModel.query.filter_by(nombre=nombre).first()
            if not existing:
                prov = ProveedorModel(
                    nombre=nombre, contacto=contacto,
                    telefono=tel, email=email, direccion=dir_
                )
                db.session.add(prov)
                db.session.flush()
                proveedores[nombre] = prov.id
            else:
                proveedores[nombre] = existing.id

        # ── Productos ──
        productos_data = [
            ('Coca-Cola 600ml', 'Refresco de cola 600ml', '7501055300120', 12.0, 18.0, 48, 10, 'pieza', 'Bebidas', 'Coca-Cola FEMSA'),
            ('Pepsi 600ml', 'Refresco Pepsi 600ml', '7501031310227', 11.0, 17.0, 36, 10, 'pieza', 'Bebidas', 'Sabritas PepsiCo'),
            ('Agua Ciel 1L', 'Agua purificada 1 litro', '7501055301028', 8.0, 14.0, 60, 15, 'pieza', 'Bebidas', 'Coca-Cola FEMSA'),
            ('Sabritas Original 45g', 'Papas fritas originales', '7501011143067', 10.0, 16.0, 30, 8, 'pieza', 'Botanas', 'Sabritas PepsiCo'),
            ('Doritos Nacho 62g', 'Frituras sabor nacho', '7501011115200', 12.0, 19.0, 25, 8, 'pieza', 'Botanas', 'Sabritas PepsiCo'),
            ('Leche Lala 1L', 'Leche entera 1 litro', '7501055363100', 22.0, 28.0, 20, 10, 'pieza', 'Lácteos', 'Lala'),
            ('Yogurt Lala 250g', 'Yogurt natural 250g', '7501055363200', 10.0, 15.0, 15, 5, 'pieza', 'Lácteos', 'Lala'),
            ('Pan Bimbo Blanco', 'Pan blanco grande 680g', '7441029500189', 38.0, 52.0, 12, 5, 'pieza', 'Panadería', 'Bimbo'),
            ('Tortillas de Maíz 1kg', 'Tortillas de maíz paquete', '0000000000001', 18.0, 25.0, 8, 5, 'kilo', 'Panadería', 'Bimbo'),
            ('Arroz SOS 1kg', 'Arroz blanco 1 kilo', '7501055305101', 20.0, 32.0, 18, 5, 'kilo', 'Abarrotes', 'La Costeña'),
            ('Frijol La Costeña 560g', 'Frijoles negros enteros', '7501017003051', 18.0, 26.0, 22, 8, 'pieza', 'Abarrotes', 'La Costeña'),
            ('Aceite 123 1L', 'Aceite vegetal comestible', '7501055310600', 32.0, 45.0, 10, 3, 'pieza', 'Abarrotes', 'La Costeña'),
            ('Jabón Zote 400g', 'Jabón de lavandería', '7501003130105', 15.0, 22.0, 14, 5, 'pieza', 'Limpieza', 'Procter & Gamble'),
            ('Shampoo Head & Shoulders 200ml', 'Shampoo anticaspa', '7500435019514', 52.0, 72.0, 6, 3, 'pieza', 'Higiene Personal', 'Procter & Gamble'),
            ('Pasta Colgate 100ml', 'Pasta dental fluorada', '7891024132104', 28.0, 38.0, 10, 4, 'pieza', 'Higiene Personal', 'Procter & Gamble'),
            ('Helado Holanda 1L', 'Helado de vainilla 1L', '7501055390001', 45.0, 65.0, 5, 3, 'pieza', 'Congelados', 'Lala'),
            ('Gansito Marinela', 'Pastelito relleno', '7441029520187', 8.0, 14.0, 40, 10, 'pieza', 'Botanas', 'Bimbo'),
            ('Cloro Cloralex 1L', 'Blanqueador', '7501025403010', 18.0, 28.0, 7, 3, 'pieza', 'Limpieza', 'Procter & Gamble'),
            ('Red Bull 250ml', 'Bebida energética', '9002490100070', 25.0, 35.0, 12, 5, 'pieza', 'Bebidas', 'Coca-Cola FEMSA'),
            ('Atún Dolores 140g', 'Atún en agua', '7501056360108', 16.0, 24.0, 15, 5, 'pieza', 'Abarrotes', 'La Costeña'),
        ]

        for (nombre, desc, barras, pc, pv, stock, smin, unidad, cat_name, prov_name) in productos_data:
            existing = ProductoModel.query.filter_by(codigo_barras=barras).first()
            if not existing:
                prod = ProductoModel(
                    nombre=nombre, descripcion=desc, codigo_barras=barras,
                    precio_compra=pc, precio_venta=pv,
                    stock_actual=stock, stock_minimo=smin,
                    unidad_medida=unidad,
                    categoria_id=categorias.get(cat_name),
                    proveedor_id=proveedores.get(prov_name),
                )
                db.session.add(prod)

        db.session.commit()
        print("✓ Datos de prueba insertados correctamente")
        print(f"  - {len(categorias_data)} categorías")
        print(f"  - {len(proveedores_data)} proveedores")
        print(f"  - {len(productos_data)} productos")


if __name__ == '__main__':
    seed()
