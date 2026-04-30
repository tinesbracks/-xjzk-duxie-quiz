#!/usr/bin/env python3
# 读取更新后的Excel文件（包含原句、题目句子、答案列）
import pandas as pd
import json
import re

def process_target_sentence(target_sentence, answer):
    """
    处理题目句子，将答案部分替换为挖空
    支持多种格式：
    1. (answer) -> ______
    2. （answer） -> ______
    3. 如果已经包含 ______，则保持不变
    """
    if not target_sentence or not answer or answer == '[待完善]':
        return target_sentence
    
    # 如果已经包含挖空，直接返回
    if '______' in target_sentence:
        return target_sentence
    
    # 替换括号中的答案（支持中英文括号）
    # 英文括号
    pattern1 = r'\(\s*' + re.escape(answer) + r'\s*\)'
    target_sentence = re.sub(pattern1, '______', target_sentence, flags=re.IGNORECASE)
    
    # 中文括号
    pattern2 = r'（\s*' + re.escape(answer) + r'\s*）'
    target_sentence = re.sub(pattern2, '______', target_sentence, flags=re.IGNORECASE)
    
    # 如果答案就在句子中（没有括号），也尝试替换
    # 但这种情况比较少见，需要谨慎处理
    
    return target_sentence

def read_updated_excel():
    file_path = 'E:/credble/读写题/读写题资料.xlsx'
    output_file = 'vocabulary_data.json'
    
    print("正在读取更新后的Excel文件...")
    
    # 读取所有工作表
    sheet_names = ['动作逻辑的转化', '形容词逻辑的转化', '名词逻辑的转化', '逻辑词的替换', '归纳范畴']
    all_data = []
    current_id = 1
    
    for sheet_name in sheet_names:
        try:
            # 读取工作表，不预设表头
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
            print(f"读取工作表 '{sheet_name}' 成功，共 {len(df)} 行，{len(df.columns)} 列")
            
            # 假设列顺序是：序号、原文表达、题目表达、中文释义、原句、题目句子、答案
            # 从第2行开始（索引1），跳过表头
            for index in range(1, len(df)):
                row = df.iloc[index]
                
                try:
                    # 获取列数据
                    original = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
                    target = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ""
                    meaning = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
                    
                    # 新添加的列
                    original_sentence = str(row.iloc[4]).strip() if len(row) > 4 and pd.notna(row.iloc[4]) else ""
                    target_sentence = str(row.iloc[5]).strip() if len(row) > 5 and pd.notna(row.iloc[5]) else ""
                    answer = str(row.iloc[6]).strip() if len(row) > 6 and pd.notna(row.iloc[6]) else ""
                    
                    # 跳过空行
                    if not original or original == 'nan' or not target or target == 'nan':
                        continue
                    
                    # 处理题目句子：将答案替换为挖空
                    if target_sentence and answer and answer != 'nan':
                        target_sentence = process_target_sentence(target_sentence, answer)
                    
                    # 检查是否有完整的例句数据
                    example = {}
                    if original_sentence and target_sentence and answer and answer != 'nan':
                        example = {
                            "original_sentence": original_sentence,
                            "target_sentence": target_sentence,
                            "answer": answer
                        }
                    else:
                        example = {
                            "original_sentence": "[待完善]",
                            "target_sentence": "[待完善]",
                            "answer": "[待完善]"
                        }
                    
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
    
    # 统计有完整例句的数据
    complete_count = sum(1 for d in all_data if d['example']['answer'] != '[待完善]')
    print(f"有完整例句: {complete_count} 条")
    print(f"待完善: {len(all_data) - complete_count} 条")
    
    # 保存到JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    
    print(f"数据已保存到 {output_file}")
    
    # 显示前5条的题目句子，检查格式
    print("\n前5条的题目句子（检查格式）:")
    for i, d in enumerate(all_data[:5]):
        print(f"{i+1}. {d['example']['target_sentence']}")
    
    print("\n完成！")

if __name__ == "__main__":
    read_updated_excel()
