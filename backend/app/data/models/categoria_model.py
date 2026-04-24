from app.data.database import db
from app.core.entities.categoria import Categoria


class CategoriaModel(db.Model):
    __tablename__ = 'categorias'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text, default='')

    def to_entity(self) -> Categoria:
        return Categoria(
            id=self.id,
            nombre=self.nombre,
            descripcion=self.descripcion or '',
        )

    @staticmethod
    def from_entity(entity: Categoria) -> 'CategoriaModel':
        return CategoriaModel(
            nombre=entity.nombre,
            descripcion=entity.descripcion,
        )
