import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://localhost:5001/productos";

function App() {
  const [productos, setProductos] = useState([]);
  const [nombre, setNombre] = useState("");
  const [precio, setPrecio] = useState("");
  const [editando, setEditando] = useState(null);

  const cargarProductos = async () => {
    const res = await fetch(API_URL);
    const data = await res.json();
    setProductos(data);
  };

  useEffect(() => {
    cargarProductos();
  }, []);

  const guardarProducto = async (e) => {
    e.preventDefault();

    const producto = {
      nombre,
      precio: Number(precio),
    };

    if (editando) {
      await fetch(`${API_URL}/${editando}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(producto),
      });
    } else {
      await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(producto),
      });
    }

    setNombre("");
    setPrecio("");
    setEditando(null);
    cargarProductos();
  };

  const eliminarProducto = async (id) => {
    await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });

    cargarProductos();
  };

  const editarProducto = (producto) => {
    setNombre(producto.nombre);
    setPrecio(producto.precio);
    setEditando(producto.id);
  };

  return (
    <div className="contenedor">
      <header className="header">
        <h1>Coquito Amarillo S.A.S.</h1>
        <p>Sistema de gestión de productos</p>
      </header>

      <section className="tarjeta">
        <h2>{editando ? "Editar producto" : "Registrar producto"}</h2>

        <form onSubmit={guardarProducto} className="formulario">
          <input
            type="text"
            placeholder="Nombre del producto"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />

          <input
            type="number"
            placeholder="Precio"
            value={precio}
            onChange={(e) => setPrecio(e.target.value)}
            required
          />

          <button type="submit">
            {editando ? "Actualizar" : "Guardar"}
          </button>
        </form>
      </section>

      <section className="tarjeta">
        <h2>Lista de productos</h2>

        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Producto</th>
              <th>Precio</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            {productos.map((producto) => (
              <tr key={producto.id}>
                <td>{producto.id}</td>
                <td>{producto.nombre}</td>
                <td>${producto.precio}</td>
                <td>
                  <button
                    className="editar"
                    onClick={() => editarProducto(producto)}
                  >
                    Editar
                  </button>

                  <button
                    className="eliminar"
                    onClick={() => eliminarProducto(producto.id)}
                  >
                    Eliminar
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}

export default App;