from dataclasses import dataclass
from typing import Optional


@dataclass
class Proveedor:
    id: Optional[int] = None
    nombre: str = ''
    contacto: str = ''
    telefono: str = ''
    email: str = ''
    direccion: str = ''
    activo: bool = True

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'contacto': self.contacto,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'activo': self.activo,
        }
