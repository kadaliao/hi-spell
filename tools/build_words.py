"""Build words.js from the KyleBing CET-4 list (BSD-3-Clause).

Each entry: [word, meaning, node, phrase, phraseCN]. `node` = freqBand*4 + lenBand,
where freqBand ranks words by OpenSubtitles frequency (hermitdave/FrequencyWords)
split into quartiles, and lenBand is 3-5 / 6-7 / 8-9 / 10+ letters.
Usage (from the repo root): python3 tools/build_words.py cet4.json en50k.txt
  cet4.json:  https://github.com/KyleBing/english-vocabulary/blob/master/json/3-CET4-顺序.json
  en50k.txt:  https://github.com/hermitdave/FrequencyWords/blob/master/content/2018/en/en_50k.txt
"""
import json, re, sys

src, freq_path = sys.argv[1], sys.argv[2]
rank = {}
for i, line in enumerate(open(freq_path, encoding='utf-8')):
    w = line.split(' ')[0]
    rank.setdefault(w, i)

merged = {}
for e in json.load(open(src, encoding='utf-8')):
    w = e['word'].strip()
    if len(w.replace('-', '')) < 3 or not re.fullmatch(r"[A-Za-z]+(-[A-Za-z]+)*", w):
        continue
    m = merged.setdefault(w, {'tr': [], 'ph': []})
    for t in e.get('translations', []):
        item = (t.get('type', '').replace(' ', ''), t['translation'].strip())
        if item not in m['tr']:
            m['tr'].append(item)
    m['ph'] += e.get('phrases', [])

def meaning(tr):
    groups = {}
    for pos, text in tr:
        pos = pos.replace('aux', '').strip() or ''
        for sense in re.split(r'[，,；;]|\s{1,}', text):
            sense = re.sub(r'^aux', '', sense.strip())
            if sense and sense not in groups.setdefault(pos, []):
                groups[pos].append(sense)
    parts, total = [], 0
    for pos, senses in groups.items():
        keep = []
        for sn in senses:
            if keep and sum(len(k) + 1 for k in keep) + len(sn) > 14:
                break
            keep.append(sn[:16])
        s = (pos + '. ' if pos else '') + '，'.join(keep)
        if parts and total + len(s) > 30:
            break
        parts.append(s); total += len(s)
    return '  '.join(parts)

def pick_phrase(w, phs):
    pat = re.compile(r'\b' + re.escape(w) + r'\b', re.I)
    best = None
    for p in phs:
        en, cn = p.get('phrase', ''), p.get('translation', '')
        if not pat.search(en) or len(en) > 32 or en.lower() == w.lower():
            continue
        if best is None or len(en) < len(best[0]):
            best = (en, re.split(r'[；;]', cn)[0].strip()[:20])
    if not best:
        return None
    return [pat.sub('_' * len(w), best[0], count=1), best[1]]

words = list(merged)
by_freq = sorted(words, key=lambda w: (rank.get(w.lower(), 10**6), len(w)))
fband = {w: min(3, i * 4 // len(by_freq)) for i, w in enumerate(by_freq)}
def lband(w):
    n = len(w.replace('-', ''))
    return 0 if n <= 5 else 1 if n <= 7 else 2 if n <= 9 else 3

out, counts = [], [0] * 16
for w in by_freq:
    node = fband[w] * 4 + lband(w)
    counts[node] += 1
    row = [w, meaning(merged[w]['tr']), node]
    ph = pick_phrase(w, merged[w]['ph'])
    if ph:
        row += ph
    out.append(row)

header = ('/* CET-4 word list derived from KyleBing/english-vocabulary (BSD-3-Clause,\n'
          '   Copyright (c) 2022-2026, KyleBing). Frequency bands from hermitdave/FrequencyWords. */\n')
js = header + 'window.CET4=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
open('words.js', 'w', encoding='utf-8').write(js)
print(len(out), 'words', len(js) // 1024, 'KB')
for f in range(4):
    print(counts[f * 4:f * 4 + 4])
