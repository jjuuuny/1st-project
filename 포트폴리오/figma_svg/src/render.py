import sys,os,importlib,subprocess,json
sys.path.insert(0,os.path.dirname(__file__))
OUT='/home/user/1st-project/포트폴리오/figma_svg'
mods=sys.argv[1:]
paths=[]
for m in mods:
    s=importlib.import_module(m).build(); paths.append(s.save(OUT))
json.dump(paths,open('/tmp/claude-0/-home-user-1st-project/53881081-6a94-55ef-b0c3-4eaa7235d38d/scratchpad/svgs.json','w'),ensure_ascii=False)
