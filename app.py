from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Simulación de base de datos de usuarios
usuarios = {}  # { "usuario": "contraseña" }

# Archivo para productos
PRODUCT_FILE = "products.json"
if os.path.exists(PRODUCT_FILE):
    with open(PRODUCT_FILE, "r") as f:
        productos = json.load(f)
else:
    productos = []

# ----- RUTAS -----

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        if usuario in usuarios and usuarios[usuario] == contraseña:
            session['usuario'] = usuario
            return redirect(url_for("productos_view"))
        else:
            flash("Usuario o contraseña incorrectos")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        if usuario in usuarios:
            flash("El usuario ya existe")
            return redirect(url_for("registro"))
        else:
            usuarios[usuario] = contraseña
            flash("Registro exitoso, ahora inicia sesión")
            return redirect(url_for("login"))
    return render_template("registro.html")

@app.route('/productos')
def productos_view():
    if 'usuario' not in session:
        return redirect(url_for("login"))
    return render_template("productos.html", productos=productos, usuario=session['usuario'])

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if 'usuario' not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")
        fecha_elaboracion = request.form.get("fecha_elaboracion")
        fecha_caducidad = request.form.get("fecha_caducidad")
        quien_hizo = request.form.get("quien_hizo")
        imagen = request.form.get("imagen")

        productos.append({
            "nombre": nombre,
            "precio": precio,
            "fecha_elaboracion": fecha_elaboracion,
            "fecha_caducidad": fecha_caducidad,
            "quien_hizo": quien_hizo,
            "imagen": imagen
        })

        with open(PRODUCT_FILE, "w") as f:
            json.dump(productos, f)
        flash("Producto agregado con éxito")
        return redirect(url_for("productos_view"))
    return render_template("agregar.html")

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
