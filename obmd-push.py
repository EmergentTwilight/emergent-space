import os
import shutil
import sys

source_dir = "D:/Obsidian-Vault/Alpha/Blog/mkdocs-blog-project/emergent-space-obmd"
target_dir = "docs"

def push(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(source_dir):
        # 计算目标路径
        for dir_name in dirs:
            target_sub_dir = os.path.join(target_dir, os.path.relpath(os.path.join(root, dir_name), source_dir))
            if not os.path.exists(target_sub_dir):
                os.makedirs(target_sub_dir)

        for file_name in files:
            src_file = os.path.join(root, file_name)
            target_file = os.path.join(target_dir, os.path.relpath(src_file, source_dir))
            shutil.copy2(src_file, target_file)
            print(f"{file_name}:  copied or updated")
    print("push completed")

if __name__ == "__main__":
    push(source_dir, target_dir)