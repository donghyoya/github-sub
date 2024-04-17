from sqlalchemy import create_engine
import os
engine = create_engine(os.getenv("DATABASE_URL"))
connection = engine.connect()
print("Connected:", connection.closed == False)
connection.close()