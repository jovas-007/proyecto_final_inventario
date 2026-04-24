from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.producto import Producto


class ProductoRepositoryInterface(ABC):

    @abstractmethod
    def obtener_todos(self) -> List[Producto]:
        pass

    @abstractmethod
    def obtener_por_id(self, producto_id: int) -> Optional[Producto]:
        pass

    @abstractmethod
    def crear(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def actualizar(self, producto: Producto) -> Producto:
        pass

    @abstractmethod
    def eliminar(self, producto_id: int) -> bool:
        pass

    @abstractmethod
    def obtener_bajo_stock(self) -> List[Producto]:
        pass

    @abstractmethod
    def contar_todos(self) -> int:
        pass

    @abstractmethod
    def contar_bajo_stock(self) -> int:
        pass

    @abstractmethod
    def valor_total_inventario(self) -> float:
        pass
