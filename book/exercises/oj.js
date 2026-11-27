/* Browser-side judge for the Python exercises.
 *
 * No server: Pyodide runs the learner's code in a WebAssembly Python, the
 * case bank is a static JSON file generated from this repository's own
 * reference solutions, and progress lives in localStorage with explicit
 * export/import so it can be moved between machines.
 */
(() => {
  'use strict';

  // Local first: if you mirror Pyodide into exercises/pyodide/, the judge
  // becomes independent of every CDN. Then try the public mirrors.
  const PYODIDE_BASES = [
    './pyodide/',
    'https://cdn.jsdelivr.net/pyodide/v0.27.5/full/',
    'https://fastly.jsdelivr.net/pyodide/v0.27.5/full/',
  ];
  const STORAGE_KEY = 'coursework-oj-v1';
  const CM_BASE = 'https://cdn.jsdelivr.net/npm/codemirror@5.65.16/';

  let pyodide = null;
  let bank = [];
  let current = null;
  let editor = null;
  let progress = {};
  let saveTimer = null;

  const $ = (sel) => document.querySelector(sel);
  const esc = (s) => String(s).replace(/[&<>"']/g,
    (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  function status(text, kind = '') {
    const el = $('#oj-status');
    if (!el) return;
    el.textContent = text;
    el.className = 'oj-status' + (kind ? ' oj-' + kind : '');
  }

  function loadProgress() {
    try {
      progress = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}') || {};
    } catch (_) {
      progress = {};
    }
  }

  function persist() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
      const d = new Date();
      const el = $('#oj-saved');
      if (el) el.textContent = `已保存 ${d.toLocaleTimeString('zh-CN', { hour12: false })}`;
    } catch (_) {
      status('浏览器拒绝写入本地存储；请用「导出进度」保存。', 'bad');
    }
  }

  function recordFor(id) {
    if (!progress[id]) progress[id] = { code: '', passed: 0, updated: 0 };
    return progress[id];
  }

  function renderList() {
    const list = $('#oj-problems');
    if (!list) return;
    list.innerHTML = bank.map((p) => {
      const rec = progress[p.id] || { passed: 0 };
      const done = rec.passed === p.tests.length;
      return `<button class="oj-problem ${current && current.id === p.id ? 'active' : ''}"
        data-id="${esc(p.id)}">
        <span class="oj-num">${esc(p.id)}</span>
        <span class="oj-name">${esc(p.title)}</span>
        <span class="oj-badge ${done ? 'done' : ''}">${rec.passed}/${p.tests.length}</span>
      </button>`;
    }).join('');
    list.querySelectorAll('.oj-problem').forEach((b) => {
      b.addEventListener('click', () => selectProblem(b.dataset.id));
    });
  }

  function setCode(code) {
    if (editor) editor.setValue(code);
    else if ($('#oj-code')) $('#oj-code').value = code;
  }

  function getCode() {
    return editor ? editor.getValue() : ($('#oj-code') ? $('#oj-code').value : '');
  }

  function selectProblem(id) {
    current = bank.find((p) => p.id === id);
    if (!current) return;
    const rec = recordFor(id);
    $('#oj-title').textContent = current.title;
    $('#oj-meta').innerHTML = `${esc(current.course)} · <a href="${esc(current.page)}">题目档案与七章解析 →</a>`;
    setCode(rec.code || current.starter);
    $('#oj-results').innerHTML = '<p class="oj-hint">点「运行评测」查看每个用例的结果。</p>';
    $('#oj-score').textContent = `${rec.passed || 0} / ${current.tests.length} 通过`;
    renderList();
    status(pyodide ? '就绪' : '正在载入 Python 运行时…', pyodide ? 'good' : '');
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = () => reject(new Error(`无法加载 ${src}`));
      document.head.appendChild(s);
    });
  }

  const withTimeout = (promise, ms) => Promise.race([
    promise,
    new Promise((_, reject) => setTimeout(() => reject(new Error(`${ms / 1000} 秒超时`)), ms)),
  ]);

  async function startRuntime() {
    let last = null;
    for (const base of PYODIDE_BASES) {
      try {
        if (typeof window.loadPyodide !== 'function') {
          await withTimeout(loadScript(base + 'pyodide.js'), 20000);
        }
        pyodide = await withTimeout(loadPyodide({ indexURL: base }), 60000);
        return;
      } catch (e) {
        last = e;
        pyodide = null;
      }
    }
    throw last || new Error('没有可用的 Python 运行时');
  }

  async function boot() {
    loadProgress();
    try {
      const res = await fetch('problems.json');
      if (!res.ok) throw new Error(`problems.json: HTTP ${res.status}`);
      bank = await res.json();
    } catch (e) {
      status(`题目数据载入失败：${e}`, 'bad');
      return;
    }

    initEditor();
    renderList();
    if (bank.length) selectProblem(bank[0].id);

    status('正在载入 Pyodide（首次约 10 MB，之后走浏览器缓存）…');
    try {
      await startRuntime();
      status('Python 运行时就绪', 'good');
      $('#oj-run').disabled = false;
    } catch (e) {
      status(`Python 运行时载入失败：${e}。可把 Pyodide 的 full/ 目录放到本页同级 pyodide/ 下，改为本地加载。`, 'bad');
    }
  }

  function initEditor() {
    const area = $('#oj-code');
    if (typeof window.CodeMirror === 'function') {
      editor = window.CodeMirror.fromTextArea(area, {
        mode: 'python', theme: 'oj-dark', lineNumbers: true,
        indentUnit: 4, tabSize: 4, matchBrackets: true, lineWrapping: false,
      });
      editor.on('change', onEdit);
    } else {
      area.addEventListener('input', onEdit);
    }
  }

  function onEdit() {
    if (!current) return;
    const rec = recordFor(current.id);
    rec.code = getCode();
    rec.updated = Date.now();
    clearTimeout(saveTimer);
    saveTimer = setTimeout(persist, 400);
  }

  async function runOne(test) {
    pyodide.globals.set('_user_code', getCode());
    pyodide.globals.set('_setup', test.setup || '');
    pyodide.globals.set('_expr', test.expr);
    pyodide.globals.set('_expect', test.expect);
    const raw = pyodide.runPython(`
import io, json, contextlib
ns = {}
buf = io.StringIO()
try:
    with contextlib.redirect_stdout(buf):
        exec(_user_code, ns)
        if _setup:
            exec(_setup, ns)
        got = repr(eval(_expr, ns))
    json.dumps({"ok": got == _expect, "got": got, "printed": buf.getvalue()})
except BaseException as exc:
    json.dumps({"ok": False, "got": "", "error": repr(exc), "printed": buf.getvalue()})
`);
    return JSON.parse(raw);
  }

  async function grade() {
    if (!pyodide) { status('运行时还没准备好', 'bad'); return; }
    if (!current) return;
    const btn = $('#oj-run');
    btn.disabled = true;
    status('正在评测…');
    const results = [];
    for (const test of current.tests) {
      try {
        results.push(await runOne(test));
      } catch (e) {
        results.push({ ok: false, error: String(e), got: '', printed: '' });
      }
    }
    const passed = results.filter((r) => r.ok).length;
    const rec = recordFor(current.id);
    rec.passed = passed;
    rec.code = getCode();
    rec.updated = Date.now();
    persist();
    renderList();

    $('#oj-score').textContent = `${passed} / ${current.tests.length} 通过`;
    $('#oj-results').innerHTML = current.tests.map((t, i) => {
      const r = results[i];
      const detail = r.ok
        ? `<span class="oj-got">结果 ${esc(r.got)}</span>`
        : `<div class="oj-fail-detail">
             <div>期望：<code>${esc(t.expect)}</code></div>
             <div>实际：<code>${esc(r.got || '—')}</code></div>
             ${r.error ? `<div class="oj-error">${esc(r.error)}</div>` : ''}
             ${r.printed ? `<pre>${esc(r.printed)}</pre>` : ''}
           </div>`;
      return `<div class="oj-case ${r.ok ? 'pass' : 'fail'}">
        <div class="oj-case-head"><span class="oj-mark">${r.ok ? '✓' : '×'}</span>
        <span>${esc(t.name)}</span></div>${detail}</div>`;
    }).join('');

    status(passed === current.tests.length
      ? '全部通过。' : `${current.tests.length - passed} 个用例未通过，展开看差异。`,
      passed === current.tests.length ? 'good' : 'bad');
    btn.disabled = false;
  }

  function exportProgress() {
    const blob = new Blob([JSON.stringify(progress, null, 2)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'coursework-oj-progress.json';
    a.click();
    URL.revokeObjectURL(a.href);
  }

  function importProgress(file) {
    const reader = new FileReader();
    reader.onload = () => {
      try {
        const data = JSON.parse(reader.result);
        if (!data || typeof data !== 'object') throw new Error('格式不对');
        progress = data;
        persist();
        renderList();
        if (current) selectProblem(current.id);
        status('进度已导入', 'good');
      } catch (e) {
        status(`导入失败：${e}`, 'bad');
      }
    };
    reader.readAsText(file);
  }

  function resetCurrent() {
    if (!current) return;
    setCode(current.starter);
    onEdit();
    status('已恢复起始代码', '');
  }

  document.addEventListener('DOMContentLoaded', () => {
    $('#oj-run')?.addEventListener('click', grade);
    $('#oj-reset')?.addEventListener('click', resetCurrent);
    $('#oj-export')?.addEventListener('click', exportProgress);
    $('#oj-import')?.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) importProgress(e.target.files[0]);
    });
    boot();
  });
})();
