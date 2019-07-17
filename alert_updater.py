from models.alert import Alert
from dotenv import load_dotenv

load_dotenv()
#alrt = Alert(item_id = "123" , price_limit = 1500.0)
#alrt.save_to_mongo()

alerts = Alert.all()

for alert in alerts:
    alert.notify_if_price_reached()