from flask.wrappers import Request
from my_app import app, bcrypt, db
from flask import render_template, jsonify, redirect, url_for, request
from my_app.models import User, Orders
from my_app.forms import RegistrationForm, LoginForm, OrderForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    error = None
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        if User.get_by_username(form.username.data) is not None or User.get_by_email(form.email.data) is not None:
            error = f"el mail {email} o el usuario {username} ya estan usados"
        else:
            user = User(username=username, email=email, password=password)
            user.save()
            login_user(user, remember=True)
            next = request.args.get("next", None)
            if next:
                return redirect(next)
            return redirect(url_for("index"))
    return render_template("registration.html", form=form, error=error)

@app.route('/log', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.get_by_username(form.username.data)
        if user is not None and user.password == form.password.data:
            login_user(user, remember=True)

            next = request.args.get("next", None)

            if next:
                return redirect(next)
            return redirect(url_for("index"))
    return render_template("login.html", form=form)

@app.route("/users")
@login_required
def usuarios():
    return render_template("lists.html", title="Users List", values=User.query.all())

@app.route("/solicitudes")
@login_required
def solicitudes():
    return render_template("lists.html", title="My Orders List", values=Orders.query.filter_by(user_id=current_user.id).all())

@app.route("/solicitudes_all")
@login_required
def solicitudes_all():
    return render_template("lists.html", title="All Orders List", values=Orders.query.all())

@app.route("/new", methods=["POST", "GET"])
@login_required
def crear_orden():
    form = OrderForm()
    if form.validate_on_submit():
        prod = form.producto.data
        cantidad = form.cantidad.data
        tipo = form.tipo.data
        order = Orders(user_id=current_user.id, producto=prod, cantidad=cantidad, tipo=tipo)
        order.save()
        next = request.args.get("next", None)
        if next:
            return redirect(next)
        return redirect(url_for("index"))
    return render_template("order.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
