from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Producto(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(
        db.String(100),
        nullable=False
    )

    precio = db.Column(
        db.Integer,
        nullable=False
    )


with app.app_context():
    db.create_all()


@app.route("/")
def inicio():

    return {
        "mensaje": "Backend funcionando"
    }


@app.route("/productos", methods=["GET"])
def obtener_productos():

    productos = Producto.query.all()

    lista_productos = []

    for producto in productos:

        lista_productos.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio
        })

    return lista_productos


@app.route("/productos", methods=["POST"])
def crear_producto():

    datos = request.json

    nuevo_producto = Producto(
        nombre=datos["nombre"],
        precio=datos["precio"]
    )

    db.session.add(nuevo_producto)

    db.session.commit()

    return {
        "mensaje": "Producto agregado"
    }

@app.route("/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):

    producto = Producto.query.get(id)

    if not producto:

        return {
            "mensaje": "Producto no encontrado"
        }

    datos = request.json

    producto.nombre = datos["nombre"]
    producto.precio = datos["precio"]

    db.session.commit()

    return {
        "mensaje": "Producto actualizado"
    }

@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):

    producto = Producto.query.get(id)

    if not producto:

        return {
            "mensaje": "Producto no encontrado"
        }

    db.session.delete(producto)

    db.session.commit()

    return {
        "mensaje": "Producto eliminado"
    }

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001
    )