from flask_app import app
from flask_app.controllers import routes
from flask_app.controllers import controller_balderdash

if __name__=="__main__":
    app.run(debug=True)