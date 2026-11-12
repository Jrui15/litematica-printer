"""Check actual Mixin-exported GUI bytecode after launching :26.3:runClient.

Run with Java 25 on PATH, from the repository root:
  python versions/26.3/tests/check_config_mixins.py
The launch must export classes with -Dmixin.debug.export=true (configured by Loom).
"""
import os
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[3]
export = root / 'run/.mixin.out/class'
javap = str(Path(os.environ['JAVA_HOME']) / 'bin/javap') if 'JAVA_HOME' in os.environ else 'javap'
code = subprocess.check_output([
    javap, '-p', '-c', '-classpath', str(export),
    'fi.dy.masa.litematica.gui.GuiConfigs',
], text=True)
for method in ('getConfigs', 'getAllConfigs'):
    match = re.search(r'  public [^\n]+ ' + method + r'\(\);\n(.*?)(?=\n  (?:public|private|protected)|\Z)', code, re.S)
    assert match, f'Missing {method}'
    body = match.group(1)
    for handler in ('moreOptions', 'moreHotkeyOptions'):
        assert len(re.findall(r'// Method .*' + handler + r'"?:', body)) == 1, (method, handler)
    assert 'Configs$Generic.OPTIONS' not in body, method
    assert 'Hotkeys.HOTKEY_LIST' not in body, method
    print(f'PASS: {method} uses printer settings and hotkeys exactly once')
