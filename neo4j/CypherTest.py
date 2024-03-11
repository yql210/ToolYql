from cypher_parser import parse

# 将 Cypher 查询转换为逻辑表达式
def cypher_to_logic(cypher_query):
    parsed = parse(cypher_query)
    # 这里我们只是简单地打印出解析后的 AST，实际的逻辑转换需要更复杂的处理
    return str(parsed)

# 将逻辑表达式转换回 Cypher 查询
def logic_to_cypher(logic_expression):
    # 这个转换同样需要复杂的逻辑，这里我们只是简单地返回原始表达式
    # 实际上，这通常是不可能的，因为逻辑表达式可能包含无法直接转换回 Cypher 的信息
    return logic_expression

# 示例 Cypher 查询
cypher_query = "MATCH (a)-[r]->(b) WHERE a.property = 'value' AND b.property > 10 RETURN a, b"

# 打印 Cypher 查询的 AST
print("Cypher AST:", cypher_to_logic(cypher_query))

# 示例逻辑表达式
logic_expression = "(a)-[r]->(b) AND a.property = 'value' AND b.property > 10"

# 打印逻辑表达式尝试转换回 Cypher
print("Logic to Cypher:", logic_to_cypher(logic_expression))