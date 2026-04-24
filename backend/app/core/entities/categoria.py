from dataclasses import dataclass
from typing import Optional


@dataclass
class Categoria:
    id: Optional[int] = None
    nombre: str = ''
    descripcion: str = ''

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
        }
