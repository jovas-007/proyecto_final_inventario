from typing import List, Optional
from app.core.entities.categoria import Categoria
from app.core.interfaces.categoria_repository import CategoriaRepositoryInterface


class CategoriaUseCases:

    def __init__(self, repository: CategoriaRepositoryInterface):
        self.repository = repository

    def listar_categorias(self) -> List[Categoria]:
        return self.repository.obtener_todos()

    def obtener_categoria(self, categoria_id: int) -> Optional[Categoria]:
        return self.repository.obtener_por_id(categoria_id)

    def crear_categoria(self, data: dict) -> Categoria:
        nombre = data.get('nombre', '').strip()
        if not nombre or len(nombre) < 3 or len(nombre) > 50:
            raise ValueError('El nombre de la categoría debe tener entre 3 y 50 caracteres')

        descripcion = data.get('descripcion', '').strip()
        if not descripcion or len(descripcion) < 10 or len(descripcion) > 255:
            raise ValueError('La descripción es obligatoria y debe tener entre 10 y 255 caracteres')

        categoria = Categoria(
            nombre=nombre,
            descripcion=descripcion,
        )
        return self.repository.crear(categoria)

    def actualizar_categoria(self, categoria_id: int, data: dict) -> Categoria:
        categoria = self.repository.obtener_por_id(categoria_id)
        if not categoria:
            raise ValueError('Categoría no encontrada')

        if 'nombre' in data:
            nombre = data['nombre'].strip()
            if not nombre or len(nombre) < 3 or len(nombre) > 50:
                raise ValueError('El nombre de la categoría debe tener entre 3 y 50 caracteres')
            categoria.nombre = nombre

        if 'descripcion' in data:
            descripcion = data['descripcion'].strip()
            if not descripcion or len(descripcion) < 10 or len(descripcion) > 255:
                raise ValueError('La descripción es obligatoria y debe tener entre 10 y 255 caracteres')
            categoria.descripcion = descripcion

        return self.repository.actualizar(categoria)

    def eliminar_categoria(self, categoria_id: int) -> bool:
        return self.repository.eliminar(categoria_id)

    def contar_categorias(self) -> int:
        return self.repository.contar_todos()
