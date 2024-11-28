import json

# 假设您已经有一个包含数据的JSON字符串
with open('./insertSql.json', 'r', encoding='utf-8') as file:
    json_data = file.read()
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        exit(1)
# 尝试解析JSON数据
try:
    data = json.loads(json_data)
except json.JSONDecodeError as e:
    print(f"JSON解析错误: {e}")
    exit(1)

# 获取表名（假设已知）
table_name = 'your_table_name'

# 开始构建SQL语句
sql = f"INSERT INTO {table_name} ("

# 添加列名
sql += ", ".join(data['data']['columnsName']) + ") VALUES\n"

# 遍历数据并添加到VALUES部分
for record in data['data']['data']:
    # 处理每个字段值
    values = []
    for value in record:
        if value is None or (isinstance(value, str) and value.lower() == 'null'):
            values.append('NULL')
        elif isinstance(value, str):
            # 对字符串进行转义处理
            value = value.replace("'", "''")
            values.append(f"'{value}'")
        else:
            values.append(str(value))

    # 添加当前记录的VALUES行
    sql += f"({', '.join(values)}),\n"

# 移除最后一个逗号并结束语句
sql = sql.rstrip(',\n') + ";"

# 打印或保存生成的SQL语句
print(sql)