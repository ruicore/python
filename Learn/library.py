# -*- coding: utf-8 -*-
# @Author:             何睿
# @Create Date:        2018-08-05 20:49:57
# @Last Modified by:   何睿
# @Last Modified time: 2018-08-05 21:22:06

import re
import os
import codecs
import imghdr
import PIL.Image
import collections
import glob
import chardet
from itertools import combinations

# 统计英文文章的所有英文单词数


def calculate_english_words_in_text(filepath):
    words_count = 0
    try:
        with codecs.open(filepath, 'r', 'utf-8') as target:
            for line in target.readlines():
                words = re.findall("[a-zA-Z]+'*-*[a-zA-Z]*", line)
                words_count += len(words)
        return words_count
    except IOError:
        print("文件读取失败，请检查文件路径")


# 把图片缩小至指定大小
def change_resoultion_to_less(pic_folder, re_w=1136, re_h=640):
    for pic_name in os.listdir(pic_folder):
        pic_path = os.path.join(pic_folder, pic_name)
        if imghdr.what(pic_path) == 'jpeg':
            with PIL.Image.open(pic_path) as target:
                w, h = target.size
                n = w / re_w if w / re_w >= h / re_h else h / re_h
                nw = int(w / n)
                nh = int(h / n)
                target.resize((nw, nh))
                target.save(pic_folder + '\\' + "resize" +
                            pic_name.split('.')[0] + '.jpg', 'jpeg')


def not_empty(s):
    return s and s.strip()


# 统计txt文件中的词频，file_path为文件路径，frerecy统计前%个单词
def count_word_frequency_in_txt(file_path, frecency):
    with codecs.open(file_path, 'r', 'utf-8') as file:
        words = []
        for line in file:
            content = re.sub(r"\"|,|\.|\”|\“|\‘|\t", " ", line)
            words.extend(content.strip().split(' '))
            # 去掉空字符
            res = filter(not_empty, words)
    return collections.Counter(res).most_common(int(abs(frecency)))


# 判断文件的编码格式,参数为完整路径名，返回格式编码
def get_charcode(file):
    with open(file, 'rb') as f:
        content = f.read()
        return (chardet.detect(content).get('encoding'))


# 得到父文件夹下的所有文件夹，参数为父文件夹路径，返回包含路径的set
def get_all_folders(directory):
    directorys = set()
    for dir_path, dir_names, file_names in os.walk(directory):
        for dir_name in dir_names:
            path = dir_path + "\\" + dir_name
            directorys.add(path)
            file_names=file_names
    return directorys


# 得到父文件夹下指定文件类型（文件名后缀）文件的完整路径，如果没有指定，则返回所有文件的完整路径，
def get_all_files(directory, filetype=None):
    directorys = []
    for dir_path, dir_names, file_names in os.walk(directory):
        # 如果输入了文件类型，则按类型查找
        if filetype:
            try:
                directorys += glob.glob(dir_path + '\\*.' + filetype)
            except Exception as e:
                print(e)
        # 如果没有输入，则返回所有的文件
        else:
            for file_name in file_names:
                path = dir_path + "\\" + file_name
                directorys.append(path)
        dir_names = dir_names
    return directorys


# 输入文件路径，返回文件名称
def get_file_name(path):
    try:
        return path.split('\\')[len(path.split('\\')) - 1]
    except Exception as e:
        print(e)


# 输入参数：string，返回参数：string
# 功能： 去掉string中的中文字符
def remove_chinese_punctuation(string):
    return re.sub(
        r"[A-Za-z0-9\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）“”：；《》？:=>【】-]+", "",
        string)


"""
输入参数：
        keywords 需要形成组合的关键词,list类型；
        words    需要匹配的单词,list类型
        nearby_words_num 求组和的最大相邻个数，默认为15
        combination_num  每个组合的个数，默认为2
返回格式:
        ['补偿', '风险', 2],list类型
"""


def calculate_nearby_words(keywords, words, nearby_words_num=15, combination_num=2):
    # 关键词的不同组合方式
    keywords_combinations = []
    # 对关键词的组合排序
    for item in list(combinations(keywords, combination_num)):
        keywords_combinations.append(sorted(item))
    # 记录每个组合的次数，初始化为0
    times_every_combination = [0 for i in range(len(keywords_combinations))]
    son_words_one = words[0:nearby_words_num]
    son_words_two = words[nearby_words_num]
    combination_temp = []
    for item in list(combinations(son_words_one, combination_num)):
        combination_temp.append(sorted(item))
    for item in combination_temp:
        if item in keywords_combinations:
            times_every_combination[keywords_combinations.index(item)] += 1
    start_positon = 1
    for i in range(nearby_words_num, len(words)):
        son_words_one = words[start_positon:start_positon+nearby_words_num-1]
        son_words_two = words[start_positon +
                              nearby_words_num-1:start_positon+nearby_words_num]
        start_positon += 1
        if son_words_two[0] in keywords:
            temp_list = [[x, y] for x in son_words_one for y in son_words_two]
            combination_temp = []
            for item in temp_list:
                combination_temp.append(sorted(item))
            for item in combination_temp:
                if item in keywords_combinations:
                    times_every_combination[keywords_combinations.index(
                        item)] += 1
        else:
            continue
    reslut = []
    for i in range(len(keywords_combinations)):
        if times_every_combination[i] != 0:
            keywords_combinations[i].append(times_every_combination[i])
            reslut.append(keywords_combinations[i])
    return reslut

def remove_last_brackets(dry):
    dry = re.sub(" ", "", dry)
    length = len(dry)
    last_left_br = length - 1
    try:
        ch_last_right_br = dry.rindex("）")
    except:
        ch_last_right_br = -1
    try:
        en_last_right_br = dry.rindex(")")
    except:
        en_last_right_br = -1
    if ch_last_right_br > 0 or en_last_right_br > 0:
        last_left_br = length - 2
    return dry[:last_left_br]
