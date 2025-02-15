# backend/main.py
from flask import Flask
from database import db
from router import router

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


app.register_blueprint(router)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
