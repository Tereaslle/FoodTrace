import mysql.connector
from mysql.connector import Error


def create_mysql_table():
    try:
        # 连接数据库
        connection = mysql.connector.connect(
            host='localhost',
            user='your_username',
            password='your_password',
            database='your_database'
        )

        if connection.is_connected():
            cursor = connection.cursor()

            # 创建表的SQL语句，这里三个引号不是注释，而是未赋值的多行字符串
            create_table_query = """
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                age INT,
                department VARCHAR(50),
                salary DECIMAL(10,2),
                join_date DATE
            )
            """

            # 执行建表语句
            cursor.execute(create_table_query)
            print("MySQL表创建成功")

    except Error as e:
        print(f"MySQL连接或建表错误: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL连接已关闭")

if __name__ == '__main__':
    create_mysql_table()