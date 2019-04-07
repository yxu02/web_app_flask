from src.commons.database import Database
from src.models.alerts.alert import Alert

Database.initialize()

outdated_alerts = Alert.find_outdated_alerts()
print(outdated_alerts)
for alert in outdated_alerts:
    alert.load_item_price()
    alert.send_email_if_price_reached()