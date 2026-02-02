# API 参考文档

## init_create.py

### 函数: `init_create(count, output_dir)`

创建指定数量的测试文件。

**参数:**
| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| count | int | 3 | 要创建的文件数量 |
| output_dir | str | "output" | 输出目录路径 |

**返回值:**
- `list[str]`: 创建的文件路径列表

**命令行参数:**
```
python init_create.py [count] [output_dir]
```

---

## file_zip.py

### 函数: `create_zip(source_dir, zip_name)`

将目录下的文件打包成zip。

**参数:**
| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| source_dir | str | "output" | 要打包的源目录 |
| zip_name | str | None | 输出的zip文件名，None则自动生成 |

**返回值:**
- `str | None`: 成功返回zip文件路径，失败返回None

**命令行参数:**
```
python file_zip.py [source_dir] [zip_name]
```

---

## 注意事项

1. 所有脚本使用 Python 3.6+ 编写
2. 无需安装额外依赖，仅使用标准库
3. 文件名自动包含时间戳，避免覆盖
4. zip文件使用 DEFLATED 压缩算法
