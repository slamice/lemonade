from flask import Flask, render_template, redirect, request, session
import model
import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
	return render_template('index.html')

@app.route('/create', methods=['GET'])
def process_project():
	return render_template('create_project.html')

@app.route('/create', methods=['POST'])
def create_project():
	# process the input data and redirect to translate page
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

	return redirect('/translate')

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
	elif commits:
		return_commit = commits[-1]
	
	#if new project with no commits, return empty commit
	else:
		return_commit = model.Commit(project_id = project_id,
						timestamp = datetime.datetime.now(),
						translation = "",
						message = "")

	return render_template('translate.html', project = project,
											 return_commit = return_commit)

@app.route('/translate', methods=['POST'])
def save_commit():
	project_id = session['project_id']

	translated = request.form.get('translated')
	message = request.form.get('message')
	timestamp = datetime.datetime.now()

	commit = model.Commit(project_id = project_id,
						timestamp = timestamp,
						translation = translated,
						message = message)

	model.session.add(commit)
	model.session.commit()

	return "", 200

@app.route('/projects', methods=['GET'])
def show_projects():
	projects = model.session.query(model.Project).all()
	return render_template('view_projects.html', projects = projects)

@app.route('/select_project/<int:id>')
def process_select_project(id):
	session['project_id'] = id
	return redirect('/translate')

@app.route('/commits', methods=['GET'])
def show_commits():
	project_id = session['project_id']
	commits = model.session.query(model.Commit).filter_by(project_id = project_id).all()

	return render_template('view_commits.html', commits = commits)

@app.route('/select_commit/<int:id>')
def process_select_commit(id):
	session['commit_id'] = id
	return redirect('/translate')

app.secret_key = 'Omgwassuuuuuuup'

if __name__ == '__main__':
	app.run(debug = True)