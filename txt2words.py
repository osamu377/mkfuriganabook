import re
import MeCab
import csv
import os
import jaconv

# 漢字を含むかどうかを判定する関数
def contains_kanji(s):
    return bool(re.search(r'[\u4e00-\u9fff]', s))

# ディレクトリ名
dirname = r"texts/"

input_files = [
    f for f in os.listdir(dirname) if os.path.isfile(os.path.join(dirname, f))
]
# print(input_files)

for filename in input_files:
     
    # 拡張子が'.txt'以外は無視
    file_body, file_extension = os.path.splitext(filename)
    if file_extension != '.txt':
        continue

    # 入力ファイル・パスと出力ファイル・パス
    in_file = dirname + filename
    out_file = dirname + "out" + file_body + '.csv'
    # print(out_file)

    # ファイル読み込み
    with open(in_file) as f:
        text = f.read()

    # Mecab で形態素解析
    tagger = MeCab.Tagger()
    result = tagger.parse(text)
    result_lines = result.split('\n')

    result_words = []   # 解析結果
    words_kana_tpl = [] # 漢字と仮名の組み合わせタプル
#    words_kana = {}     # 漢字を含む語句とその読み仮名を辞書として

    for result_line in result_lines:
        result_words.append(re.split('[\t,]', result_line))

    for result_word in result_words:

        if (result_word[0] not in ('EOS', '')
            and contains_kanji(result_word[0])):
                # 漢字を含む語句のリスト
                # words.append(result_word[0])
                # 読み仮名がない語句はデバッグ用のエラー出力
                if len(result_word) <= 8:
                    print(result_word, ":", "読み仮名がありません")
                # 値を'ネ'と読んでしまうのを修正
                elif (result_word[0] == '値' and result_word[8] == 'ネ'):
                    words_kana_tpl.append(('値','アタイ','あたい'))
                # 読み仮名がある場合は辞書に追加
                else:
#                    words_kana[result_word[0]] = result_word[8]
                    words_kana_tpl.append((result_word[0],
                                           result_word[8],
                                           jaconv.kata2hira(result_word[8])))
    #            print(result_word[8])

    # 重複排除
    unique_list = list(dict.fromkeys(words_kana_tpl))
    # CSVファイルにsjisで書き込む
    with open(out_file, mode='w', newline='', encoding='sjis') as of:
        writer = csv.writer(of)
        writer.writerows(unique_list)

