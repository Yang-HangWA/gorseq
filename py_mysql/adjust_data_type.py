import pymysql

# 打开数据库连接
db = pymysql.connect(
    host='10.8.80.239',
    user='gorse',
    password='gorse_pass',
    database='tyedu2021',
    port=3308,
)

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# # 使用 execute()  方法执行 SQL 查询
# cursor.execute("SELECT VERSION()")

# 查询修改ty_know_id数据类型。
cursor.execute("select * from items limit 1")
# 使用 fetchone() 方法获取单条数据.
data = cursor.fetchone()

print(data)

# 关闭数据库连接
db.close()
