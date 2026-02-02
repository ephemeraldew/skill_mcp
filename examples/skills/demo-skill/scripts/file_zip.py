#!/usr/bin/env python3
"""
打包文件为zip的脚本
用法: python file_zip.py [源目录] [输出zip文件名]
"""
import os
import sys
import zipfile
from datetime import datetime


def create_zip(source_dir='output', zip_name=None):
    """
    将指定目录下的所有文件打包成zip

    Args:
        source_dir: 源目录，默认为 output
        zip_name: 输出的zip文件名，默认自动生成带时间戳的名称
    """
    if not os.path.exists(source_dir):
        print(f'[ERROR] 目录不存在: {source_dir}')
        return None

    # 自动生成zip文件名
    if zip_name is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        zip_name = f'archive_{timestamp}.zip'

    # 确保有.zip后缀
    if not zip_name.endswith('.zip'):
        zip_name += '.zip'

    # 获取所有文件
    files_to_zip = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            files_to_zip.append(file_path)

    if not files_to_zip:
        print(f'[WARN] 目录 {source_dir} 中没有文件')
        return None

    # 创建zip文件
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in files_to_zip:
            # 使用相对路径作为zip内的文件名
            arcname = os.path.relpath(file_path, source_dir)
            zipf.write(file_path, arcname)
            print(f'[ADD] {arcname}')

    file_size = os.path.getsize(zip_name)
    print(f'\n[OK] 已创建: {zip_name} ({file_size} bytes)')
    print(f'共打包 {len(files_to_zip)} 个文件')

    return zip_name


if __name__ == '__main__':
    source_dir = sys.argv[1] if len(sys.argv) > 1 else 'output'
    zip_name = sys.argv[2] if len(sys.argv) > 2 else None

    create_zip(source_dir, zip_name)
