#!/usr/bin/env python3
# 生成完整的词汇数据（199条）
import pandas as pd
import json
import re

# 生成例句的函数
def generate_example(original, target, meaning):
    """
    为词汇对生成例句
    确保挖空后只填一个单词
    """
    # 常见模式的例句模板
    templates = {
        # 动作逻辑转化
        "decide to": {"original": "I decide to build a house.", "target": "I make a ______ to build a house.", "answer": "decision"},
        "choose": {"original": "I choose the red one.", "target": "I make a ______.", "answer": "choice"},
        "visit": {"original": "I visit a center.", "target": "I pay a ______ to a center.", "answer": "visit"},
        "think of": {"original": "I think of an idea.", "target": "I come up with an ______.", "answer": "idea"},
        "join": {"original": "I join a group.", "target": "I take ______ in a group.", "answer": "part"},
        "realize": {"original": "I realize my duty.", "target": "I become ______ of my duty.", "answer": "aware"},
        "happen": {"original": "It happens.", "target": "It takes ______.", "answer": "place"},
        "remember": {"original": "I remember his words.", "target": "I keep his words in ______.", "answer": "mind"},
        "die": {"original": "He dies.", "target": "He ______ away.", "answer": "passes"},
        "look after": {"original": "I look after the baby.", "target": "I take ______ of the baby.", "answer": "care"},
    }
    
    # 尝试匹配模板
    for key, template in templates.items():
        if key in original.lower():
            return template
    
    # 如果没有匹配模板，生成通用例句
    # 尝试从target中提取答案词（假设是单个单词）
    target_words = target.split()
    answer = "[待完善]"
    
    # 简单启发式：如果target包含"a"或"an"，答案可能是后面的单词
    if "a" in target_words or "an" in target_words:
        try:
            idx = target_words.index("a") if "a" in target_words else target_words.index("an")
            if idx + 1 < len(target_words):
                answer = target_words[idx + 1].rstrip(',.;')
        except:
            pass
    
    # 生成通用例句
    # 确保句子首字母大写
    orig_sentence = original if original[0].isupper() else original.capitalize()
    original_sentence = f"{orig_sentence}."
    
    # 生成目标句子，挖空答案词
    if answer != "[待完善]":
        # 如果知道答案，在目标句子中挖空
        target_sentence = f"{orig_sentence.replace(original, target)}."
        # 将答案词替换为空白
        target_sentence = target_sentence.replace(answer, "______", 1)
    else:
        # 否则，简单替换
        target_sentence = f"{orig_sentence.replace(original, target)}."
        # 在target中找一个合适的位置挖空
        if "a " in target or "an " in target:
            # 在"a/an"后面挖空
            target_sentence = target_sentence.replace("a " + answer if answer != "[待完善]" else "a ", "a ______", 1)
    
    return {
        "original_sentence": original_sentence,
        "target_sentence": target_sentence,
        "answer": answer
    }

# 主程序
if __name__ == "__main__":
    file_path = 'E:/credble/读写题/读写题资料.xlsx'
    output_file = 'vocabulary_data.json'
    
    print("正在读取Excel文件...")
    
    # 读取所有工作表
    sheet_names = ['动作逻辑的转化', '形容词逻辑的转化', '名词逻辑的转化', '逻辑词的替换', '归纳范畴']
    all_data = []
    current_id = 1
    
    for sheet_name in sheet_names:
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"读取工作表 '{sheet_name}' 成功，共 {len(df)} 行")
            
            # 处理每一行
            for index, row in df.iterrows():
                try:
                    # 获取列数据（假设列顺序是：序号、原文表达、题目表达、中文释义）
                    original = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
                    target = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
                    meaning = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
                    
                    # 跳过空行或标题行
                    if not original or original == 'nan' or not target or target == 'nan':
                        continue
                    
                    # 生成例句
                    example = generate_example(original, target, meaning)
                    
                    # 添加到数据列表
                    all_data.append({
                        "id": current_id,
                        "original": original,
                        "target": target,
                        "meaning": meaning,
                        "category": sheet_name,
                        "mastered": False,
                        "example": example
                    })
                    
                    current_id += 1
                    
                except Exception as e:
                    print(f"处理第 {index+1} 行时出错: {e}")
                    continue
                    
        except Exception as e:
            print(f"读取工作表 '{sheet_name}' 失败: {e}")
            continue
    
    print(f"共读取 {len(all_data)} 条数据")
    
    # 保存到JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到 {output_file}")
    print("完成！")
