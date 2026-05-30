import os
import shutil

def copy_and_rename(source_path=None, newprefix="new_", newfiletype=".txt", oldprefix="", oldfiletype=".txt"):
    if source_path is None: source_path = os.getcwd()

    count = 0
    current_dir = os.getcwd()
    
    # 规范化路径分隔符，兼容 Windows 输入
    source_path = os.path.normpath(source_path)

    print(f"📂 开始扫描目录: {source_path}")
    
    with os.scandir(source_path) as entries:
        for entry in entries:
            if entry.is_dir(): continue
            filename = entry.name
            
            # 过滤
            if oldprefix and oldprefix not in filename: continue
            if not filename.endswith(oldfiletype): continue

            new_filename = f"{newprefix}{count}{newfiletype}"
            target_copy_path = os.path.join(current_dir, new_filename)

            if os.path.exists(target_copy_path):
                print(f"⚠️ 跳过已存在: {new_filename}")
                count += 1
                continue

            try:
                shutil.copyfile(entry.path, target_copy_path)
                print(f"✅ 已复制: {filename} -> {new_filename}")
                count += 1
            except Exception as e:
                print(f"❌ 失败: {filename}, 错误: {e}")

    print(f"🎉 处理完成，共复制 {count} 个文件。")

if __name__ == "__main__":
    print("="*30)
    print("   文件批量复制重命名工具")
    print("="*30)
    
    # 获取输入
    src = input("1. 请输入源文件夹路径: ").strip('"').strip("'") # 自动去除用户可能粘贴的引号
    old_pre = input("2. 源文件名前缀 (默认不匹配前缀): ").strip()
    old_typ = input("3. 源文件后缀 (默认 .txt): ").strip()
    pre = input("2. 新文件名前缀 (默认 new_): ").strip()
    typ = input("3. 新文件后缀 (默认 .txt): ").strip()
    
    # 设置默认值
    # if not pre: pre = "new_"
    # if not typ: typ = ".txt"
    
    # 执行
    copy_and_rename(src, newprefix=pre, newfiletype=typ, oldprefix=old_pre, oldfiletype=old_typ)
    
    # 防止窗口关闭
    input("\n按回车键退出...")