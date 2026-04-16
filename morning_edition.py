#!/usr/bin/env python3
"""Morning Edition — Hacker News Curation Magazine Generator"""

import os, re
os.environ.setdefault("DOTENV_PATH", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError: pass

import requests
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List

@dataclass
class Story:
    id: str; title: str; url: str; domain: str; points: int
    num_comments: int; author: str
    interest_keywords: List[str] = field(default_factory=list)
    personal_pick: bool = False; final_score: float = 0.0; spread_index: int = 0

def extract_domain(url):
    if not url: return "news.ycombinator.com"
    try:
        from urllib.parse import urlparse
        return urlparse(url).netloc.replace("www.", "")
    except: return "unknown"

def fetch_hn_stories(n=30):
    try:
        r = requests.get("https://hn.algolia.com/api/v1/search", params={"tags":"front_page","hitsPerPage":n}, timeout=10)
        r.raise_for_status()
        return [Story(
            id=str(h["objectID"]), title=h["title"],
            url=h.get("url") or f"https://news.ycombinator.com/item?id={h['objectID']}",
            domain=extract_domain(h.get("url","")),
            points=h.get("points",0), num_comments=h.get("num_comments",0),
            author=h.get("author","anonymous")
        ) for h in r.json().get("hits",[])]
    except Exception as e:
        print(f"[ERROR] {e}"); return []

INTEREST_KEYWORDS = {
    "ai": ["ai","llm","gpt","claude","gemini","openai","language model","inference","ollama","diffusion","copilot"],
    "creative": ["design","figma","obsidian","editor","3d","blender","typography","canva","ui design"],
    "dev": ["cli","terminal","ide","vscode","neovim","debugger","build","open source","library","framework","api","docker","rust","go ","typescript","python","database"],
    "privacy": ["privacy","security","encryption","self-hosted","vpn","signal","firewall"],
    "science": ["quantum","neuroscience","biology","physics","astronomy","genetics","fusion","consciousness","evolution","james webb"],
    "actionable": ["show hn","launch","open source","released","introducing","how to","tutorial","guide","course","tool"],
}
SKIP = [r'\bcrypto\b',r'\bbitcoin\b',r'\bethereum\b',r'\bnft\b',r'\bweb3\b',r'\bblockchain\b',r'\btrump\b',r'\bbiden\b',r'\bpolitics\b',r'\belection\b']

def curate(stories):
    for s in stories:
        c = (s.title+s.url).lower()
        if any(re.search(p,c) for p in SKIP): continue
        s.interest_keywords = list({kw for kws in INTEREST_KEYWORDS.values() for kw in kws if kw.lower() in c})
        s.final_score = s.points + s.num_comments*0.5 + 50*len(s.interest_keywords)
        s.personal_pick = s.final_score > 50 or len(s.interest_keywords) >= 3
    stories.sort(key=lambda x: x.final_score, reverse=True)
    for i,s in enumerate(stories[:10],1): s.spread_index = i
    return stories[:10]

def build_html(stories, date_str):
    def meta(s):
        b = '<span class="badge">&#9733; For You</span>' if s.personal_pick else ''
        return f'<div class="m">{b}<a href="{s.url}" target="_blank" class="ml">{s.domain}</a><span class="ms">{s.points} pts</span><a href="https://news.ycombinator.com/item?id={s.id}" target="_blank" class="mc">{s.num_comments} comments</a><span class="ma">by {s.author}</span></div>'
    
    # Spreads: each returns complete <section> with inline <style>
    def s1(s):
        n = f"{s.spread_index:02d}"
        b = '<span class="badge" style="position:absolute;top:40px;right:40px">&#9733; For You</span>' if s.personal_pick else ''
        return f'<section class="sp1"><style>.sp1{{min-height:100vh;background:#FDF6E3;display:flex;align-items:flex-end;padding:80px;position:relative;overflow:hidden}}.sp1::after{{content:"";position:absolute;bottom:0;left:80px;right:80px;height:2px;background:#2D2A26;opacity:.15}}.n1{{position:absolute;top:-20px;left:-10px;font-family:Fraunces,serif;font-size:clamp(180px,25vw,320px);font-weight:900;color:#2D2A26;opacity:.06;line-height:1;user-select:none}}.c1{{position:relative;z-index:1;max-width:900px}}.t1{{font-family:Fraunces,serif;font-size:clamp(36px,5vw,72px);font-weight:700;line-height:1.1;color:#2D2A26;margin-bottom:30px}}.m{{display:flex;align-items:center;gap:16px;flex-wrap:wrap}}.ml,.ms,.mc,.ma{{font-size:13px;color:#6B6560}}.ml{{text-decoration:underline}}.badge{{display:inline-block;background:#D4704A;color:white;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;padding:4px 10px;border-radius:3px}}</style><div class="n1">{n}</div>{b}<div class="c1"><h2 class="t1">{s.title}</h2>{meta(s)}</div></section>'
    
    def s2(s):
        n = f"{s.spread_index:02d}"
        b = '<span class="badge" style="background:rgba(255,255,255,.15);position:absolute;top:40px;right:40px">&#9733; For You</span>' if s.personal_pick else ''
        return f'<section class="sp2"><style>.sp2{{min-height:100vh;background:#0D1B2A;display:flex;align-items:center;padding:80px;position:relative;overflow:hidden}}.n2{{position:absolute;right:-20px;top:50%;transform:translateY(-50%);font-family:Fraunces,serif;font-size:clamp(160px,22vw,280px);font-weight:900;color:#1E3A5F;line-height:1;user-select:none}}.c2{{position:relative;z-index:1;max-width:800px}}.t2{{font-family:Fraunces,serif;font-size:clamp(28px,4vw,56px);font-weight:700;line-height:1.2;color:#fff;margin-bottom:30px}}.dm{{display:flex;align-items:center;gap:16px;flex-wrap:wrap}}.dl{{font-size:13px;color:#8BA3B9;text-decoration:underline}}.ds,.da{{font-size:13px;color:#6B8CAE}}.dc{{font-size:13px;color:#8BA3B9;text-decoration:underline}}.dc:hover{{color:#fff}}</style><div class="n2">{n}</div>{b}<div class="c2"><h2 class="t2">{s.title}</h2><div class="dm"><a href="{s.url}" class="dl" target="_blank">{s.domain}</a><span class="ds">{s.points} pts</span><a href="https://news.ycombinator.com/item?id={s.id}" class="dc" target="_blank">{s.num_comments} comments</a><span class="da">by {s.author}</span></div></div></section>'
    
    def s3(s):
        n = f"{s.spread_index:02d}"
        brd = "border-left:4px solid #D4704A;" if s.personal_pick else ""
        b = '<span class="badge" style="background:#D4704A">&#9733; For You</span>' if s.personal_pick else ''
        return f'<section class="sp3"><style>.sp3{{min-height:100vh;background:#F4ACB7;display:flex;align-items:center;padding:80px;position:relative}}.st3{{position:absolute;top:40px;right:40px;width:90px;height:90px;background:#D4704A;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:Fraunces,serif;font-size:36px;font-weight:900;color:white;box-shadow:0 4px 20px rgba(212,112,74,.3)}}.c3{{max-width:900px;padding-left:20px}}.l3{{font-size:11px;font-weight:600;letter-spacing:.15em;text-transform:uppercase;color:#D4704A;margin-bottom:16px}}.t3{{font-family:Fraunces,serif;font-size:clamp(28px,4vw,52px);font-weight:700;line-height:1.2;color:#2D2A26;margin-bottom:30px}}.rm{{display:flex;align-items:center;gap:16px;flex-wrap:wrap}}.rl,.rs,.ra{{font-size:13px;color:#6B6560}}.rl{{text-decoration:underline}}.rc{{font-size:13px;color:#6B6560;text-decoration:underline}}.rc:hover{{color:#D4704A}}</style><div class="st3">{n}</div><div class="c3" style="{brd}"><div class="l3">{b}<span> Worth Reading</span></div><h2 class="t3">{s.title}</h2><div class="rm"><a href="{s.url}" class="rl" target="_blank">{s.domain}</a><span class="rs">{s.points} pts</span><a href="https://news.ycombinator.com/item?id={s.id}" class="rc" target="_blank">{s.num_comments} comments</a><span class="ra">by {s.author}</span></div></div></section>'
    
    def s4(s):
        n = f"{s.spread_index:02d}"
        b = '<span class="badge" style="background:#2D4A3E;color:#E8F0E8;position:absolute;top:40px;right:40px">&#9733; For You</span>' if s.personal_pick else ''
        return f'<section class="sp4"><style>.sp4{{min-height:100vh;background:#1A2F23;display:flex;align-items:center;padding:80px;position:relative;overflow:hidden}}.sp4::before{{content:"";position:absolute;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.03) 2px,rgba(0,0,0,.03) 4px);pointer-events:none}}.c4{{position:relative;z-index:1;max-width:900px}}.n4{{position:absolute;right:-20px;bottom:-60px;font-family:Fraunces,serif;font-size:clamp(120px,18vw,200px);font-weight:900;color:rgba(232,240,232,.05);line-height:1;user-select:none}}.p4{{display:flex;align-items:flex-start;gap:12px;margin-bottom:40px}}.ps{{font-size:clamp(28px,4vw,48px);font-weight:700;color:#7FCC8F;flex-shrink:0;margin-top:4px}}.pt{{font-family:Fraunces,serif;font-size:clamp(22px,3vw,44px);font-weight:700;line-height:1.2;color:#E8F0E8}}.tm{{display:flex;align-items:center;gap:10px;flex-wrap:wrap}}.tl,.tc,.ta,.ts,.tsep{{font-family:monospace;font-size:14px}}.tl{{color:#7FCC8F}}.tc,.ta,.ts{{color:#5A8A6A}}.tsep{{color:#3D5A45}}.tc:hover{{color:#E8F0E8}}</style>{b}<div class="c4"><div class="n4">{n}</div><div class="p4"><span class="ps">$</span><span class="pt">{s.title}</span></div><div class="tm"><a href="{s.url}" class="tl" target="_blank">&rarr; {s.domain}</a><span class="tsep">|</span><a href="https://news.ycombinator.com/item?id={s.id}" class="tc" target="_blank">// {s.num_comments} comments</a><span class="tsep">|</span><span class="ta">// {s.author}</span><span class="tsep">|</span><span class="ts">{s.points} pts</span></div></div></section>'
    
    def s5(s):
        n = f"{s.spread_index:02d}"
        b = '<span class="badge aca">&#9733; For You</span>' if s.personal_pick else ''
        fl = s.title[0]; rt = s.title[1:]
        return f'<section class="sp5"><style>.sp5{{min-height:100vh;background:#FAF9F6;display:flex;align-items:center;padding:10vw;position:relative}}.n5{{position:absolute;top:40px;left:10vw;font-family:Fraunces,serif;font-size:72px;font-weight:300;color:#6B6560;opacity:.3}}.c5{{max-width:700px;margin:0 auto}}.t5{{font-family:Fraunces,serif;font-size:clamp(26px,3.5vw,44px);font-weight:700;line-height:1.3;color:#2D2A26;margin-bottom:20px}}.dc{{float:left;font-family:Fraunces,serif;font-size:clamp(100px,12vw,160px);font-weight:900;line-height:.8;color:#D4704A;margin-right:8px;margin-top:8px}}.ar{{width:80px;height:2px;background:#D4704A;margin-bottom:24px}}.am{{display:flex;align-items:center;gap:16px;flex-wrap:wrap}}.al,.as,.ac,.aa{{font-size:13px;color:#6B6560}}.al{{text-decoration:underline}}.ac:hover{{color:#D4704A}}.aca{{margin-left:4px}}</style><div class="n5">{n}</div><div class="c5"><h2 class="t5"><span class="dc">{fl}</span>{rt}</h2><div class="ar"></div><div class="am"><a href="{s.url}" class="al" target="_blank">{s.domain}</a>{b}<span class="as">{s.points} pts</span><a href="https://news.ycombinator.com/item?id={s.id}" class="ac" target="_blank">{s.num_comments} comments</a><span class="aa">by {s.author}</span></div></div></section>'
    
    def s6(s):
        n = f"{s.spread_index:02d}"
        b = '<span class="badge" style="position:absolute;top:40px;right:40px">&#9733; For You</span>' if s.personal_pick else ''
        return f'<section class="sp6"><style>.sp6{{min-height:100vh;background:#E8E4E1;display:flex;align-items:center;justify-content:center;padding:80px;position:relative;overflow:hidden}}.n6{{position:absolute;right:-40px;top:50%;transform:translateY(-50%);font-family:Fraunces,serif;font-size:clamp(180px,25vw,320px);font-weight:900;color:#2D2A26;opacity:.04;line-height:1;user-select:none}}.c6{{text-align:center;position:relative;z-index:1;max-width:800px}}.v6{{font-family:Fraunces,serif;font-size:clamp(80px,14vw,160px);font-weight:900;color:#2D2A26;line-height:1}}.l6{{font-size:clamp(14px,2vw,20px);color:#6B6560;letter-spacing:.15em;text-transform:uppercase;margin-bottom:40px}}.t6{{font-family:Fraunces,serif;font-size:clamp(20px,3vw,36px);font-weight:400;font-style:italic;line-height:1.3;color:#2D2A26;margin-bottom:30px}}.bm{{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap}}.bl,.bc,.ba,.bsep{{font-size:13px;color:#6B6560}}.bl{{text-decoration:underline}}.bc:hover{{color:#D4704A}}</style><div class="n6">{n}</div>{b}<div class="c6"><div class="v6">{s.points}</div><div class="l6">points</div><h2 class="t6">{s.title}</h2><div class="bm"><a href="{s.url}" class="bl" target="_blank">{s.domain}</a><span class="bsep">&middot;</span><a href="https://news.ycombinator.com/item?id={s.id}" class="bc" target="_blank">{s.num_comments} comments</a><span class="bsep">&middot;</span><span class="ba">by {s.author}</span></div></div></section>'
    
    def s7(s):
        n = f"{s.spread_index:02d}"
        b = '<span class="badge" style="background:#D4704A">&#9733; For You</span>' if s.personal_pick else ''
        return f'<section class="sp7"><style>.sp7{{min-height:100vh;background:#F5F0E1;display:flex;flex-direction:column;padding:60px 80px}}.mh{{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}}.me{{font-family:Fraunces,serif;font-size:14px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:#6B6560}}.md{{font-size:12px;color:#6B6560}}.rr{{border-top:1px solid #2D2A26;margin-bottom:40px}}.rdd{{border-bottom:1px solid #2D2A26;margin-bottom:0;margin-top:4px}}.bd{{flex:1;display:flex;flex-direction:column;justify-content:center;padding:40px 0}}.an{{font-family:Fraunces,serif;font-size:40px;font-weight:700;color:#2D2A26;opacity:.25;margin-bottom:10px;width:60px;height:60px;border:2px solid #2D2A26;border-radius:50%;display:flex;align-items:center;justify-content:center;line-height:1}}.t7{{font-family:Fraunces,serif;font-size:clamp(24px,3.5vw,42px);font-weight:700;line-height:1.2;color:#2D2A26;margin-bottom:24px;max-width:800px}}.nm{{display:flex;align-items:center;gap:14px;flex-wrap:wrap}}.nl,.ns,.nc,.na{{font-family:monospace;font-size:12px;color:#6B6560}}.nl{{text-decoration:underline}}.nc:hover{{color:#D4704A}}</style><div class="mh"><span class="me">Morning Edition</span><span class="md">{datetime.now().strftime("%B %d, %Y")}</span></div><div class="rr rdd"></div><div class="bd"><div class="an">{n}</div><h2 class="t7">{s.title}</h2><div class="nm"><a href="{s.url}" class="nl" target="_blank">{s.domain}</a>{b}<span class="ns">{s.points} pts</span><a href="https://news.ycombinator.com/item?id={s.id}" class="nc" target="_blank">{s.num_comments} comments</a><span class="na">by {s.author}</span></div></div><div class="rr"></div></section>'
    
    def s8(s):
        n = f"{s.spread_index:02d}"
        b = '<span class="badge" style="background:#FF6B9D;color:#1A1A2E;position:absolute;top:40px;right:40px">&#9733; For You</span>' if s.personal_pick else ''
        return f'<section class="sp8"><style>.sp8{{min-height:100vh;background:#1A1A2E;display:flex;align-items:center;justify-content:center;padding:80px;position:relative;overflow:hidden}}.rt,.rb{{position:absolute;left:80px;right:80px;height:1px;background:#FF6B9D;box-shadow:0 0 8px #FF6B9D,0 0 20px rgba(255,107,157,.3)}}.rt{{top:60px}}.rb{{bottom:60px}}.c8{{text-align:center;max-width:900px;position:relative;z-index:1}}.n8{{font-family:Fraunces,serif;font-size:clamp(100px,18vw,240px);font-weight:900;color:#fff;line-height:1;text-shadow:0 0 20px #FF6B9D,0 0 40px #FF6B9D,0 0 80px rgba(255,107,157,.5);margin-bottom:30px}}.t8{{font-family:Fraunces,serif;font-size:clamp(22px,3.5vw,48px);font-weight:700;line-height:1.2;color:#fff;margin-bottom:20px}}.dom{{margin-bottom:20px}}.nl{{font-family:monospace;font-size:14px;color:#FF6B9D;text-decoration:none;letter-spacing:.05em}}.neom{{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap}}.ns,.nc,.na,.nsep{{font-size:13px;color:rgba(255,255,255,.5)}}.nc:hover{{color:#FF6B9D}}</style>{b}<div class="rt"></div><div class="c8"><div class="n8">{n}</div><h2 class="t8">{s.title}</h2><div class="dom"><a href="{s.url}" class="nl" target="_blank">{s.domain}</a></div><div class="neom"><span class="ns">{s.points} pts</span><span class="nsep">&middot;</span><a href="https://news.ycombinator.com/item?id={s.id}" class="nc" target="_blank">{s.num_comments} comments</a><span class="nsep">&middot;</span><span class="na">by {s.author}</span></div></div><div class="rb"></div></section>'
    
    def s9(s):
        n = f"{s.spread_index:02d}"
        b = '<span class="badge" style="margin-right:12px">&#9733; For You</span>' if s.personal_pick else ''
        return f'<section class="sp9"><style>.sp9{{min-height:100vh;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 40px;position:relative}}.n9{{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-family:Fraunces,serif;font-size:clamp(200px,30vw,400px);font-weight:300;color:#2D2A26;opacity:.03;line-height:1;user-select:none;pointer-events:none}}.c9{{max-width:600px;width:100%;text-align:center;position:relative;z-index:1}}.t9{{font-family:Fraunces,serif;font-size:clamp(20px,3vw,40px);font-weight:400;line-height:1.4;color:#2D2A26;margin-bottom:24px}}.rr9{{width:40px;height:1px;background:#2D2A26;margin:0 auto 24px;opacity:.2}}.minm{{display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap}}.minl,.mins,.minc,.minsep{{font-size:13px;color:#6B6560}}.minl{{text-decoration:underline}}.minc:hover{{color:#D4704A}}</style><div class="n9">{n}</div><div class="c9"><h2 class="t9">{s.title}</h2><div class="rr9"></div><div class="minm">{b}<a href="{s.url}" class="minl" target="_blank">{s.domain}</a><span class="minsep">&middot;</span><span class="mins">{s.points} pts</span><span class="minsep">&middot;</span><a href="https://news.ycombinator.com/item?id={s.id}" class="minc" target="_blank">{s.num_comments} comments</a></div></div></section>'
    
    def s10(s):
        n = f"{s.spread_index:02d}"
        b = '<span class="badge" style="background:#FDF6E3;color:#D4704A;position:absolute;top:40px;right:40px">&#9733; For You</span>' if s.personal_pick else ''
        return f'<section class="sp10"><style>.sp10{{min-height:100vh;background:#D4704A;display:flex;align-items:center;justify-content:center;padding:80px;position:relative;overflow:hidden}}.n10{{position:absolute;bottom:-30px;right:-20px;font-family:Fraunces,serif;font-size:clamp(180px,25vw,320px);font-weight:900;color:#FDF6E3;opacity:.12;line-height:1;user-select:none}}.c10{{text-align:center;max-width:800px;position:relative;z-index:1}}.t10{{font-family:Fraunces,serif;font-size:clamp(26px,4vw,52px);font-weight:700;line-height:1.2;color:#fff;margin-bottom:30px}}.wm{{display:flex;align-items:center;justify-content:center;gap:14px;flex-wrap:wrap;margin-bottom:60px}}.wl,.ws,.wc,.wa{{font-size:13px;color:rgba(255,255,255,.7)}}.wl{{text-decoration:underline}}.wc:hover{{color:#fff}}.cl{{opacity:.6;text-align:center}}.fl{{font-size:20px;color:#FDF6E3;margin-bottom:8px}}.ct{{font-family:Fraunces,serif;font-size:clamp(16px,2.5vw,24px);font-weight:400;font-style:italic;color:#FDF6E3}}</style><div class="n10">{n}</div>{b}<div class="c10"><h2 class="t10">{s.title}</h2><div class="wm"><a href="{s.url}" class="wl" target="_blank">{s.domain}</a><span class="ws">{s.points} pts</span><a href="https://news.ycombinator.com/item?id={s.id}" class="wc" target="_blank">{s.num_comments} comments</a><span class="wa">by {s.author}</span></div><div class="cl"><div class="fl">&#10022;</div><div class="ct">That\'s all for today.</div></div></div></section>'
    
    spreads = [s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]
    body = "\n".join(spreads[s.spread_index-1](s) for s in stories)
    
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Morning Edition — {date_str}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,700;0,9..144,900;1,9..144,300;1,9..144,400;1,9..144,700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
html{{scroll-behavior:smooth}}
body{{font-family:'Inter',-apple-system,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
.badge{{display:inline-block;background:#D4704A;color:white;font-size:11px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;padding:4px 10px;border-radius:3px}}
a{{color:inherit;text-decoration:none}}
.cover{{min-height:100vh;background:#FDF6E3;display:flex;align-items:center;justify-content:center}}
.cover-i{{text-align:center;padding:40px}}
.cover-d{{font-family:Fraunces,serif;font-size:clamp(16px,3vw,22px);font-weight:400;font-style:italic;color:#D4704A;margin-bottom:20px;letter-spacing:.05em}}
.cover-t{{font-family:Fraunces,serif;font-size:clamp(72px,14vw,180px);font-weight:900;line-height:.9;letter-spacing:-.02em;color:#2D2A26;text-transform:uppercase}}
.cover-s{{font-family:'Inter',sans-serif;font-size:clamp(12px,1.5vw,16px);color:#6B6560;margin-top:30px;letter-spacing:.15em;text-transform:uppercase}}
.cover-o{{font-size:24px;color:#D4704A;margin:40px auto;opacity:.6}}
.cover-h{{font-family:'Inter',sans-serif;font-size:12px;color:#6B6560;letter-spacing:.1em;text-transform:uppercase;animation:b 2s ease-in-out infinite}}
@keyframes b{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(6px)}}}}
</style>
</head>
<body>
<section class="cover">
<div class="cover-i">
<div class="cover-d">{date_str}</div>
<h1 class="cover-t">Morning<br>Edition</h1>
<div class="cover-s">Curated from Hacker News</div>
<div class="cover-o">&#10022;</div>
<div class="cover-h">Scroll to read &#8595;</div>
</div>
</section>
{body}
</body>
</html>"""

def build_txt(stories, date_str):
    lines = ["="*60,"MORNING EDITION",f"Curated from Hacker News — {date_str}","="*60,""]
    for s in stories:
        p = "[* FOR YOU] " if s.personal_pick else ""
        lines += [f"--- Story {s.spread_index:02d} ---",f"{p}{s.title}",f"URL: {s.url}",f"Source: {s.domain} | {s.points} pts | {s.num_comments} comments | by {s.author}"]
        if s.interest_keywords: lines.append(f"Tags: {', '.join(s.interest_keywords[:5])}")
        lines.append("")
    lines += ["="*60,"That's all for today.","="*60]
    return "\n".join(lines)

def save(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path

def send_email(html_path, txt_path, date_str):
    u,p,t = os.getenv("EMAIL_USER"),os.getenv("EMAIL_PASS"),os.getenv("EMAIL_TO")
    if not all([u,p,t]): print("[WARN] Email not configured"); return False
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        msg = MIMEMultipart("alternative")
        msg["From"],msg["To"],msg["Subject"] = u,t,f"Morning Edition — {date_str}"
        msg.attach(MIMEText(html_path.read_text(encoding="utf-8"),"html","utf-8"))
        msg.attach(MIMEText(txt_path.read_text(encoding="utf-8"),"plain","utf-8"))
        server = smtplib.SMTP_SSL("smtp.qq.com",465)
        server.login(u,p)
        server.sendmail(u,[t],msg.as_string())
        server.quit()
        print(f"[OK] Email sent to {t}")
        return True
    except Exception as e:
        print(f"[ERROR] Email: {e}"); return False

def send_telegram(stories, date_str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id: print("[WARN] Telegram not configured"); return False
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        msg = f"&#128240; <b>Morning Edition</b> — {date_str}\n\n"
        for s in stories:
            star = "&#9733; " if s.personal_pick else ""
            tags = f" [{', '.join(s.interest_keywords[:3])}]" if s.interest_keywords else ""
            msg += f"{s.spread_index}. {star}{s.title}\n"
            msg += f"   {s.domain} | {s.points} pts{tags}\n\n"
        msg += f"&#128228; Check email for full magazine"
        data = {"chat_id": chat_id, "text": msg, "parse_mode": "HTML"}
        r = requests.post(url, json=data, timeout=10)
        if r.status_code == 200: print("[OK] Telegram sent"); return True
        print(f"[ERROR] Telegram: {r.text}"); return False
    except Exception as e:
        print(f"[ERROR] Telegram: {e}"); return False

def mock_stories():
    data=[
        {"title":"Show HN: I built a local AI coding assistant with Llama 3","url":"https://github.com/example/llama-code","points":342,"num_comments":89,"author":"dev123"},
        {"title":"PostgreSQL 17 adds improved query planning","url":"https://postgresql.org/blog/17","points":215,"num_comments":45,"author":"db_admin"},
        {"title":"The NSA releases an open-source reverse engineering tool","url":"https://github.com/NSA/...","points":198,"num_comments":67,"author":"sec_researcher"},
        {"title":"Ask HN: What's your privacy-focused homelab setup?","url":"https://news.ycombinator.com/item?id=1","points":156,"num_comments":134,"author":"homenet"},
        {"title":"Researchers achieve quantum entanglement at room temperature","url":"https://nature.com/quantum","points":445,"num_comments":201,"author":"sci_fan"},
        {"title":"A visual guide to building your own programming language","url":"https://craftinginterpreters.com","points":289,"num_comments":56,"author":"lang_dev"},
        {"title":"Figma announces AI-powered design features","url":"https://figma.com/blog/ai","points":178,"num_comments":43,"author":"designer_jane"},
        {"title":"How we scaled our API from 1K to 100K requests/second","url":"https://engineering.example.com/scaling","points":267,"num_comments":78,"author":"backend_pro"},
        {"title":"Signal introduces new end-to-end encrypted group calls","url":"https://signal.org/blog/groups","points":334,"num_comments":112,"author":"privacy_advocate"},
        {"title":"Blender 4.0 released with real-time ray tracing","url":"https://blender.org/4.0","points":423,"num_comments":95,"author":"3d_artist"},
    ]
    return [Story(id=f"mock-{i}",title=d["title"],url=d["url"],domain=extract_domain(d["url"]),
                 points=d["points"],num_comments=d["num_comments"],author=d["author"]) for i,d in enumerate(data)]

def main():
    import argparse
    a = argparse.ArgumentParser()
    a.add_argument("--test",action="store_true")
    a.add_argument("--no-email",action="store_true")
    a.add_argument("--no-telegram",action="store_true")
    a.add_argument("--save",action="store_true",help="Save HTML/TXT files locally")
    args = a.parse_args()
    ds = datetime.now().strftime("%Y-%m-%d")
    
    print("\n[1/4] Fetching Hacker News...")
    stories = fetch_hn_stories(30)
    if not stories:
        print("[WARN] Using mock data"); stories = mock_stories()
    print(f"    {len(stories)} stories fetched")
    
    print("\n[2/4] Curating...")
    curated = curate(stories)
    print(f"    Selected {len(curated)}")
    for s in curated:
        f_ = "[*] " if s.personal_pick else ""
        t_ = f"[{len(s.interest_keywords)}]" if s.interest_keywords else ""
        print(f"    {s.spread_index:02d}. {f_}{s.title[:60]}... {t_}")
    
    print("\n[3/4] Rendering...")
    html = build_html(curated, ds)
    txt = build_txt(curated, ds)
    
    if args.save:
        out = Path("magazines")
        html_path = save(out/f"{ds}.html", html)
        txt_path = save(out/f"{ds}.txt", txt)
        print(f"    Saved: {html_path}")
    
    print("\n[4/4] Sending...")
    if not args.no_email:
        from io import BytesIO
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        import smtplib
        u,p,t = os.getenv("EMAIL_USER"),os.getenv("EMAIL_PASS"),os.getenv("EMAIL_TO")
        if u and p and t:
            msg = MIMEMultipart("alternative")
            msg["From"],msg["To"],msg["Subject"] = u,t,f"Morning Edition — {ds}"
            msg.attach(MIMEText(html,"html","utf-8"))
            msg.attach(MIMEText(txt,"plain","utf-8"))
            try:
                server = smtplib.SMTP_SSL("smtp.qq.com",465)
                server.login(u,p)
                server.sendmail(u,[t],msg.as_string())
                server.quit()
                print("[OK] Email sent")
            except Exception as e: print(f"[ERROR] Email: {e}")
        else: print("[WARN] Email not configured")
    
    if not args.no_telegram:
        send_telegram(curated, ds)
    
    print("\n[OK] Done!")

if __name__ == "__main__": main()
