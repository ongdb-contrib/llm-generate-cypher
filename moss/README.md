# 生成 Cypher 能力：MOSS VS ChatGLM

>&emsp;&emsp;MOSS介绍：MOSS 是复旦大学自然语言处理实验室发布的国内第一个对话式大型语言模型。MOSS是⼀个⽀持中英双语和多种插件的开源对话语⾔模型，moss-moon系列模型具有160亿参数，在FP16精度下可在单张A100/A800或两张3090显卡运⾏，在INT4/8精度下可在单张3090显卡运⾏。
>MOSS基座语⾔模型在约七千亿中英⽂以及代码单词上预训练得到，后续经过对话指令微调、插件增强学习和⼈类偏好训练具备多轮对话能⼒及使⽤多种插件的能⼒，MOSS的最⼤对话⻓度为2048（输⼊+输出）。
><br>
>&emsp;&emsp;局限性：由于模型参数量较⼩和⾃回归⽣成范式，MOSS仍然可能⽣成包含事实性错误的误导性回 复或包含偏⻅/歧视的有害内容，请谨慎鉴别和使⽤MOSS⽣成的内容，请勿将MOSS⽣成的有害 内容传播⾄互联⽹。若产⽣不良后果，由传播者⾃负。

>&emsp;&emsp;ChatGLM 是由清华大学 KEG 实验室和智谱 AI 基于千亿基座模型 GLM-130B 开发的对话语言模型。ChatGLM 在 GLM-130B 的基础上持续进行文本和代码预训练并通过有监督微调等技术实现人类意图对齐，具备文案写作、信息抽取、角色扮演、问答、对话等能力。

>&emsp;&emsp;下面测试结果为`MOSS`和`ChatGLM`两个大语言模型生成Cypher的展示，总体效果`MOSS`要好于`ChatGLM`。
>在六次测试中，只有`MOSS`在5和6案例中生成了完全正确可执行的Cypher（但是都多了一行注释），其它结果都不太好。
>从目前测试过的结果来看，正确生成Cypher的能力`GPT4 > GPT3.5 > MOSS > ChatGLM`。


1. QA:你好

>&emsp;&emsp;该问题`MOSS`生成了创建节点的Cypher，真实的目标是对于此类问题不生成Cypher，因此回答是错误的。
>`ChatGLM`无法生成Cypher，是正确的，但是`ChatGLM`的回复显得有些冗长。

```
RE-MOSS:

CREATE (n:Person {name:'你好'}) RETURN n 
```

```
RE-ChatGLM:

欢迎，有什么需要帮助的吗？

# 查询用户信息
user_id:int(什么是用户ID?), name:text(用户姓名), email:text(用户邮箱), password:text(用户密码)
        
# 查询订单信息
order_id:int(订单ID), customer_id:int(客户ID), product_id:int(产品ID), total:float(总价), status:text(状态：完成/未支付/取消)
        
# 查询用户订单
user_order:list(用户订单列表)
        
# 查询商品订单
product_order:list(商品订单列表)

请提供您的查询需求，我会尽力生成正确的Cypher语句。
```


2. QA:最近半导体上涨的原因是什么？

>&emsp;&emsp;该问题`MOSS`和`ChatGLM`都无法生成正确的Cypher，是正确的。
>但是`MOSS`和`ChatGLM`都回复了一个SQL，确实没有明白我在Prompt中定义的想生成Cypher的意图。

```
RE-MOSS:

SELECT * FROM cypher_example WHERE message = '最近半导体上涨的原因是什么？' 
```

```
RE-ChatGLM:

SELECT 
    CASE 
        WHEN A.column_name = 'reason' THEN 'reason' 
        WHEN A.column_name = 'bubble_up' THEN 'bubble_up' 
        WHEN A.column_name = 'bubble_down' THEN 'bubble_down' 
        WHEN A.column_name = 'stock_price' THEN 'stock_price' 
        WHEN A.column_name = 'future_price' THEN 'future_price' 
        ELSE 'default' 
        END AS reason 
     FROM 
        columns A 
     WHERE 
     A.table_name = 'stock' 
     ORDER BY 
     stock_price DESC 
LIMIT 1;
```


3. QA:海南有哪些上市公司？

>&emsp;&emsp;该问题`MOSS`生成了看似正确的Cypher，但是节点`n`是没有`name`属性的，`Cypher`运行没有结果。
> 给出的示例中是直接输出`节点变量`，而不是某个具体字段。
>`ChatGLM`没有生成正确的Cypher。
>`ChatGLM`回复了一个看似正确的Cypher但是语法有错误，单独复制粘贴后Cypher无法运行，另外结果中还多了一些废话。

```
RE-MOSS:

MATCH (n:股票)-[:地域]->(n2:地域) WHERE n2.name='海南' RETURN DISTINCT n.name as name LIMIT 10 
```

```
RE-ChatGLM:

match (n0：股票)-[r0：地域]->(n1：地域) WHERE n1.value='海南' return distinct n0 as n4 limit 10;

这是一条简单的Cypher查询，它匹配了一个股票向一个地域的反向匹配，并返回该股票的所有地区名称。请注意，此查询可能无法完全准确地返回所有海南上市公司的详细信息，因为它只返回了海南的股票。如果您需要更详细的信息，请提供更多上下文。
```

4. QA:电气设备行业有多少家上市公司？

>&emsp;&emsp;该问题`MOSS`没有生成Cypher，`ChatGLM`也没有生成正确的Cypher。
>`ChatGLM`也是回复了一个看似正确的Cypher但是语法有错误，单独复制粘贴后Cypher无法运行，另外结果中还多了一些废话。

```
RE-MOSS:

# 请问电气设备行业的公司名称是什么？
```

```
RE-ChatGLM:


match p0=(n0：股票)-[r0：所属行业]->(n1：行业) 
WHERE n1.value='电气设备'
RETURN COUNT(DISTINCT n0) AS n4;


该查询将返回电气设备行业中上市公司的总数量。请注意，该查询将返回所有股票，无论它们属于哪个行业。如果您只需要返回特定行业的数量，请在WHERE子句中更改该条件。
```

5. QA:水泥行业博士学历的男性高管有多少位？

>&emsp;&emsp;该问题`MOSS`生成了完全正确的Cypher（但是多了一行注释），`ChatGLM`没有生成正确的Cypher。
>`ChatGLM`回复了一个看似正确的Cypher但是语法有错误，单独复制粘贴后Cypher无法运行，但这次好一些废话没有了。

```
# RE-MOSS:

# 水泥行业博士学历的男性高管有多少位？
MATCH p0=(n1:行业)<-[r0:所属行业]-(n0:股票)<-[r1:任职于]-(n2:高管)-[r2:性别]->(n3:性别)-[r4:别名]->(n5:性别_别名), p1=(n2)-[r3:学历]->(n4:学历) WHERE n1.value='水泥' AND n5.value='男性' AND n4.value='博士' RETURN COUNT(DISTINCT n2) AS n3; 
```

```
RE-ChatGLM:

MATCH 
    p0=(n1：行业)<-[r0：所属行业]-(n0：股票)<-[r1：任职于]-(n2：高管)-[r2：性别]->(n3：性别)-[r4：别名]->(n5：性别_别名),
    p1=(n2)-[r3：学历]->(n4：学历) 
WHERE n1.value='水泥' AND n5.value='男性' AND n4.value='博士'
RETURN COUNT(DISTINCT n2) AS n3;
```

6. QA:在北京由硕士学历的女性高管任职的上市公司，都属于哪些行业？

>&emsp;&emsp;该问题`MOSS`生成了完全正确的Cypher（仍然多了一行注释），`ChatGLM`没有生成正确的Cypher。
>`ChatGLM`也是回复了一个看似正确的Cypher但是语法有错误，单独复制粘贴后Cypher无法运行，另外结果中仍然多了一些废话。

```
RE-MOSS:

# 在北京由硕士学历的女性高管任职的上市公司，都属于哪些行业？
MATCH p1=(n1:`地域`)<-[:`地域`]-(n2:`股票`)<-[:`任职于`]-(n3:`高管`)-[:`性别`]->(n4:`性别`), p2=(n3)-[:`学历`]->(n5:学历), p3=(n2)-[:`所属行业`]->(n6:行业) WHERE n1.value='北京' AND n5.value='硕士' AND n4.value='F' RETURN DISTINCT n6.value AS hy 
```

```
RE-ChatGLM:

match p1=(n1:`地域`)<-[:`地域`]-(n2:`股票`)<-[:`任职于`]-(n3:`高管`)-[:`性别`]->(n4:`性别`),
    p2=(n3)-[:`学历`]->(n5：学历),
    p3=(n2)-[:`所属行业`]->(n6：行业)
WHERE n1.value='北京' AND n5.value='硕士' AND n4.value='F'
RETURN DISTINCT n6.value AShy;

这是一个匹配“在北京由硕士学历的女性高管任职的上市公司”的三元组Cypher查询，使用了以下语法：

- `match`：匹配三元组中的元素。
- `p1`：匹配`n1`中的`地域`元素。
- `p2`：匹配`n3`中的`学历`元素。
- `p3`：匹配`n2`中的`所属行业`元素。
- `WHERE`：在查询条件中添加过滤条件。
- `n1.value='北京' AND n5.value='硕士' AND n4.value='F'`：过滤条件，只有“北京”和“硕士”且“女性”的高管才能任职上市公司。
- `RETURN DISTINCT n6.value AShy`：返回每个行业的代码值。

请注意，这个查询只匹配了北京的数据，并且只使用了硕士和女性这两个条件。如果有更多的条件，可能需要在查询条件中包含它们。
```
