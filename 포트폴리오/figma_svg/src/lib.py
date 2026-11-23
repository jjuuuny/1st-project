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
        p=os.path.join(ROOT,path); mime='image/png' if p.endswith('.png') else 'image/jpeg'
        b=base64.b64encode(open(p,'rb').read()).decode()
        par='xMidYMid meet' if mode=="meet" else 'xMidYMid slice'
        s.el.append(f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{par}" href="data:{mime};base64,{b}"/>')
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
