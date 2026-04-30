import pandas as pd
import json
import random

# 读取 Excel
df = pd.read_excel('E:/credble/读写题/读写题资料.xlsx')

# 为所有数据生成例句
def generate_all_examples():
    examples = {}
    
    # 逐条定义合适的例句，确保挖空后只填一个单词
    sentence_templates = [
        # 1. decide to build -> make a decision to build
        {
            'original': 'decide to build',
            'original_sentence': 'I decide to build a house.',
            'target_sentence': 'I make a ______ to build a house.',
            'answer': 'decision'
        },
        # 2. choose -> make a choice
        {
            'original': 'choose',
            'original_sentence': 'I choose the red one.',
            'target_sentence': 'I make a ______.',
            'answer': 'choice'
        },
        # 3. visit a center -> pay a visit to a center
        {
            'original': 'visit a center',
            'original_sentence': 'I visit a center.',
            'target_sentence': 'I pay a ______ to a center.',
            'answer': 'visit'
        },
        # 4. think of an idea -> come up with an idea
        {
            'original': 'think of an idea',
            'original_sentence': 'I think of an idea.',
            'target_sentence': 'I come up with an ______.',
            'answer': 'idea'
        },
        # 5. join a group -> take part in / be a member of
        {
            'original': 'join a group',
            'original_sentence': 'I join a group.',
            'target_sentence': 'I take ______ in a group.',
            'answer': 'part'
        },
        # 6. realize a duty -> become aware of a duty
        {
            'original': 'realize a duty',
            'original_sentence': 'I realize my duty.',
            'target_sentence': 'I become ______ of my duty.',
            'answer': 'aware'
        },
        # 7. happen -> take place
        {
            'original': 'happen',
            'original_sentence': 'The meeting happens tomorrow.',
            'target_sentence': 'The meeting ______ tomorrow.',
            'answer': 'takes place'
        },
        # 8. remember his words -> keep his words in mind
        {
            'original': 'remember his words',
            'original_sentence': 'I remember his words.',
            'target_sentence': 'I keep his words in ______.',
            'answer': 'mind'
        },
        # 9. die (death) -> pass away / lose one's life
        {
            'original': 'die (death)',
            'original_sentence': 'He dies in the accident.',
            'target_sentence': 'He ______ away in the accident.',
            'answer': 'passes'
        },
        # 10. look after -> take care of
        {
            'original': 'look after',
            'original_sentence': 'I look after my sister.',
            'target_sentence': 'I take ______ of my sister.',
            'answer': 'care'
        },
        # 11. get -> obtain
        {
            'original': 'get',
            'original_sentence': 'I get a book from the library.',
            'target_sentence': 'I ______ a book from the library.',
            'answer': 'obtain'
        },
        # 12. help -> give a hand
        {
            'original': 'help',
            'original_sentence': 'I help my mother.',
            'target_sentence': 'I give a ______ to my mother.',
            'answer': 'hand'
        },
        # 13. buy -> purchase
        {
            'original': 'buy',
            'original_sentence': 'I buy a pen.',
            'target_sentence': 'I ______ a pen.',
            'answer': 'purchase'
        },
        # 14. need -> require
        {
            'original': 'need',
            'original_sentence': 'I need help.',
            'target_sentence': 'I ______ help.',
            'answer': 'require'
        },
        # 15. use -> make use of
        {
            'original': 'use',
            'original_sentence': 'I use a computer.',
            'target_sentence': 'I make ______ of a computer.',
            'answer': 'use'
        },
        # 16-50 暂时用模板生成，后续手动调整
    ]
    
    for item in sentence_templates:
        examples[item['original']] = item
    
    return examples

# 获取预定义的例句
predefined_examples = generate_all_examples()

# 转换数据
data = []
for idx, row in df.iterrows():
    original = row['原文表达 (Original)']
    
    item = {
        'id': int(row['序号']),
        'original': original,
        'target': row['题目表达 (Target/Summary)'],
        'meaning': row['中文释义'],
        'mastered': False
    }
    
    # 如果有预定义的例句，使用它
    if original in predefined_examples:
        item['example'] = {
            'original_sentence': predefined_examples[original]['original_sentence'],
            'target_sentence': predefined_examples[original]['target_sentence'],
            'answer': predefined_examples[original]['answer']
        }
    else:
        # 否则，生成占位符（后续手动完善）
        item['example'] = {
            'original_sentence': f'[待完善] {original}',
            'target_sentence': f'[待完善] ______',
            'answer': '[待完善]'
        }
    
    data.append(item)

# 保存为 JSON
with open('vocabulary_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'已生成 vocabulary_data.json，共 {len(data)} 条数据')
print('\n已有例句的条目:')
for item in data:
    if '[待完善]' not in item['example']['original_sentence']:
        print(f"{item['id']}. {item['original']}")
        print(f"   {item['example']['original_sentence']}")
        print(f"   {item['example']['target_sentence']}")
        print()
