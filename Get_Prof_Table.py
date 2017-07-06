#This program creates objects that contains information about faculty, direction, profile, level, form,
#basis, category of each profile and link to original table of profile and save it into xml-like
#document named "Isu_Prof_Table.ProfTab"

import requests

#consts for cropping
sb = 'block_search'
sov = '<option value=\"'
sa = '\"'
st = '</strong>'
sp = '</p>'
td = '<td>'
tde = '</td>'
hr = '<a href =\"'

#http page that contains list of faculties
facs_lnk = 'http://isu.ru/Abitur/ru/rating'

#http page that returns list directs of each faculty on GET request
dirs_lnk = 'http://isu.ru/Abitur/control/jsp/rating/get_directions.jsp'

#http page that contains other information about each direction
lnk_lnk = 'http://isu.ru/Abitur/control/jsp/rating/get_direction_info.jsp'

#const that tells that all requests were successful
#if == 0 then everything is all right
#if == 1 then connection error
#if == 2 then connect timeout
#if == 3 then read timeout
#if == 4 then HTTP error
fail = 0

class prof:
    pass

#function that get substr from end of first s string entrance in t string to end of t (if m == TRUE)
#or from begin of t to begin of first entrance s sting in t (if m == false)
def crop(t, s, m):
    return t[t.find(s)+len(s):] if m else t[:t.find(s)]

#function that get list of faculties
def facs():
    list = []
    try:
        r = requests.get(facs_lnk)
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
        HTTPErrNum = err
    return list

#function that get list of directs of current faculty
def dirs(fac):
    list = []
    try:
        r = requests.get(dirs_lnk, params = { 'fac' : fac })
        r.raise_for_status()
        q = r.text
        while (q.find(sov) != -1):
            q = crop(q, sov, 1)
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

#function that get list of profiles of current direction and all information of this profile 
def lnk(fac, dir):
    list = []
    try:
        r = requests.get(lnk_lnk, params = { 'fac' : fac, 'dir' : dir})
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

#count of objects
count = 0

f = open('Isu_Prof_Table.ProfTab', 'w', encoding = 'UTF-8')
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
                        print('<object number=\"' + str(count) + '\">', file = f)
                        print('    <faculty>' + k.fac + '</faculty>', file = f)
                        print('    <direction>' + k.dir + '</direction>', file = f)
                        print('    <type>' + k.type + '</type>', file = f)
                        if (k.type == 'with_profile'):
                            print('    <profile>' + k.prf + '</profile>', file = f)
                        print('    <level>' + k.lvl + '</level>', file = f)
                        print('    <form>' + k.form + '</form>', file = f)
                        print('    <basis>' + k.base + '</basis>', file = f)
                        print('    <category>' + k.cat + '</category>', file = f)
                        print('    <link>' + k.link + '</link>', file = f)
                        print('</object>', file = f)
f.close()

if fail:
    print("FAIL\n")
    if fail == 1:
        print("CONNECTION_ERROR")
    elif fail == 2:
        print("CONNECTON_TIMEOUT")
    elif fail == 3:
        print("READ_TIMEOUT")
    elif fail == 4:
        print("HTTP_ERROR\n"+HTTPErrNum)
else:
    print(count)
