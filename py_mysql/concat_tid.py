import pymysql
import ast
import json
import multiprocessing as mp


def get_data(
    sql, host="10.8.80.239", user="math", passwd="math_pass", db="tyedu2021", port=3308
):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port)
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    col = cur.description
    # columnDes = cur.description

    return data, col


q1 = "select * from items"
data1, col = get_data(q1)
tid_list = [item[0] for item in data1]
tid_list = list(set(tid_list))
print(len(tid_list))
pre_insert = "insert into  items_new1 ("
key_str = ""
for item in col:
    key_str += item[0] + ", "

pre_insert = (pre_insert + key_str)[:-2] + ") values "


def insert_data(
    sql, host="10.8.80.239", user="math", passwd="math_pass", db="tyedu2021", port=3308
):
    conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port)
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def process_tiddata(tid_data, pre_insert=pre_insert):
    concat_index = 32
    t_ind_a, t_ind_b = 19, 20
    res = []
    for data in tid_data:
        res.extend(ast.literal_eval(data[concat_index]))
    temp = list(tid_data[0])
    temp[concat_index] = json.dumps(res)

    temp[t_ind_a] = temp[t_ind_a].strftime("%Y-%m-%d, %H:%M:%S")
    temp[t_ind_b] = temp[t_ind_b].strftime("%Y-%m-%d, %H:%M:%S")

    insert_sql = pre_insert + str(tuple(temp))
    insert_sql = insert_sql.replace("None", "'None'")
    print(insert_sql)
    insert_data(insert_sql)


def process_worker(tid):
    q2 = f"select * from items where tid={tid}"
    tid_data, _ = get_data(q2)
    try:
        process_tiddata(tid_data)
    except Exception as e:
        print(tid, str(e))


if __name__ == "__main__":
    pool = mp.Pool(5)

    pool.map(process_worker, tid_list)
