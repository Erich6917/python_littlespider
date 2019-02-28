# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding("utf-8")
import random
import jieba


def autotxt():
    # file = open(fname1)
    # string=file.read()
    # dataset_file=string.split()
    dataset_file = [
        "真理惟一可靠的标准就是永远自相符合。",
        "土地是以它的肥沃和收获而被估价的；才能也是土地，不过它生产的不是粮食，而是真理。如果只能滋生瞑想和幻想的话，即使再大的才能也只是砂地或盐池，那上面连小草也长不出来的。",
        "我需要三件东西：爱情友谊和图书。然而这三者之间何其相通！炽热的爱情可以充实图书的内容，图书又是人们最忠实的朋友。"
        "时间是一切财富中最宝贵的财富。",
        "世界上一成不变的东西，只有“任何事物都是在不断变化的”这条真理。",
    ]

    print("\n分词前：", dataset_file)
    for i, each_sentence in enumerate(dataset_file):
        dataset_file[i] = " ".join(jieba.cut(each_sentence))
        print("\n分词后：", dataset_file)
    model = {}

    for line in dataset_file:
        line = line.lower().split()
        for i, word in enumerate(line):
            if i == len(line) - 1:
                model['END'] = model.get('END', []) + [word]
            else:
                if i == 0:
                    model['START'] = model.get('START', []) + [word]
                model[word] = model.get(word, []) + [line[i + 1]]
    print("\n模型：", model)
    generated = []
    while True:
        if not generated:
            words = model['START']
        elif generated[-1] in model['END']:
            break
        else:
            words = model[generated[-1]]
        generated.append(random.choice(words))

    print 'rtmsg:'
    print ''.join(generated)
    # print("\n生成的一个结果：" + "".join(generated))
    # file.close()


#########################
autotxt()
