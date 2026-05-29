import pytest
import json
import sys
import os


sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app import app, db, Producto


@pytest.fixture
def cliente():
    """Configura la app en modo prueba con base de datos en memoria."""
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.create_all()

    with app.test_client() as cliente:
        yield cliente

    with app.app_context():
        db.drop_all()


def test_ruta_raiz(cliente):
    """GET / debe retornar mensaje de bienvenida."""
    respuesta = cliente.get("/")
    datos = json.loads(respuesta.data)

    assert respuesta.status_code == 200
    assert "mensaje" in datos


def test_obtener_productos_vacio(cliente):
    """GET /productos sin datos debe retornar lista vacía."""
    respuesta = cliente.get("/productos")
    datos = json.loads(respuesta.data)

    assert respuesta.status_code == 200
    assert isinstance(datos, list)
    assert len(datos) == 0


def test_crear_producto(cliente):
    """POST /productos debe agregar un nuevo producto."""
    nuevo = {"nombre": "Mango Tommy", "precio": 3500}
    respuesta = cliente.post(
        "/productos",
        data=json.dumps(nuevo),
        content_type="application/json"
    )
    datos = json.loads(respuesta.data)

    assert respuesta.status_code == 200
    assert datos["mensaje"] == "Producto agregado"


def test_obtener_productos_con_datos(cliente):
    """GET /productos debe retornar los productos creados."""


    cliente.post(
        "/productos",
        data=json.dumps({"nombre": "Papaya", "precio": 4000}),
        content_type="application/json"
    )

    respuesta = cliente.get("/productos")
    datos = json.loads(respuesta.data)

    assert respuesta.status_code == 200
    assert len(datos) == 1
    assert datos[0]["nombre"] == "Papaya"
    assert datos[0]["precio"] == 4000


def test_actualizar_producto(cliente):
    """PUT /productos/<id> debe actualizar nombre y precio."""

    cliente.post(
        "/productos",
        data=json.dumps({"nombre": "Piña", "precio": 2000}),
        content_type="application/json"
    )

  
    productos = json.loads(cliente.get("/productos").data)
    producto_id = productos[0]["id"]

    respuesta = cliente.put(
        f"/productos/{producto_id}",
        data=json.dumps({"nombre": "Piña Gold", "precio": 2500}),
        content_type="application/json"
    )
    datos = json.loads(respuesta.data)

    assert respuesta.status_code == 200
    assert datos["mensaje"] == "Producto actualizado"

    # Verificar cambio
    productos_actualizados = json.loads(cliente.get("/productos").data)
    assert productos_actualizados[0]["nombre"] == "Piña Gold"
    assert productos_actualizados[0]["precio"] == 2500


def test_actualizar_producto_no_existente(cliente):
    """PUT /productos/999 debe retornar mensaje de no encontrado."""
    respuesta = cliente.put(
        "/productos/999",
        data=json.dumps({"nombre": "X", "precio": 100}),
        content_type="application/json"
    )
    datos = json.loads(respuesta.data)

    assert respuesta.status_code == 200
    assert datos["mensaje"] == "Producto no encontrado"

def test_eliminar_producto(cliente):
    """DELETE /productos/<id> debe eliminar el producto."""


    cliente.post(
        "/productos",
        data=json.dumps({"nombre": "Guanábana", "precio": 5000}),
        content_type="application/json"
    )

    productos = json.loads(cliente.get("/productos").data)
    producto_id = productos[0]["id"]


    respuesta = cliente.delete(f"/productos/{producto_id}")
    datos = json.loads(respuesta.data)

    assert respuesta.status_code == 200
    assert datos["mensaje"] == "Producto eliminado"


    productos_restantes = json.loads(cliente.get("/productos").data)
    assert len(productos_restantes) == 0


def test_eliminar_producto_no_existente(cliente):
    """DELETE /productos/999 debe retornar mensaje de no encontrado."""
    respuesta = cliente.delete("/productos/999")
    datos = json.loads(respuesta.data)

    assert respuesta.status_code == 200
    assert datos["mensaje"] == "Producto no encontrado"



def test_estructura_producto(cliente):
    """Los productos deben tener id, nombre y precio."""
    cliente.post(
        "/productos",
        data=json.dumps({"nombre": "Lulo", "precio": 3000}),
        content_type="application/json"
    )

    productos = json.loads(cliente.get("/productos").data)
    producto = productos[0]

    assert "id" in producto
    assert "nombre" in producto
    assert "precio" in producto


def test_crear_multiples_productos(cliente):
    """Se deben poder crear varios productos y obtenerlos todos."""
    items = [
        {"nombre": "Maracuyá", "precio": 2800},
        {"nombre": "Tomate de árbol", "precio": 3200},
        {"nombre": "Mora", "precio": 4500},
    ]

    for item in items:
        cliente.post(
            "/productos",
            data=json.dumps(item),
            content_type="application/json"
        )

    productos = json.loads(cliente.get("/productos").data)
    assert len(productos) == 3
