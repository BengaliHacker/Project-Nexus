from flask import Flask, render_template
from werkzeug.security import generate_password_hash


def create_app():
    app = Flask(__name__, template_folder="website/templates")

    from website.models import db, User

    from website.blueprints.auth import auth_bp
    from website.blueprints.admin import admin_bp
    from website.blueprints.teacher import teacher_bp
    from website.blueprints.student import student_bp
    from website.blueprints.faculty import faculty_bp

    # Configuration
    app.config["SECRET_KEY"] = "your-secret-key-change-this"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///website.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize Databse
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(teacher_bp, url_prefix="/teacher")
    app.register_blueprint(faculty_bp, url_prefix="/faculty")
    app.register_blueprint(student_bp, url_prefix="/student")

    # Create Tables
    with app.app_context():
        db.create_all()

        admin_user = User.query.filter_by(username="admin").first()
        if not admin_user:
            hashed_password = generate_password_hash("admin123")
            admin_user = User(
                username="admin",
                email="admin@teamnexus.com",
                password=hashed_password,
                role="admin",
            )
            db.session.add(admin_user)
            db.session.commit()
            print("Default Admin User Created : admin : admin123")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
