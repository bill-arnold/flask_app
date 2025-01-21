from flask import Flask , render_template, request , url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db,Projects



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
        db.session.commit()
    return redirect(url_for('projects'))
        
    


if __name__ == '__main__':
    app.run(debug=True)