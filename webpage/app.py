from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('run.html')

@app.route('/run_script')
def run_script():
    try:
        result = subprocess.check_output(['python', 'script1.py'], universal_newlines=True)
        return result
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"

if __name__ == '__main__':
    app.run(debug=True)
