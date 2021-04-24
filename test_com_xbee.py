# Module de lecture/ecriture du port sÃ©rie
from serial import *
from time import *
# Port sÃ©rie ttyACM0
# Vitesse de baud : 9600
# Timeout en lecture : 1 sec
# Timeout en Ã©criture : 1 sec
 
#a=str.encode("3")
 
#
#rList = [1, 2, 3, 4, 5]
#arr = bytes(rList)
chaine = "Mon @ & un a : (je mange]{des frites=+- gros"
chaine = "test.txt"
chemin = "cheTest.txt"
global ChiffreRecu
global ChiffreEnvoi
ChiffreEnvoi=1
PortSerie = Serial(port="COM3", baudrate=9600, timeout=0.1, writeTimeout=0.1)
#%%
def sup():
    PortSerie.close()
    PortSerie.open()
 
    Etat = connection()
    if Etat == True:
        suppression(chaine)
   
    
def lec():
    PortSerie.close()
    PortSerie.open()
    Etat = connection()
    if Etat == True:
        Etat = lecture(chemin)
        if Etat == True:
            RecevoirData()
 
def ecr():
    PortSerie.close()
    PortSerie.open()
    Etat = connection()
    if Etat == True:
        ecriture(chemin, "test2021")
#%%
def connection():
    rep=[[],True]
    global ChiffreEnvoi
    if PortSerie.isOpen():
        TestConnexion=0
        while TestConnexion <10 and rep[1]==True:
            PortSerie.write(bytes(ChToAsNb('dc00000',ChiffreEnvoi)))
            print(bytes(ChToAsNb('dc00000',ChiffreEnvoi)))
            rep = Attente()
            if rep[1] == True:
                EtatPortSerie = rep[0]
            else:
                print("TimeOut d'attente connection")
                return(False)
                break
           
                print("le retour doit etre ",bytes(ChToAsNb('dc00val',ChiffreEnvoi)))
            if EtatPortSerie == bytes(ChToAsNb('dc00val',ChiffreEnvoi)):
                print("connexion établie")
                IChiffreEnvoi()
                return(True)
                break
            elif EtatPortSerie == bytes(ChToAsNb('dc0refm',ChiffreEnvoi)):
                print("le robot est en match")
                IChiffreEnvoi()
                return(False)
                break
            else:
                print("erreur de communication")
                return(False)
                TestConnexion+=1
            IChiffreEnvoi()
 
#%%
def suppression(chaine):
    rep= [[],True]
    if PortSerie.isOpen():
        PortSerie.write(bytes(ChToAsNb('dtd0000',ChiffreEnvoi)))
        print(bytes(ChToAsNb('dtd0000',ChiffreEnvoi)))
        EtatPortSerie = Attente()
        print(bytes(ChToAsNb('dtd0deb',ChiffreEnvoi)))
        if EtatPortSerie[0] == bytes(ChToAsNb('dtd0deb',ChiffreEnvoi)):
            print("suppression accordée")   
            liste=decoupe(chaine)
            EnvoiListe(liste)
            rep = Attente()
            if rep[1] == True:
                EtatPortSerie = rep[0]
                if EtatPortSerie == bytes(ChToAsNb('dtd0fin',ChiffreEnvoi)):
                    print("suppression fini")
                elif EtatPortSerie == bytes(ChToAsNb('dtd00nt',ChiffreEnvoi)):
                    print("suppression chemin non trouver")
                elif EtatPortSerie == bytes(ChToAsNb('dtd0int',ChiffreEnvoi)):
                    print("suppression chemin interdie")
            else:
                print("TimeOut d'attente sup")
        else:
            if EtatPortSerie == b'err byte':
                print("probleme de transmition")
            else:   
                print("suppression refusé")
    else:
        print("le port est fermé")  
#%%
def lecture(chemin):
    TestConnexion = 0
    if PortSerie.isOpen():
        PortSerie.write(bytes(ChToAsNb('dtr0000',ChiffreEnvoi)))
        print(bytes(ChToAsNb('dtr0000',ChiffreEnvoi)))
        EtatPortSerie = Attente()
        IChiffreEnvoi()
        if EtatPortSerie[0] == bytes(ChToAsNb('dtr0deb',ChiffreEnvoi-1)):#check le -1
            
            liste=decoupe(chemin)
            print("je suis la")
            EnvoiListe(liste)
            EtatPortSerie = Attente()
            while TestConnexion <10 :
                if EtatPortSerie[0] == bytes(ChToAsNb('dtr0ntr',ChiffreEnvoi)):
                    print("chemin non trouvé")
                    return(False)
                    break
                elif EtatPortSerie[0] == bytes(ChToAsNb('dtr00tr',ChiffreEnvoi)):
                    print("chemin trouvé")
                    PortSerie.write(bytes(ChToAsNb('dtrpret',ChiffreEnvoi)))
                    IChiffreEnvoi()    
                    return(True)
                    break        
#faire verif
                else:
                    print("Erreur communication")
                    PortSerie.write(bytes(ChToAsNb('dtr1000',ChiffreEnvoi)))
                    #pas gerer
                TestConnexion += 1
            if TestConnexion >= 10:
                return(False)
#%%
def ecriture(chemin,chaine):
    if PortSerie.isOpen():
        PortSerie.write(bytes(ChToAsNb('dte0000',ChiffreEnvoi)))
        print("j'ai ecris",bytes(ChToAsNb('dte0000',ChiffreEnvoi)))
        EtatPortSerie = Attente()
        print(EtatPortSerie[0],bytes(ChToAsNb('dte0deb',ChiffreEnvoi)))
        if EtatPortSerie[0] == bytes(ChToAsNb('dte0deb',ChiffreEnvoi)):
            IChiffreEnvoi()
            Liste = decoupe(chemin)
            print(Liste)
            EnvoiListe(Liste)
            EtatPortSerie = Attente()
            if EtatPortSerie[0] == bytes(ChToAsNb('dte00ok',ChiffreEnvoi)):
                print("chemin trouvé")
                EnvoiListe(decoupe(chaine))
                EtatPortSerie = Attente()
                print(bytes(ChToAsNb('dte0fin',ChiffreEnvoi)))
                if EtatPortSerie[0] == bytes(ChToAsNb('dte0fin',ChiffreEnvoi)):# juste check reception pour valider
                    print("Ecriture réussie")
            elif EtatPortSerie[0] == bytes(ChToAsNb('dte0nok',ChiffreEnvoi)):
                print("chemin non trouvé")
            elif EtatPortSerie[0] == bytes(ChToAsNb('dte0int',ChiffreEnvoi)):
                print("chemin interdit")
            else:
                print("probleme")
        else:
            IChiffreEnvoi()
            print("probleme cond")
#%%
               
def ReceptionCo():
    global ChiffreRecu
    print("Entrée reception")
    print("chiffre " ,ChiffreRecu )
    EtatPortSerie = Attente()
    print("EtatPortSerie",EtatPortSerie)
    if EtatPortSerie[1]==True:
        print(EtatPortSerie)
        print(EtatPortSerie[0][0])
        print("ChiffreRecu",ChiffreRecu)
        if EtatPortSerie[0][0] == ChiffreRecu+1:
            ChiffreRecu=EtatPortSerie[0][0]
            PortSerie.write(EtatPortSerie[0])
            print('reception correct')
            return[EtatPortSerie[0],True]
           
        elif EtatPortSerie[0][0] == ChiffreRecu :
            PortSerie.write(EtatPortSerie[0])
            print("reception -1")
            return[EtatPortSerie[0],False]
        else:
            PortSerie.write(b'erreurby')   #a definir
            print("erreur bytes")
            return[b'erreurby']
    else:
        print("rien a lire ici")
        return[b'erreurby']
 
#%%
def RecevoirData():
    global ChiffreRecu
    ChiffreRecu= 0
    TestConnexion= 0
    Att=""
    Liste = []
    EtatPortSerie = b' '
    NbTest = 10
    print("Entrée")
    
    while EtatPortSerie[0] != bytes(ChToAsNb('\xff\xff\xff\xff\xff\xff\xff',ChiffreRecu)) and TestConnexion <NbTest:
        TestConnexion = 0
        EtatPortSerie= ReceptionCo()
 
        if EtatPortSerie[0] != b'erreurby':
            if EtatPortSerie[1] == True:
                    Liste+=[Att]
                    Att=EtatPortSerie[0]
            while EtatPortSerie[1] != True and TestConnexion <NbTest :
                EtatPortSerie = ReceptionCo()
                print("EtatPortSerie",EtatPortSerie)
                if EtatPortSerie[0] != b'erreurby':
                    if EtatPortSerie[1] == True:
                        Att = EtatPortSerie[0]
                TestConnexion+=1
        if TestConnexion >= NbTest:
            break
    Liste+=[Att]
   
    print(1,Liste)
    print("Data recu")
    return()
 
#%%
def decoupe(chaine):
    nb = len(chaine)
    liste = []
    listeCH=[]
    listeatt =[]
    for i in range(nb):
        listeCH +=[ord(chaine[i])]
    for i in range(nb):
        if i%7!=0 :
            listeatt += [listeCH[i]]
        else:
            liste+=[listeatt]
            listeatt = [listeCH[i]]
           
    while len(listeatt) != 7:
        listeatt +=[0]
    liste+=[listeatt]+[[255,255,255,255,255,255,255]]
           
    liste.remove([])
    return(liste)
 
#%%
def EnvoiListe(liste): #retourner le succée ou non de la liste
    global ChiffreEnvoi
    rep=[[],True]
    continu = True
    if PortSerie.isOpen():
        print("liste",liste)
        for i in range(len(liste)):
            PortSerie.write(bytes([ChiffreEnvoi]+liste[i]))
            print("j'ecris",bytes([ChiffreEnvoi]+liste[i]))
            EtatPortSerie = Attente()
            while EtatPortSerie[0] != bytes([ChiffreEnvoi]+liste[i]) and rep[1] :
                PortSerie.write(bytes([ChiffreEnvoi]+liste[i]))
                print("j'ecris",bytes([ChiffreEnvoi]+liste[i]))
                rep = Attente()               
                if rep[1] == True:
                    EtatPortSerie = rep[0]
                else:
                    print("TimeOut d'attente envoi liste")
                    continu = False
                    break
            if continu == False:
                print("stop")
                break
            IChiffreEnvoi()
    PortSerie.write(bytes(ChToAsNb('2345678',ChiffreEnvoi)))
    print("j'ecris",bytes(ChToAsNb('2345678',ChiffreEnvoi)))
 
#%%
def Attente():
    temps = perf_counter()
    t=0
    var = True
    rep = True
    tempsAtt = 0
    EtatPortSerie = ""
    TempsAAtt = 3
    while var and tempsAtt < TempsAAtt: 
        t= PortSerie.inWaiting()
        if t==8:
            var = False  
        tempsAtt =  perf_counter() - temps
    if tempsAtt >= TempsAAtt:
        rep= False
        print("rien a lire")
    else:
        EtatPortSerie = PortSerie.readline()
        print("j'ai lu",EtatPortSerie)
    return(EtatPortSerie,rep)
#%%
def ChToAs(Chaine7,nb):
    Liste=[]
    for i in range(len(Chaine7)):
        Liste+=[ord(Chaine7[i])]
    Liste=[nb]+Liste
    return(Liste)
#%%
def IChiffreEnvoi():
    global ChiffreEnvoi
    ChiffreEnvoi+=1
    if ChiffreEnvoi == 9:
        ChiffreEnvoi =1
    return(ChiffreEnvoi)
#%%          
def ChToAsNb(Chaine7,nb):
    Liste=[]
    for i in range(len(Chaine7)):
        Liste+=[ord(Chaine7[i])]
    Liste=[nb]+Liste
    return(Liste)
