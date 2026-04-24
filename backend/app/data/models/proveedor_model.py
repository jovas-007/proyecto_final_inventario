from app.data.database import db
from app.core.entities.proveedor import Proveedor


class ProveedorModel(db.Model):
    __tablename__ = 'proveedores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(200), nullable=False)
    contacto = db.Column(db.String(200), default='')
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), default='')
    direccion = db.Column(db.Text, default='')
    activo = db.Column(db.Boolean, default=True)

    def to_entity(self) -> Proveedor:
        return Proveedor(
            id=self.id,
            nombre=self.nombre,
            contacto=self.contacto or '',
            telefono=self.telefono,
            email=self.email or '',
            direccion=self.direccion or '',
            activo=self.activo,
        )

    @staticmethod
    def from_entity(entity: Proveedor) -> 'ProveedorModel':
        return ProveedorModel(
            nombre=entity.nombre,
            contacto=entity.contacto,
            telefono=entity.telefono,
            email=entity.email,
            direccion=entity.direccion,
            activo=entity.activo,
        )
