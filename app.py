from flask import Flask , render_template, request , url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Projects, Staff, Details




app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'


migrate=Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
       
        return  render_template ('/index.html')

@app.route('/projects', methods=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        # Get project name and details from the form
        project_name = request.form.get('project_name')
        project_details = request.form.get('project_details')
        
        # Create a new project instance
        new_project = Projects(name=project_name, description=project_details)
        
        # Add the project to the database session and commit
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('projects'))  # Redirect to avoid duplicate form submissions
    
    # Fetch all projects for GET requests
    all_projects = Projects.query.all()
    return render_template('project.html', projects=all_projects)

#project route delete
@app.route('/projects/delete/<int:id>', methods=['POST'])
def delete_project(id):
    project_to_delete = Projects.query.get(id)
    if project_to_delete:
        db.session.delete(project_to_delete)
        db.session.commit() #After modifying data, you must call db.session.commit() to commit the changes to the database. Otherwise, they will be discarded at the end of the request.
    return redirect(url_for('projects'))

#project update route

@app.route('/projects/update/<int:id>', methods=['POST'])
def update_project(id):
    project_to_update = Projects.query.get(id)
    if project_to_update:
        project_name = request.form.get('project_name')
        project_details = request.form.get('project_details')
        project_to_update.name = project_name
        project_to_update.description = project_details
        db.session.commit()
    return redirect(url_for('projects'))

@app.route('/staff', methods=['GET','POST'])
def staff():
     if request.method == 'POST':
       first_name = request.form.get('first_name')
       last_name = request.form.get('last_name')
       profile_photo = request.form.get('profile_photo')
       new_staff = Staff(first_name=first_name,last_name=last_name,profile_photo=profile_photo)
       db.session.add(new_staff)
       db.session.commit()

       return redirect(url_for('staff'))
     
     all_staff = Staff.query.all()
     return render_template('staff.html', staff=all_staff)

@app.route('/staff/delete/<int:id>', methods=['POST'])
def delete_staff(id):
    staff_to_delete = Staff.query.get(id)
    if staff_to_delete:
        db.session.delete(staff_to_delete)
        db.session.commit() #After modifying data, you must call db.session.commit() to commit the changes to the database. Otherwise, they will be discarded at the end of the request.
    return redirect(url_for('staff'))

@app.route('/staff/update/<int:id>', methods=['POST'])
def update_staff(id):
    staff_to_update = Staff.query.get(id)
    if staff_to_update:
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        profile_photo = request.form.get('profile_photo')
        staff_to_update.first_name = first_name
        staff_to_update.last_name = last_name
        staff_to_update.profile_photo = profile_photo
        db.session.commit()
    return redirect(url_for('staff'))





@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        project_id = request.form.get('project_id')
        project_name = request.form.get('project_name')

        new_detail = Details(project_id=project_id, project_name=project_name)
        db.session.add(new_detail)
        db.session.commit()

        return redirect(url_for('details'))

    all_details = Details.query.all()
    return render_template('details.html', details=all_details)


@app.route('/details/update/<int:id>', methods=['POST'])
def update_detail(id):
    detail = Details.query.get_or_404(id)
    detail.project_id = request.form.get('project_id')
    detail.project_name = request.form.get('project_name')
    db.session.commit()
    return redirect(url_for('details',  message='Detail updated successfully!'))


@app.route('/details/delete/<int:id>', methods=['POST'])
def delete_detail(id):
    detail = Details.query.get_or_404(id)
    db.session.delete(detail)
    db.session.commit()
    return redirect(url_for('details', message='Detail deleted successfully!'))

if __name__ == '__main__':
    app.run(debug=True)