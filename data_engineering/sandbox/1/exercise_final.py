#clean version
inp_list = ['tea', 'ate', 'eat', 'til', 'lit', 'sam']
odict = {}

# Step 1: Group everything into a dictionary using a single loop
for wd in inp_list:
    s = ''.join(sorted(wd.lower()))
    odict.setdefault(s, []).append(wd)

# Step 2: Extract all values directly into the final list
olist = list(odict.values())

print(olist)
# Output: [['tea', 'ate', 'eat'], ['til', 'lit'], ['sam']]
