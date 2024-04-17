from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import *
from app import db
from app.forms import LoginForm
from datetime import timedelta

def init_app(app):
    @app.route("/", methods=["GET", "POST"])
    def index():
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(Email=form.email.data).first()
            
            if not user:
                flash("Incorrect email, please check!")
                return redirect(url_for("logout"))
            
            elif not check_password_hash(user.Password, form.senha.data):
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
        usuarios = User.query.order_by(User.Id).all()
        return render_template("user/list/user-list.html", usuarios=usuarios)
    
    @app.route("/user/register", methods=["GET", "POST"])
    @login_required
    def register_user():
        if request.method == "POST":
            formEmailValue = request.form["email"]
            formNameValue = request.form["nome"]        
            passwordHash = generate_password_hash(request.form["senha"])
            
            newUser = User(Email=formEmailValue, Name=formNameValue, Password=passwordHash)
            db.session.add(newUser)
            db.session.commit()
            flash("User created successfully!")       
            return redirect(url_for("user_list"))
            
        return render_template("user/form/user-form.html")
    
    @app.route("/update/user/<int:Id>", methods=["GET", "POST"])
    @login_required
    def update_user(Id):
        user = User.query.get_or_404(Id)
        if request.method == "POST":
            user.nome = request.form["nome"]
            user.email = request.form["email"]        
            user.senha = generate_password_hash(request.form["senha"])
            
            db.session.commit()
            flash("User updated successfully!")     
            return redirect(url_for("user_list"))
        return render_template("user/form/user-update-form.html", user=user) 
    
    @app.route("/delete/user/<int:Id>")
    @login_required
    def delete_user(Id):
        userToDelete = User.query.get(Id)
        if userToDelete:
            db.session.delete(userToDelete)
            db.session.commit()
            flash("User deleted successfully!")
        return redirect(url_for("user_list"))
    
    @app.route("/initiative/list")
    @login_required
    def initiative_list():
        iniciativas = Initiative.query.order_by(Initiative.Id).all()
        return render_template("initiative/list/initiative-list.html", iniciativas=iniciativas)
    
    @app.route("/initiative/register", methods=["GET", "POST"])
    @login_required
    def initiative_register():
        if request.method == "POST":
            nome = request.form["nome"]
            nome_gerente_projeto = request.form["nome_gerente_projeto"]
            data_inicio = request.form["data_inicio"]
            data_fim = request.form["data_fim"]
            
            new_initiative = Initiative(Name=nome, ProjectManagerName=nome_gerente_projeto, PlannedStartDate=data_inicio, PlannedEndDate=data_fim)
            db.session.add(new_initiative)
            db.session.commit()
            
            flash("Iniciativa criada com sucesso!")
            return redirect(url_for("initiative_list"))
        
        return render_template("initiative/form/initiative-form.html")
    
    @app.route("/update/initiative/<int:Id>", methods=["GET", "POST"])
    @login_required
    def update_initiative(Id):
        initiative = Initiative.query.get_or_404(Id)
        comments = Comment.query.where(Comment.FK_Initiative_Id == Id).all()
        if request.method == "POST":
            initiative.Name = request.form["nome"]
            initiative.ProjectManagerName = request.form["nome_gerente_projeto"]
            initiative.PlannedStartDate = request.form["data_inicio"]
            initiative.PlannedEndDate = request.form["data_fim"]
            initiative.RealStartDate = request.form["data_inicio_real"]
            initiative.RealEndDate = request.form["data_fim_real"]
            
            db.session.commit()
            flash("Iniciativa atualizada com sucesso!")
            return redirect(url_for("initiative_list"))
        
        return render_template("initiative/form/initiative-update-form.html", initiative=initiative, comments=comments)
   
    @app.route("/delete/initiative/<int:Id>")
    @login_required
    def delete_initiative(Id):
        initativeToDelete = Initiative.query.get(Id)
        if initativeToDelete:
            db.session.delete(initativeToDelete)
            db.session.commit()
            flash("Initiative deleted successfully!")
        return redirect(url_for("initiative_list"))

    @app.route("/comment/register/<int:Id>", methods=["GET", "POST"])
    @login_required
    def comment_register(Id):
        initiative = Initiative.query.get_or_404(Id)
        if request.method == "POST":

            text = request.form["comment"]
            
            new_comment = Comment(Text=text, FK_Initiative_Id=Id, initiative=initiative)
            print(new_comment)
            db.session.add(new_comment)
            db.session.commit()
            
            return redirect(f"/update/initiative/{Id}")
        
        return redirect(f"/update/initiative/{Id}")
    
    @app.route("/delete/comment/<int:Id>")
    @login_required
    def delete_comment(Id):
        commentToDelete = Comment.query.get(Id)
        if commentToDelete:
            db.session.delete(commentToDelete)
            db.session.commit()
            flash("Comment deleted successfully!")
        return redirect(url_for("initiative_list"))
    
    