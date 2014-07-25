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

    # ADDING AN INITIAL COMMIT OBJECT
    project_id = project.id
    diffs = json.dumps([])
    return_commit = model.Commit(project_id = project_id,
                    parent_id = None,
                    timestamp = datetime.datetime.now(),
                    message = "created a project",
                    diffs = diffs)

    model.session.add(return_commit)

    # after the project & commit objects are added, set the current project & commit
    model.session.commit()
    session['project_id'] = project_id
    session['commit_id'] = return_commit.id


    return redirect('/translate')

# show translation page for current project/commit
@app.route('/translate', methods=['GET'])
def show_editor():
    #takes project_id from either projects list, commit list, or created project
    project_id = session['project_id']
    project = model.session.query(model.Project).filter_by(id = project_id).one()
    commits = model.session.query(model.Commit).filter_by(project_id = project_id).all()
    
    #if requesting text from commit list
    if 'commit_id' in session:
        commit_id = session['commit_id']
        return_commit = model.session.query(model.Commit).filter_by(id = commit_id).one()
        session.pop('commit_id')

    # loads latest commit by default
    else:
        return_commit = commits[-1]

    return render_template('translate.html', project = project,
                                             return_commit = return_commit)

# add a new commit to db
@app.route('/translate', methods=['POST'])
def save_commit():
    project_id = session['project_id']

    translated = request.form.get('translated')
    # compare translated to generated text to generate diffs
    message = request.form.get('message')
    timestamp = datetime.datetime.now()

    #id, project_id, parent_id, timestamp, message, diffs
    commit = model.Commit(project_id = project_id,
                        parent_id = parent_id,
                        timestamp = timestamp,
                        message = message,
                        diffs = diffs)

    model.session.add(commit)
    model.session.commit()

    return "", 200

# show all existing projects
@app.route('/projects', methods=['GET'])
def show_projects():
    projects = model.session.query(model.Project).all()
    return render_template('view_projects.html', projects = projects)

# display latest version on translate page for selected project
@app.route('/select_project/<int:id>')
def process_select_project(id):
    session['project_id'] = id
    return redirect('/translate')

# show all commits
@app.route('/commits', methods=['GET'])
def show_commits():
    project_id = session['project_id']
    commits = model.session.query(model.Commit).filter_by(project_id = project_id).all()

    if len(commits) >= 1:
        return render_template('view_commits.html', commits = commits)
    else:
        return "No commits!"

# display version associated with requested commit
@app.route('/select_commit/<int:id>')
def process_select_commit(id):
    session['commit_id'] = id
    return redirect('/translate')

app.secret_key = 'Omgwassuuuuuuup'

if __name__ == '__main__':
    app.run(debug = True)