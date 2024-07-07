import os
import shutil
import sys
import re

# set attachment extensions
extensions = ['.jpg', '.jpeg', '.png']

# set dirs
processing_directory = "docs"
attachments_directory = "D:/Obsidian-Vault/Alpha/0 Foundation/1 Attachment"

# hl syntax match
hl_pattern = r'hl="([\d,-]+)"'
def replace_hl(match):
    lines = match.group(1).replace(",", " ")
    return f'hl_lines="{lines}"'

def find_file_in_directory(filename, directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == filename:
                return os.path.normpath(os.path.join(root, file))
    print(f"Error: {filename} not found in {directory}")
    sys.exit(1)

def process_markdown_file(md_path, attachments_dir):
    with open(md_path, 'r', encoding='utf-8') as md:
        md_content = md.read()

    md_content = re.sub(hl_pattern, replace_hl, md_content)

    md_updated_content = md_content
    wikilinks = re.findall(r'\[\[(.*?)\]\]', md_content)

    for link in wikilinks:
        if any(link.endswith(ext) for ext in extensions):
            # get name and path
            attachment_name = os.path.basename(link)
            attachment_name_new = attachment_name.replace(' ', '-')
            attachment_path_new = os.path.normpath(os.path.join(os.path.dirname(md_path), attachment_name_new))
            # find and copy, rename
            attachment_path = find_file_in_directory(attachment_name, attachments_dir)
            shutil.copy(attachment_path, attachment_path_new)
            md_updated_content = md_updated_content.replace(f"[[{link}]]", f"[{attachment_name}]({attachment_name_new})")

    with open(md_path, 'w', encoding='utf-8') as md:
        md.write(md_updated_content)


def process_direcotry(directory, attachment_dir):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.normpath(os.path.join(root, file))
                process_markdown_file(file_path, attachment_dir)

if __name__ == '__main__':
    process_direcotry(processing_directory, attachments_directory)