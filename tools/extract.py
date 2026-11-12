import re,html,sys,json
src=open(sys.argv[1],encoding='utf-8').read()
sd=re.search(r'<tw-storydata.*?</tw-storydata>',src,re.S).group(0)
out=[]
for m in re.finditer(r'<tw-passagedata([^>]*)>(.*?)</tw-passagedata>',sd,re.S):
    a=dict(re.findall(r'(\w+)="([^"]*)"',m.group(1)))
    out.append((a,html.unescape(m.group(2))))
for a,t in out:
    print("=== [%s] %s tags=%s pos=%s"%(a['pid'],a['name'],a.get('tags'),a.get('position')))
    print(t)
st=re.search(r'<style role="stylesheet"[^>]*>(.*?)</style>',sd,re.S)
print("=== STYLESHEET\n",st.group(1) if st else None)
sc=re.search(r'<script role="script"[^>]*>(.*?)</script>',sd,re.S)
print("=== SCRIPT\n",sc.group(1) if sc else None)
