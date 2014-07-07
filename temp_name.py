from flask import Flask, render_template, redirect, request, session
import model

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
	return redirect('/translate')

@app.route('/translate', methods=['GET'])
def show_editor():
	return render_template('translate.html')

@app.route('/projects', methods=['GET'])
def show_projects():
	return render_template('view_projects.html')

@app.route('/commits/<int:id>', methods=['GET'])
def show_commits(id):
	# id refers to project id
	# need to process commits for each project
	return render_template('view_commits.html')

if __name__ == '__main__':
	app.run(debug = True)