---
name: demo-skill
description: 生成测试文件并打包成zip，用于测试skill功能
---

# Demo Skill - 文件生成与打包工具

## 概述

本skill提供文件生成和zip打包功能，主要用于测试skill的脚本调用能力。

## 适用场景

- 测试skill的多脚本调用能力
- 验证skill的参数传递功能
- 需要快速生成测试文件的场景

## 核心工作流程

### 第1步：收集用户需求

询问用户：
- 需要生成多少个文件？（默认3个）
- 输出目录名称？（默认 output）
- zip文件名称？（默认自动生成）

### 第2步：生成测试文件

调用 `scripts/init_create.py` 创建文件：

```bash
# 基本用法
python scripts/init_create.py

# 指定文件数量
python scripts/init_create.py 5

# 指定文件数量和输出目录
python scripts/init_create.py 5 my_output
```

### 第3步：打包成zip

调用 `scripts/file_zip.py` 进行打包：

```bash
# 基本用法（打包output目录）
python scripts/file_zip.py

# 指定源目录
python scripts/file_zip.py my_output

# 指定源目录和zip文件名
python scripts/file_zip.py my_output result.zip
```

### 第4步：完成提示

告知用户：
- 文件创建位置
- zip包的名称和大小
- 包含的文件数量

## 参考资料

详细用法请参考：
- `reference/usage_examples.md` - 使用示例
- `reference/api_reference.md` - API参考文档
