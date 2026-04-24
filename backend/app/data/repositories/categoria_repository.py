from typing import List, Optional
from app.data.database import db
from app.data.models.categoria_model import CategoriaModel
from app.core.entities.categoria import Categoria
from app.core.interfaces.categoria_repository import CategoriaRepositoryInterface


class CategoriaRepository(CategoriaRepositoryInterface):

    def obtener_todos(self) -> List[Categoria]:
        modelos = CategoriaModel.query.order_by(CategoriaModel.nombre).all()
        return [m.to_entity() for m in modelos]

    def obtener_por_id(self, categoria_id: int) -> Optional[Categoria]:
        modelo = CategoriaModel.query.get(categoria_id)
        return modelo.to_entity() if modelo else None

    def crear(self, categoria: Categoria) -> Categoria:
        modelo = CategoriaModel.from_entity(categoria)
        db.session.add(modelo)
        db.session.commit()
        return modelo.to_entity()

    def actualizar(self, categoria: Categoria) -> Categoria:
        modelo = CategoriaModel.query.get(categoria.id)
        if not modelo:
            raise ValueError('Categoría no encontrada')

        modelo.nombre = categoria.nombre
        modelo.descripcion = categoria.descripcion

        db.session.commit()
        return modelo.to_entity()

    def eliminar(self, categoria_id: int) -> bool:
        modelo = CategoriaModel.query.get(categoria_id)
        if not modelo:
            return False
        db.session.delete(modelo)
        db.session.commit()
        return True

    def contar_todos(self) -> int:
        return CategoriaModel.query.count()
