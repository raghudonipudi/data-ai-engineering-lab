inp_list = ['tea', 'ate', 'eat', 'til', 'lit', 'sam']

ana_set = set()

for wd in inp_list:
    wdc = sorted(wd.lower())
    wd = ''.join(wdc)
    ana_set.add(wd)

odict = {}

for s in ana_set:
    for wd in inp_list:
        wdc = sorted(wd.lower())
        wdn = ''.join(wdc)
        if wdn == s:
            if s in odict:
                odict[s].append(wd)
            else:
                odict[s] = [wd]            
            

olist = []

for v in odict.values():
    olist.append(v)

print(olist)


