from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.entities.proveedor import Proveedor


class ProveedorRepositoryInterface(ABC):

    @abstractmethod
    def obtener_todos(self) -> List[Proveedor]:
        pass

    @abstractmethod
    def obtener_por_id(self, proveedor_id: int) -> Optional[Proveedor]:
        pass

    @abstractmethod
    def crear(self, proveedor: Proveedor) -> Proveedor:
        pass

    @abstractmethod
    def actualizar(self, proveedor: Proveedor) -> Proveedor:
        pass

    @abstractmethod
    def eliminar(self, proveedor_id: int) -> bool:
        pass

    @abstractmethod
    def contar_todos(self) -> int:
        pass
