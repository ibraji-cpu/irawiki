import os
import re
import yaml

# Script ini berada di dalam repo irawiki/ (sejajar dengan folder content/)
content_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")

# 1. Kumpulkan semua entitas (title, aliases, filename)
entities = {}  # Format: { "term lowercase": ("filename", "Original Term") }

# Kumpulkan semua file .md menggunakan os.walk agar mendukung sub-folder
files_info = [] 
for root, dirs, files in os.walk(content_dir):
    for filename in files:
        if filename.endswith('.md'):
            if filename.lower() == 'index.md':
                continue # Skip index.md dari target
            
            filepath = os.path.join(root, filename)
            files_info.append((filepath, filename))
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
            if not match:
                continue
            
            fm_text = match.group(1)
            try:
                fm = yaml.safe_load(fm_text) or {}
            except:
                continue
                
            base_name = filename[:-3] # hapus .md
            
            # Tambahkan title
            title = fm.get('title')
            if title:
                entities[title.lower()] = (base_name, title)
                
            # Tambahkan aliases
            aliases = fm.get('aliases', [])
            if isinstance(aliases, list):
                for al in aliases:
                    if isinstance(al, str):
                        entities[al.lower()] = (base_name, al)
                    
            # Tambahkan filename itu sendiri
            clean_basename = base_name.replace('-', ' ')
            entities[clean_basename.lower()] = (base_name, clean_basename)

# Urutkan berdasarkan panjang teks (dari yang terpanjang ke terpendek)
sorted_terms = sorted(entities.keys(), key=len, reverse=True)
sorted_terms = [t for t in sorted_terms if len(t) > 2]

def replace_terms(text, current_file_basename):
    placeholders = []
    
    protect_patterns = [
        r'```.*?```',           # Code blocks
        r'\[\[.*?\]\]',         # Wiki links yang sudah ada
        r'\[.*?\]\(.*?\)',      # Markdown links
        r'https?://[^\s<>]+',   # Raw URL
        r'`[^`]*`',             # Inline code
        r'^#+\s+.*$',           # Headings
    ]
    
    def replacer(match):
        placeholders.append(match.group(0))
        return f"__PLACEHOLDER_{len(placeholders)-1}__"
    
    # Gantikan code block dan heading
    text = re.sub(r'```.*?```', replacer, text, flags=re.DOTALL)
    text = re.sub(r'^#+\s+.*$', replacer, text, flags=re.MULTILINE)
    
    for pat in protect_patterns[1:-1]:
        text = re.sub(pat, replacer, text)
        
    # Proses pembuatan Wiki Link
    for term in sorted_terms:
        target_file, orig_term = entities[term]
        
        # Hindari self-linking
        if target_file == current_file_basename:
            continue
            
        escaped_term = re.escape(term)
        pattern = re.compile(rf'(?i)(?<![a-zA-Z0-9_])({escaped_term})(?![a-zA-Z0-9_])')
        
        def term_replacer(match):
            matched_text = match.group(1)
            return f"[[{target_file}|{matched_text}]]"
            
        text = pattern.sub(term_replacer, text)

    # Kembalikan teks yang dilindungi
    for i in range(len(placeholders)-1, -1, -1):
        text = text.replace(f"__PLACEHOLDER_{i}__", placeholders[i])
        
    return text

count_modified = 0
for filepath, filename in files_info:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not match:
        continue
        
    fm_text = match.group(1)
    body = match.group(2)
    base_name = filename[:-3]
    
    new_body = replace_terms(body, base_name)
    
    if new_body != body:
        new_content = f"---\n{fm_text}\n---{new_body}"
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count_modified += 1

print(f"[Autolink] Berhasil menambahkan wiki link otomatis pada {count_modified} file.")
