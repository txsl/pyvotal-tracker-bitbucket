try:
    from settings import key
    key
except ImportError:
    raise Exception("You need to import your Pivotal Tracker key before starting")


from flask import Flask, request
app = Flask(__name__)
from pyvotaltracker import PivotalTracker

@app.route('/commit', methods=['POST'])
def commit_route():
	# Check key here.. 
	#searchword = request.args.get('key', '')

	payload = request.form['payload']
	p = PivotalTracker(key)

	p.handle(payload)

	return 'Thanks'

if __name__ == '__main__':
    app.run(debug=True)