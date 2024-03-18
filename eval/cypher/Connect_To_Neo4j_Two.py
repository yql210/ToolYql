from neo4j import GraphDatabase

# 连接的URI，用户名和密码
uri = "bolt://172.16.44.106:7687"
username = "neo4j"
password = "neo4jneo4j"

# 设置超时时间（以秒为单位）
timeout = 10  # 例如，设置为10秒

# 创建一个配置字典，包含超时设置
config = {
    "encrypted": False,  # 如果是加密连接，设置为True
    "timeout": timeout,  # 设置连接超时时间
    # 其他可能的配置项...
}

# # 创建一个超时配置对象
# timeout_config = GraphDatabase.TimeoutConfig(
#     connect_timeout=10.0,  # 连接超时时间，单位秒
#     read_timeout=30.0,      # 读取超时时间，单位秒
#     write_timeout=10.0     # 写入超时时间，单位秒
# )

# 创建一个连接池配置对象
pool_config = GraphDatabase.ConnectionPoolConfig(
    max_size=10,  # 连接池中的最大连接数
    max_lifetime=600,  # 连接的最大生命周期（秒）
    timeout=30,  # 连接的默认超时时间（秒）
    liveness_check_timeout=5  # 存活性检查的超时时间（秒）
)


# 使用GraphDatabase.driver()创建一个驱动程序实例
driver = GraphDatabase.driver(uri, auth=(username, password), )

# 使用驱动程序创建会话并执行查询
with driver.session() as session:
    result = session.run("MATCH (n) RETURN n LIMIT 1")
    print(result.single())
# 确保在最后关闭驱动程序
driver.close()


