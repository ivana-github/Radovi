import sys
import copy
popis_klauzula=[]


'strategija brisanja' \
'i  ako postoji klauzula  f i (f i g ) == f '\
'brises sve klauze koje sadrze a i neA' \
'ako je jedna klauza podskup druge druga ju sadrzava '


'skup potopre klauzule dobivene negacijom cilja i sve novoizvedene klauzule' \
'barem jedna roditeljska klauzula je uvijek iz tog skupa' \
'povećava se kako izvodimo nove klauzule' \
''
def ispisi_put(popis_za_printanje,ciljna_klauzula,prosireni_ispis):
    string=""
    i =1
    for prvi in popis_za_printanje.values():
        for pp in prvi:
            if isinstance(pp,list):
                string += str(i) + '. '
                for p in pp:
                    if isinstance(p,list):
                        for z in p:
                            string += z+' v '
                        string=string[:-2]
                    else:
                        if(p=='NIL'):
                            string += p + ' '
                        else:
                            string += p + ' v '
                string = string[:-2]+'\n'
                i += 1
            else:
                string += str(i)+'. ' + pp+'\n'
                i += 1
        string += "============\n"
    if prosireni_ispis:
        print(string[:-1])
    if isinstance(ciljna_klauzula, str):
        print(ciljna_klauzula.strip(), "is true")
    else:
        cilj_string=""
        for cilj in ciljna_klauzula:
            cilj_string += cilj + ' v '
        cilj_string = cilj_string[:-2] + "is true"
        print(cilj_string.strip())

def f_negacija(klauzula):
    nova = []
    if isinstance(klauzula, str):
        klauzula=klauzula.split()
    for k in klauzula:
        if(k.startswith('~')):
            nova.append(k[1:])
        else:
           nova.append('~'+k)

    return nova

def skup_parova_za_rjesavanje(popis_klauzula, sos1, index):
    parovi=[]
    sos=sos1[index]
    svi_prethodni=list(popis_klauzula+sos1[0:index])

    if isinstance(sos, str):
        sos = sos.split()
    for s in sos:
        if s.startswith('~'):
            negacija = s[1:]
        else:
            negacija='~'+s
        for klauzule in svi_prethodni:
            if isinstance(klauzule, str):
                klauzule = klauzule.split()

            if negacija in klauzule:
                for k in klauzule:
                    if k.strip() == negacija.strip():
                        parovi.append((sos,klauzule))
                        break
    return parovi

def plResolve(prva, druga):
    rez=list()
    prva_klauzula = copy.deepcopy(prva)
    druga_klauzula=copy.deepcopy(druga)
    if isinstance(prva_klauzula, str):
        prva_klauzula=prva_klauzula.split()
    if isinstance(druga_klauzula, str):
        druga_klauzula=druga_klauzula.split()

    for prva in prva_klauzula:
        if prva.startswith('~'):
            negacija = prva[1:]
        else:
            negacija = '~' + prva
        if negacija in druga_klauzula:
            prva_klauzula.remove(prva)
            druga_klauzula.remove(negacija)
            if(len(prva_klauzula)==0 and len(druga_klauzula)==0):
                rez="NIL"
                return rez
            rez =sorted(set(prva_klauzula+druga_klauzula))
    return rez

def rezolucija_opovrgavanjem(popis_klauzula,ciljna_klauzula,prosireni_ispis):
    popis_za_printanje = {}
    popis_svih = []
    lista_rezolventi_s_indeksima = []
    index=0
    sos=f_negacija(ciljna_klauzula)

    popis_za_printanje[1]=popis_klauzula
    popis_za_printanje[2]=f_negacija(ciljna_klauzula) #negirani cilj
    new=[]

    for i in popis_klauzula:
        if isinstance(i, str):
            popis_svih.append([i])
        else:
            popis_svih.append(i)
    for i in sos:
        if isinstance(i, str):
            popis_svih.append([i])
        else:
            popis_svih.append(i)

    while(1):
        parovi= skup_parova_za_rjesavanje(popis_klauzula,sos, index)
        index+=1
        rezolventi = []
        prije=new[:]
        ispis=[]
        for par in parovi:
            potencijalno_rjesenje = plResolve(par[0], par[1])
            if "NIL" == potencijalno_rjesenje:
                sos.append(potencijalno_rjesenje)
                ispis = str('(' + str(popis_svih.index(par[0]) + 1) + ',' + str(popis_svih.index(par[1]) + 1) + ')')
                lista_rezolventi_s_indeksima.append([potencijalno_rjesenje,ispis])
                popis_svih.append((potencijalno_rjesenje))

                popis_za_printanje[3] = lista_rezolventi_s_indeksima
                ispisi_put(popis_za_printanje,ciljna_klauzula,prosireni_ispis)
                return True
            if potencijalno_rjesenje in rezolventi :
                continue
            if(potencijalno_rjesenje in popis_svih):
                continue
            rezolventi.append(potencijalno_rjesenje)
            ispis.append(str('(' + str(popis_svih.index(par[1]) + 1) + ',' + str(popis_svih.index(par[0]) + 1) + ')'))
        i=0
        for pot in rezolventi:
            lista_rezolventi_s_indeksima.append([potencijalno_rjesenje,ispis[i]])
            new.append(pot)
            sos.append(pot)
            popis_svih.append(pot)
            i += 1


        if(prije==new and len(sos)==index):
            if isinstance(ciljna_klauzula, str):
                print(ciljna_klauzula.strip(), "is unknown")
            else:
                cilj_string = ""
                for cilj in ciljna_klauzula:
                    cilj_string += cilj + ' v '
                cilj_string = cilj_string[:-2] + "is unknown"
                print(cilj_string.strip())
            return False

def pretvori_klauzulu(klauzula):
    klauzula=klauzula.lower()
    nova=[]
    if not (" v " in klauzula):
        return klauzula.strip()
    else:
        lista_klauzula = (klauzula.split(' v '))
        for l in lista_klauzula:
            nova.append(l.strip())
        return nova

def procitaj_klauzule(prva_datoteka, res_cok):
    i=0
    popis=[]
    for datoteka in prva_datoteka:
        if (datoteka.startswith('#') or datoteka=="\n"):
            continue
        else:
            popis.append(datoteka)
    duljina=len(popis)
    for p in popis:
        i+=1
        if i== duljina:
            if p.endswith('\n'):
                cilj=pretvori_klauzulu(p[:-1])
            else:
                cilj=pretvori_klauzulu(p)
        else:
            if p.endswith('\n'):
                popis_klauzula.append(pretvori_klauzulu(p[:-1]))
            else:
                popis_klauzula.append(pretvori_klauzulu(p))

    #za drugi dio mora dodati i zadnju klauzulu u redu koja je prije bila ciljna na popis klauzula
    if (res_cok == "cooking_interactive") or (res_cok == "cooking_test"):
        popis_klauzula.append(cilj)

    return popis_klauzula, cilj

def f_cooking_test(popis_klauzula, popis_naredbi):
    for unos in popis_naredbi:
        if unos.strip().endswith('+'):
            klauzula_za_dodati = pretvori_klauzulu(unos[:-2])
            if(isinstance(klauzula_za_dodati, str)):
                klauzula_za_dodati=klauzula_za_dodati.strip()
            if not (klauzula_za_dodati in popis_klauzula):
                popis_klauzula.append(klauzula_za_dodati)

        if unos.strip().endswith('-'):
            klauzula_za_obrisati = pretvori_klauzulu(unos[:-2])
            if (isinstance(klauzula_za_obrisati,str)):
                klauzula_za_obrisati=klauzula_za_obrisati.strip()
            if klauzula_za_obrisati in popis_klauzula:
                popis_klauzula.remove(klauzula_za_obrisati)

        if unos.strip().endswith('?'):
            ciljna_klauzula = pretvori_klauzulu(unos[:-2])
            if(isinstance(ciljna_klauzula,str)):
                ciljna_klauzula=ciljna_klauzula.strip()
            rezolucija_opovrgavanjem(popis_klauzula, ciljna_klauzula, False)

def f_cooking_interactive(popis_klauzula, prosireni_ispis):
    do = 1
    ciljna_klauzula = []
    while (do):
        unos = input("Please enter your query\n")
        if (unos == 'exit'):
            do = 0
            break
        if unos.endswith('+'):
            klauzula_za_dodati = pretvori_klauzulu(unos[:-2])
            if klauzula_za_dodati in popis_klauzula:
                print(klauzula_za_dodati, "klauzula već postoji u ",popis_klauzula )
            else:
                popis_klauzula.append(unos[:-2])
                print("Dodana klauzula, trenutni popis:", popis_klauzula)
        if unos.strip().endswith('-'):
            klauzula_za_obrisati = pretvori_klauzulu(unos[:-2])
            if klauzula_za_obrisati in popis_klauzula:
                popis_klauzula.remove(klauzula_za_obrisati)
                print("Obrisana klauzula",klauzula_za_obrisati,"\nPopis klauzula", popis_klauzula)
            else:
                print(klauzula_za_obrisati, " Nema u popisu klauzula:",popis_klauzula)

        if unos.endswith('?'):
            ciljna_klauzula = pretvori_klauzulu(unos[:-2])
            rezolucija_opovrgavanjem(popis_klauzula, ciljna_klauzula, prosireni_ispis)


#-----------------------main----------------------------
if(sys.argv[-1]=='verbose'):
    prosireni_ispis = True

    if(sys.argv[-3]=="resolution"):
        popis_klauzula, ciljna_klauzula = procitaj_klauzule(open(sys.argv[-2], "r").readlines(),"resolution")
        rezolucija_opovrgavanjem(popis_klauzula,ciljna_klauzula,prosireni_ispis)

    if (sys.argv[-3] == "cooking_interactive"):
        popis_klauzula, ciljna_klauzula = procitaj_klauzule(open(sys.argv[-2], "r").readlines(), "cooking_interactive")
        f_cooking_interactive(popis_klauzula,prosireni_ispis)


elif(sys.argv[-1].endswith('.txt')):
    prosireni_ispis = False
    if (sys.argv[-2] == "resolution"):
        popis_klauzula, ciljna_klauzula = procitaj_klauzule(open(sys.argv[-1], "r").readlines(),"resolution")
        rezolucija_opovrgavanjem(popis_klauzula,ciljna_klauzula,prosireni_ispis)

    if (sys.argv[-2] == "cooking_interactive"):
        popis_klauzula, ciljna_klauzula = procitaj_klauzule(open(sys.argv[-1], "r").readlines(), "cooking_interactive")
        f_cooking_interactive(popis_klauzula,prosireni_ispis)

    if(sys.argv[1] == "cooking_test"):
        popis_klauzula, ciljna_klauzula=procitaj_klauzule(open(sys.argv[2], "r").readlines(), "cooking_test")
        f_cooking_test(popis_klauzula,open(sys.argv[3], "r").readlines())
