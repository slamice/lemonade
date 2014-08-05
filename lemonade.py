from flask import Flask, render_template, redirect, request, session
import model
import datetime
import generators
import keys

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
    session['project_id'] = project_id
    session['commit_id'] = None

    return redirect('/translate')

# show translation page for current project/commit
@app.route('/translate', methods=['GET'])
def show_editor():

    #takes project_id from either projects list, commit list, or created project
    project_id = session['project_id']
    commit_id = session['commit_id']
    project = model.Project.query_project_by_id(project_id)
    commits = model.Commit.query_commits_by_proj_id(project_id)[::-1]

    if commit_id == None:
        translation = ""
    else:
        tokens = generators.construct_commit_id(commit_id)
        translation = ' '.join(tokens)

    return render_template('translate.html', project = project,
                                             translation = translation,
                                             commits = commits)

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
    after_tokens = generators.tokenize(translated)
    if parent_id == None:
        before_tokens = [""]
    else:
        before_tokens = generators.construct_commit_id(parent_id)
    diffs = generators.generate_diffs(before_tokens, after_tokens)

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
    # catch for situation in which project is not selected (for sidebar)
    if 'project_id' in session:
        project_id = session['project_id']
    else:
        project_id = None
    projects = model.Project.query_all_projects()[::-1]
    commits = []

    last_timestamps = {}
    for project in projects:
        proj_commits = model.Commit.query_commits_by_proj_id(project.id)[::-1]
        if project.id == project_id:
            commits = proj_commits

        # catch for situation in which there are no commits
        if commits:
            last_commit = commits[0]
            last_timestamps[project.id] = last_commit.timestamp
        else:
            last_timestamps[project.id] = None

    return render_template('view_projects.html', 
                            projects = projects,
                            last_timestamps = last_timestamps,
                            commits = commits)

# display latest version on translate page for selected project
@app.route('/select_project/<int:id>')
def process_select_project(id):
    project_id = id

    commits = model.Commit.query_commits_by_proj_id(project_id)
    session['project_id'] = project_id
    if commits:
        session['commit_id'] = commits[-1].id
    else: session['commit_id'] = None

    return redirect('/translate')

# show all commits
@app.route('/commits', methods=['GET'])
def show_commits():
    # catch for situation in which there is no current project for sidebar
    if 'project_id' in session:
        project_id = session['project_id']
    else:
        project_id = None

    commits = model.Commit.query_commits_by_proj_id(project_id)[::-1]

    previews = {}
    for commit in commits:
        text = generators.construct_commit_id(commit.id)
        # displays last 2 sentences
        previews[commit.id] = ' '.join(text[-2:])

    # if there are commits
    if commits:
        title = commits[0].project.title
        description = commits[0].project.description

        return render_template('view_commits.html',
                                title = title,
                                description = description,
                                commits = commits,
                                previews = previews)
        
    # if there are no commits to display
    else:
        title = "Uh oh, you need to get workin'."

    return render_template('view_commits.html',
                            title = title,
                            commits = commits,
                            previews = previews)

# display version associated with requested commit
@app.route('/select_commit/<int:id>')
def process_select_commit(id):
    session['commit_id'] = id
    return redirect('/translate')

app.secret_key = keys.app_secret_key

if __name__ == '__main__':
    app.run(debug = True)