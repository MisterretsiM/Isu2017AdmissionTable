#This program creates objects that contains information about faculty, direction, profile, level, form,
#basement, category of each profile and link to original table of profile and save it into xml-like
#document named "Isu_Prof_Table.ProfTab"

import requests

sb = 'block_search'
sov = '<option value=\"'
sa = '\"'
st = '</strong>'
sp = '</p>'
td = '<td>'
tde = '</td>'
hr = '<a href =\"'

fail = 0

class prof:
    pass

#function that get substr from end of first s string entrance in t string to end of t (if m == TRUE)
#or from begin of t to begin of first endtrance s sting in t (if m == false)
def crop(t, s, m):  # m == TRUE fpr cropping begin, m == FALSE for cropping end 
    return t[t.find(s)+len(s):] if m else t[:t.find(s)]

def facs():
    list = []
    try:
        r = requests.get('http://isu.ru/Abitur/ru/rating')
        r.raise_for_status()
        q = r.text
        q = crop(q, sb, 1)
        q = crop(q, sb, 1)
        while (q.find(sov) != -1):
            q = crop(q,sov,1)
            list.append(crop(q, sa, 0))
    except requests.exceptions.ConnectTimeout:
        fail = 2
    except requests.exceptions.ReadTimeout:
        fail = 3
    except requests.exceptions.ConnectionError:
        fail = 1
    except requests.exceptions.HTTPError as err:
        fail = 4
    return list

def dirs(fac):
    list = []
    try:
        r = requests.get('http://isu.ru/Abitur/control/jsp/rating/get_directions.jsp', params = { 'fac' : fac })
        r.raise_for_status()
        q = r.text
        while (q.find(sov) != -1):
            q = crop(q,sov,1)
            list.append(crop(q, sa, 0))
    except requests.exceptions.ConnectTimeout:
        fail = 2
    except requests.exceptions.ReadTimeout:
        fail = 3
    except requests.exceptions.ConnectionError:
        fail = 1
    except requests.exceptions.HTTPError as err:
        fail = 4
    return list

def lnk(fac, dir):
    list = []
    try:
        r = requests.get('http://isu.ru/Abitur/control/jsp/rating/get_direction_info.jsp', params = { 'fac' : fac, 'dir' : dir})
        r.raise_for_status()
        q = r.text
        while (q.find(hr) != -1):
            a = prof()
            a.fac = fac
            a.dir = dir
            q = crop(q, hr, 1)
            a.link = 'isu.ru'+crop(q, '\">', 0)
            a.type = 'without_profile'
            if (q.find(st) != -1):
                a.type = 'with_profile'
                q = crop(q, st, 1)
                a.prf = crop(q, sp, 0)
            q = crop(q, td, 1)
            q = crop(q, td, 1)
            a.lvl = crop(q, tde, 0)
            q = crop(q, td, 1)
            q = crop(q, td, 1)
            a.form = crop(q, tde, 0)
            q = crop(q, td, 1)
            q = crop(q, td, 1)
            a.base = crop(q, tde, 0)
            q = crop(q, td, 1)
            q = crop(q, td, 1)
            a.cat = crop(q, tde, 0)
            list.append(a)
    except requests.exceptions.ConnectTimeout:
        fail = 2
    except requests.exceptions.ReadTimeout:
        fail = 3
    except requests.exceptions.ConnectionError:
        fail = 1
    except requests.exceptions.HTTPError as err:
        fail = 4
    return list

count = 0
f = open('Isu_Prof_Table.ProfTab', 'wb')
fc = facs()
if(fail == 0):
    for i in fc:
        l = dirs(i)
        if(fail == 0):
            for j in l:
                z = lnk(i, j)
                if(fail == 0):
                    for k in z:
                        count = count + 1
                        f.write(('<object number=\"' + str(count) + '\">\n').encode('UTF-8'))
                        f.write(('    <faculty>' + k.fac + '</faculty>\n').encode('UTF-8'))
                        f.write(('    <direction>' + k.dir + '</direction>\n').encode('UTF-8'))
                        f.write(('    <type>' + k.type + '</type>\n').encode('UTF-8'))
                        if (k.type == 'with_profile'):
                            f.write(('    <profile>' + k.prf + '</profile>\n').encode('UTF-8'))
                        f.write(('    <level>' + k.lvl + '</level>\n').encode('UTF-8'))
                        f.write(('    <form>' + k.form + '</form>\n').encode('UTF-8'))
                        f.write(('    <basement>' + k.base + '</basement>\n').encode('UTF-8'))
                        f.write(('    <category>' + k.cat + '</category>\n').encode('UTF-8'))
                        f.write(('    <link>' + k.link + '</link>\n').encode('UTF-8'))
                        f.write(('</object>\n').encode('UTF-8'))
if(fail):
    f.write('FAIL'.encode('UTF-8'))

f.close()
