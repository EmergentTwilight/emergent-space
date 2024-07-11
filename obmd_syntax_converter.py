import os
import shutil
import sys
import re

# <<<<<<<<<< settings >>>>>>>>>> #

# links replacement
extension_names = ['.jpg', '.jpeg', '.png', '.pdf']
processing_directory = "docs"
attachment_directory = "D:/Obsidian-Vault/Alpha"

# code block highlight syntax match
hl_pattern = r'hl="([\d,-]+)"'

# permalink forbidden chars
chars_to_delete = ['*', '，', '\\']

# <<<<<<<<<< utils >>>>>>>>>> #

def replace_hl(match):
    lines = match.group(1).replace(',', ' ')
    return f'hl_lines="{lines}"'


def md_ignore_codes(md_content):
    md_content = re.sub(r'```.*?```', '', md_content, flags=re.DOTALL)  # remove code blocks
    md_content = re.sub(r'`.*?`', '', md_content)  # remove inline code
    return md_content


def add_md_ext(filenameOrPath):
    if not filenameOrPath.endswith('.md'):
        filenameOrPath += '.md'
    return filenameOrPath


def extract_wikilink_components(wikilink):  # [[path#anchor|title]]
    match = re.match(r'([^|#]+)?(?:#([^|]*))?(?:\|([^#]*))?', wikilink)
    if match:
        path = match.group(1) if match.group(1) else None
        anchor = match.group(2) if match.group(2) else None
        title = match.group(3) if match.group(3) else None
        return path, anchor, title
    print(f'        Extracting "{wikilink}" failed: not matched')
    sys.exit(1)


def process_anchor(anchor):
    # process chars to delete directly
    print(f'        Processing anchor "{anchor}"')
    anchor = ''.join([char for char in anchor if char not in chars_to_delete])
    anchor = anchor.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = anchor.replace(' ', '-')
    print(f'        Processing result "{anchor}"')
    return anchor


def find_file_in_directory(filenameOrPath, directory):  # relative to pwd, easy to copy attachments
    filename = os.path.basename(filenameOrPath)  # allow redundant path
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.normpath(os.path.join(root, filename))
    print(f'        Error: "{filename}" not found in "{directory}"')
    sys.exit(1)


def find_file_in_directory_relative(filenameOrPath, directory, basepath):
    filename = os.path.basename(filenameOrPath)  # allow redundant path
    for root, dirs, files in os.walk(directory):
        if filename in files:
            return os.path.normpath(os.path.relpath(os.path.join(root, filename), basepath))
    print(f'        Error: "{filename}" not found in "{directory}"')
    sys.exit(1)


def convert_wikilinks(md_content, md_filename, md_dir):
    md_content_ignored = md_ignore_codes(md_content)
    wikilinks = re.findall(r'\[\[(.*?)\]\]', md_content_ignored)
    for wikilink in wikilinks:
        link_path, link_anchor, link_title = extract_wikilink_components(wikilink)
        # handle attachments
        if link_path and any(link_path.endswith(ext) for ext in extension_names):
            # process name, name without space is valid
            attachment_name = os.path.basename(link_path)
            attachment_name_no_space = attachment_name.replace(' ', '-')
            print(f'    Finding attachment "{attachment_name}" in "{attachment_directory}"')
            # find and copy
            attachment_path = find_file_in_directory(attachment_name, attachment_directory)
            shutil.copy(attachment_path, os.path.join(md_dir, attachment_name_no_space))
            # update link
            link_title_new = link_title if link_title else (attachment_name + link_anchor) if link_anchor else attachment_name
            md_content = md_content.replace(f"[[{wikilink}]]", f"[{link_title_new}]({attachment_name_no_space})")
        # handle links to other content
        else:
            link_anchor_new = process_anchor(link_anchor) if link_anchor else None
            # in-file anchor
            if link_path is None or add_md_ext(os.path.basename(link_path)) == md_filename:
                print(f'    Converting in-file wikilink "{wikilink}"')
                link_title_new = link_title if link_title else link_anchor
                md_content = md_content.replace(f"[[{wikilink}]]", f"[{link_title_new}](#{link_anchor_new})")
            # inter-file link
            else:
                print(f'    Converting inter-file wikilink "{wikilink}"')
                rel_path = find_file_in_directory_relative(add_md_ext(link_path), processing_directory, md_dir)
                link_title_new = link_title if link_title else f"{os.path.basename(link_path)}#{link_anchor}" if link_anchor else os.path.basename(link_path)
                rel_path_new = f"{rel_path}#{link_anchor_new}" if link_anchor else rel_path
                md_content = md_content.replace(f"[[{wikilink}]]", f"[{link_title_new}]({rel_path_new})")

    return md_content



# <<<<<<<<<< process functions >>>>>>>>>> #

def process_md_file(md_dir, md_filename):
    md_path = os.path.join(md_dir, md_filename)
    print(f'Processing md file "{md_path}"')
    # open and read content
    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # fix code block highlight
    md_content = re.sub(hl_pattern, replace_hl, md_content)

    # convert wikilinks
    md_content = convert_wikilinks(md_content, md_filename, md_dir)

    # open and write
    with open(md_path, 'w', encoding='utf-8') as md:
        md.write(md_content)


def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                process_md_file(root, file)

process_directory(processing_directory)
