from py2neo import Graph, NodeMatcher, RelationshipMatcher

# 连接到Neo4j数据库
graph = Graph("http://172.16.44.106:7474", auth=("neo4j", "neo4jneo4j"))

# # 使用NodeMatcher查询节点
# node_matcher = NodeMatcher(graph)
# person = node_matcher.match("Person", name="Alice").first()
# print(person)
#
# # 使用RelationshipMatcher查询关系
# relationship_matcher = RelationshipMatcher(graph)
# relationships = relationship_matcher.match("Alice", "KNOWS", "Bob").first()
# print(relationships)






# 执行Cypher查询
result = graph.run("match (n:ENTITY{name:'九年级物理/北大绿卡'})-[:Relationship*1..2]->(x) where x.name<>'出版物' return distinct x.name").data()
for record in result:
    print(record)









