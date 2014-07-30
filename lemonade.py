from flask import Flask, render_template, redirect, request, session
import model
import datetime
import generators
import json

app = Flask(__name__)

# show main page
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# show project creation page
@app.route('/create', methods=['GET'])
def input_project():
    return render_template('create_project.html')

# process new project
@app.route('/create', methods=['POST'])
def create_project():
    # process the input data and redirect to translate page

    # ADDING A PROJECT OBJECT
    title = request.form.get('title')
    description = request.form.get('description')
    source_text = request.form.get('source-text')

    project = model.Project(title = title,
                        description = description,
                        source_text = source_text)

    model.session.add(project)
    model.session.commit()


    project_id = project.id

    # diffs = json.dumps([])
    # return_commit = model.Commit(project_id = project_id,
    #                 parent_id = None,
    #                 timestamp = datetime.datetime.now(),
    #                 message = "created a project",
    #                 diffs = diffs)

    # model.session.add(return_commit)

    # after the project & commit objects are added, set the current project & commit
    model.session.commit()
    
    session['project_id'] = project_id
    session['commit_id'] = None

    return redirect('/translate')

# show translation page for current project/commit
@app.route('/translate', methods=['GET'])
def show_editor():

    #takes project_id from either projects list, commit list, or created project
    project_id = session['project_id']
    commit_id = session['commit_id']
    project = model.session.query(model.Project).filter_by(id = project_id).one()
    commits = model.session.query(model.Commit).filter_by(project_id = project_id).all()
    if commit_id == None:
        translation = ""
    else:
        translation = generators.construct_text_from_commit_id(commit_id)

    return render_template('translate.html', project = project,
                                             translation = translation)

# add a new commit to db
@app.route('/translate', methods=['POST'])
def save_commit():
    project_id = session['project_id']
    commit_id = session['commit_id']

    # parent_id is the commit_id of the text the new one is being compared to 
    parent_id = commit_id
    timestamp = datetime.datetime.now()
    message = request.form.get('message')

    # compare translated to generated text to generate diffs
    translated = request.form.get('translated')
    diffs = generators.generate_new_diffs(translated, project_id)

    #id, project_id, parent_id, timestamp, message, diffs
    commit = model.Commit(project_id = project_id,
                        parent_id = parent_id,
                        timestamp = timestamp,
                        message = message,
                        diffs = diffs)

    model.session.add(commit)
    model.session.commit()

    # reset commit_id in session to the newly created commit
    session['commit_id'] = commit.id

    return "", 200

# show all existing projects
@app.route('/projects', methods=['GET'])
def show_projects():
    projects = model.session.query(model.Project).all()
    return render_template('view_projects.html', projects = projects)

# display latest version on translate page for selected project
@app.route('/select_project/<int:id>')
def process_select_project(id):
    project_id = id

    commits = model.session.query(model.Commit).filter_by(project_id = project_id).all()
    session['project_id'] = project_id
    session['commit_id'] = commits[-1].id

    return redirect('/translate')

# show all commits
@app.route('/commits', methods=['GET'])
def show_commits():
    project_id = session['project_id']
    commits = model.session.query(model.Commit).filter_by(project_id = project_id).all()

    return render_template('view_commits.html', commits = commits)

# display version associated with requested commit
@app.route('/select_commit/<int:id>')
def process_select_commit(id):
    session['commit_id'] = id
    return redirect('/translate')

app.secret_key = 'Omgwassuuuuuuup'

if __name__ == '__main__':
    app.run(debug = True)