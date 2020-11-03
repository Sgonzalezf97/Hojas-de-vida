from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hojas_vida.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class Persona(db.Model):
    __tablename__ = "persona"
    id = db.Column('id', db.Integer, primary_key = True)
    documento = db.Column(db.String(15))
    primer_nombre = db.Column(db.String(50))
    segundo_nombre = db.Column(db.String(50))
    primer_apellido = db.Column(db.String(50))
    segundo_apellido = db.Column(db.String(50))
    celular = db.Column(db.String(50))
    correo = db.Column(db.String(150))
    direccion = db.Column(db.String(250))

    def __init__(self, datos):
        self.documento = datos["documento"]
        self.primer_nombre = datos["primer_nombre"]
        self.segundo_nombre = datos["segundo_nombre"]
        self.primer_apellido = datos["primer_apellido"]
        self.segundo_apellido = datos["segundo_apellido"]
        self.celular = datos["celular"]
        self.correo = datos["correo"]
        self.direccion = datos["direccion"]

class Academica(db.Model):
    __tablename__ = "academica"
    id = db.Column('id', db.Integer, primary_key = True)
    institucion = db.Column(db.String(50))
    programa = db.Column(db.String(50))
    titulo = db.Column(db.String(50))
    anio = db.Column(db.Integer)
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'))

    def __init__(self, datos):
        self.institucion = datos["institucion"]
        self.programa = datos["programa"]
        self.titulo = datos["titulo"]
        self.anio = datos["anio"]
        self.persona_id = datos["persona_id"]
        
class Interes(db.Model):
    __tablename__ = "interes"
    id = db.Column('id', db.Integer, primary_key = True)
    tipo = db.Column(db.String(50))
    descripcion = db.Column(db.String(150))
    persona_id = db.Column(db.Integer, db.ForeignKey('persona.id'))

    def __init__(self, datos):
        self.tipo = datos["tipo"]
        self.descripcion = datos["descripcion"]
        self.persona_id = datos["persona_id"]

@app.route('/')
def show_all():
    return render_template('list.html', rows = Persona.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
       if not request.form['documento'] or not request.form['primer_nombre'] or not request.form['primer_apellido']:
           flash('Please enter all the fields', 'error')
       else:
         datos = {
            'documento' : request.form['documento'], 
            'primer_nombre' : request.form['primer_nombre'], 
            'segundo_nombre' : request.form['segundo_nombre'], 
            'primer_apellido' : request.form['primer_apellido'], 
            'segundo_apellido' : request.form['segundo_apellido'], 
            'celular' : request.form['celular'], 
            'correo' : request.form['correo'], 
            'direccion' : request.form['direccion']
         }
         persona = Persona(datos)

         db.session.add(persona)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

@app.route('/new_academic', methods = ['GET', 'POST'])
def new_academic():
   if request.method == 'POST':
       if not request.form['institucion'] or not request.form['programa'] or not request.form['titulo']:
           flash('Please enter all the fields', 'error')
       else:
         datos = {
            'institucion' : request.form['institucion'], 
            'programa' : request.form['programa'], 
            'titulo' : request.form['titulo'], 
            'anio' : request.form['anio'], 
            'persona_id' : request.form['persona_id'] 
         }
         academica = Academica(datos)

         db.session.add(academica)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new_academic.html')

@app.route('/interes', methods = ['GET', 'POST'])
def interes():
   if request.method == 'POST':
       if not request.form['tipo'] or not request.form['descripcion']:
           flash('Por favor complete todos los campos', 'error')
       else:
         datos = {
            'tipo' : request.form['tipo'], 
            'descripcion' : request.form['descripcion'], 
            'persona_id' : request.form['persona_id'] 
         }
         interes = Interes(datos)

         db.session.add(interes)
         db.session.commit()
         flash('la información se añadio correctamente')
         return redirect(url_for('show_all'))
   return render_template('intereses.html')

@app.route("/update", methods=["POST"])
def update():
    id = request.form.get("id")
    persona = Persona.query.filter_by(id=id).first()
    return render_template('update.html', result = Persona, id = id)

@app.route("/update_record", methods=["POST"])
def update_record():
    id = request.form.get("id")
    persona = Persona.query.filter_by(id=id).first()
    Persona.documento = request.form['documento']
    Persona.primer_nombre = request.form['primer_nombre']
    Persona.segundo_nombre = request.form['segundo_nombre']
    Persona.primer_apellido = request.form['primer_apellido']
    Persona.segundo_apellido = request.form['segundo_apellido']
    Persona.celular = request.form['celular']
    Persona.correo = request.form['correo']
    Persona.direccion = request.form['direccion']
    db.session.commit()
    return redirect('/')

@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    persona = Persona.query.filter_by(id=id).first()
    db.session.delete(persona)
    db.session.commit()
    return redirect("/")

@app.route('/')
def index():
   archivos = os.listdir("static")
   lista = []
   for a in archivos:
       if a.split(".")[1] in ["jpg", "png", "jpeg"]:
           lista.append(a)

   return render_template('index.html', msg = "file loaded successfully", rows = lista)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')

@app.route('/uploader', methods = ['POST'])
def uploader_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.root_path, 'static', secure_filename(f.filename)))

      archivos = os.listdir("static")
      lista = []
      for a in archivos:
          if a.split(".")[1] in ["jpg", "png", "jpeg"]:
              lista.append(a)

      return render_template('index.html', msg = "file loaded successfully", rows = lista)


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)