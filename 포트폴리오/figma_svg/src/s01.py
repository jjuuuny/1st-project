from lib import *
def build():
    s=Slide("01_표지")
    s.image("디자인/이미지/선택/보정_D8_정렬.png",960,0,960,1080)
    s.text(140,150,"ONGYEOL",22,weight=500,color=MUTE,ls=30)
    s.text(140,300,"온결",150,serif=True,weight=700,lh=1.2)
    s.text(470,400,"(가칭)",24,color=MUTE)
    s.text(146,520,"채우고, 잠그는 장벽",52,serif=True,weight=700)
    s.rect(146,620,80,3,WINE)
    s.text(146,660,"마르지 않게, 무너지지 않게",30)
    s.text(146,840,["건성 피부를 위한 수분 장벽 라인 상품기획","상품기획(MD) · 브랜드매니저 포트폴리오"],22,color=MUTE,lh=1.6)
    s.text(146,975,["가상 브랜드 기획안 · 제품 이미지는 AI로 생성한 가상 브랜드 목업 (일부 합성·보정)","슬로건은 실증 자료와 함께 쓰는 것을 전제로 한다"],15,color=MUTE)
    return s
