from antlr4 import *
from CypherLexer import CypherLexer
from CypherParser import CypherParser
import graphviz
import json


# 输入Cypher查询字符串
cypher_query = "MATCH (a)-[r]->(b) RETURN a, b"

# 创建输入流
input_stream = InputStream(cypher_query)

# 创建词法分析器
lexer = CypherLexer(input_stream)

# 创建Token流
token_stream = CommonTokenStream(lexer)

# 创建解析器
parser = CypherParser(token_stream)

# 解析查询
# tree = parser.query()
tree = parser.oC_Query()

# 这里可以添加一个监听器来访问或操作AST


def get_ast(statement):
    reader = InputStream(statement)
    lexer = CypherLexer(reader)
    stream = CommonTokenStream(lexer)
    parser = CypherParser(stream)
    return parser.oC_Statement()


ast_tree = get_ast('match (n) return n limit 10')
ast_tree_m = get_ast('match (yuanql) return yuanql limit 10')

print(ast_tree.toStringTree())
print(tree.toStringTree())

js = json.loads(ast_tree)

# 使用Graphviz可视化语法树
dot = ast_tree.toStringTree()
graph = graphviz.Source(dot)
# graph.render("YourGrammar.gv", format='png', cleanup=True)

print("end")