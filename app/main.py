import os

# connection = {
#     'charset': "utf8mb4",
#     'connect_timeout': 10,
#     'database': "testdb",
#     'host': "mysql-c84cbdd-shanurislam-api.a.aivencloud.com",
#     'password': "AVNS_KfXrQqgF7G0Yp3FXD2Z",
#     'port': 19082,
#     'user': "avnadmin",
# }

connection = {
    'charset': "utf8mb4",
    'connect_timeout': 10,
    'database': os.environ.get("MYSQL_DATABASE"),
    'host': os.environ.get("MYSQL_HOST"),
    'password': os.environ.get("MYSQL_PASSWORD"),
    'port': int(os.environ.get("MYSQL_PORT", 3306)),  # Default to 3306 if not set
    'user': os.environ.get("MYSQL_USER"),
}