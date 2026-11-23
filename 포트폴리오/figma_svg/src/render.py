import sys,os,importlib,json
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
OUT='/home/user/1st-project/포트폴리오/figma_svg'
paths=[]
for m in sys.argv[1:]:
    mod=importlib.import_module(m)
    ss=mod.build_all() if hasattr(mod,'build_all') else [mod.build()]
    paths+= [s.save(OUT) for s in ss]
json.dump(paths,open('/tmp/claude-0/-home-user-1st-project/53881081-6a94-55ef-b0c3-4eaa7235d38d/scratchpad/svgs.json','w'),ensure_ascii=False)
print(len(paths))
