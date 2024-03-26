import datetime
from flask import Flask, render_template
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库配置
DATABASE_URI = 'sqlite:///data.db'  # 使用 SQLite

app = Flask(__name__)

# Database connection and model definition
engine = create_engine(DATABASE_URI)
Base = declarative_base()

class MyTable(Base):
  __tablename__ = 'log_table'
  id = Column(Integer, primary_key=True)
  data_field1 = Column(String)
  data_field2 = Column(String)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.route('/read_and_log')
def read_and_log():
  # Open file for appending in write mode ('a')
  with open('data_log.txt', 'a') as log_file:
    session = SessionLocal()
    # Fetch all data from the table
    data = session.query(MyTable).all()

    # Write timestamp to log
    log_file.write(f"Data retrieved at {datetime.datetime.now()}\n")

    # Loop through data and write each row to log
    for row in data:
      log_file.write(f"{row.id}, {row.data_field1}, {row.data_field2}\n")

    session.close()
    return '数据读取并记录成功!'

if __name__ == '__main__':
  app.run(debug=True)