import os
import subprocess
import re

content_dir = "/home/ubuntu/irawiki/content"

# Get all markdown files in content except index.md
files = []
for root, _, filenames in os.walk(content_dir):
    for filename in filenames:
        if filename.endswith(".md") and filename not in ["index.md", "iraamalia-id.md"]:
            filepath = os.path.join(root, filename)
            files.append(filepath)

# Get git commit date for each file
def get_git_date(filepath):
    try:
        result = subprocess.run(["git", "log", "-1", "--format=%at", "--", filepath], capture_output=True, text=True, check=True, cwd=content_dir)
        timestamp = result.stdout.strip()
        if timestamp:
            return int(timestamp)
    except Exception:
        pass
    # Fallback to file modified time
    return os.path.getmtime(filepath)

files_with_dates = [(f, get_git_date(f)) for f in files]
# Sort by date descending
files_with_dates.sort(key=lambda x: x[1], reverse=True)

# Generate list of markdown links (top 10)
top_files = files_with_dates[:10]
markdown_links = []
for filepath, _ in top_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    title = None
    match = re.search(r'^---\n.*?title:\s*([^\n]+).*?\n---', content, re.DOTALL)
    if match:
        title = match.group(1).strip()
        title = title.strip('"\'')
    else:
        title = os.path.basename(filepath).replace(".md", "").replace("-", " ").title()
        
    rel_path = os.path.relpath(filepath, content_dir)
    rel_path = rel_path.replace(".md", "")
    
    # Format the relative link correctly (e.g., ./folder/article or ./article)
    markdown_links.append(f"- [{title}](./{rel_path})")

# Read index.md
index_path = os.path.join(content_dir, "index.md")
with open(index_path, 'r', encoding='utf-8') as f:
    index_content = f.read()

# Replace between `# Start Here` and `# Atau Telusuri Semua`
start_marker = "# Start Here\n\n"
end_marker = "\n\n# Atau Telusuri Semua"

if start_marker in index_content and end_marker in index_content:
    before = index_content.split(start_marker)[0] + start_marker
    after = end_marker + index_content.split(end_marker)[1]
    
    new_content = before + "\n".join(markdown_links) + after
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Berhasil memperbarui index.md dengan artikel terbaru.")
else:
    print("Gagal menemukan `# Start Here` di index.md")
