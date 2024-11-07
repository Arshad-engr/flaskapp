from flask import Flask, request,url_for,redirect,render_template,session,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, logout_user, login_required,current_user, UserMixin,AnonymousUserMixin 
import boto3
from botocore.exceptions import NoCredentialsError
import uuid 
import os
import string
import random
from datetime import timedelta
from werkzeug.utils import secure_filename


from sqlalchemy.sql import func
app = Flask(__name__)


# create the extension
db = SQLAlchemy()
migrate = Migrate(app, db)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "randome_number"


# initialize the app with the extension
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.anonymous_user = AnonymousUserMixin

login_manager.init_app(app)
login_manager.login_view = 'login'  # Route to redirect to if not logged


UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'assets', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    if current_user==None:
            return redirect(url_for('login'))
    else:
            return redirect(url_for('dashboard'))
        
    

@app.route('/dashboard')
@login_required
def dashboard():
    total_users = User.query.count() 
    return render_template('index.html',total_users=total_users)

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash("Logged in successfully!")
            return redirect(url_for('home'))
        else:
            flash("Invalid login credentials")
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('login')

# image validation 
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
@app.route('/register',methods =['GET','POST'])
def register():
    if request.method == "POST":
         user_profile = request.files['profil_image'] if 'profil_image' in request.files else None
         user_profile_str = None
         if user_profile is not None:
              if allowed_file(user_profile.filename):
                   filename = secure_filename(user_profile.filename)
                   file_extension = os.path.splitext(filename)[1] 
                   user_profile_str = ''.join(random.choices(string.ascii_letters, k=7))+'_'+request.form['email']+file_extension
                   user_profile.save(os.path.join(app.config['UPLOAD_FOLDER'], user_profile_str))
              else:
                  flash('Invalid file provided')   
                  return redirect(url_for('register'))  
         new_user = User(first_name=request.form['first_name'],
                         last_name=request.form['last_name'],email=request.form['email'],
                         password=request.form['password'],is_active=True,profil_image=user_profile_str)
         role = Role.query.filter_by(name='Writer').first()
         new_user.roles.append(role)
         db.session.add(new_user)
         db.session.commit()
         flash('Successfully registerd, Please login here')
         return redirect(url_for("login"))
    return render_template('register.html')

@app.route('/profile',methods=['GET','POST'])
@login_required
def profile():
    if request.method =='POST':
        current_user.first_name = request.form['first_name']
        current_user.last_name = request.form['last_name']
        current_user.email = request.form['email']
        if request.files['profil_image']:
            if current_user.profil_image : os.remove(os.path.join(app.config['UPLOAD_FOLDER'], current_user.profil_image))
            user_profile = request.files['profil_image']
            if allowed_file(user_profile.filename):
                   filename = secure_filename(user_profile.filename)
                   file_extension = os.path.splitext(filename)[1] 
                   user_profile_str = ''.join(random.choices(string.ascii_letters, k=7))+'_'+request.form['email']+file_extension
                   user_profile.save(os.path.join(app.config['UPLOAD_FOLDER'], user_profile_str))
                   current_user.profil_image = user_profile_str
                   
            else:
                  flash('Invalid file provided','error') 
        db.session.commit()
        flash('Profile updated successfully!') 
        return redirect(url_for("profile"))
            
            
    return render_template('profile.html')

@app.route('/removeProfile',methods=['POST'])
@login_required
def removeProfile():
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], current_user.profil_image))
    current_user.profil_image = None
    db.session.commit()
    response = {
        'message': "Profile image deleted successfully!"
    }
    return jsonify(response)

# suspend user
@app.route('/deactiveUser',methods=['POST'])
@login_required
def updateUserStatus():
    if request.method == 'POST':
        data = request.json
        user  = User.query.filter(User.id == data.get('id')).first_or_404()
        user.is_active =  data.get('status')
        db.session.commit()
        response = {
            'message': "User updated successfully!"
        }
    return jsonify(response)

@app.route('/deleteUser',methods=['POST'])
@login_required
def deleteUser():
    if request.method == 'POST':
        data = request.json
        user  = User.query.filter(User.id == data.get('id')).first_or_404()
        db.session.delete(user)
        db.session.commit()
        response = {
            'message': "User deleted successfully!"
        }
    return jsonify(response)
    
# list of all users
@app.route('/users')
@login_required
def users():
    users = users = User.query.filter(User.id != current_user.id).all()
    return render_template('users.html',users=users)
    
# create table in database for assigning roles
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))  
# create table in database for storing roles
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True,nullable=False)
    password = db.Column(db.String)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    profil_image = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=True, default=lambda: str(uuid.uuid4()))

    # backreferences the user_id from roles_users table
    roles = db.relationship('Role', secondary=roles_users, backref='roled')
    
    def __repr__(self):
      return f'<User {self.first_name}>'
    def get_id(self):
        return self.id  # Return the primary key of the user
    @property
    def is_authenticated(self):
        return True




 # Define the user_loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)
