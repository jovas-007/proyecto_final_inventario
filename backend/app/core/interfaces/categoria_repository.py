from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.categoria import Categoria


class CategoriaRepositoryInterface(ABC):

    @abstractmethod
    def obtener_todos(self) -> List[Categoria]:
        pass

    @abstractmethod
    def obtener_por_id(self, categoria_id: int) -> Optional[Categoria]:
        pass

    @abstractmethod
    def crear(self, categoria: Categoria) -> Categoria:
        pass

    @abstractmethod
    def actualizar(self, categoria: Categoria) -> Categoria:
        pass

    @abstractmethod
    def eliminar(self, categoria_id: int) -> bool:
        pass

    @abstractmethod
    def contar_todos(self) -> int:
        pass
