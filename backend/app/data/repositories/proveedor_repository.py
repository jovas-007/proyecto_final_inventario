from typing import List, Optional
from app.data.database import db
from app.data.models.proveedor_model import ProveedorModel
from app.core.entities.proveedor import Proveedor
from app.core.interfaces.proveedor_repository import ProveedorRepositoryInterface


class ProveedorRepository(ProveedorRepositoryInterface):

    def obtener_todos(self) -> List[Proveedor]:
        modelos = ProveedorModel.query.order_by(ProveedorModel.nombre).all()
        return [m.to_entity() for m in modelos]

    def obtener_por_id(self, proveedor_id: int) -> Optional[Proveedor]:
        modelo = ProveedorModel.query.get(proveedor_id)
        return modelo.to_entity() if modelo else None

    def crear(self, proveedor: Proveedor) -> Proveedor:
        modelo = ProveedorModel.from_entity(proveedor)
        db.session.add(modelo)
        db.session.commit()
        return modelo.to_entity()

    def actualizar(self, proveedor: Proveedor) -> Proveedor:
        modelo = ProveedorModel.query.get(proveedor.id)
        if not modelo:
            raise ValueError('Proveedor no encontrado')

        modelo.nombre = proveedor.nombre
        modelo.contacto = proveedor.contacto
        modelo.telefono = proveedor.telefono
        modelo.email = proveedor.email
        modelo.direccion = proveedor.direccion
        modelo.activo = proveedor.activo

        db.session.commit()
        return modelo.to_entity()

    def eliminar(self, proveedor_id: int) -> bool:
        modelo = ProveedorModel.query.get(proveedor_id)
        if not modelo:
            return False
        db.session.delete(modelo)
        db.session.commit()
        return True

    def contar_todos(self) -> int:
        return ProveedorModel.query.filter_by(activo=True).count()
