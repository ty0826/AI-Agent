import numpy as np

"""
计算两个向量的余弦相似度（衡量方向相似性，剔除长度影响）

参数：
    vec_a (np.array): 向量A
    vec_b (np.array): 向量B
返回：
    float: 余弦相似度结果（范围[-1,1]，越接近1方向越一致）
公式：
    cos_sim = (vec_a · vec_b) / (||vec_a|| × ||vec_b||)
    拆解：
    1. 点积：vec_a · vec_b = vec_a[0]×vec_b[0] + vec_a[1]×vec_b[1] + ... + vec_a[n]×vec_b[n]
    2. 模长：||vec_a|| = √(vec_a[0]² + vec_a[1]² + ... + vec_a[n]²)
    3. 模长：||vec_b|| = √(vec_b[0]² + vec_b[1]² + ... + vec_b[n]²)

A: [0.5, 0.5]
B: [0.7, 0.7]
C: [0.7, 0.5]
D: [-0.6, -0.5]
"""


# 计算两个的点积
def cos_sim(list1, list2):
    sum1 = 0
    for a, b in zip(list1, list2):
        sum1 = sum1 + a * b
    return sum1


# 计算模长
def cos_sim2(list):
    sum2 = 0
    for a in list:
        sum2 = sum2 + a * a
    return np.sqrt(sum2)


# 计算余弦相似度
def vec_a(list1, list2):
    result = cos_sim(list1, list2) / (cos_sim2(list1) * cos_sim2(list2))
    print(result)
    return result


vec_a([0.5, 0.5], [0.7, 0.7])
vec_a([0.5, 0.5], [0.7, 0.5])
vec_a([0.5, 0.5], [-0.7, -0.5])
