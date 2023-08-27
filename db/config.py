import os

db_path = os.path.join(os.path.expanduser('~'), '.cfparser', "settings.db")
db_conn_str = f"sqlite:///{db_path}"
