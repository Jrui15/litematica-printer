"""Run after :26.3:runClient exports both Easy Place classes through Mixin.

Uses Java 25 javap (JAVA_HOME or PATH). Checks real transformed bytecode,
not just the source annotations; an unhooked activation path fails this test.
"""
import os
from pathlib import Path
import re
import subprocess

root = Path(__file__).resolve().parents[3]
javap = str(Path(os.environ['JAVA_HOME']) / 'bin/javap') if 'JAVA_HOME' in os.environ else 'javap'
for target, method in [('EasyPlaceUtils', 'handleEasyPlace'), ('WorldUtils', 'doEasyPlaceAction')]:
    code = subprocess.check_output([javap, '-p', '-c', '-classpath',
        str(root / 'run/.mixin.out/class'), 'fi.dy.masa.litematica.util.' + target], text=True)
    body = re.search(r'  private static [^\n]+ ' + method + r'\([^\n]*\);\n(.*?)(?=\n  (?:public|private|protected)|\Z)', code, re.S)
    assert body, (target, method)
    assert 'onDoEasyPlaceAction' in body[1], f'{target} bypasses printer'
    assert 'CallbackInfoReturnable.isCancelled' in body[1], f'{target} ignores printer result'
    assert 'Printer.doPrinterAction' in code, f'{target} has no printer delegation'
    assert 'Printer.doEasyPlaceFakeRotation' in code, f'{target} loses fake rotation mode'
    print(f'PASS: {target}.{method} invokes the cancellable printer handler')
