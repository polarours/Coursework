#!/usr/bin/env python3
"""Inject an English-first language switch into the rendered book.

Content bodies are bilingual (Chinese paragraph followed by English).
At runtime we classify leaf block elements by script: CJK-containing blocks
get .zh-only, Latin-only get .en-only, and a segmented control in the top nav
lets readers choose English (default) or Chinese. The choice persists in
localStorage and is restored on navigation.
"""
import glob
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Allow CI to pass book/_book as the render output directory.
SITE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(BASE, "book", "_site")

INJECT = r"""
<style>
/* Language switch — segmented control, one primary interaction. */
.cw-lang-switch { display:inline-flex; margin-left:.6rem; vertical-align:middle; }
.cw-lang-switch button {
  border:1px solid var(--cw-line,#dfe6e3); background:transparent;
  color:var(--cw-muted,#5b6b73); padding:.18rem .6rem; font-size:.82rem;
  cursor:pointer; line-height:1.2;
}
.cw-lang-switch button:first-child { border-radius:5px 0 0 5px; }
.cw-lang-switch button:last-child { border-radius:0 5px 5px 0; border-left:0; }
.cw-lang-switch button[aria-pressed="true"] {
  background:var(--cw-teal,#0f5f63); color:#fff; border-color:var(--cw-teal,#0f5f63);
}
/* Hide Chinese blocks in English mode; hide Latin blocks in Chinese mode. */
body.cw-en .zh-block, body.cw-en .cjk { display:none !important; }
body.cw-zh .en-block { display:none !important; }
body.cw-zh .zh-inline { color:var(--cw-body,#1c2733); font-size:1em; }
body.cw-en .zh-inline { color:var(--cw-muted,#5b6b73); }
</style>
<script>
(function(){
  var KEY='cw-lang';
  function mode(){ try{ return localStorage.getItem(KEY)||'en'; }catch(e){ return 'en'; } }
  function apply(m){
    document.body.classList.remove('cw-en','cw-zh');
    document.body.classList.add(m==='zh'?'cw-zh':'cw-en');
    document.documentElement.lang = (m==='zh'?'zh':'en');
    document.querySelectorAll('.cw-lang-switch button').forEach(function(b){
      b.setAttribute('aria-pressed', String(b.dataset.lang===m));
    });
  }
  function classify(){
    var cjk=/[\u3400-\u9fff]/;
    var blocks=document.querySelectorAll('#quarto-document-content p, #quarto-document-content li, #quarto-document-content figcaption');
    blocks.forEach(function(el){
      if(el.dataset.cwClass) { el.className += ' ' + el.dataset.cwClass; return; }
      var text=el.textContent||'';
      var hasCjk=cjk.test(text);
      var cls= hasCjk?'zh-block':'en-block';
      el.dataset.cwClass=cls; el.className += ' ' + cls;
      // Mixed bilingual lines (title/heading already handled): if a block has
      // substantial Latin too, keep it visible in both modes.
      // Chinese academic prose embeds many Latin proper nouns (university
      // names, book titles). Detect Chinese function words to tell it apart
      // from a genuinely bilingual heading. A true bilingual line has CJK but
      // no Chinese grammar markers.
      var zhFunction=/(的|是|在|把|而|我们|这|那|为|从|中|对|与|并|也|都|将)/.test(text);
      if(hasCjk && !zhFunction){ el.classList.add('bilingual'); }
    });
    // bilingual blocks stay visible: override hide with a later rule
    var s=document.createElement('style');
    s.textContent='body.cw-en .zh-block.bilingual, body.cw-zh .en-block.bilingual { display:block !important; }';
    document.head.appendChild(s);
  }
  function mount(){
    // Place the switch inline in the top toolbar, just before the search button.
    var nav=document.querySelector('.quarto-secondary-nav .container-fluid') ||
            document.querySelector('.quarto-secondary-nav');
    if(!nav || document.querySelector('.cw-lang-switch')) return;
    var wrap=document.createElement('div');
    wrap.className='cw-lang-switch';
    wrap.setAttribute('role','group');
    wrap.setAttribute('aria-label','Language / 语言');
    ['en','zh'].forEach(function(m){
      var b=document.createElement('button');
      b.type='button'; b.dataset.lang=m;
      b.textContent=(m==='en'?'EN':'中文');
      b.addEventListener('click',function(){
        try{localStorage.setItem(KEY,m);}catch(e){}
        apply(m);
      });
      wrap.appendChild(b);
    });
    var search=nav.querySelector('.quarto-search-button');
    if(search){ nav.insertBefore(wrap, search); } else { nav.appendChild(wrap); }
    apply(mode());
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',function(){classify();mount();});
  }else{ classify(); mount(); }
})();
</script>
"""

changed = 0
for f in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True):
    with open(f, encoding="utf-8") as fh:
        html = fh.read()
    if "cw-lang-switch" in html:
        continue
    if "</body>" in html:
        html = html.replace("</body>", INJECT + "\n</body>", 1)
    else:
        html += INJECT
    with open(f, "w", encoding="utf-8") as fh:
        fh.write(html)
    changed += 1
print(f"injected language switch into {changed} pages")
