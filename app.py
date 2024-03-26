import datetime
from flask import Flask, render_template, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 数据库配置
DATABASE_URI = 'sqlite:///data.db'  # 使用 SQLite

app = Flask(__name__)

# 连接数据库并定义
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
  """读取数据库数据并写入日志文件"""
  # 打开文件以追加模式写入 ('a')
  with open('data_log.txt', 'a') as log_file:
    session = SessionLocal()
    # 查询所有数据
    data = session.query(MyTable).all()
    # 写入时间戳到日志
    log_file.write(f"数据检索时间：{datetime.datetime.now()}\n")

    # 遍历数据并写入每一行到日志
    for row in data:
      log_file.write(f"{row.id}, {row.data_field1}, {row.data_field2}\n")

    session.close()
    return '数据库读取并写入日志成功！'
@app.route('/write_data', methods=['GET', 'POST'])
def write_data():
  if request.method == 'POST':
    data_field1 = request.form['data_field1']
    data_field2 = request.form['data_field2']

    print(data_field1)
    print(data_field2)
    session = SessionLocal()
    # Create a new data entry
    new_data = MyTable(data_field1=data_field1, data_field2=data_field2)
    session.add(new_data)
    session.commit()
    session.close()
    
    return '数据库写入成功!'
  else:
    # 渲染表单
    return render_template('write_data_form.html')

if __name__ == '__main__':
  app.run(debug=True)