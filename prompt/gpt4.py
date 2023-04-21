# Reference:https://medium.com/neo4j/context-aware-knowledge-graph-chatbot-with-gpt-4-and-neo4j-d3a99e8ae21e
import requests


# 使用HTTP封装的GPT-4接口，请根据具体接口情况替换
def gpt4(msg):
    # 设置请求头

    headers = {"Content-type": "application/json"}
    url = 'http://localhost:8080/cgpt-api/gpt4_question'
    data = {
        "ask_str": msg,
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()['data']['content']


# 从下面graph-qabot-demo可配置知识图谱问答项目中获取原始样例查询，然后将ID（ID为配置系统为Cypher生成）替换为具体的字段属性过滤，生成examples
# https://github.com/ongdb-contrib/graph-qabot
# https://github.com/ongdb-contrib/graph-qabot-demo
def examples():
    return '''
            # 火力发电行业博士学历的男性高管有多少位？
            MATCH 
                p0=(n1:行业)<-[r0:所属行业]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r4:别名]->(n5:性别_别名),
                p1=(n2)-[r3:学历]->(n4:学历) 
            WHERE n1.value='火力发电' AND n5.value='男性' AND n4.value='博士'
            RETURN COUNT(DISTINCT n2) AS n3

            # 山西都有哪些上市公司？
            MATCH p0=(n0:股票)-[r0:地域]->(n1:地域) WHERE n1.value='山西' 
            RETURN DISTINCT n0 AS n4 LIMIT 10

            # 富奥股份的高管都是什么学历？
            MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:学历]->(n3:学历) 
            WHERE n1.value='富奥股份'
            RETURN DISTINCT n3 AS n2 LIMIT 10

            # 中国宝安属于什么行业？
            MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)-[r1:所属行业]->(n2:行业) 
            WHERE n1.value='中国宝安'
            RETURN DISTINCT n2 AS n5 LIMIT 10

            # 建筑工程行业有多少家上市公司？
            MATCH p0=(n0:股票)-[r0:所属行业]->(n1:行业) 
            WHERE n1.value='建筑工程'
            RETURN COUNT(DISTINCT n0) AS n4

            # 刘卫国是哪个公司的高管？
            MATCH p0=(n0:股票)<-[r0:任职于]-(n1:高管) 
            WHERE n1.value='刘卫国'
            RETURN DISTINCT n0 AS n4 LIMIT 10

            # 美丽生态上市时间是什么时候？
            MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)-[r1:上市日期]->(n2:上市日期) 
            WHERE n1.value='美丽生态'
            RETURN DISTINCT n2 AS n1 LIMIT 10

            # 山西的上市公司有多少家？
            MATCH p0=(n0:股票)-[r0:地域]->(n1:地域) 
            WHERE n1.value='山西'
            RETURN COUNT(DISTINCT n0) AS n4

            # 博士学历的高管都有哪些？
            MATCH p0=(n0:高管)-[r0:学历]->(n1:学历) 
            WHERE n1.value='博士' 
            RETURN DISTINCT n0 AS n3 LIMIT 10

            # 上市公司是博士学历的高管有多少个？
            MATCH p0=(n0:高管)-[r0:学历]->(n1:学历) 
            WHERE n1.value='博士'
            RETURN COUNT(DISTINCT n0) AS n3

            # 刘卫国是什么学历？
            MATCH p0=(n0:高管)-[r0:学历]->(n1:学历) 
            WHERE n0.value='刘卫国'
            RETURN DISTINCT n1 AS n2 LIMIT 10

            # 富奥股份的男性高管有多少个？
            MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r3:别名]->(n4:性别_别名) 
            WHERE n1.value='富奥股份' AND n4.value='男性'
            RETURN COUNT(DISTINCT n2) AS n3

            # 同在火力发电行业的上市公司有哪些？
            MATCH p0=(n0:股票)-[r0:所属行业]->(n1:行业) 
            WHERE n1.value='火力发电' 
            RETURN DISTINCT n0 AS n4 LIMIT 10

            # 同在火力发电行业的上市公司有多少家？
            MATCH p0=(n0:股票)-[r0:所属行业]->(n1:行业) 
            WHERE n1.value='火力发电'
            RETURN COUNT(DISTINCT n0) AS n4

            # 大悦城和荣盛发展是同一个行业嘛？
            MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)-[r1:所属行业]->(n2:行业) 
            WHERE n1.value IN ['大悦城','荣盛发展']
            RETURN DISTINCT n2 AS n5 LIMIT 10

            # 同在河北的上市公司有哪些？
            MATCH p0=(n0:股票)-[r0:地域]->(n1:地域) 
            WHERE n1.value='河北' 
            RETURN DISTINCT n0 AS n4 LIMIT 10

            # 神州高铁是什么时候上市的？
            MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)-[r1:上市日期]->(n2:上市日期) 
            WHERE n1.value='神州高铁' 
            RETURN DISTINCT n2 AS n1 LIMIT 10

            # 火力发电行业男性高管有多少个？
            MATCH p0=(n1:行业)<-[r0:所属行业]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r3:别名]->(n4:性别_别名) 
            WHERE n1.value='火力发电' AND n4.value='男性'
            RETURN COUNT(DISTINCT n2) AS n3

            # 2023年三月六日上市的股票代码？
            MATCH p0=(n0:股票)-[r0:上市日期]->(n1:上市日期) 
            WHERE (n1.value>=20230306 AND n1.value<=20230306) 
            RETURN DISTINCT n0 AS n4 LIMIT 10

            # 2023年三月六日上市的股票有哪些？
            MATCH p0=(n0:股票)-[r0:上市日期]->(n1:上市日期) 
            WHERE (n1.value>=20230306 AND n1.value<=20230306) 
            RETURN DISTINCT n0 AS n4 LIMIT 10

            # 2023年三月六日上市的股票有多少个？
            MATCH p0=(n0:股票)-[r0:上市日期]->(n1:上市日期) 
            WHERE (n1.value>=20230306 AND n1.value<=20230306) 
            RETURN COUNT(DISTINCT n0) AS n4

            # 胡永乐是什么性别？
            MATCH p0=(n0:高管)-[r0:性别]->(n1:性别) 
            WHERE n0.value='胡永乐' 
            RETURN DISTINCT n1 AS n7 LIMIT 10

            # 在山东由硕士学历的男性高管任职的上市公司，都属于哪些行业？
            MATCH 
    	        p1=(n1:`地域`)<-[:`地域`]-(n2:`股票`)<-[:`任职于`]-(n3:`高管`)-[:`性别`]->(n4:`性别`),
                p2=(n3)-[:`学历`]->(n5:学历),
                p3=(n2)-[:`所属行业`]->(n6:行业)
            WHERE n1.value='山东' AND n5.value='硕士' AND n4.value='M'
            RETURN DISTINCT n6.value AS hy
        '''


def prompt(ask):
    return f"""
        您是一名助手，能够根据示例Cypher查询生成Cypher查询。
        示例Cypher查询有：\n {examples()} \n
        除了Cypher查询之外，不要回复任何解释或任何其他信息。
        您永远不要为你的不准确回复感到抱歉，并严格根据提供的cypher示例生成cypher语句。
        不要提供任何无法从Cypher示例中推断出的Cypher语句。
        当由于缺少对话上下文而无法推断密码语句时，通知用户，并说明缺少的上下文是什么。
        现在请为这个查询生成Cypher:
        # {ask}
        """


if __name__ == '__main__':
    # 输入问题
    ask = '在北京由硕士学历的女性高管任职的上市公司，都属于哪些行业？'

    print(gpt4(prompt(ask)))

# GPT-4 Test Result:
# QA:你好（正确生成）
# RE:请提供您希望查询的信息，以便我为您生成相应的Cypher查询语句。如果可以，请提供与示例Cypher查询相似的信息和要求。

# QA:最近半导体上涨的原因是什么？（正确生成）
# RE:您好，根据提供的Cypher示例，我无法为您生成关于 "最近半导体上涨的原因是什么" 的Cypher查询。请提供与您需求相关的Cypher查询示例以便我为您提供有效的查询语句。

# QA:海南有哪些上市公司？（正确生成）
# RE:
#   MATCH p0=(n0:股票)-[r0:地域]->(n1:地域) WHERE n1.value='海南'
#   RETURN DISTINCT n0 AS n4 LIMIT 10

# QA:电气设备行业有多少家上市公司？（正确生成）
# RE:
#   MATCH p0=(n0:股票)-[r0:所属行业]->(n1:行业)
#   WHERE n1.value='电气设备'
#   RETURN COUNT(DISTINCT n0) AS n4

# QA:水泥行业博士学历的男性高管有多少位？（正确生成）
# RE:
#   MATCH
#       p0=(n1:行业)<-[r0:所属行业]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r4:别名]->(n5:性别_别名),
#       p1=(n2)-[r3:学历]->(n4:学历)
#   WHERE n1.value='水泥' AND n5.value='男性' AND n4.value='博士'
#   RETURN COUNT(DISTINCT n2) AS n3

# QA:在北京由硕士学历的女性高管任职的上市公司，都属于哪些行业？
# RE:
#   MATCH
#       p1=(n1:地域)<-[:地域]-(n2:股票)<-[:任职于]-(n3:高管)-[:性别]->(n4:性别),
#       p2=(n3)-[:学历]->(n5:学历),
#       p3=(n2)-[:所属行业]->(n6:行业)
#   WHERE n1.value='北京' AND n5.value='硕士' AND n4.value='F'
#   RETURN DISTINCT n6.value AS hy
