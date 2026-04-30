import pandas as pd
import json
import re

# 读取 Excel
df = pd.read_excel('E:/credble/读写题/读写题资料.xlsx')

# 为每组数据构造示例句子
def generate_example(item):
    original = item['原文表达 (Original)']
    target = item['题目表达 (Target/Summary)']
    meaning = item['中文释义']
    
    # 根据短语特点构造句子
    # 这里需要先分析 original 和 target 的关系，构造合适的句子
    
    examples = {
        'decide to build': {
            'original_sentence': 'I decide to build a house.',
            'target_sentence': 'I make a ______ to build a house.',
            'answer': 'decision'
        },
        'choose': {
            'original_sentence': 'I choose the red one.',
            'target_sentence': 'I make a ______.',
            'answer': 'choice'
        },
        'visit a center': {
            'original_sentence': 'I visit a center.',
            'target_sentence': 'I pay a ______ to a center.',
            'answer': 'visit'
        },
        'think of an idea': {
            'original_sentence': 'I think of an idea.',
            'target_sentence': 'I come up with an ______.',
            'answer': 'idea'
        },
        'join a group': {
            'original_sentence': 'I join a group.',
            'target_sentence': 'I take ______ in a group.',
            'answer': 'part'
        },
        'realize a duty': {
            'original_sentence': 'I realize a duty.',
            'target_sentence': 'I become ______ of a duty.',
            'answer': 'aware'
        },
        'happen': {
            'original_sentence': 'It happens tomorrow.',
            'target_sentence': 'It ______ tomorrow.',
            'answer': 'takes place'
        },
        'remember his words': {
            'original_sentence': 'I remember his words.',
            'target_sentence': 'I keep his words in ______.',
            'answer': 'mind'
        },
        'die (death)': {
            'original_sentence': 'He dies in the accident.',
            'target_sentence': 'He ______ away in the accident.',
            'answer': 'passes'
        },
        'look after': {
            'original_sentence': 'I look after my sister.',
            'target_sentence': 'I take ______ of my sister.',
            'answer': 'care'
        }
    }
    
    # 如果预定义了示例，使用预定义的
    if original in examples:
        return examples[original]
    
    # 否则，尝试自动生成（这里需要更复杂的逻辑）
    # 暂时返回占位符
    return {
        'original_sentence': f'[待生成] {original}',
        'target_sentence': f'[待生成] {target}',
        'answer': '[待生成]'
    }

# 转换数据
data = []
for idx, row in df.iterrows():
    item = {
        'id': int(row['序号']),
        'original': row['原文表达 (Original)'],
        'target': row['题目表达 (Target/Summary)'],
        'meaning': row['中文释义'],
        'mastered': False,
        'example': generate_example(row)
    }
    data.append(item)

# 保存为 JSON
with open('vocabulary_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'已生成 vocabulary_data.json，共 {len(data)} 条数据')
print('\n前10条示例:')
for item in data[:10]:
    print(f"{item['id']}. {item['original']} -> {item['target']}")
    print(f"   例句: {item['example']['original_sentence']}")
    print(f"   题目: {item['example']['target_sentence']}")
    print()
