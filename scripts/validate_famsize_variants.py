"""Execute the scenario notebooks in separate assistant IPython namespaces.

This is not a Jupyter-kernel or selected VS Code environment validation.
"""
import base64
import hashlib
import io
import json
import os
from pathlib import Path

os.environ['MPLBACKEND'] = 'Agg'
import matplotlib.pyplot as plt
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

root = Path(__file__).resolve().parents[1]
os.chdir(root / 'notebooks')
raw_path = root / 'data/raw/student_data.csv'
raw_hash = hashlib.sha256(raw_path.read_bytes()).hexdigest()
preview = root / 'outputs/famsize_scenario/validation'
preview.mkdir(parents=True, exist_ok=True)
summary = []
for name in ['data_exploration_famsize.ipynb', 'data_preprocessing_famsize.ipynb']:
    path = root / 'notebooks' / name
    notebook = json.loads(path.read_text(encoding='utf-8'))
    InteractiveShell.clear_instance()
    shell = InteractiveShell.instance()
    shell.ast_node_interactivity = 'last_expr'
    count = 0
    figures = 0
    for index, item in enumerate(notebook['cells']):
        if item['cell_type'] != 'code':
            continue
        count += 1
        outputs = []

        def save_figures(*args, **kwargs):
            global figures
            for number in plt.get_fignums():
                figure = plt.figure(number)
                buffer = io.BytesIO()
                figure.savefig(buffer, format='png', bbox_inches='tight', dpi=110)
                payload = buffer.getvalue()
                figures += 1
                (preview / f'{path.stem}_{figures}.png').write_bytes(payload)
                outputs.append({'output_type': 'display_data', 'metadata': {},
                                'data': {'image/png': base64.b64encode(payload).decode('ascii')}})
                plt.close(figure)

        plt.show = save_figures
        with capture_output() as captured:
            result = shell.run_cell(''.join(item['source']), store_history=False)
            save_figures()
        if not result.success:
            print(captured.stdout, captured.stderr)
            raise RuntimeError(f'{name}: failed cell {index}: {result.error_in_exec or result.error_before_exec}')
        if captured.stdout:
            outputs.insert(0, {'output_type': 'stream', 'name': 'stdout', 'text': captured.stdout})
        if captured.stderr:
            outputs.append({'output_type': 'stream', 'name': 'stderr', 'text': captured.stderr})
        # Save bounded rich representations of the final expression.
        if result.result is not None:
            value = result.result
            data = {'text/plain': repr(value)}
            if hasattr(value, '_repr_html_'):
                html = value._repr_html_()
                if html:
                    data['text/html'] = html
            outputs.append({'output_type': 'execute_result', 'execution_count': count,
                            'metadata': {}, 'data': data})
        item.update(execution_count=count, outputs=outputs)
    notebook['metadata']['famsize_validation'] = {
        'method': 'Sequential assistant IPython namespace; not selected VS Code kernel',
        'code_cells': count, 'raw_sha256': raw_hash
    }
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    summary.append({'notebook': name, 'code_cells': count, 'figures': figures})
    print(summary[-1])
assert hashlib.sha256(raw_path.read_bytes()).hexdigest() == raw_hash
(preview / 'execution_summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
