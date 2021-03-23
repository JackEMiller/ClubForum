from models import create_app
try:
    import views
except:
    from src import views

app = create_app()
app.register_blueprint(views.app)

if __name__ == "__main__":
    app = create_app()
    app.register_blueprint(views.app)
    app.run(host='0.0.0.0',port=5000,debug=True)


