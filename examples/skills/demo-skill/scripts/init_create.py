#!/usr/bin/env python3
"""
生成测试文件的脚本
用法: python init_create.py [文件数量] [输出目录]
"""
import os
import sys
import random
import string
from datetime import datetime


def generate_random_content(lines=10):
    """生成随机文本内容"""
    content = []
    for _ in range(lines):
        line = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=random.randint(20, 80)))
        content.append(line)
    return '\n'.join(content)


def init_create(count=3, output_dir='output'):
    """
    创建指定数量的测试文件

    Args:
        count: 要创建的文件数量，默认3个
        output_dir: 输出目录，默认为 output
    """
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    created_files = []
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    for i in range(1, count + 1):
        filename = f'test_file_{i}_{timestamp}.txt'
        filepath = os.path.join(output_dir, filename)

        content = f"""# 测试文件 {i}
# 创建时间: {datetime.now().isoformat()}
# 这是一个用于测试skill功能的文件

{generate_random_content(random.randint(5, 15))}
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        created_files.append(filepath)
        print(f'[OK] 已创建: {filepath}')

    print(f'\n共创建 {len(created_files)} 个文件到 {output_dir}/ 目录')
    return created_files


if __name__ == '__main__':
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    output_dir = sys.argv[2] if len(sys.argv) > 2 else 'output'

    init_create(count, output_dir)
