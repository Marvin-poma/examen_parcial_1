from flask import Flask, render_template, request, session, redirect, make_response

app = Flask(__name__)
app.secret_key = "clave_secreta_123"

usuarios = {
    "carlos": "1111",
    "laura": "2222",
    "diego": "3333"
}

libros = [
    {"titulo": "Python desde cero", "autor": "Juan Pérez", "disponibles": 4},
    {"titulo": "Desarrollo Web", "autor": "María López", "disponibles": 2},
    {"titulo": "Inteligencia Artificial", "autor": "Pedro García", "disponibles": 0}
]


@app.route("/")
def inicio():
    # Leer la cookie
    ultimo = request.cookies.get("ultimo_usuario")
    return render_template("index.html", ultimo_usuario=ultimo)


@app.route("/login", methods=["GET", "POST"])
def login():
    mensaje = ""
    if request.method == "POST":
        usuario = request.form["usuario"]
        password = request.form["password"]

        if usuario in usuarios and usuarios[usuario] == password:
            session["usuario"] = usuario
            # Guardar cookie con el último usuario
            respuesta = make_response(redirect("/libros"))
            respuesta.set_cookie("ultimo_usuario", usuario)
            return respuesta
        else:
            mensaje = "Usuario o contraseña incorrectos."

    return render_template("login.html", mensaje=mensaje)


@app.route("/libros")
def ver_libros():
    return render_template("libros.html", libros=libros, usuario=session.get("usuario"))


@app.route("/perfil")
def perfil():
    if "usuario" not in session:
        return redirect("/login")
    return render_template("perfil.html", usuario=session["usuario"])


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/?mensaje=adios")


@app.route("/borrar_cookie")
def borrar_cookie():
    respuesta = make_response(redirect("/"))
    respuesta.delete_cookie("ultimo_usuario")
    return respuesta


if __name__ == "__main__":
    app.run(debug=True)