#coding:utf-8

import codecs

def convert_str_to_vec(input_str):
    output_vec = []
    hira_lists = [\
            [u"ア", u"イ", u"ウ", u"エ", u"オ"],\
            [u"ァ", u"ィ", u"ゥ", u"ェ", u"ォ"],\
            [u"カ", u"キ", u"ク", u"ケ", u"コ"],\
            [u"ガ", u"ギ", u"グ", u"ゲ", u"ゴ"],\
            [u"サ", u"シ", u"ス", u"セ", u"ソ"],\
            [u"ザ", u"ジ", u"ズ", u"ゼ", u"ゾ"],\
            [u"タ", u"チ", u"ツ", u"テ", u"ト"],\
            [u"ダ", u"ヂ", u"ヅ", u"デ", u"ド"],\
            [u"ナ", u"ニ", u"ヌ", u"ネ", u"ノ"],\
            [u"ハ", u"ヒ", u"フ", u"ヘ", u"ホ"],\
            [u"バ", u"ビ", u"ブ", u"ベ", u"ボ"],\
            [u"パ", u"ピ", u"プ", u"ペ", u"ポ"],\
            [u"マ", u"ミ", u"ム", u"メ", u"モ"],\
            [u"ヤ", u"", u"ユ", u"", u"ヨ"],\
            [u"ャ", u"", u"ュ", u"", u"ョ"],\
            [u"ラ", u"リ", u"ル", u"レ", u"ロ"],\
            [u"ワ", u"ヰ", u"", u"ヱ", u"ヲ"]]

    for char in input_str:
        consonant_vec = [0] * 20
        vowel_vec = [0] * 5
        if char == u"ン":
            consonant_vec[17] = 1
        elif char == u"ー":
            consonant_vec[18] = 1
        elif char == u"ッ":
            consonant_vec[19] = 1
        elif char == u"ヴ":
            consonant_vec[10] = 1
            vowel_vec[2] = 1
        else:
            for i, hira_list in enumerate(hira_lists):
                if char in hira_list:
                    index = hira_list.index(char)
                    consonant_vec[i] = 1
                    vowel_vec[index] = 1
                    break

        output_vec.append(consonant_vec + vowel_vec)

    return output_vec


def make_input_vec_list(string_list, max_num_step):
    output_list = []
    for string in string_list:
        convert_list = convert_str_to_vec(string)
        if len(convert_list) < max_num_step:
            #zero padding
            #len(convert_list[0]) is v_size
            pad_list = [[0 for i in range(len(convert_list[0]))] for j in range(max_num_step - len(convert_list))]
            convert_list = convert_list + pad_list
        output_list.append(convert_list)

    return output_list


def make_label(input_str, answer_str, max_num_step):
    output_vec = [[1, 0] for i in range(max_num_step)]
    used_list = []
    for i, c in enumerate(input_str):
        if c in answer_str and c not in used_list:
            output_vec[i] = [0, 1]
            used_list.append(c)
    return output_vec


def make_label_list(string_list, answer_str_list, max_num_step):
    output_list = []
    for string, answer in zip(string_list, answer_str_list):
        output_list.append(make_label(string, answer, max_num_step))
    return output_list


def read_file(file_path):
    str_list = []
    answer_list = []

    with codecs.open(file_path, "r", "UTF-8") as f:
        line = f.readline()
        while line:
            line = line.split("\n")[0]
            str_list.append(line.split(",")[0])
            answer_list.append(line.split(",")[1])
            line = f.readline()

    return str_list, answer_list
