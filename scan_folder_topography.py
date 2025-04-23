
import os
import json

def get_folder_topography(base_path, max_depth=5):
    result = {}

    def scan_dir(current_path, depth):
        if depth > max_depth:
            return None
        tree = {}
        try:
            for item in os.listdir(current_path):
                full_path = os.path.join(current_path, item)
                if os.path.isdir(full_path):
                    subtree = scan_dir(full_path, depth + 1)
                    tree[item] = subtree if subtree is not None else {}
                else:
                    tree.setdefault("__files__", []).append(item)
        except PermissionError:
            tree = {"__error__": "Permission denied"}
        return tree

    result[base_path] = scan_dir(base_path, 0)
    return result

if __name__ == "__main__":
    base_path = r"C:\real_memory_system"
    output_path = os.path.join(base_path, "folder_topography.json")

    structure = get_folder_topography(base_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(structure, f, indent=2)

    print(f"✅ Folder map written to: {output_path}")
