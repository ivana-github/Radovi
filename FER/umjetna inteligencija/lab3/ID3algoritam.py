import copy
import sys
from pathlib import Path
import operator
import math
from decimal import Decimal, ROUND_HALF_UP

znacajke=[]
skup_za_ucenje=[]
skup_za_testiranje=[]

lista_predvidanje=[]

mapa_konf={"mode": "test", "model": "ID3", "max_depth" : -1, "num_trees": 1, "feature_ratio" : 1., "example_ratio" : 1.}


def napravi_tablicu(skup, znacajke_lista):
    tablica=[]
    for s in skup:
        red_tablice=[]
        for i in range(0, len(s)):
            if i == len(s)-1:
                red_tablice.append((znacajke_lista[i][:-1], s[i][:-1]))
            else:
                red_tablice.append((znacajke_lista[i], s[i]))
        tablica.append(red_tablice)
    return tablica

def ucitaj_file():
    izlaz=[]
    baza_za_ucenje = open(Path(sys.argv[1]), "r").readlines()
    baza_za_testiranje = open(Path(sys.argv[2]), "r").readlines()
    konfiguracija = open(Path(sys.argv[3]), "r").readlines()

    znacajke_lista=baza_za_ucenje[0].split(',')
    for linija in baza_za_ucenje[1:]:
        parametri = linija.split(',')
        skup_za_ucenje.append(parametri)
        if izlaz.__contains__(parametri[-1][:-1]):
            continue
        else:
            izlaz.append(parametri[-1][:-1])

    for linija in baza_za_testiranje[1:]:
        parametri = linija.split(',')
        skup_za_testiranje.append(parametri)

    for linija in konfiguracija:
        kljuc, vrijednost = linija.split("=")
        mapa_konf[kljuc] = vrijednost[:-1]

    tablica_ucenja = napravi_tablicu(skup_za_ucenje,znacajke_lista)
    tablica_testiranja = napravi_tablicu(skup_za_testiranje,znacajke_lista)

    return tablica_ucenja, tablica_testiranja, izlaz

def izracunaj_entropiju(vrijednosti):
    suma = 0
    entropija_skupa = 0
    for b in vrijednosti:
        suma += b
    for b in vrijednosti:
        if b == 0:
            return 0
        entropija_skupa += b / suma * math.log2(b / suma)
    entropija_skupa *= -1
    x = Decimal(str(entropija_skupa))
    x.quantize(Decimal('0.001'), ROUND_HALF_UP)
    return round(entropija_skupa, 3)


def IG(znacajke, tablica_ucenja):
    lista_entropija=[]
    atribut_brojIzlaza={}
    skup_za_ucenje=[]
    brojac = 0
    zapamti_indekse = []
    l_znacajki = []
    for red_tablice in tablica_ucenja:
        red = []
        for i in range(0, len(red_tablice)):
            if i == len(red_tablice)-1:
                skup_za_ucenje.append((red, red_tablice[i][1]))
            else:
                red.append(red_tablice[i][1])

    for i in range(0, len(znacajke)-1):
        brojac_ukupnih = [0] * len(izlaz)
        for j in range(0, len(skup_za_ucenje)):
            if(skup_za_ucenje[j][0][i] not in atribut_brojIzlaza.keys()):
                index = izlaz.index(skup_za_ucenje[j][1])
                lista_izlaza = [0]*len(izlaz)
                brojac_ukupnih[index] += 1
                lista_izlaza[index] = 1
                atribut_brojIzlaza[skup_za_ucenje[j][0][i]] = lista_izlaza
            else:
                index = izlaz.index(skup_za_ucenje[j][1])
                lista_izlaza = atribut_brojIzlaza.get(skup_za_ucenje[j][0][i])
                brojac_ukupnih[index] += 1
                lista_izlaza[index] += 1
                atribut_brojIzlaza[skup_za_ucenje[j][0][i]] = lista_izlaza

        entropija_skupa = izracunaj_entropiju(brojac_ukupnih)
        entropija_znacajke = 0
        for atribut in atribut_brojIzlaza.values():
            suma_z = 0
            suma_skupa = 0
            for k in range(0, len(atribut)):
                suma_z += atribut[k]
                suma_skupa += brojac_ukupnih[k]
            entropija_znacajke += (suma_z/suma_skupa)*izracunaj_entropiju(atribut)
        lista_entropija.append(entropija_skupa-entropija_znacajke)
        atribut_brojIzlaza = {}
        brojac_ukupnih.clear()
    maksimalna_entropija = max(lista_entropija)

    for i in range(0, len(lista_entropija)):
        if lista_entropija[i] == maksimalna_entropija:
            brojac += 1
            zapamti_indekse.append(i)
    if brojac > 1:
        for i in zapamti_indekse:
            l_znacajki.append(znacajke[i])
        l_znacajki.sort()
        maksimalna_znacajka = l_znacajki[0]
    else:
        maksimalna_znacajka = znacajke[lista_entropija.index(maksimalna_entropija)]
    return maksimalna_znacajka, maksimalna_entropija

def prebroji_izlaze(tablica_ucenja):
    temp_dict = {}
    for i in range(0, len(tablica_ucenja)):
        krajnji = tablica_ucenja[i][-1][1]
        if krajnji not in temp_dict.keys():
            temp_dict[krajnji] = 1
        else:
            temp_dict[krajnji] += 1
    return temp_dict

def najcesca_oznaka(tablica_ucenja):
    zapamti_kljuceve = []
    brojac = 0
    temp_dict = prebroji_izlaze(tablica_ucenja)
    najveci = max(temp_dict.items(), key=operator.itemgetter(1))[0]
    vrijednost_najveceg = temp_dict[najveci]

    for kljuc in temp_dict.keys():
        if temp_dict[kljuc] == vrijednost_najveceg:
            zapamti_kljuceve.append(kljuc)
            brojac += 1
    if brojac > 1:
        zapamti_kljuceve.sort()
        return zapamti_kljuceve[0]
    return najveci

def nadi_podznacajke(tablica_ucenja, pocetna_znacajka):
    lista_podznacajki = []
    i = 0
    for prvi_red in tablica_ucenja[0]:
        if prvi_red[0] == pocetna_znacajka:
            break
        i += 1
    for red_tablice in tablica_ucenja:
        if red_tablice[i][1] in lista_podznacajki:
            continue
        lista_podznacajki.append(red_tablice[i][1])
    return lista_podznacajki


def napravi_novu_tablicu(tablica_ucenja, pocetna_znacajka, z):
    i = 0
    nova = []
    table_copy = copy.deepcopy(tablica_ucenja)

    for prvi_red in tablica_ucenja[0]:
        if prvi_red[0] == pocetna_znacajka:
            break
        i += 1

    for red in table_copy:
        if(red[i][1] == z):
            nova.append(red)

    for red in nova:
        red.pop(i)
    return nova


def fit(tablica_ucenja,dubina,max_dubina, stablo=None):
    lista_krajnjih = []
    znacajke.clear()

    for prvi_red in tablica_ucenja[0]:
        znacajke.append(prvi_red[0])
    #print(znacajke)

    broj_izlaza = prebroji_izlaze(tablica_ucenja)

    for k in broj_izlaza.keys():
        lista_krajnjih.append(broj_izlaza.get(k))
    #print(lista_krajnjih)
    ent = izracunaj_entropiju(lista_krajnjih)

    if (dubina == max_dubina) and (max_dubina != 0 or max_dubina != -1):
        return najcesca_oznaka(tablica_ucenja)

    if ent == 0.0 or len(znacajke) == 1:
        return najcesca_oznaka(tablica_ucenja)

    pocetna_znacajka, vrijednost_entropije_znacajke = IG(znacajke, tablica_ucenja)

    if stablo is None:
        stablo = {}
        stablo[pocetna_znacajka] = {}

    pod_znacajke = nadi_podznacajke(tablica_ucenja, pocetna_znacajka)
    #print(pod_znacajke, pocetna_znacajka)

    for z in pod_znacajke:

        nova_tablica_ucenja = napravi_novu_tablicu(tablica_ucenja, pocetna_znacajka, z)
        stablo[pocetna_znacajka][z] = fit(nova_tablica_ucenja, dubina+1, max_dubina)

    return stablo


def nadi_tezine(model, dubina, lista):
    try:
        for kljuc in model.keys():
            lista.append(str(str(dubina) + ":" + str(kljuc)))
    except:
        return

    for kljuc in model.keys():
        stablo_2 = model.get(kljuc)

        for kljuc_2 in stablo_2.keys():
            nadi_tezine(stablo_2.get(kljuc_2), dubina + 1, lista)

    return lista


def isprintaj(model, dubina, lista):
    ispis=""
    tezine_znacajke = nadi_tezine(model,dubina,lista)
    #print(tezine_znacajke)
    for t in tezine_znacajke:
        ispis += t + ", "
    print(ispis[:-2])


def f_predict(tablica_testiranja_red, model, tablica_testiranja):
    try:
        for parovi in tablica_testiranja_red:
            if model.keys().__contains__(parovi[0]):
                novi_model = model.get(parovi[0]).get(parovi[1])
                nova_tablica_testiranja = napravi_novu_tablicu(tablica_testiranja, parovi[0], parovi[1])
                prediction = f_predict(tablica_testiranja_red, novi_model, nova_tablica_testiranja)
                if prediction == None:
                    return najcesca_oznaka(tablica_testiranja)
                return prediction
    except:
        if model not in izlaz:
            return najcesca_oznaka(tablica_testiranja)
        return model

def f_tocnost_matricaZabune(izlaz, tablica_testiranja):
    broj_tocnih = 0
    matrica_zabune = [[0 for i in range(len(izlaz))] for i in range(len(izlaz))]

    for i in range(len(tablica_testiranja)):
        if (lista_predvidanje[i] == tablica_testiranja[i][-1][1]):
            broj_tocnih += 1
            indeks = izlaz.index(lista_predvidanje[i])
            matrica_zabune[indeks][indeks] += 1
        else:
            indeks1 = izlaz.index(tablica_testiranja[i][-1][1])
            indeks2 = izlaz.index(lista_predvidanje[i])
            matrica_zabune[indeks1][indeks2] += 1

    tocnost = broj_tocnih / len(tablica_testiranja)
    return matrica_zabune, tocnost
#---------------------------------------------------------------------

tablica_ucenja, tablica_testiranja, izlaz = ucitaj_file()
#print(tablica_ucenja)
max_dubina = int(mapa_konf.get("max_depth"))

model = fit(tablica_ucenja, 0, max_dubina)

isprintaj(model, 0, [])
for tablica_testiranja_red in tablica_testiranja:
    p = f_predict(tablica_testiranja_red, model, tablica_ucenja)
    lista_predvidanje.append(p)
    print(p, end=" ")
print("")

znacajke.clear()
izlaz.sort()
matrica_zabune, tocnost = f_tocnost_matricaZabune(izlaz, tablica_testiranja)

print(tocnost)
for redak in matrica_zabune:
    for i in range(len(redak)):
        print(redak[i], end=" ")
    print()
