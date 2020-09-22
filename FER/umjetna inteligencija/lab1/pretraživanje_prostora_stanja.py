from queue import PriorityQueue

f_opisnikStanja = open("istra.txt", "r").readlines()
poc_brojac=0
kraj_brojac=0
opisnik_prostora={}
kraj=[]

'Ucitavanje podataka iz opisnika stanja ' \
'posebna vaijabla je pocetak i polje kraj (moguca vise zavrsnih stanja)' \
'stanja i prijelaze sortirani su u mapi opisnik_stanja[ime grada]= moguci prijelazi oblika (sljedeci_grad,udaljenost)'
for stanje in f_opisnikStanja:
  if(stanje.startswith('#')):
    continue
  if(poc_brojac==0):
    pocetak=stanje.strip() #ucitavanje polazista
    poc_brojac=1
    continue
  if (kraj_brojac == 0):
    kraj = stanje.split() #ucitavanje odredista
    kraj_brojac = 1
    continue
  grad_putevi= stanje.split(':') #ucitavanje mogucih puteva s odredenih lokacija
  novi_putevi=grad_putevi[1].strip()
  stanje_vrijednost=novi_putevi.split(' ')  #razdvajanje slijedeceg poteza i njegove vrijednosto
  opisnik_prostora[grad_putevi[0]]=stanje_vrijednost

'ucitavanje zadane heuristike, vraca mapu mapa_heuristike[grad]=udaljenost'
def ucitaj_heuristiku(datoteka):
    f_heuristika = open(datoteka, "r").readlines()
    mapa_heuristike = {}
    for heuristika in f_heuristika:
        pomocna_varijabla = heuristika.split(':') #razdvaja liniju grad:udaljenost za spremanje u mapu
        mapa_heuristike[pomocna_varijabla[0]] = pomocna_varijabla[1].strip()
    return mapa_heuristike

'nalazi put kojim od pocetnog do krajnjeg stanja koristeći mapu mapa_roditelj_dijete[iduci_grad]=prethodni ' \
'pomoću koje smo zapamtili prijelaze kojima smo išli u pretrazi algoritma'
def backtrace(mapa_roditelj_dijete, pocetak, kraj):
    path = [kraj]
    # prati put dok ne dode do početka
    while kraj != pocetak:
        kraj = mapa_roditelj_dijete[kraj]
        path.insert(0, kraj)
    return path
def printPath(path):
    rezultat=""
    for p in path:
        rezultat+= p +" => \n"
    print(rezultat[:-4])
    
'BFS search : vraća polje mogućih sljedecih poteza iz trenutnog stanja' \
'clan polja je oblika (slijedeci_grad,razina)'
def expand(n, popis_sljedecih_gradova_sa_vrijednostima):
    polje_slj_g=[] #prazno polje u koje cu staviti listu slijedecih gradova s vrijednostima cvora
    for popis_sljedecih_gradova in popis_sljedecih_gradova_sa_vrijednostima:
        polje_slj_g.append((popis_sljedecih_gradova.split(',')[0],n+1))
    return polje_slj_g

'algoritam koji ide razinu po razinu i tako dolazi do kraja(cilja)' \
'u listi open pohranjeni su cvorovi (grad,razina) po kojima algoritam trazi slijedno kako smo čvorove stavili u listu' \
'obideni je set u kojem se pohranjuju imena svih gradova/stanja koje je algoritam prosao' \
'trazimo kraj dok ima cvorova u listi open ili dok ne dodemo do krajnjega stanja' \
' lista_obilaska je lista koja je sluzila za provjeru posjecivanja pojedinih cvorova (usporedba s rucnim rjesenjem obilaska stabla)'
def BFS(pocetak,opisnik_prostora,kraj):
    mapa_roditelj_dijete={}
    d=0
    open=[]
    obideni=set()
    lista_obilaska = []
    open.append((pocetak,d))  #oblika (grad,cvor)
    while len(open)!=0:
        trenutni_grad = open.pop(0)
        obideni.add(trenutni_grad[0])
        'provjera jesmo li dosli do krajnjeg stanja (moze postojati vise krajnjih stanja (zato je kraj lista)' \
        'ako jesmo ispisujemo sve što nas traži i izlazimo iz f-je'
        if (trenutni_grad[0] in kraj):
            for k in kraj:
                if (trenutni_grad[0] == k):
                    lista_obilaska.append(trenutni_grad)
                    print(lista_obilaska) #uvjerava u ispravnost obilaska cvorova
                    print(len(lista_obilaska))
                    print("States visited = ", len(obideni))
                    print("Found path of lenght ", trenutni_grad[1] + 1, ":")
                    path=backtrace(mapa_roditelj_dijete, pocetak, k)
                    printPath(path)
                    break
            break
        lista_iducih_gradova=expand(trenutni_grad[1],opisnik_prostora.get(trenutni_grad[0]))
        lista_obilaska.append(trenutni_grad)
        'u mapi mapa_roditelj_dijete pamtimo relaciju sljedeci-trenutni kako bismo mogli sa funkcijom traceroute naci put'
        for iduci_grad in lista_iducih_gradova:
            if iduci_grad[0] not in mapa_roditelj_dijete:
                mapa_roditelj_dijete[iduci_grad[0]]=trenutni_grad[0]
            open.append(iduci_grad) #ubacujemo sljedeca stanja u listu open kojom pretrazujemo
    return False

'UCS search : vraća polje mogućih sljedecih poteza iz trenutnog stanja' \
'clan polja je oblika (slijedeci_grad,cost,razina)'
def expand1(trenutni_grad, opisnik_prostora):
    popis_gradova=[]
    gradovi_obiljezlja = opisnik_prostora.get(trenutni_grad[1])
    for grad in gradovi_obiljezlja:
        popis_gradova.append([grad.split(',')[0],int(grad.split(',')[1])+trenutni_grad[0],trenutni_grad[2]+1])
    return popis_gradova

'algoritam koji sljedeci cvor uzima na temelju minimalne vrijednosti cost grada(stanja u kojm se nalazi) do cilja i tako dolazi do kraja(cilja)' \
'u prioritetnom redu open pohranjeni su cvorovi (cost,grad,razina) koji gradi prioritet na temelju minimalne vrijednosti varijable cost' \
'obideni je set u kojem se pohranjuju imena svih gradova/stanja koje je algoritam prosao' \
'trazimo kraj dok ima cvorova u listi open ili dok ne dodemo do krajnjega stanja' \
' lista_obilaska je lista koja je sluzila za provjeru posjecivanja pojedinih cvorova (usporedba s rucnim rjesenjem obilaska stabla)'
def USC(pocetak,opisnik_prostora,kraj):
    mapa_roditelj_dijete = {}
    d = 0
    open = PriorityQueue()
    obideni = set()
    lista_obilaska = []
    open.put((d,pocetak,d))  # oblika (cost,grad,razina)
    mapa_roditelj_dijete['Buzet'] = 'Lupoglav'
    while not open.empty():
        trenutni_grad =open.get()
        obideni.add(trenutni_grad[1])
        'provjera jesmo li dosli do krajnjeg stanja (moze postojati vise krajnjih stanja (zato je kraj lista)' \
        'ako jesmo ispisujemo sve što nas traži i izlazimo iz f-je'
        if (trenutni_grad[1] in kraj):
            for k in kraj:
                if (trenutni_grad[1] == k):
                    lista_obilaska.append(trenutni_grad[1])
                    # print(lista_obilaska)
                    print("States visited = ", len(obideni))
                    print("Found path of lenght ", trenutni_grad[2] + 1, "with total cost", trenutni_grad[0], ":")
                    path=backtrace(mapa_roditelj_dijete, pocetak, trenutni_grad[1])
                    printPath(path)

                    break
            break
        lista_iducih_gradova=expand1(trenutni_grad,opisnik_prostora)
        lista_obilaska.append(trenutni_grad[1])
        'u mapi mapa_roditelj_dijete pamtimo relaciju sljedeci-trenutni kako bismo mogli sa funkcijom traceroute naci put'
        for iduci_grad in lista_iducih_gradova:
            if (iduci_grad[0] not in mapa_roditelj_dijete):
                mapa_roditelj_dijete[iduci_grad[0]]=trenutni_grad[1]
            if (iduci_grad[0] not in obideni):
                open.put((iduci_grad[1],iduci_grad[0],iduci_grad[2])) #ubacujemo sljedeca stanja u listu open kojom pretrazujemo ukoliko ga nismo vec obisli
    return False

def expand2(trenutni_grad, opisnik_prostora,mapa_heuristike):
    popis_gradova = []
    gradovi_obiljezlja = opisnik_prostora.get(trenutni_grad[1])
    for grad in gradovi_obiljezlja:
        popis_gradova.append((int(grad.split(',')[1]) + trenutni_grad[0],grad.split(',')[0], trenutni_grad[2] + 1,int((int(grad.split(',')[1]) + trenutni_grad[0]+int(mapa_heuristike.get(grad.split(',')[0]))))))
    return popis_gradova

'funkcija vraca najmanje mjesto u listi lista po kriteriju place mjesta koje se nalazi varijabla unutar liste'
def getMin(open,place):
    pom=list(open)[0]
    for o in open:
        if(o[place]<pom[place]):
            pom=o
    return pom
    
'algoritam koji sljedeci cvor uzima na temelju minimalne vrijednosti cost grada(stanja u kojm se nalazi) do cilja i njegove heuristike (procjene do cilja)' \
'u setu open pohranjeni su cvorovi (cost,grad,razina,heuristika+ cost) koji gradi prioritet na temelju minimalne vrijednosti varijable dotadasnjeg puta cost i procjene puta do cilja(heuristike)' \
'closed je set u kojem se pohranjuju imena svih gradova/stanja koje je algoritam prosao' \
'trazimo kraj dok ima cvorova u listi open ili dok ne dodemo do krajnjega stanja'
def Astar(pocetak,opisnik_prostora,kraj,f_heuristika):
    d=0
    obideni = set()
    open=set()
    open.add((d,pocetak,d,int(f_heuristika.get(pocetak))))
    closed=set()
    mapa_roditelj_dijete={}
    mapa_obideni_cost={}
    while len(open)!=0:
        trenutni_grad=getMin(open,3)
        open.remove(trenutni_grad)
        obideni.add(trenutni_grad[1])
        mapa_obideni_cost[trenutni_grad[1]]=trenutni_grad[0]
        if(trenutni_grad[1] in kraj):
            for k in kraj:
                if (trenutni_grad[1] == k):
                    print("States visited = ", len(obideni))
                    print("Found path of lenght ", trenutni_grad[2] + 1, "with total cost", trenutni_grad[0], ":")
                    path=backtrace(mapa_roditelj_dijete, pocetak, trenutni_grad[1])
                    printPath(path)
                    break
            break
        closed.add((trenutni_grad[0],trenutni_grad[1]))
        lista_gradova =expand2(trenutni_grad,opisnik_prostora, f_heuristika)
        remember=set()
        remember_o=set()
        'provjerava se ima li u open ili closed setovima neki grad za kojega vrijedi da je cost udaljenost' \
        'manja od novo pronađenog čvora pomocu funkcije expand' \
        'ako je to tocno ne stavljamo ga u set closed/open' \
        'ukoliko je novi čvor kraci od onoga u setu open/closed ubacujemo ga unutra, a stari(isti grad,veca udaljenost) micemo s popisa'
        for grad in lista_gradova:
            for c in closed:
                if (c[1]==grad[1]):
                    if(c[0]<grad[0]):
                        continue
                    else:
                        remember.add(c)
            for r in remember:
                closed.remove(r)
            for o in open:
                if (o[1]==grad[1]):
                    if(o[0]<grad[0]):
                        continue
                    else:
                        remember_o.add((o))
            for r in remember_o:
                open.remove((r))
            if (grad[1] not in mapa_roditelj_dijete):
                'u mapi mapa_roditelj_dijete pamtimo relaciju sljedeci-trenutni kako bismo mogli sa funkcijom traceroute naci put'
                mapa_roditelj_dijete[grad[1]] = trenutni_grad[1]
            if(grad[1]=='Buzet'):
                mapa_roditelj_dijete[grad[1]] = trenutni_grad[1]
            remember.clear()
            remember_o.clear()
            open.add((grad[0],grad[1],grad[2],grad[3]))
    return False
    
'funkcija vraca daje li opisnik prostora uz zadanu heuristiku optimalan put' \
'krećemo od kraja i tako obilazimo sve moguce veze izmedu gradova' \
'pamtimo one koje smo obisli da ne udemo u beskonacnu petlju' \
'kada dodemo do odredenog grada pribrojimo mu udaljenost od odredista prethodnog grada sa njegovom udaljenoscu' \
'i na kraju u mapi gdje su zapisani svi gradovi i njihove minimalne udaljenosti do odredista provjeravamo jesu li veće od pretpostavljene heuristicke vrijednosti'
def optimal(mapa_heuristika, opisnik_prostora, kraj):
    mapa={}
    gradovi=[]
    for key in mapa_heuristike.keys():
        gradovi.append(key)
    for g in gradovi:
        mapa[g]=0
    lista_posjecenih=[]
    lista_za_posjetiti=[]
    rezultat=""
    print("Checking if heuristic is optimistic.")
    for k in kraj:
        for razdvoji in opisnik_prostora.get(k):
            ra=razdvoji.split(',')
            lista_za_posjetiti.append((ra[0]))
            mapa[ra[0]]=float(ra[1].strip())
        lista_posjecenih.append((k))
    while len(lista_za_posjetiti)!=0:
        trenutni_grad=lista_za_posjetiti.pop(0)
        for sljedeci in opisnik_prostora.get(trenutni_grad):
            slj=sljedeci.split(',')
            if slj[0] in lista_posjecenih:
                continue
            lista_za_posjetiti.append((slj[0]))
            if((mapa.get(slj[0])!=0 and mapa.get(slj[0])> (float(slj[1].strip())+ float(mapa.get(trenutni_grad))))or mapa.get(slj[0])==0):
                mapa[slj[0]] = float(slj[1].strip())+ float(mapa.get(trenutni_grad))
            lista_posjecenih.append(slj[0])
    for g in gradovi:
        if((float(mapa_heuristika.get(g)) > float(mapa.get(g))) ):
            rezultat+="[ERR] h("+ g+") > h* : "+str(mapa_heuristika.get(g))+" > "  + str(mapa.get(g))+"\n"
    if(rezultat==""):
        print("Heuristic is optimistic")
    else:
        print(rezultat[:-1])
        print("Heuristic is not optimistic")

'funkcija provjerava konzistentnost gramatike tako da za svaki grad provjerava' \
'je li njegova heuristika veca od njegovog sljedbenika+udaljenosti izmedu trenutnog grada i sljedbenika '
def consistent(mapa_heuristike, opisnik_prostora):
    gradovi = []
    rezultat=""
    print("Checking if heuristic is consistent.")
    for key in mapa_heuristike.keys():
        gradovi.append(key)
    for grad in gradovi:
        for grad_sljedeci in opisnik_prostora.get(grad):
            if(float(mapa_heuristike.get(grad))>(float(mapa_heuristike.get(grad_sljedeci.split(',')[0]))+float(grad_sljedeci.split(',')[1]))):
                rezultat+="[ERR] h(" +grad +") > h(" +grad_sljedeci.split(',')[0]+") + c: "+str(float(mapa_heuristike.get(grad)))+" > "+str(float(mapa_heuristike.get(grad_sljedeci.split(',')[0])))+" + "+str(float(grad_sljedeci.split(',')[1]))+"\n"
    if (rezultat == ""):
        print("Heuristic is consistent")
    else:
        print(rezultat[:-1])
        print("Heuristic is not consistent")


print("Starting BFS:")
BFS(pocetak,opisnik_prostora,kraj)
print("")
print("Starting UCS:")
USC(pocetak,opisnik_prostora,kraj)
print("")
mapa_heuristike=ucitaj_heuristiku("istra_heuristic.txt")
print("Starting A* + optimistic")
Astar(pocetak,opisnik_prostora,kraj,mapa_heuristike)
print("")
mapa_heuristike=ucitaj_heuristiku("istra_pessimistic_heuristic.txt")
print("Starting A* + pessimistic")
Astar(pocetak,opisnik_prostora,kraj,mapa_heuristike)
print("")
mapa_heuristike=ucitaj_heuristiku("istra_heuristic.txt")
print("Za istra_heuristic:")
optimal(mapa_heuristike, opisnik_prostora, kraj)
consistent(mapa_heuristike, opisnik_prostora)
print("")
mapa_heuristike=ucitaj_heuristiku("istra_pessimistic_heuristic.txt")
print("Za istra_pessimistic_heuristic")
optimal(mapa_heuristike, opisnik_prostora, kraj)
consistent(mapa_heuristike, opisnik_prostora)
