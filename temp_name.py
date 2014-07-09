from flask import Flask, render_template, redirect, request, session
import model
import datetime
import pdb

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
	session['current_proj'] = project_id

	return redirect('/translate')

@app.route('/translate', methods=['GET'])
def show_editor():
	project_id = session['current_proj']
	project = model.session.query(model.Project).filter_by(id = project_id).one()
	# commit = model.session.query(model.Commit).filter_by(project_id = project_id).one()

	return render_template('translate.html', project = project)

@app.route('/translate', methods=['POST'])
def save():
	project_id = session['current_proj']
	project = model.session.query(model.Project).filter_by(id = project_id).one()
	
	pdb.set_trace()
	print "WE ARE PRINTING STUFF"
	print request.data
	translated = request.data.get('text')
	message = request.data.get('message')
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
	return render_template('view_projects.html')

@app.route('/commits', methods=['GET'])
def show_commits():
	project_id = session['current_proj']
	commits = model.session.query(model.Commit).filter_by(project_id = project_id).all()
	return render_template('view_commits.html', commits = commits)


app.secret_key = 'Omgwassuuuuuuup'


if __name__ == '__main__':
	app.run(debug = True)