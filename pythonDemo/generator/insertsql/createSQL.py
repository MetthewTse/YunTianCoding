import json


def generate_sql(path, table_name):
    with open(path, 'r', encoding='utf-8') as file:
        json_data = file.read()
        try:
            data = json.loads(json_data)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            exit(1)


        sql = f"INSERT INTO {table_name} ("

        sql += ", ".join(data['data']['columnsName']) + ") VALUES\n"

        # 遍历数据并添加到VALUES部分
        for record in data['data']['data']:
            # 处理每个字段值
            values = []
            for value in record:
                if value is None or value.lower() == 'null':
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
        return sql


class CreateSQLGenerator:
    def __init__(self, json_path):
        self.json_path = json_path
