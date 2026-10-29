import pymupdf, re, json, glob, os, sys
doc=pymupdf.open('/home/claude/sun_src/sun_new_testament.pdf')
toc=''.join(doc[i].get_text() for i in range(0,4))
books=[(b.strip(),int(p)-1) for b,p in re.findall(r'The Book of ([0-9A-Za-z ]+?)\.{3,}(\d+)', toc)]
starts={p:b for b,p in books}
verses=[]; cur_book=books[0][0]; pending=None; chap=0; verse=None; buf=[]
def flush():
    global buf
    if verse is not None and buf:
        t=re.sub(r' +',' ',''.join(buf)).strip(); verses.append([cur_book,chap,verse,t])
    buf=[]
def start_verse(n):
    global chap, verse, cur_book, pending
    flush()
    if pending and n==1:
        cur_book=pending; pending=None; chap=0
    if n==1 or (verse is not None and n<verse): chap+=1
    verse=n
for pno in range(4,len(doc)):
    if pno in starts and starts[pno]!=cur_book: pending=starts[pno]
    page=doc[pno]; d=page.get_text('rawdict'); mid=page.rect.width/2
    blocks=[blk for blk in d['blocks'] if blk.get('lines')]
    blocks.sort(key=lambda blk:(0 if blk['bbox'][0]<mid else 1, blk['bbox'][1]))
    for blk in blocks:
        for l in blk['lines']:
            prev_x1=None; numbuf=''
            for s in l['spans']:
                font=s['font']; sz=s['size']
                if 'SUN' in font:
                    if numbuf: start_verse(int(numbuf)); numbuf=''; prev_x1=None
                    for ch in s['chars']:
                        x0,y0,x1,y1=ch['bbox']
                        if prev_x1 is not None and x0-prev_x1 > sz*0.18: buf.append(' ')
                        buf.append(ch['c'] if ch['c']!=' ' else ' '); prev_x1=x1
                else:
                    if s['bbox'][1] > page.rect.height*0.9: continue
                    is_versenum = 10.0 <= sz <= 11.0 and 'Bold' in font
                    for ch in s['chars']:
                        c=ch['c']
                        if c.isdigit() and is_versenum: numbuf+=c
                        elif c.strip() and sz>=12:
                            if numbuf: start_verse(int(numbuf)); numbuf=''
                            buf.append(c)
                    prev_x1=s['bbox'][2]
            if numbuf: start_verse(int(numbuf)); numbuf=''
            buf.append(' ')
flush()
json.dump(verses, open('sun_nt_verses.json','w'), ensure_ascii=False)
codes={'MAT':'Matthew','MRK':'Mark','LUK':'Luke','JHN':'John','ACT':'Acts','ROM':'Romans','1CO':'1 Corinthians','2CO':'2 Corinthians','GAL':'Galatians','EPH':'Ephesians','PHP':'Philippians','COL':'Colossians','1TH':'1 Thessalonians','2TH':'2 Thessalonians','1TI':'1 Timothy','2TI':'2 Timothy','TIT':'Titus','PHM':'Philemon','HEB':'Hebrews','JAS':'James','1PE':'1 Peter','2PE':'2 Peter','1JN':'1 John','2JN':'2 John','3JN':'3 John','JUD':'Jude','REV':'Revelation'}
ulb={}
for f in sorted(glob.glob('/home/claude/sun_src/ulb/en_ulb/*.usfm')):
    code=os.path.basename(f)[3:6]
    if code not in codes: continue
    book=codes[code]; chap=0
    for line in open(f,encoding='utf-8'):
        line=line.strip()
        if line.startswith('\\c '): chap=int(line.split()[1]); continue
        m=re.match(r'\\v (\d+)(?:-(\d+))? (.*)', line)
        if m:
            txt=re.sub(r'\\[a-z0-9*]+\s?','',m.group(3)); txt=re.sub(r'\|[^\\]*','',txt)
            ulb[(book,chap,int(m.group(1)))]=txt.strip()
pairs=[]; miss=[]
for b,c,v,t in verses:
    e=ulb.get((b,c,v))
    if e is None: miss.append((b,c,v))
    else: pairs.append([[b,c,v],t,e])
print(len(verses),'sun verses;',len(pairs),'paired;',len(miss),'unmatched', miss[:12])
json.dump(pairs, open('pairs.json','w'), ensure_ascii=False)
