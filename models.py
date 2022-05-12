from app import db

class Direccion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250))
    direccion = db.Column(db.String(250))

    def __str__(self):
        return (
            f'Id: {self.id}, '
            f'nombre: {self.nombre}, '
            f'direccion: {self.direccion}'
        )

#class NuevaDireccion(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    buscar = db.Column(db.String(250))
#
#    def __str__(self):
#        return (
#            f'id: {self.id}'
#            f'buscar: {self.buscar}'
#        )
