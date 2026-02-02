# 使用示例

## 生成文件示例

### 基本用法
```bash
# 生成默认3个文件到 output 目录
python scripts/init_create.py

# 生成5个文件到 output 目录
python scripts/init_create.py 5

# 生成10个文件到 my_files 目录
python scripts/init_create.py 10 my_files
```

### 输出示例
```
[OK] 已创建: output/test_file_1_20260130_120000.txt
[OK] 已创建: output/test_file_2_20260130_120000.txt
[OK] 已创建: output/test_file_3_20260130_120000.txt

共创建 3 个文件到 output/ 目录
```

## 打包zip示例

### 基本用法
```bash
# 打包 output 目录，自动生成zip文件名
python scripts/file_zip.py

# 打包指定目录
python scripts/file_zip.py my_files

# 打包并指定zip文件名
python scripts/file_zip.py output my_archive.zip
```

### 输出示例
```
[ADD] test_file_1_20260130_120000.txt
[ADD] test_file_2_20260130_120000.txt
[ADD] test_file_3_20260130_120000.txt

[OK] 已创建: archive_20260130_120001.zip (1234 bytes)
共打包 3 个文件
```

## 组合使用

完整工作流：
```bash
# 1. 生成文件
python scripts/init_create.py 5

# 2. 打包成zip
python scripts/file_zip.py output result.zip
```
