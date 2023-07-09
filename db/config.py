import os

db_path = os.path.join(os.path.dirname(__file__), "settings.db")
db_conn_str = f"sqlite:///{db_path}"
