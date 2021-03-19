try:
    from src.models import create_app
    from src import views
except:
    from models import create_app
    import views

app = create_app()
app.register_blueprint(views.app)

if __name__ == "__main__":
    app = create_app()
    app.register_blueprint(views.app)
    app.run(host='127.0.0.1',port=8080,debug=True)


