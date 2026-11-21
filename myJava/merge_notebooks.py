import os
import re
import glob
import json
import uuid

def get_notebook_files(directory=".", output_file="merged_all_notes.ipynb"):
    """Finds and sorts all .ipynb files numerically (0Syllabus, 1basics, ... 22StreamAPIAndLambdas),
    excluding the target output file."""
    pattern = os.path.join(directory, "*.ipynb")
    files = glob.glob(pattern)
    
    # Exclude output file and any merged files
    out_abs = os.path.abspath(output_file)
    files = [
        f for f in files
        if os.path.abspath(f) != out_abs and "merged" not in os.path.basename(f).lower()
    ]

    def extract_order(path):
        filename = os.path.basename(path)
        m = re.search(r"(\d+)", filename)
        return int(m.group(1)) if m else 9999

    files.sort(key=extract_order)
    return files

def merge_notebooks(input_dir=r"d:\cdac\myJava", output_file=r"d:\cdac\myJava\java_notes.ipynb"):
    """Merges all .ipynb files in input_dir into a single output notebook file one by one."""
    notebook_files = get_notebook_files(input_dir, output_file)
    print(f"Found {len(notebook_files)} notebook(s) to merge:")
    for f in notebook_files:
        print(f"  - {os.path.basename(f)}")

    merged_cells = []
    base_metadata = None

    for idx, nb_path in enumerate(notebook_files):
        with open(nb_path, "r", encoding="utf-8") as f:
            nb = json.load(f)

        if base_metadata is None:
            base_metadata = nb.get("metadata", {})

        nb_name = os.path.basename(nb_path).replace(".ipynb", "").upper()

        # Section divider markdown cell
        divider_cell = {
            "cell_type": "markdown",
            "id": uuid.uuid4().hex[:8],
            "metadata": {},
            "source": [
                f"# ========================================================\n",
                f"# NOTEBOOK: {nb_name}\n",
                f"# ========================================================\n"
            ]
        }
        merged_cells.append(divider_cell)

        # Append all cells from current notebook with unique IDs
        for cell in nb.get("cells", []):
            cell_copy = dict(cell)
            cell_copy["id"] = uuid.uuid4().hex[:8]
            merged_cells.append(cell_copy)

    # Build final merged notebook structure
    merged_notebook = {
        "cells": merged_cells,
        "metadata": base_metadata or {
            "kernelspec": {
                "display_name": "Java",
                "language": "java",
                "name": "java"
            },
            "language_info": {
                "codemirror_mode": "java",
                "file_extension": ".jshell",
                "mimetype": "text/x-java-source",
                "name": "Java",
                "pygments_lexer": "java",
                "version": "21.0.12+7-LTS-205"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 5
    }

    # Write merged notebook
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(merged_notebook, f, indent=1)

    print(f"\nSuccessfully merged {len(notebook_files)} notebooks into:")
    print(f"-> {output_file} (Total cells: {len(merged_cells)})")

if __name__ == "__main__":
    merge_notebooks()
