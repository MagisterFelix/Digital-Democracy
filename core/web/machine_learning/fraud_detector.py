import os

import pandas as pd
from django.conf import settings
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

from core.web.models.log import Log

PATH = os.path.join(settings.BASE_DIR, "core", "web", "machine_learning", "data", "user_behavior.csv")


def predict_fraud(log):
    data = pd.read_csv(PATH)
    for user_log in Log.objects.filter(user=log.user).exclude(created_at=log.created_at):
        data.loc[len(data)] = [user_log.action, user_log.ip, user_log.user.passport, int(user_log.is_fraud)]

    le_ip = LabelEncoder()
    le_user_id = LabelEncoder()

    data["ip_encoded"] = le_ip.fit_transform(data["ip"])
    data["user_id_encoded"] = le_user_id.fit_transform(data["user_id"])

    x = data[["action", "ip_encoded", "user_id_encoded"]]
    y = data["is_fraud"]

    clf = KNeighborsClassifier(n_neighbors=10).fit(x, y)

    try:
        ip_encoded = le_ip.transform([log.ip])[0]
    except ValueError:
        ip_encoded = le_ip.fit_transform([log.ip])[0]

    try:
        user_id_encoded = le_user_id.transform([log.user.passport])[0]
    except ValueError:
        user_id_encoded = le_user_id.fit_transform([log.user.passport])[0]

    encoded_data = [
        {
            "action": log.action,
            "ip_encoded": ip_encoded,
            "user_id_encoded": user_id_encoded
        }
    ]
    encoded_data_df = pd.DataFrame(encoded_data)

    prediction = clf.predict(encoded_data_df)[0]

    log.update_is_fraud(bool(prediction))

    return prediction
