# Reference:https://medium.com/neo4j/context-aware-knowledge-graph-chatbot-with-gpt-4-and-neo4j-d3a99e8ae21e
import requests
import Levenshtein


# GPT-3.5 的最大长度是 4097 token，汉字=2token，英文=0.5 token。也就是 GPT-3.5 的上下文最多放弃 2k 汉字或 8k 英文字符 的内容。
# 文字输入限制提升至2.5万字：GPT-4.0可以接受更长的文字输入，达到2.5万字，比GPT-3.5的2048字（8k 英文字符）大幅增加。这意味着它可以处理更复杂和更全面的内容。
# 使用HTTP封装的GPT-3.5接口，请根据具体接口情况替换
def gpt3_5(msg):
    # 设置请求头
    headers = {"Content-type": "application/json"}
    url = 'http://localhost:8080/cgpt-api/push_question'
    data = {
        "ask_str": msg,
    }

    response = requests.post(url, json=data, headers=headers)
    return response.json()['data']['content']


# 从下面graph-qabot-demo可配置知识图谱问答项目中获取原始样例查询，然后将ID（ID为配置系统为Cypher生成）替换为具体的字段属性过滤，生成examples
# https://github.com/ongdb-contrib/graph-qabot
# https://github.com/ongdb-contrib/graph-qabot-demo
def example_list():
    ex_list = [{
        'qa': '火力发电行业博士学历的男性高管有多少位？',
        'cypher': '''
            MATCH 
                p0=(n1:行业)<-[r0:所属行业]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r4:别名]->(n5:性别_别名),
                p1=(n2)-[r3:学历]->(n4:学历) 
            WHERE n1.value='火力发电' AND n5.value='男性' AND n4.value='博士'
            RETURN COUNT(DISTINCT n2) AS n3;
            '''
    }, {
        'qa': '山西都有哪些上市公司？',
        'cypher': '''
            MATCH p0=(n0:股票)-[r0:地域]->(n1:地域) WHERE n1.value='山西' 
            RETURN DISTINCT n0 AS n4 LIMIT 10;
               '''
    }, {
        'qa': '富奥股份的高管都是什么学历？',
        'cypher': '''
                 MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:学历]->(n3:学历) 
            WHERE n1.value='富奥股份'
            RETURN DISTINCT n3 AS n2 LIMIT 10;
                   '''
    }, {
        'qa': '中国宝安属于什么行业？',
        'cypher': '''
                MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)-[r1:所属行业]->(n2:行业) 
            WHERE n1.value='中国宝安'
            RETURN DISTINCT n2 AS n5 LIMIT 10;
                       '''
    }, {
        'qa': '建筑工程行业有多少家上市公司？',
        'cypher': '''
                MATCH p0=(n0:股票)-[r0:所属行业]->(n1:行业) 
            WHERE n1.value='建筑工程'
            RETURN COUNT(DISTINCT n0) AS n4;
                           '''
    }, {
        'qa': '刘卫国是哪个公司的高管？',
        'cypher': '''
             MATCH p0=(n0:股票)<-[r0:任职于]-(n1:高管) 
            WHERE n1.value='刘卫国'
            RETURN DISTINCT n0 AS n4 LIMIT 10;
                            '''
    }, {
        'qa': '美丽生态上市时间是什么时候？',
        'cypher': '''
                MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)-[r1:上市日期]->(n2:上市日期) 
            WHERE n1.value='美丽生态'
            RETURN DISTINCT n2 AS n1 LIMIT 10;
                                '''
    }, {
        'qa': '山西的上市公司有多少家？',
        'cypher': '''
                MATCH p0=(n0:股票)-[r0:地域]->(n1:地域) 
            WHERE n1.value='山西'
            RETURN COUNT(DISTINCT n0) AS n4;
                                    '''
    }, {
        'qa': '博士学历的高管都有哪些？',
        'cypher': '''
                MATCH p0=(n0:高管)-[r0:学历]->(n1:学历) 
            WHERE n1.value='博士' 
            RETURN DISTINCT n0 AS n3 LIMIT 10;
                                        '''
    }, {
        'qa': '上市公司是博士学历的高管有多少个？',
        'cypher': '''
               MATCH p0=(n0:高管)-[r0:学历]->(n1:学历) 
            WHERE n1.value='博士'
            RETURN COUNT(DISTINCT n0) AS n3;
                                            '''
    }, {
        'qa': '刘卫国是什么学历？',
        'cypher': '''
                MATCH p0=(n0:高管)-[r0:学历]->(n1:学历) 
            WHERE n0.value='刘卫国'
            RETURN DISTINCT n1 AS n2 LIMIT 10;
                                                '''
    }, {
        'qa': '富奥股份的男性高管有多少个？',
        'cypher': '''
               MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r3:别名]->(n4:性别_别名) 
            WHERE n1.value='富奥股份' AND n4.value='男性'
            RETURN COUNT(DISTINCT n2) AS n3;
                                                    '''
    }, {
        'qa': '同在火力发电行业的上市公司有哪些？',
        'cypher': '''
                MATCH p0=(n0:股票)-[r0:所属行业]->(n1:行业) 
            WHERE n1.value='火力发电' 
            RETURN DISTINCT n0 AS n4 LIMIT 10;
                                                        '''
    }, {
        'qa': '同在火力发电行业的上市公司有多少家？',
        'cypher': '''
                MATCH p0=(n0:股票)-[r0:所属行业]->(n1:行业) 
            WHERE n1.value='火力发电'
            RETURN COUNT(DISTINCT n0) AS n4;
                                                            '''
    }, {
        'qa': '大悦城和荣盛发展是同一个行业嘛？',
        'cypher': '''
                MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)-[r1:所属行业]->(n2:行业) 
            WHERE n1.value IN ['大悦城','荣盛发展']
            RETURN DISTINCT n2 AS n5 LIMIT 10;
                                                                '''
    }, {
        'qa': '同在河北的上市公司有哪些？',
        'cypher': '''
                MATCH p0=(n0:股票)-[r0:地域]->(n1:地域) 
            WHERE n1.value='河北' 
            RETURN DISTINCT n0 AS n4 LIMIT 10;
                                                                    '''
    }, {
        'qa': '神州高铁是什么时候上市的？',
        'cypher': '''
               MATCH p0=(n1:股票名称)<-[r0:股票名称]-(n0:股票)-[r1:上市日期]->(n2:上市日期) 
            WHERE n1.value='神州高铁' 
            RETURN DISTINCT n2 AS n1 LIMIT 10;
                                                                       '''
    }, {
        'qa': '火力发电行业男性高管有多少个？',
        'cypher': '''
               MATCH p0=(n1:行业)<-[r0:所属行业]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r3:别名]->(n4:性别_别名) 
            WHERE n1.value='火力发电' AND n4.value='男性'
            RETURN COUNT(DISTINCT n2) AS n3;
                                                                          '''
    }, {
        'qa': '2023年三月六日上市的股票代码？',
        'cypher': '''
               MATCH p0=(n0:股票)-[r0:上市日期]->(n1:上市日期) 
            WHERE (n1.value>=20230306 AND n1.value<=20230306) 
            RETURN DISTINCT n0 AS n4 LIMIT 10;
                                                                             '''
    }, {
        'qa': '2023年三月六日上市的股票有哪些？',
        'cypher': '''
               MATCH p0=(n0:股票)-[r0:上市日期]->(n1:上市日期) 
            WHERE (n1.value>=20230306 AND n1.value<=20230306) 
            RETURN DISTINCT n0 AS n4 LIMIT 10;
                                                                                 '''
    }, {
        'qa': '2023年三月六日上市的股票有多少个？',
        'cypher': '''
                MATCH p0=(n0:股票)-[r0:上市日期]->(n1:上市日期) 
            WHERE (n1.value>=20230306 AND n1.value<=20230306) 
            RETURN COUNT(DISTINCT n0) AS n4;
                                                                                     '''
    }, {
        'qa': '胡永乐是什么性别？',
        'cypher': '''
                 MATCH p0=(n0:高管)-[r0:性别]->(n1:性别) 
            WHERE n0.value='胡永乐' 
            RETURN DISTINCT n1 AS n7 LIMIT 10;
                                                                                         '''
    }, {
        'qa': '在山东由硕士学历的男性高管任职的上市公司，都属于哪些行业？',
        'cypher': '''
               MATCH 
    	        p1=(n1:`地域`)<-[:`地域`]-(n2:`股票`)<-[:`任职于`]-(n3:`高管`)-[:`性别`]->(n4:`性别`),
                p2=(n3)-[:`学历`]->(n5:学历),
                p3=(n2)-[:`所属行业`]->(n6:行业)
            WHERE n1.value='山东' AND n5.value='硕士' AND n4.value='M'
            RETURN DISTINCT n6.value AS hy;
                                                                                            '''
    }]
    return ex_list


def examples(ask):
    examples_str = ''
    examples_list = []
    for index, map in enumerate(example_list()):
        qa = map['qa']
        cypher = map['cypher']
        dis = Levenshtein.distance(ask, qa)
        examples_list.append({'qa': qa, 'cypher': cypher, 'dis': dis})

    sorted_list = sorted(examples_list, key=lambda map: map['dis'])

    for map in sorted_list:
        qa = map['qa']
        cypher = map['cypher']
        dis = map['dis']
        ex = f'''
          # {qa}
          {cypher}
          '''
        # `prompt(ask)` Prompt Length 300
        if dis < 6 and len(examples_str + ex) + 300 <= 2048:
            examples_str += ex

    return examples_str


def prompt(ask):
    return f"""
        您是一名助手，能够根据示例Cypher查询生成Cypher查询。
        示例Cypher查询有：\n {examples(ask)} \n
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

    # This model's maximum context length is 4097 tokens.
    # However, you requested 4364 tokens (2316 in the messages, 2048 in the completion).
    # Please reduce the length of the messages or completion.
    print(gpt3_5(prompt(ask)))

# Test Result:
#   GPT4每个请求响应时间为22秒左右，GPT3.5每个请求响应时间为12秒左右；
#   当库中存在与当前问题相似的`examples`配置时，Cypher生成效果差不多；
#   当库中不存在与当前问题相似的`examples`配置时，GPT4不会生成Cypher，GPT3.5会使用网络资料生成Cypher，脱离当前Prompt的要求。

# QA:你好
# RE-GPT4（正确生成）:请提供您希望查询的信息，以便我为您生成相应的Cypher查询语句。如果可以，请提供与示例Cypher查询相似的信息和要求。
# RE-GPT3.5（正确生成）:无法根据示例Cypher查询推断出生成Cypher查询的特定上下文。请提供更具体的问题或信息。

# QA:最近半导体上涨的原因是什么？
# RE-GPT4（正确生成）:您好，根据提供的Cypher示例，我无法为您生成关于 "最近半导体上涨的原因是什么" 的Cypher查询。请提供与您需求相关的Cypher查询示例以便我为您提供有效的查询语句。
# RE-GPT3.5（错误生成）:
#   MATCH (c:Company)-[r:CAUSED]->(p:Price)
#   WHERE c.name = '半导体' AND r.reason = '上涨'
#   RETURN r.reason, p.reason

# QA:海南有哪些上市公司？
# RE-GPT4（正确生成）:
#   MATCH p0=(n0:股票)-[r0:地域]->(n1:地域) WHERE n1.value='海南'
#   RETURN DISTINCT n0 AS n4 LIMIT 10
# RE-GPT3.5（正确生成）:
#   MATCH p0=(n0:股票)-[r0:地域]->(n1:地域) WHERE n1.value='海南'
#   RETURN DISTINCT n0 AS n4 LIMIT 10;

# QA:电气设备行业有多少家上市公司？
# RE-GPT4（正确生成）:
#   MATCH p0=(n0:股票)-[r0:所属行业]->(n1:行业)
#   WHERE n1.value='电气设备'
#   RETURN COUNT(DISTINCT n0) AS n4
# RE-GPT3.5（正确生成）:
#   MATCH p0=(n0:股票)-[r0:所属行业]->(n1:行业)
#   WHERE n1.value='电气设备'
#   RETURN COUNT(DISTINCT n0) AS n4;

# QA:水泥行业博士学历的男性高管有多少位？
# RE-GPT4（正确生成）:
#   MATCH
#       p0=(n1:行业)<-[r0:所属行业]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r4:别名]->(n5:性别_别名),
#       p1=(n2)-[r3:学历]->(n4:学历)
#   WHERE n1.value='水泥' AND n5.value='男性' AND n4.value='博士'
#   RETURN COUNT(DISTINCT n2) AS n3
# RE-GPT3.5（正确生成）:
#   MATCH
#       p0=(n1:行业)<-[r0:所属行业]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r4:别名]->(n5:性别_别名),
#       p1=(n2)-[r3:学历]->(n4:学历)
#   WHERE n1.value='水泥' AND n5.value='男性' AND n4.value='博士'
#   RETURN COUNT(DISTINCT n2) AS n3;

# QA:在北京由硕士学历的女性高管任职的上市公司，都属于哪些行业？
# RE-GPT4（正确生成）:
#   MATCH
#       p1=(n1:地域)<-[:地域]-(n2:股票)<-[:任职于]-(n3:高管)-[:性别]->(n4:性别),
#       p2=(n3)-[:学历]->(n5:学历),
#       p3=(n2)-[:所属行业]->(n6:行业)
#   WHERE n1.value='北京' AND n5.value='硕士' AND n4.value='F'
#   RETURN DISTINCT n6.value AS hy
# RE-GPT3.5:
#   MATCH
#       p1=(n1:`地域`)<-[:`地域`]-(n2:`股票`)<-[:`任职于`]-(n3:`高管`)-[:`性别`]->(n4:`性别`),
#       p2=(n3)-[:`学历`]->(n5:学历),
#       p3=(n2)-[:`所属行业`]->(n6:行业)
#   WHERE n1.value='北京' AND n5.value='硕士' AND n4.value='F'
#   RETURN DISTINCT n6.value AS hy;

