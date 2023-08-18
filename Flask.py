from flask import Flask, request, jsonify, render_template
import re
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/preprocess_text", methods=["POST"])
def preprocess_text():

                 # **分句整理部份**
    # 删除类似以下一种
    input_text = request.json["text"]
    output = re.sub("以下.种|如下|下列", "以下", input_text)
    # 删除内部句号
    lines = output.split("\n")
    contents = ""
    for line in lines:
        if not line.startswith("（") and "。" in line[:-1]:
            line = line.replace("。", "。\n")
        line += "\n"
        contents += line

    contents = contents.replace("\n\n", "\n")
    contents = contents.replace(" \n", "\n")

    a = r"：\n（1(） [^\n]*。\n（[0-9])+"
    for match in re.finditer(a, contents):
        f = ''
        sentences = match.group(0)
        new_sentences = sentences.replace("。\n", "；\n")
        contents = contents.replace(match.group(0), new_sentences)
    content = re.sub(r"([^；。\n])；(?=[^；。\n])", r"\1。", contents)

    b = r"(\n.+以下.+：\n)((（.+?[。；]\n)+)"
    for match in re.finditer(b, content):
        f = ''
        sentences = match.group(0)
        first_sentence = match.group(1)
        other_sentences = match.group(2)
        other_sentences = other_sentences.replace("\n", "")
        print(other_sentences)
        osentences = other_sentences.split("；")
        # print(  osentences)
        osentences = [re.sub(r"（\d+） |。", "", sentence) for sentence in osentences]
        # osentences = [a.replace("\n","") for a in osentences]
        # print(osentences)
        for i in range(len(osentences)):
            aa = first_sentence.replace("以下", osentences[i], 1)
            # print(aa)
            f += aa
            # print(f)
        f = f.replace("\n\n", "\n")
        f = f.replace("：\n", "。\n")
        content = content.replace(match.group(0), f)
    # print(content)
    # content = content.replace("：\n","。\n")

    # In[97]:

    b = r"(\n（\d+）.+以下.+：)((\n\d+）.+[；。])+)"
    for match in re.finditer(b, content):
        f2 = ''
        sentences = match.group(0)
        first_sentence = match.group(1)
        other_sentences = match.group(2)
        other_sentences = other_sentences.replace("。\n（", "；\n（")
        # print(first_sentence)
        osentences = other_sentences.split("；")
        osentences = [re.sub(r"\n\d+） |。", "", sentence) for sentence in osentences]
        # print(osentences)
        for i in range(len(osentences)):
            bb = first_sentence.replace("以下", osentences[i], 1)
            f2 += bb
        # f= f.replace("\n\n","\n")
        f2 = f2.replace("：\n", "。\n")
        content = content.replace(match.group(0), f2)
    # print(content)
    # 本段研究1）形式 或许a、b的顺序也值得研究，目前影响不大

    c = r"(\n.+包括：\n)((（.+?[。；]\n)+)"
    for match in re.finditer(c, content):
        f = ''
        sentences = match.group(0)
        first_sentence = match.group(1)
        other_sentences = match.group(2)
        other_sentences = other_sentences.replace("\n", "")
        # other_sentences = other_sentences.replace("。\n（","；\n（")
        # print( other_sentences)
        osentences = other_sentences.split("；")
        osentences = [re.sub(r"（\d+） |。", "", sentence) for sentence in osentences]
        # print(osentences)
        for i in range(len(osentences)):
            aa = first_sentence.replace("：", osentences[i] + "。", 1)
            # print(aa)
            f += aa
            # print(f)
        f = f.replace("。。", "。")
        f = f.replace("\n\n", "\n")
        content = content.replace(match.group(0), f)
    # print(content)
    # 本段主要研究包括：（1）形式

    d = r"(\n.+顺序以下：)((\n（.+?[。；])+)"
    for match in re.finditer(d, content):
        sentences = match.group(0)
        first_sentence = match.group(1)
        other_sentences = match.group(2)
        other_sentences = other_sentences.replace("\n", "")
        osentences = other_sentences.split("；")
        osentences = [re.sub(r"（\d+） ", "", sentence) for sentence in osentences]
        # print(osentences)
        dd = ""
        for i in osentences:
            i += "、"
            dd += i
        dd = dd[:-1]
        first_sentence += dd
        content = content.replace(match.group(0), first_sentence.replace("以下：", "为"))
    # print(content)
    # 本段主要研究优先顺序以下：

    # In[100]:

    e = r"(\n.+[除专用合同条件另有约定外|应|则|承包人|发包人][^为\n]*：\n)((（.+?[。；]\n)+)"
    for match in re.finditer(e, content):
        f = ''
        sentences = match.group(0)
        first_sentence = match.group(1)
        other_sentences = match.group(2)
        other_sentences = other_sentences.replace("\n", "")
        # other_sentences = other_sentences.replace("。\n（","；\n（")
        # print( other_sentences)
        osentences = other_sentences.split("；")
        osentences = [re.sub(r"（\d+） |。", "", sentence) for sentence in osentences]
        # print(osentences)
        for i in range(len(osentences)):
            aa = first_sentence.replace("：", osentences[i] + "。", 1)
            # print(aa)
            f += aa
            # print(f)
        f = f.replace("。。", "。")
        f = f.replace("\n\n", "\n")
        content = content.replace(match.group(0), f)
    # 遗留问题：但在第(5)目的情况下，承包人无须提前告知发包人其解除合同意向，可直接发出正式解除合同通知立即解除合同：
    # 语义缺失了！
    content = content.replace("：\n", "。\n")
    content = content.replace("：", "")
    # ：之后换成。再分句
    content = content.replace("；", "。")
    content = re.sub(r"。([^\na-zA-Z…])", r"。\n\1", content)  # 考虑了某些公式

             # 内部整理部分(不改变句子个数)

    import codecs

    lines = content.replace('\n', '*').strip('*').split('*')
    preprocessed_lines = []
    preprocess = ''
    i = 0
    for line in lines:
        # Remove lines that match the pattern "第X条 一般约定" or "X.X 词语定义和解释"
        if not re.match(r"((^第[0-9]{1,2}条 |^\d+\.\d+ )[^\n]*)|^[0-9]{1,2}(\.\d+){1,2}\.[0-9]{1,2} [^\n，。；：]*$", line):
            # Remove the numbers at the beginning of lines that match the pattern "X.X.X.X "
            line = re.sub(r"^[0-9]{1,2}(\.[0-9]{1,2}){0,3} ", "", line)
            # Remove expressions such as "第X.X款（条、项、目、种）[履约担保]" or "（如果有）"
            line = re.sub(r"第?[0-9]{1,2}\.[0-9]{1,2}款\[[^\]]*\]|第[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}款\[[^\]]*\]|（如果有）",
                          "", line)  # 1.26加？
            line = re.sub(
                r"第[0-9]{1,2}\.[0-9]{1,2}项\[[^\]]*\]|第[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}项\[[^\]]*\]|第[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{1,2}项",
                "", line)
            line = re.sub(r"第[0-9]{1,2}\.[0-9]{1,2}条\[[^\]]*\]|第[0-9]{1,2}条\[[^\]]*\]", "", line)
            line = re.sub(r"第（[0-9]）目", "", line)
            line = re.sub(r"第（[0-9]）种", "", line)

            # 去掉了七句例如（1）打头的标题
            line = re.sub(r"（[0-9]） [^\n。；：]*$", "", line)  # 1.26新补充

            line = re.sub(r"（[^）]*）[ ]?", "", line)

            # 还有类似附件6[价格指数权重表]——目前想法是直接把框删了就成
            # 去除标点及特殊符号
            line = re.sub(r"《|》|“|”|'|'", "", line)

            # # Replace "：是指"、"：指"、"：包括" with ""
            # line = re.sub(r"：是指|：指|：包括","", line)

            line = re.sub(r"和的", "的", line)  # 1.21新补充
            line = re.sub(r"(遵循|遵守|根据)的", r"\1", line)  # 需验证#1.24新补充
            if line != '':
                i += 1
                preprocess = preprocess + line + "\n"
                preprocessed_lines.append(line)

    # print(i)  # 1069句
    # preprocessed_lines

    return jsonify({"output": preprocess})

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True)
