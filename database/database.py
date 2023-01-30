from sqlalchemy import create_engine
import json
from sqlalchemy.ext.declarative import declarative_base

# Opening JSON file
with open('config.json') as json_file:
    cfg = json.load(json_file)

engine =create_engine(f'mysql+pymysql://{cfg["database"]["user"]}:{cfg["database"]["password"]}@{cfg["database"]["ip"]}:{cfg["database"]["port"]}/{cfg["database"]["dbname"]}')
Base=declarative_base()
del cfg