import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
from tkinter import filedialog
import sys

print("成績ファイルを選択してください")
typ = [('成績ファイル', '*.csv')]
dir = 'C:'
your_file = filedialog.askopenfilename(filetypes=typ, initialdir=dir)

if your_file == '':
    print('ファイルが選択されていません。プログラムを終了します。')
    sys.exit()

major_dict = {
    1: 'biology',
    2: 'chemistry',
    3: 'physics',
    4: 'mathematics',
}
# initial setting
your_major = major_dict[int(input(
    '専攻を選択してください\n1: 生物専攻\n2: 化学専攻\n3: 物理専攻\n4: 数学専攻\n'))]

judge_list = {
    '学問への扉': 2,
    '基盤教養教育科目': 6,
    '情報教育科目': 2,
    '健康・スポーツ教育科目': 2,
    '高度教養教育科目': 2,
    'グローバル理解': 2,
    '第２外国語': 3,
    '実践英語': 2,
    '総合英語': 6,
    '高度国際性涵養科目': 2,
    '選択必修科目': 38,
    '必修科目': 12,
    '選択科目': 17,
    '専門基礎教育科目': 24,
    'アドヴァンスト・セミナー': 0,
    '自由単位': 5,
}

# define function
list_judge = []


def judge_with_columns(df, judge_name):
    search_condition = (df['科目小区分'].str.contains(
        judge_name, na=False) & (df['合否'] == '合'))
    number_judge = df.loc[search_condition, ['単位数']].astype(int).sum()[0]
    judge_condition = number_judge >= judge_list[judge_name]
    rest_number = judge_list[judge_name]-number_judge
    if (judge_condition):
        list_judge.append(
            ['OK', judge_name, judge_list[judge_name], int(number_judge), rest_number])
    else:
        list_judge.append(
            ['NG', judge_name, judge_list[judge_name], int(number_judge), rest_number])
    df = df[~search_condition]
    return df


def filter_judge(df):
    if (your_major == 'biology') | (your_major == 'chemistry'):
        condition_engi = df['開講科目名 '].str.contains('同演義', na=False)
        df.loc[condition_engi, '単位数'] = 2
        condition_toukei = df['開講科目名 '].str.contains('統計学Ｃ', na=False)
        df.loc[condition_toukei, '単位数'] = 0
    if (your_major == 'physics') | (your_major == 'mathematics'):
        condition_toukei = df['開講科目名 '].str.contains('統計学Ｂ', na=False)
        df.loc[condition_toukei, '単位数'] = 0
    return df


# get the number of rows to skip and strip "\t"
lines = []
with open(your_file, 'r', encoding="shift-jis") as file:
    csv_reader = csv.reader(file)
    target_string = '学生所属コード'
    counter_target = 0
    for i, row in enumerate(csv_reader):
        # print(row)
        if target_string in row:
            counter_target += 1

        if counter_target == 4:
            if '\t' in row:
                row.pop(-1)
            lines.append(row)

# read the lines
df = pd.DataFrame(lines[1:], columns=lines[0])

# 　get the unit number
for key in judge_list.keys():
    if key == '専門基礎教育科目':
        df = filter_judge(df)
    if key == '自由単位':
        list_judge.append(['-', '自由単位', judge_list['自由単位'], 0, 5])
        continue
    df = judge_with_columns(df, key)

# display the result
data = pd.DataFrame(list_judge, columns=[
                    '判定', '科目名', '必要単位数', '取得単位数', '残り単位数'])
print(data.to_markdown())

print(data.sum(numeric_only=True))
