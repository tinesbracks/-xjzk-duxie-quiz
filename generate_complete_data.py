#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的新疆中考英语读写题词汇数据
包含5个分类：动作逻辑的转化、形容词逻辑的转化、名词逻辑的转化、逻辑词的替换、归纳范畴
"""

import pandas as pd
import json
import re

def clean_text(text):
    """清理文本，去除多余空格和换行"""
    if pd.isna(text):
        return ""
    return str(text).strip()

def generate_sentence_for_action(original, target, meaning):
    """为动作逻辑转化生成例句"""
    sentences = {
        "decide to build": {
            "original": "I decide to build a house.",
            "target": "I make a ______ to build a house.",
            "answer": "decision"
        },
        "choose": {
            "original": "I choose the red one.",
            "target": "I make a ______.",
            "answer": "choice"
        },
        "visit a center": {
            "original": "I visit a center.",
            "target": "I pay a ______ to a center.",
            "answer": "visit"
        },
        "think of an idea": {
            "original": "I think of an idea.",
            "target": "I come up with an ______.",
            "answer": "idea"
        },
        "join a group": {
            "original": "I join a group.",
            "target": "I take ______ in a group.",
            "answer": "part"
        },
        "realize a duty": {
            "original": "I realize a duty.",
            "target": "I become ______ of a duty.",
            "answer": "aware"
        },
        "happen": {
            "original": "It happens.",
            "target": "It takes ______.",
            "answer": "place"
        },
        "remember his words": {
            "original": "I remember his words.",
            "target": "I keep his words in ______.",
            "answer": "mind"
        },
        "die (death)": {
            "original": "He dies.",
            "target": "He ______ away.",
            "answer": "passes"
        },
        "look after": {
            "original": "I look after the baby.",
            "target": "I take ______ of the baby.",
            "answer": "care"
        }
    }
    
    if original in sentences:
        return sentences[original]
    
    # 默认生成简单例句
    return {
        "original_sentence": f"I {original}.",
        "target_sentence": f"I {target}.",
        "answer": "[待完善]"
    }

def generate_sentence_for_adjective(original, target, meaning):
    """为形容词逻辑转化生成例句"""
    sentences = {
        "important": {
            "original": "This is important.",
            "target": "This is of great ______.",
            "answer": "importance"
        },
        "difficult": {
            "original": "It is difficult.",
            "target": "It is a ______.",
            "answer": "challenge"
        },
        "famous": {
            "original": "He is famous.",
            "target": "He is ______-known.",
            "answer": "well"
        }
    }
    
    if original in sentences:
        return sentences[original]
    
    return {
        "original_sentence": f"It is {original}.",
        "target_sentence": f"It is {target}.",
        "answer": "[待完善]"
    }

def generate_sentence_for_noun(original, target, meaning):
    """为名词逻辑转化生成例句"""
    sentences = {
        "success": {
            "original": "I achieve success.",
            "target": "I ______ successfully.",
            "answer": "succeed"
        },
        "decision": {
            "original": "I make a decision.",
            "target": "I decide to ______.",
            "answer": "do"
        },
        "choice": {
            "original": "I make a choice.",
            "target": "I ______.",
            "answer": "choose"
        },
        "contribution": {
            "original": "I make a contribution to the project.",
            "target": "I contribute to the ______.",
            "answer": "project"
        }
    }
    
    if original in sentences:
        return sentences[original]
    
    return {
        "original_sentence": f"It is a {original}.",
        "target_sentence": f"It is {target}.",
        "answer": "[待完善]"
    }

def generate_sentence_for_logic(original, target, logic_type):
    """为逻辑词替换生成例句"""
    sentences = {
        "because": {
            "original": "I like it because it is good.",
            "target": "I like it ______ of its goodness.",
            "answer": "because"
        },
        "so": {
            "original": "It rained, so I stayed home.",
            "target": "It rained. ______ a result, I stayed home.",
            "answer": "As"
        },
        "but": {
            "original": "I want to go, but I can't.",
            "target": "I want to go. ______, I can't.",
            "answer": "However"
        }
    }
    
    if original in sentences:
        return sentences[original]
    
    return {
        "original_sentence": f"He {original} I am happy.",
        "target_sentence": f"He {target}.",
        "answer": "[待完善]"
    }

def generate_sentence_for_category(concrete, category, category_name):
    """为归纳范畴生成例句"""
    # 归纳范畴的题目形式不同：给出具体项，选择概括词
    examples = {
        "tangyuan / yuanxiao": {
            "original": "Tangyuan and yuanxiao are traditional food.",
            "target": "Tangyuan and yuanxiao belong to ______.",
            "answer": "food"
        },
        "running / swimming": {
            "original": "Running and swimming are good sports.",
            "target": "Running and swimming belong to ______.",
            "answer": "sports"
        },
        "train / bus / plane": {
            "original": "Train, bus and plane are ways to travel.",
            "target": "Train, bus and plane belong to ______.",
            "answer": "ways"
        }
    }
    
    key = concrete
    if key in examples:
        return examples[key]
    
    return {
        "original_sentence": f"{concrete} are examples of {category}.",
        "target_sentence": f"{concrete} belong to ______.",
        "answer": category
    }

def read_all_sheets(excel_path):
    """读取所有工作表并生成完整数据"""
    xl = pd.ExcelFile(excel_path)
    categories = xl.sheet_names
    
    all_data = []
    current_id = 1
    
    for category in categories:
        df = pd.read_excel(excel_path, sheet_name=category)
        
        # 处理"名词逻辑的转化"表的特殊情况（第一行不是列名）
        if category == "名词逻辑的转化":
            # 重新读取，不设置header
            df = pd.read_excel(excel_path, sheet_name=category, header=None)
            # 设置列名
            df.columns = ['序号', '原文表达 (Original)', '题目表达 (Target/Summary)', '中文释义']
            df = df.iloc[1:].reset_index(drop=True)  # 跳过第一行
        
        print(f"\n处理分类: {category} ({len(df)} 条)")
        
        for idx, row in df.iterrows():
            original = clean_text(row.get('原文表达 (Original)', row.get('原文具体项 (Concrete)', '')))
            target = clean_text(row.get('题目表达 (Target/Summary)', row.get('题目概括项 (Target/Word)', '')))
            meaning = clean_text(row.get('中文释义', row.get('概括范畴', row.get('逻辑转换', ''))))
            
            if not original or not target:
                continue
            
            # 根据分类生成例句
            example = None
            if category == "动作逻辑的转化":
                example = generate_sentence_for_action(original, target, meaning)
            elif category == "形容词逻辑的转化":
                example = generate_sentence_for_adjective(original, target, meaning)
            elif category == "名词逻辑的转化":
                example = generate_sentence_for_noun(original, target, meaning)
            elif category == "逻辑词的替换":
                example = generate_sentence_for_logic(original, target, meaning)
            elif category == "归纳范畴":
                example = generate_sentence_for_category(original, target, meaning)
            
            item = {
                "id": current_id,
                "category": category,
                "original": original,
                "target": target,
                "meaning": meaning,
                "mastered": False,
                "example": example
            }
            
            all_data.append(item)
            current_id += 1
    
    return all_data

def main():
    excel_path = "E:/credble/读写题/读写题资料.xlsx"
    
    print("开始读取Excel文件...")
    all_data = read_all_sheets(excel_path)
    
    print(f"\n总共读取 {len(all_data)} 条数据")
    
    # 保存为JSON文件
    output_path = "vocabulary_data.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到 {output_path}")
    
    # 统计每个分类的数量
    categories = {}
    for item in all_data:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n各分类数量:")
    for cat, count in categories.items():
        print(f"  {cat}: {count} 条")

if __name__ == "__main__":
    main()
