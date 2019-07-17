from flask import Blueprint , render_template , request , redirect , url_for, session
from models.alert import Alert
from models.store import Store
from models.item import Item
from models.user import requires_login

alert_blueprint = Blueprint("alerts" , __name__ )

@alert_blueprint.route('/')
@requires_login             #   This decorator should go below the flask decorator
def index():
    print(session['email'])
    alerts = Alert.find_many_by('user_email', session['email'])
    for i in alerts:
        i.__post__init__()
    return render_template('alerts/index.html' , alerts = alerts, current = session['email'])

@alert_blueprint.route('/new' , methods=['GET','POST'])
@requires_login
def new_alert():
    if request.method == 'POST':
        item_url = request.form['item_url']
        price_limit = float(request.form['price_limit'].strip())
        name = request.form['name']

        store = Store.find_by_url(item_url)

        item = Item(item_url , store.tag_name , store.query)
        item.load_price()
        item.save_to_mongo()

        Alert(item._id, name, price_limit ,session['email']).save_to_mongo()
        alerts = Alert.find_many_by('user_email', session['email'])
        for i in alerts:
            i.__post__init__()
        return render_template("alerts/index.html" , alerts = alerts, current = session['email'])
    return render_template("alerts/new_alert.html")

@alert_blueprint.route('/edit/<string:alert_id>' , methods=['GET','POST'])
@requires_login
def edit_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    alert.__post__init__()
    if request.method == "POST":
        price_limit = float(request.form['price_limit'].strip())
        alert.price_limit = price_limit
        alert.save_to_mongo()
        return redirect(url_for('.index'))
    return render_template("alerts/edit_alert.html" , alert = alert)

@alert_blueprint.route('/delete/<string:alert_id>' , methods=['GET'])
@requires_login
def delete_alert(alert_id):
    alert = Alert.get_by_id(alert_id)
    alert.remove_from_mongo()
    alerts = Alert.find_many_by('user_email', session['email'])
    for i in alerts:
        i.__post__init__()
    return render_template("alerts/index.html" , alerts = alerts, current = session['email'])

