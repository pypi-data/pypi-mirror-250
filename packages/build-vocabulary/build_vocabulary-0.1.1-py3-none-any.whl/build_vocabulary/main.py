import argparse
import logging
import math
import os.path
import re
from datetime import datetime
from multiprocessing.pool import Pool

from nltk.stem import WordNetLemmatizer

from build_vocabulary.file_reader import Reader

with open(os.path.join(os.path.dirname(__file__), ".assert", "60000.txt"), encoding="utf-8") as f:
    COCA_LIST = f.read().split()

# 配置日志
logging.basicConfig(level=logging.INFO)


class TextProcessor:
    @classmethod
    def run(cls, text):
        words_list = set(re.findall("[a-zA-Z]{3,}", text.lower()))
        lemmatized_tokens = cls._lemmatize_tokens(words_list)
        return lemmatized_tokens

    @staticmethod
    def _lemmatize_tokens(words_list):
        wnl = WordNetLemmatizer()
        tokens = set(wnl.lemmatize(token) for token in words_list)
        return tokens


def _find_start_and_end_indexes(text, start_marker, end_marker):
    start_index = 0
    end_index = -1
    if start_marker:
        head = re.search(start_marker, text)
        if not head:
            logging.warning("头部没有匹配到。")
        else:
            start_index = head.span()[0]
    if end_marker:
        tail = re.search(end_marker, text)
        if not tail:
            logging.warning("尾部没有匹配到。")
        else:
            end_index = tail.span()[1]
    return start_index, end_index


def _process_and_save_word_set(word_set, save_path):
    word_set.intersection_update(set(COCA_LIST))
    string_lists = sorted(word_set, key=lambda x: COCA_LIST.index(x))
    string_list_group = [string_lists[i * 5000:(i + 1) * 5000] for i in
                         range(math.ceil(len(string_lists) / 5000))]
    for index, group in enumerate(string_list_group):
        index = "" if len(string_list_group) == 1 else f"_{index}"
        with open(save_path + f"{index}.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(group))


def process_and_save_text_segment(save_path, text, start, end):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    start_index, end_index = _find_start_and_end_indexes(text, start, end)
    word_set = TextProcessor.run(text[start_index:end_index])
    _process_and_save_word_set(word_set, save_path)


def main(text=None, file_path=None, directory=None, start=None, end=None, file_filter=None):
    parser = argparse.ArgumentParser(
        description="这个程序能够将英文文本拆分成单个单词，并可以通过过滤功能来专注于学习不熟悉的单词。")
    parser.add_argument("file_path", default="", type=str,
                        help="指定单个文件的路径，该文件可以是pdf、pptx、docx或文本格式。如果未指定，程序将等待进一步的指令。",
                        nargs="?")
    parser.add_argument("-r", "--directory", default="", type=str,
                        help="指定一个文件夹路径，程序将会处理该文件夹内所有支持的文本文件。")
    parser.add_argument("-s", "--start", default="", type=str,
                        help="在处理单个文件或大段文本时，指定正则表达式匹配的起始点。留空则从文本的开始处处理。")
    parser.add_argument("-e", "--end", default="", type=str,
                        help="在处理单个文件或大段文本时，指定正则表达式匹配的结束点。留空则处理到文本的结束处。")
    parser.add_argument("-t", "--text", default="", type=str, help="直接提供一大段文本进行处理，而不是通过文件路径。")
    parser.add_argument("-f", "--file_filter", default="", type=str,
                        help="指定一个文件路径，程序会在最终生成的单词列表中排除掉这个文件中出现的单词。这个选项适用于想要创建一个不含特定单词的单词列表的情况。")

    args = parser.parse_args()
    directory = args.directory or directory
    text = args.text or text
    file_path = args.file_path or file_path
    start = args.start or start
    end = args.end or end
    file_filter = args.file_filter or file_filter
    msg = "处理后的文件位于{}内。".format(os.path.abspath("./vocabulary"))
    if text:
        save_path = "vocabulary/" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        process_and_save_text_segment(save_path, text, start, end)

    elif file_path and os.path.isfile(file_path):
        text = Reader.read(file_path)
        os.makedirs("vocabulary", exist_ok=True)
        save_path = os.path.join("vocabulary", os.path.basename(file_path))
        process_and_save_text_segment(save_path, text, start, end)

    elif directory and os.path.isdir(directory):
        string_lists, paths = Reader.read_directory(directory)
        pool = Pool()
        async_results = []
        for single_string in string_lists:
            async_results.append(pool.apply_async(TextProcessor.run, args=(single_string,)))
        results = [item.get() for item in async_results]
        commonpath = os.path.commonpath(paths)
        os.makedirs("vocabulary", exist_ok=True)
        for word_set, path in zip(results, paths):
            save_path = path.replace(commonpath, "vocabulary")
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            _process_and_save_word_set(word_set, save_path)

    else:
        parser.print_help()
        msg = ""
    if msg:
        logging.info(msg)


if __name__ == "__main__":
    main()
