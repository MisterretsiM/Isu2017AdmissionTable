import sys
import os

l_objn = "<object number=\""
l_objne = "\">"
l_obje = "</object>"
l_fc = "<faculty>"
l_fce = "</faculty>"
l_dir = "<direction>"
l_dire = "</direction>"
l_tp = "<type>"
l_tpe = "</type>"
l_prof = "<profile>"
l_profe = "</profile>"
l_lvl = "<level>"
l_lvle = "</level>"
l_form = "<form>"
l_forme = "</form>"
l_base = "<basement>"
l_basee = "</basement>"
l_cat = "<category>"
l_cate = "</category>"
l_lnk = "<link>"
l_lnke = "</link>"

def crop(t, s, m):
    return t[t.find(s)+len(s):] if m else t[:t.find(s)]

class prf:
    def __init__(self, p_fc, p_dir, p_tp, p_prof, p_lvl, p_form, p_base, p_cat, p_lnk):
        self.p_fc = p_fc
        self.p_dir = p_dir
        self.p_tp = p_tp
        self.p_prof = p_prof
        self.p_lvl = p_lvl
        self.p_form = p_form
        self.p_base = p_base
        self.p_cat = p_cat
        self.p_lnk = p_lnk

    def __repr__(self):
        return repr(self.p_fc, self.p_dir, self.p_tp, self.p_prof, self.p_lvl, self.p_form, self.p_base, self.p_cat, self.p_lnk)



f = open('Isu_Prof_Table.ProfTab', 'r', encoding = 'UTF-8')
fc_list = []
flag = 0
count = 0
s = f.read()

argvb = list(map(os.fsencode, sys.argv))

while s.find(l_objn) != -1:
    count = count + 1
    p_fc = crop(crop(s, l_fc, 1), l_fce, 0)
    p_dir = crop(crop(s, l_dir, 1), l_dire, 0)
    p_tp = crop(crop(s, l_tp, 1), l_tpe, 0)
    if p_tp == 'with_profile':
        p_prof = crop(crop(s, l_prof, 1), l_profe, 0)
    else:
        p_prof = 'EMPTY'
    p_lvl = crop(crop(s, l_lvl, 1), l_lvle, 0)
    p_form = crop(crop(s, l_form, 1), l_forme, 0)
    p_base = crop(crop(s, l_base, 1), l_basee, 0)
    p_cat = crop(crop(s, l_cat, 1), l_cate, 0)
    p_lnk = crop(crop(s, l_lnk, 1), l_lnke, 0)
    fc_list.append(prf(p_fc, p_dir, p_tp, p_prof, p_lvl, p_form, p_base, p_cat, p_lnk))
    s = crop(s, l_obje, 1)
    for i in argvb:
        i = i.decode('UTF-8')
        if i == fc_list[count - 1].p_fc or i == fc_list[count - 1].p_dir or i == fc_list[count - 1].p_lvl or i == fc_list[count - 1].p_prof or i == fc_list[count - 1].p_form or i == fc_list[count - 1].p_base or i == fc_list[count - 1].p_cat:
            count = count - 1
            fc_list.pop()
f.close()

order_list = []



for i in argvb:
    i = i.decode('UTF-8')
    if i == 'BY_FACULTY':
        order_list.append("p_fc")
    elif i == 'BY_DIRECTION':
        order_list.append("p_dir")
    elif i== 'BY_PROFILE':
        order_list.append("p_prof")
    elif i == 'BY_LEVEL':
        order_list.append("p_lvl")
    elif i == 'BY_FORM':
        order_list.append("p_form")
    elif i == 'BY_BASEMENT':
        order_list.append("p_base")
    elif i == 'BY_CATEGORY':
        order_list.append("p_cat")


def comp(a1, a2):
    for i in order_list:
        if getattr(a1, i) < getattr(a2, i):
            return 1
        elif getattr(a1, i) > getattr(a2, i):
            return 0
    return 0

def quicksort(data):
    if not len(data):
        return data
    pivot = data[0]
    left = []
    right = []
    for x in range(1, len(data)):
        if comp(data[x],pivot):
            left.append(data[x])
        else:
            right.append(data[x])
    left = quicksort(left)
    right = quicksort(right)
    foo = [pivot]
    return left + foo + right

if order_list:
    fc_list = quicksort(fc_list)

count = 0

f = open('Sorted_Prof_Table.ProfTab', 'w', encoding = 'UTF-8')
for k in fc_list:
    count = count + 1
    print('<object number=\"' + str(count) + '\">', file = f)
    print('    <faculty>' + k.p_fc + '</faculty>', file = f)
    print('    <direction>' + k.p_dir + '</direction>', file = f)
    print('    <type>' + k.p_tp + '</type>', file = f)
    if (k.p_tp == 'with_profile'):
        print('    <profile>' + k.p_prof + '</profile>', file = f)
    print('    <level>' + k.p_lvl + '</level>', file = f)
    print('    <form>' + k.p_form + '</form>', file = f)
    print('    <basement>' + k.p_base + '</basement>', file = f)
    print('    <category>' + k.p_cat + '</category>', file = f)
    print('    <link>' + k.p_lnk + '</link>', file = f)
    print('</object>', file = f)
f.close()