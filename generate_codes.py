#!/usr/bin/env python3
# 生成50个登录码并保存到JSON文件
import json
import random
import string

def generate_access_codes(count=50, length=6):
    """生成指定数量的登录码"""
    chars = string.ascii_uppercase + string.digits  # 大写字母和数字
    codes = set()
    
    while len(codes) < count:
        code = ''.join(random.choices(chars, k=length))
        codes.add(code)
    
    return sorted(list(codes))

if __name__ == "__main__":
    # 生成50个登录码
    codes = generate_access_codes(50, 6)
    
    # 保存到JSON文件
    output_file = 'access_codes.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(codes, f, indent=2)
    
    print(f"已生成 {len(codes)} 个登录码，保存到 {output_file}")
    print("\n前10个登录码：")
    for i, code in enumerate(codes[:10]):
        print(f"{i+1}. {code}")
    print("...")
    print(f"\n后10个登录码：")
    for i, code in enumerate(codes[-10:]):
        print(f"{len(codes)-10+i+1}. {code}")
    
    # 同时保存到文本文件，方便查看
    with open('access_codes.txt', 'w', encoding='utf-8') as f:
        f.write("新疆中考英语读写题核心训练系统 - 登录码\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"共 {len(codes)} 个登录码（不区分大小写）\n\n")
        for i, code in enumerate(codes):
            f.write(f"{i+1:2d}. {code}\n")
    
    print(f"\n登录码已同时保存到 access_codes.txt")
    print("完成！")
