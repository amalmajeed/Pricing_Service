from flask import Flask, render_template
from views.alerts import alert_blueprint
from views.stores import store_blueprint
from views.users import user_blueprint
import os


app = Flask(__name__)

# Secret key should be set for secure session else it will cause runtime error

app.secret_key = os.urandom(64) # this wont work on windows , only mac and linux

# Adding environemnt variables to the app

app.config.update(ADMIN= os.environ.get('ADMIN'))

app.register_blueprint(alert_blueprint, url_prefix="/alerts")
app.register_blueprint(store_blueprint, url_prefix="/stores")
app.register_blueprint(user_blueprint, url_prefix="/users")


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)  #, host='0.0.0.0' for unrestricted access to all machines in the network
