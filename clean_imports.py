import os
import re

def clean_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Very aggressive replacement for space before @
        # Looks for any space character followed by @/
        new_content = content.replace("' @/", "'@/").replace('" @/', '"@/').replace("  @/", "@/")
        
        if content != new_content:
            with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(new_content)
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False

def main():
    base_dir = os.path.join('frontend', 'src')
    fixed_count = 0
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(('.tsx', '.ts')):
                full_path = os.path.join(root, file)
                if clean_file(full_path):
                    print(f"Fixed: {full_path}")
                    fixed_count += 1
    print(f"Total files fixed: {fixed_count}")

if __name__ == '__main__':
    main()