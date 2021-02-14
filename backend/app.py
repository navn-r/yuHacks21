#  ____                           
# / ___|  ___ _ ____   _____ _ __ 
# \___ \ / _ \ '__\ \ / / _ \ '__|
#  ___) |  __/ |   \ V /  __/ |   
# |____/ \___|_|    \_/ \___|_|   
#
# https://pythonbasics.org/flask-tutorial-routes/
   
"""
flask imports
  Flask: main app
  request: to get the request body   
"""
from flask import Flask, request, jsonify 
from verify import verify

# create flask app
app = Flask(__name__)

"""
Route: / 
RequestMethod: POST
RequestBody: 
{ 
  text: string;
}
"""
@app.route('/check', methods = ['POST'])
def index():
  if request.method == 'POST':
    text = request.get_json()['text']
    return jsonify({'score': verify([text])})


@app.route('/')
def index():
    return "<div><h1>FæktChɛk Backend Server<h1>Uh Oh! There's nothing here!</div>"

if __name__ == '__main__':
  app.run(threaded=True, port=5000)