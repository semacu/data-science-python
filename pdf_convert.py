"""
Script to convert notebooks to PDFs.

Ensure that you have the correct LaTeX packages installed on your machine
for nbconvert to use else you will recieve an OSError.
"""

import re
import os
import platform
import shutil
import subprocess

if not os.path.exists('pdfs'):
    os.mkdir('pdfs')

for nb in os.listdir('notebooks'):
    # Skip non-notebooks
    if not re.search(r'\.ipynb$', nb):
        continue

    # Convert to PDF
    system = platform.system()
    if system == 'Windows':
        process = subprocess.Popen([
            'jupyter', 'nbconvert',
            f'notebooks/{nb}',
            '--to', 'pdf',
            '--TagRemovePreprocessor.enabled=True',
            "--TagRemovePreprocessor.remove_cell_tags=['remove_cell']",
            "--TagRemovePreprocessor.remove_input_tags=['remove_input']",
            "--TagRemovePreprocessor.remove_single_output_tags=['remove_single_output']",
            "--TagRemovePreprocessor.remove_all_outputs_tags=['remove_all_output']",
        ], shell=True)
    elif system in ('Linux', 'Darwin'):
        process = subprocess.Popen(' '.join([
            'jupyter nbconvert',
            f"notebooks/{nb}",
            '--to pdf',
            '--TagRemovePreprocessor.enabled=True',
            "--TagRemovePreprocessor.remove_cell_tags=\"['remove_cell']\"",
            "--TagRemovePreprocessor.remove_input_tags=\"['remove_input']\"",
            "--TagRemovePreprocessor.remove_single_output_tags=\"['remove_single_output']\"",
            "--TagRemovePreprocessor.remove_all_outputs_tags=\"['remove_all_output']\"",
        ]), shell=True)
    else:
        raise NotImplementedError("build does currently not support system")
    process.wait()
    
    # Move file
    pdf = nb.replace('ipynb', 'pdf')
    shutil.move(f'notebooks/{pdf}', f'pdfs/{pdf}')
 
