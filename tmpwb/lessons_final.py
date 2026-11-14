import re
from lessons_rest_base import LESSONS
P='am_puck';Q='am_liam'
def liven(l):
    exn=0
    for st in l['steps']:
        if 'v' in st: continue
        kinds=[w[0] for w in st['write']];s=st['say']
        if 'title' in kinds:
            st['v']=P;s=re.sub(r'^Today we learn',"Hi everyone! Welcome back! Today we are learning",s)
        elif 'line' in kinds:
            st['v']=Q;s=s.replace('The formula is:',"Here is the formula!")
        elif 'wrong' in kinds:
            st['v']=Q;s=s.replace('Be careful!','Watch out!')
            if not s.rstrip().endswith('!'):s=s.rstrip()+'!'
        elif 'note' in kinds:
            st['v']=P;s=s.replace('Great job!','You did it! Great job!')
        else:
            st['v']=P if exn%2==0 else Q
            if exn==0:
                s=s.replace('Look at these examples.',"Let's look at some examples!")
                s=s.rstrip()+' Awesome!'
            exn+=1
        st['say']=s
for l in LESSONS[1:]:liven(l)
