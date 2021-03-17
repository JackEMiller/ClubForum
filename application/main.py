from flask import Flask
from init_app import db

app = Flask(__name__)
# engine = sqlalchemy.create_engine("mysql+mysqlconnector://pyuser:pydemo@localhost:33060/db",echo=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# session = db.session()
# cursor = session.execute(db).cursor
db.init_app(app)
db.create_all(app=app)

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=8080,debug=True)



