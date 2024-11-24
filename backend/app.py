from flask import Flask, render_template, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app= Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db = SQLAlchemy(app)

CORS(app, resources={r"/*":{'origins': "*"}})
CORS(app, resources={r"/*":{'origins': 'http://localhost:8080',"allow_headers":"Access-Control-Allow-Origin"}})


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    ambient_temp = db.Column(db.String(200), nullable=True)
    weather_conditions = db.Column(db.String(200), nullable=True)
    track_conditions = db.Column(db.String(200), nullable=True)
    setup_sheet = db.Text()

    def __repr__(self):
        return '<Session %r>' % self.id
    
    
with app.app_context():
        db.create_all()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__== "__main__":
    app.run(debug=True)