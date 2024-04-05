import datetime
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import iniciativa, usuario
from app import db
from app.forms import LoginForm
from datetime import timedelta

def init_app(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        form = LoginForm()

        if form.validate_on_submit():
            user = usuario.query.filter_by(email=form.email.data).first()
            
            if not user:
                flash("Incorrect email, please check!")
                return redirect(url_for("logout"))
            
            elif not check_password_hash(user.senha, form.senha.data):
                flash("Incorrect password, please check")
            
            login_user(user, remember=form.remember.data, duration=timedelta(days=7))
            return redirect(url_for("user_list"))

        return render_template("login-form.html", form=form)

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("index")) 
    
    @app.route("/user/list")
    @login_required
    def user_list():
        usuarios = usuario.query.order_by(usuario.id).all()
        return render_template("user/list/user-list.html", usuarios=usuarios)
    
    @app.route("/user/register", methods=["GET", "POST"])
    @login_required
    def register_user():
        if request.method == "POST":
            email = request.form["email"]
            nome = request.form["nome"]        
            senha = generate_password_hash(request.form["senha"])
            
            newUser = usuario(email=email, nome=nome, senha=senha)
            db.session.add(newUser)
            db.session.commit()
            flash("User created successfully!")       
            return redirect(url_for("user_list"))
            
        return render_template("user/form/user-form.html")
    
    @app.route("/update/user/<int:id>", methods=["GET", "POST"])
    @login_required
    def update_user(id):
        user = usuario.query.get_or_404(id)
        if request.method == "POST":
            user.nome = request.form["nome"]
            user.email = request.form["email"]        
            user.senha = generate_password_hash(request.form["senha"])
            
            db.session.commit()
            flash("User updated successfully!")     
            return redirect(url_for("user_list"))
        return render_template("user/form/user-update-form.html", user=user) 
    
    @app.route("/delete/user/<int:id>")
    @login_required
    def delete_user(id):
        userToDelete = usuario.query.get(id)
        if userToDelete:
            db.session.delete(userToDelete)
            db.session.commit()
            flash("User deleted successfully!")
        return redirect(url_for("user_list"))
    
    @app.route("/initiative/list")
    @login_required
    def initiative_list():
        iniciativas = iniciativa.query.order_by(iniciativa.id).all()
        return render_template("initiative/list/initiative-list.html", iniciativas=iniciativas)
    
    @app.route("/intiative/register", methods=["GET", "POST"])
    @login_required
    def initiative_register():
        if request.method == "POST":
            nome = request.form["nome"]
            data_inicio = request.form["data_inicio"]
            data_fim = request.form["data_fim"]
            
            new_iniciativa = iniciativa(nome=nome, data_inicio=data_inicio, data_fim=data_fim)
            db.session.add(new_iniciativa)
            db.session.commit()
            
            flash("Iniciativa created successfully!")
            return redirect(url_for("initiative_list"))
        
        return render_template("initiative/form/initiative-form.html")
    
    @app.route("/update/initiative/<int:id>", methods=["GET", "POST"])
    @login_required
    def update_initiative(id):
        initiative = iniciativa.query.get_or_404(id)
        if request.method == "POST":
            initiative.nome = request.form["nome"]
            initiative.data_inicio = request.form["data_inicio"]
            initiative.data_fim = request.form["data_fim"]
            
            db.session.commit()
            flash("Iniciativa updated successfully!")
            return redirect(url_for("initiative_list"))
        
        return render_template("initiative/form/initiative-update-form.html", initiative=initiative)
   
    @app.route("/delete/initiative/<int:id>")
    @login_required
    def delete_initiative(id):
        initativeToDelete = iniciativa.query.get(id)
        if initativeToDelete:
            db.session.delete(initativeToDelete)
            db.session.commit()
            flash("Iniciativa deleted successfully!")
        return redirect(url_for("initiative_list"))