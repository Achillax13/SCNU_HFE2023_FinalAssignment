# 导入相关库和应用接口密钥
import openai
import openpyxl as pyxl
import time
openai.api_key = input("Enter your API key:")

# 定义ChatGPT交互函数
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.8, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

#撰写默认提示
default_prompt = """
请你充当一个可以进行英语教学且教学语言简单易懂的Python IDLE\n
你拥有以下几个方面的知识：英语构词法（包括词根、词缀及词源学知识）、谐音记忆法、英语口语知识\n
你还可以使用wordfrequency.info查询英语单词的词频信息
接下来请你完成以下几个任务\n
Task1 使用构词法讲解目标单词的词源学知识\n
Task2 编写一个80字数以内的  生动有趣的小故事帮助学生记忆\n
Task3 使用谐音记忆法帮助学生记忆\n
Task4 给出一个英文例句，并用括号将中文释义标注在句子后面\n
Task5 使用wordfrequency.info查询目标单词的词频信息，仅输出一个词频数值，所有数值格式必须是integer，不得出现float或percentage\n
Task6 给出一个与目标单词对应的口语单词，使用wordfrequency.info查询这个口语词的词频信息，最终按照以下文本格式输出：口语词(词频数值)\n
Task7 用这个口语词替换上述英文例句中的目标单词，并用括号将中文释义标注在句子后面\n
Task8 给出一个与目标单词近义的学术单词，使用wordfrequency.info查询这个近义词的词频信息，最终按照以下文本格式输出：近义词(词频数值)\n
Task9 用这个近义词替换上述英文例句中的目标单词，并用括号将中文释义标注在句子后面\n
当你回答时，只需要以Python的字典格式给出，每一个任务及其回答对应的一个键值对，
也就是说，你只需要给我1个字典数据，这个字典里包含9个键值对，分别对应上述9个任务，
除此之外，你不需要使用多余的自然语言。\n
注意：你需要全程使用中文回答，并且仔细检查是否完成以上任务。\n
现在，我们需要学习的单词是：
"""
# 开始学习
wb = pyxl.load_workbook("待学单词.xlsx")
ws = wb["Sheet1"]
flag = 1
cost_time = []
while flag == 1:
    target_words = input("请输入想要学习的一个或多个单词（用半角逗号分割）：")
    words = target_words.split(",")
    for word in words: 
        prompt = default_prompt + word
        start_time = time.time()
        response=get_completion(prompt)
        end_time = time.time()
        duration = end_time-start_time
        cost_time.append(duration)
        with open('OuputExample.txt','w',encoding='utf-8') as exp:
            exp.write(response)
        res = eval(response)
        ink = [word]
        for i in range(1,10):
            ink.append(res["Task"+str(i)])
        ws.append(ink)
        print('已添加单词{}，用时{:.2f}秒'.format(word,duration))
    wb.save("待学单词.xlsx")
    print("---已成功添加{}个单词,平均用时{:.2f}秒---".format(len(words),sum(cost_time)/len(cost_time)))
    flag = eval(input("继续学习请输入1，退出请输入其他数字："))
# 结束学习
time.sleep(0.5)
print("本次程序运行结束，请及时学习哦，再见！")
