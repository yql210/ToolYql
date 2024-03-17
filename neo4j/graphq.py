from graphq_trans.sparql.translator import Translator as SparqlTranslator
from graphq_trans.ir.translator import Translator as IRTranslator

# from graphq_trans.cypher.translator import Translator as
from graphq_trans.cypher.translator import Translator as CYTranslator

sparql_translator = SparqlTranslator() # Create a SparqlTranslator that translates SPARQL to graphqIR
ir_translator = IRTranslator() # Create a IRTranslator that translates graphqIR to Cypher
cyl_translator = CYTranslator()

# the SPARQL query for "Get all entities that are human"
sparql_query = 'SELECT DISTINCT ?e WHERE { ?e <pred:instance_of> ?c . ?c <pred:name> "human" } '

ir = sparql_translator.to_ir(sparql_query) # translates sparql to ir
cypher_query = ir_translator.to_cypher(ir) # translates ir to cypher

print(cypher_query)
print()
print(ir)

print("\n-------------------\n")
ir = None
# cypher_query = 'MATCH (:ENTITY{name:"艺术家"})<-[:Tag{name:"标签"}]-(m) RETURN DISTINCT m.name limit 5'
# cypher_query = "MATCH (:ENTITY{name:taggsees})<-[:Tag{name:taggseessdasd}]-(m) RETURN DISTINCT m.name LIMIT 5"
cypher_query = "MATCH (:ENTITY{name:taggsees})<-[:Tag{name:taggseessdasd}]-(m) RETURN DISTINCT m.name"
# cypher_query = "MATCH (:ENTITY{name:})<-[:Tag{name}]-(m) RETURN DISTINCT m.name limit 5"
# cypher_query = "MATCH (:ENTITY{name:})<-[:Tag{name}]-(m) RETURN DISTINCT m.name limit 5"
# cypher_query = "MATCH (n1:human) RETURN n1.name"
# cypher_query = 'MATCH (n1:human) RETURN DISTINCT n1.name limit 5'
print(cypher_query)
ir = cyl_translator.to_ir(cypher_query)
print(ir)
print()

cypher_query1 = ir_translator.to_cypher(ir)
print(cypher_query1)
# print("--- - -- - -  -- - - - -- - - - - - - - -- -  ")
#
# ir = None
# cypher_query = "MATCH (e:ENTITY) OPTIONAL MATCH (e)<-[:Tag]-(t:Tag {name: taggseessdasd}) RETURN DISTINCT e.name AS name LIMIT 5"
# cypher_query = "MATCH (e:ENTITY) OPTIONAL MATCH (e)<-[:Tag]-(t:Tag {name: taggseessdasd}) RETURN DISTINCT e.name AS name"
# print(cypher_query)
# ir = cyl_translator.to_ir(cypher_query)
# print(ir)
# print()
#
# cypher_query1 = ir_translator.to_cypher(ir)
# print(cypher_query1)
# print("--- - -- - -  -- - - - -- - - - - - - - -- -  ")
#
# ir = None
# cypher_query = "MATCH (e:ENTITY) OPTIONAL MATCH (e)<-[:Tag]-(t:Tag {name: taggseessdasd}) WHERE e.name = taggsees RETURN DISTINCT e.name LIMIT 5"
#
# print(cypher_query)
# ir = cyl_translator.to_ir(cypher_query)
# print(ir)
#
# print()
#
# cypher_query1 = ir_translator.to_cypher(ir)
#
# print(cypher_query1)
# print("--- - -- - -  -- - - - -- - - - - - - - -- -  ")
#

while True:
    # 提示用户输入
    user_input = input("\n请输入一些信息: ")

    # 打印用户输入的内容
    print("你输入的内容是: " + user_input)
    print()
    ir = cyl_translator.to_ir(user_input)

    print(ir)
    print()
    cypher_query1 = ir_translator.to_cypher(ir)
    print(cypher_query1)


    # # 提示用户输入
    # user_input_ir = input("\n请输入一些信息iriririirir: ")
    #
    # # 打印用户输入的内容
    # print("你输入的内容是iriririirir: " + user_input_ir)
    # print()
    # cypher_query1 = ir_translator.to_cypher(user_input_ir)
    # print(cypher_query1)
