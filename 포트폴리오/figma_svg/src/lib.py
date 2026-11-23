import base64, html, os
ROOT='/home/user/1st-project'
BG="#EAE0CF"; WINE="#521827"; IV="#F3ECE2"; MUTE="#7A5A5A"; OR="#C8553D"; BODY="#5A3A3A"
W,H=1920,1080
class Slide:
    def __init__(s,name,bg=BG):
        s.name=name; s.el=[f'<rect width="{W}" height="{H}" fill="{bg}"/>']
    def rect(s,x,y,w,h,fill,op=1,rx=0,stroke=None):
        st=f' stroke="{stroke}" stroke-width="1"' if stroke else ''
        s.el.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{op}"{st}/>')
    def text(s,x,y,lines,size=24,serif=False,weight=400,color=WINE,ls=0,lh=1.45,anchor="start"):
        if isinstance(lines,str): lines=lines.split('\n')
        fam="Noto Serif KR" if serif else "Noto Sans KR"
        base=y+(size*lh-size)/2+size*0.88
        sp=f' letter-spacing="{size*ls/100:.2f}"' if ls else ''
        ts=''.join(f'<tspan x="{x}" y="{base+i*size*lh:.1f}">{html.escape(l)}</tspan>' for i,l in enumerate(lines))
        s.el.append(f'<text font-family="{fam}" font-size="{size}" font-weight="{weight}" fill="{color}"{sp} text-anchor="{anchor}">{ts}</text>')
        return y+size*lh*len(lines)
    def image(s,path,x,y,w,h,mode="meet"):
        # Figma ignores preserveAspectRatio -> size the <image> to the picture's exact ratio
        from PIL import Image as _I
        p=os.path.join(ROOT,path); iw,ih=_I.open(p).size; mime='image/png' if p.endswith('.png') else 'image/jpeg'
        b=base64.b64encode(open(p,'rb').read()).decode()
        r=min(w/iw,h/ih) if mode=="meet" else max(w/iw,h/ih)
        nw,nh=iw*r,ih*r; nx,ny=x+(w-nw)/2,y+(h-nh)/2
        if mode!="meet":  # crop via clipPath
            cid=f"c{len(s.el)}"
            s.el.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath><g clip-path="url(#{cid})"><image x="{nx:.1f}" y="{ny:.1f}" width="{nw:.1f}" height="{nh:.1f}" href="data:{mime};base64,{b}"/></g>')
        else:
            s.el.append(f'<image x="{nx:.1f}" y="{ny:.1f}" width="{nw:.1f}" height="{nh:.1f}" href="data:{mime};base64,{b}"/>')

    def svg(s):
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'+''.join(s.el)+'</svg>'
    def save(s,outdir):
        p=os.path.join(outdir,s.name+'.svg'); open(p,'w').write(s.svg()); return p
# common header/footer
def std(n,label,title,msg=None,src=None,ai=False):
    s=Slide(f"{n:02d}_{label}")
    s.text(140,100,f"{n:02d}",22,weight=700,ls=10); s.text(200,100,label,22,color=MUTE)
    s.rect(140,145,1640,1,WINE,.3)
    s.text(140,180,title,56,serif=True,weight=700)
    if msg: s.text(140,278,msg,26)
    if src: s.text(140,1010,src,15,color=MUTE)
    if ai: s.text(1780,1010,"AI로 생성한 가상 브랜드 목업 (일부 합성·보정)",15,color=MUTE,anchor="end")
    return s

def tw(t,size):
    w=0
    for ch in t:
        o=ord(ch)
        if 0xAC00<=o<=0xD7A3 or 0x3130<=o<=0x318F: w+=0.93
        elif ch==' ': w+=0.26
        elif ch in '.,·:;()\'"’‘“”[]/|-—–→↑%': w+=0.36
        elif ch.isdigit(): w+=0.56
        elif ch.isupper(): w+=0.64
        else: w+=0.52
    return w*size
def wrap(text,size,maxw):
    out=[]
    for para in text.split('\n'):
        words=para.split(' '); line=''
        for wd in words:
            cand=(line+' '+wd).strip()
            if tw(cand,size)<=maxw or not line: line=cand
            else: out.append(line); line=wd
        out.append(line)
    return out
def para(s,x,y,text,size=22,w=1640,**k):
    lines=wrap(text,size,w); return s.text(x,y,lines,size,**k)
def bullets(s,x,y,w,items,size=22,gap=22):
    cy=y
    for t,b in items:
        cy=para(s,x,cy,t,size,w,weight=700)+2
        cy=para(s,x,cy,b,size-2,w,color=BODY)+gap
    return cy
def table(s,x,y,cols,rows,head=False,firstMute=False,size=22,gap=18,bold=lambda r,c:False):
    cy=y
    for ri,r in enumerate(rows):
        hd=head and ri==0; h=0; cx=x
        for ci,cell in enumerate(r):
            mute=hd or (firstMute and ci==0)
            sz=18 if mute else size
            bot=para(s,cx,cy,cell,sz,cols[ci]-30,color=MUTE if mute else WINE,weight=700 if bold(ri,ci) else 400)
            h=max(h,bot-cy); cx+=cols[ci]
        cy+=h+gap
        s.rect(x,cy-gap/2,sum(cols),1,WINE,.5 if hd else .18)
    return cy
