import re
from typing import List, Optional
from app.core.entities.proveedor import Proveedor
from app.core.interfaces.proveedor_repository import ProveedorRepositoryInterface

class ProveedorUseCases:

    def __init__(self, repository: ProveedorRepositoryInterface):
        self.repository = repository

    def listar_proveedores(self) -> List[Proveedor]:
        return self.repository.obtener_todos()

    def obtener_proveedor(self, proveedor_id: int) -> Optional[Proveedor]:
        return self.repository.obtener_por_id(proveedor_id)

    def _validar_datos(self, data: dict):
        nombre = data.get('nombre', '').strip()
        if not nombre or len(nombre) < 3 or len(nombre) > 100:
            raise ValueError('El nombre del proveedor es obligatorio y debe tener entre 3 y 100 caracteres')
            
        contacto = data.get('contacto', '').strip()
        if not contacto or len(contacto) < 3 or len(contacto) > 100:
            raise ValueError('La persona de contacto es obligatoria y debe tener entre 3 y 100 caracteres')
        
        telefono = data.get('telefono', '').strip()
        if not telefono or not re.match(r'^\d{10}$', telefono):
            raise ValueError('El teléfono es obligatorio y debe tener exactamente 10 dígitos numéricos')
            
        email = data.get('email', '').strip()
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValueError('El correo electrónico es obligatorio y debe tener un formato válido')
            
        direccion = data.get('direccion', '').strip()
        if not direccion or len(direccion) < 10 or len(direccion) > 255:
            raise ValueError('La dirección es obligatoria y debe tener entre 10 y 255 caracteres')

    def crear_proveedor(self, data: dict) -> Proveedor:
        self._validar_datos(data)

        proveedor = Proveedor(
            nombre=data['nombre'].strip(),
            contacto=data.get('contacto', '').strip(),
            telefono=data['telefono'].strip(),
            email=data.get('email', '').strip(),
            direccion=data.get('direccion', '').strip(),
            activo=data.get('activo', True),
        )
        return self.repository.crear(proveedor)

    def actualizar_proveedor(self, proveedor_id: int, data: dict) -> Proveedor:
        proveedor = self.repository.obtener_por_id(proveedor_id)
        if not proveedor:
            raise ValueError('Proveedor no encontrado')

        # Si se están actualizando campos de validación, validamos los nuevos valores
        temp_data = {
            'nombre': data.get('nombre', proveedor.nombre),
            'telefono': data.get('telefono', proveedor.telefono),
            'email': data.get('email', proveedor.email)
        }
        self._validar_datos(temp_data)

        proveedor.nombre = data.get('nombre', proveedor.nombre).strip()
        proveedor.contacto = data.get('contacto', proveedor.contacto).strip()
        proveedor.telefono = data.get('telefono', proveedor.telefono).strip()
        proveedor.email = data.get('email', proveedor.email).strip()
        proveedor.direccion = data.get('direccion', proveedor.direccion).strip()
        proveedor.activo = data.get('activo', proveedor.activo)

        return self.repository.actualizar(proveedor)

    def eliminar_proveedor(self, proveedor_id: int) -> bool:
        return self.repository.eliminar(proveedor_id)

    def contar_proveedores(self) -> int:
        return self.repository.contar_todos()
