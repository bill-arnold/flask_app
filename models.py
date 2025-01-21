from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Join Table for Many-to-Many relationship between Staff and Projects
staff_projects = db.Table(
    'staff_projects',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('staff_id', db.Integer, db.ForeignKey('staff.id'), primary_key=True)
)

class Projects(db.Model):  # Fixed typo: Changed db.model to db.Model
    __tablename__ = 'projects'  # Fixed table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)  # Fixed Text to String for length limit
    description = db.Column(db.String(200), nullable=True)  # Fixed typo in 'description'
    
    # Many-to-Many relationship to Staff using the join table
    staff = db.relationship('Staff', secondary=staff_projects, backref='projects', lazy='dynamic')

    # One-to-Many relationship to Details
    details = db.relationship('Details', backref='project', lazy=True)  # Fixed Details relationship


class Staff(db.Model):  # Fixed typo: Changed db.model to db.Model
    __tablename__ = 'staff'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    profile_photo = db.Column(db.String(200), nullable=True)


class Details(db.Model):  # Fixed typo: Changed db.model to db.Model
    __tablename__ = 'details'
    details_id = db.Column(db.Integer, primary_key=True)  # Fixed typo in 'details_id'
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)  # Fixed ForeignKey syntax
    project_name = db.Column(db.String(200), nullable=False)  # Fixed typo in 'project_name'
