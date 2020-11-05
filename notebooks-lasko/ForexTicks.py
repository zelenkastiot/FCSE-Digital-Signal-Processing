# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 15:04:09 2018

@author: Lasko
"""


import numpy as np
import matplotlib.pyplot as plt
import glob
import pandas as pd
import OptimalParameters as op
import datetime

def NapraviData(DataZbor):    
    Godina = int(DataZbor[0:4])
    Mesec = int(DataZbor[4:6])
    Den = int(DataZbor[6:8])
    Chas = int(DataZbor[9:11])
    Minuta = int(DataZbor[11:13])
    Sekunda = int(DataZbor[13:15])
    Milisekunda = 1000 * int(DataZbor[15:18])
    return datetime.datetime(Godina, Mesec, Den, Chas, Minuta, Sekunda, Milisekunda)

def sum1forline(filename):
    with open(filename) as f:
        return sum(1 for line in f)

def ZemiDnevniPodatoci(OdKade, Pochetok):
    DolzhinaNaDatoteka = sum1forline(OdKade)
    BrRedovi = 50   
    if Pochetok + BrRedovi >= DolzhinaNaDatoteka - 1:
        VkupnoBrRedovi = DolzhinaNaDatoteka - Pochetok - 1
        Najden = True
        Podatoci = pd.read_csv(OdKade, skiprows = Pochetok, nrows = VkupnoBrRedovi)        
    else:      
        Podatoci = pd.read_csv(OdKade, skiprows = Pochetok, nrows = BrRedovi) 
        Mesec = NapraviData(Podatoci.iloc[0, 0]).month        
        if NapraviData(Podatoci.iloc[0, 0]).hour < 17:
            Den = (NapraviData(Podatoci.iloc[0, 0])).day                    
        else:               
            Den = (NapraviData(Podatoci.iloc[0, 0]) - datetime.timedelta(hours = 17)).day        
#        print(' denot e' , Den, ' a podatocite od ', OdKade)        
#        Den = NapraviData(Podatoci.iloc[0, 0]).day
        Najden = False
        while not Najden:
            if Pochetok + BrRedovi >= DolzhinaNaDatoteka - 1:
                VkupnoBrRedovi = DolzhinaNaDatoteka - Pochetok - 1              
                Najden = True                
            else:        
                if ((NapraviData(Podatoci.iloc[-1, 0]) - datetime.timedelta(hours = 17)).day > Den) and ((NapraviData(Podatoci.iloc[-1, 0]) - datetime.timedelta(hours = 17)).month == Mesec):        
                    Najden = True
                    VkupnoBrRedovi = BrRedovi
        #            print('pomina')
                else:
                    BrRedovi *= 2
                    Podatoci = pd.read_csv(OdKade, skiprows = Pochetok, nrows = BrRedovi)

        Levo = 0
        Desno = VkupnoBrRedovi - 1
        Sredina = Levo + (Desno - Levo) / 2
        Najden = False
        while not Najden:
            if Desno - Levo == 1:
                Najden = True
            else:    
                if (NapraviData(Podatoci.iloc[Sredina, 0]) - datetime.timedelta(hours = 17)).day > Den: 
                # levo e
                    Desno = Sredina
                else:
                    Levo = Sredina
                Sredina = Levo + (Desno - Levo) / 2 
#                print(Levo, '     ', NapraviData(prvPodatoci.iloc[Levo, 0]), ' -  ',  Desno, NapraviData(prvPodatoci.iloc[Desno, 0]))           
        if (NapraviData(Podatoci.iloc[Desno, 0]) - datetime.timedelta(hours = 17)).day == Den:
            VkupnoBrRedovi = Desno + 1
#            print('desno')
        else:
            VkupnoBrRedovi = Levo + 1
#            print('levo')
        
    Podatoci = pd.read_csv(OdKade, skiprows = Pochetok, nrows = VkupnoBrRedovi)
    if Podatoci.shape[0] > 0:     
        print(NapraviData(Podatoci.iloc[0, 0]), '  ', NapraviData(Podatoci.iloc[-1, 0]))
    
    return Podatoci, Pochetok + VkupnoBrRedovi


dir_name = "/Users/Lasko/podatoci/varijansa/novi/"
KajSePodatocite = '/Users/Lasko/podatoci/varijansa/'
KajDaSnima = '/Shared Folder/Lasko/proekti/FOREX/rezultati/'

PragNaSignal = 0.0005
DocenenjePoSignal = 10.0 # vo sekundi

prvPar = KajSePodatocite + 'csv_12_2018/ETX_EUR_12_18.csv'
vtorPar = KajSePodatocite + 'csv_12_2018/AUD_JPY_12_18.csv'

KrajNaDatoteka = False
kolkuPodatociPrv = sum1forline(prvPar)
kolkuPodatociVtor = sum1forline(vtorPar)

print(kolkuPodatociPrv, kolkuPodatociVtor)
PochetokPrv = 0
PochetokVtor = 0
BrDenovi = 0
BrTrguvanja = 0
Dobivka = 0
PrinosiPoSignal = []
VremeNaPrinos = []
DnevnaDobivka = 0
DnevniTrguvanja = 0

PostojanaDnevnaDobivka = 0
BrPostojaniTrguvanja = 0

while not KrajNaDatoteka:
    prvPodatoci, SledenPochetokPrv = ZemiDnevniPodatoci(prvPar, PochetokPrv)
    vtorPodatoci, SledenPochetokVtor = ZemiDnevniPodatoci(vtorPar, PochetokVtor)        
            
    SePoklopuvaat = False
    while not SePoklopuvaat:
        
        if (prvPodatoci.iloc[0, 0] < vtorPodatoci.iloc[-1, 0]) and (prvPodatoci.iloc[-1, 0] > vtorPodatoci.iloc[0, 0]):
            SePoklopuvaat = True
        elif prvPodatoci.iloc[0, 0] > vtorPodatoci.iloc[-1, 0]:
            vtorPodatoci, SledenPochetokVtor = ZemiDnevniPodatoci(vtorPar, PochetokVtor)
            PochetokVtor = SledenPochetokVtor
        elif prvPodatoci.iloc[-1, 0] < vtorPodatoci.iloc[0, 0]:  
            prvPodatoci, SledenPochetokPrv = ZemiDnevniPodatoci(prvPar, PochetokPrv)
            PochetokPrv = SledenPochetokPrv            
        if (SledenPochetokPrv + 1 >= kolkuPodatociPrv) or (SledenPochetokVtor + 1 >= kolkuPodatociVtor):
            KrajNaDatoteka = True
            SePoklopuvaat = True
    
    zemeniPodatociPrv = len(prvPodatoci)
    zemeniPodatociVtor = len(vtorPodatoci) 
    BrPostojaniTrguvanja = 0
    BrTrguvanja = 0

    DnevnaDobivka = 0
    PostojanaDnevnaDobivka = 0    
    
    if ((SledenPochetokPrv  + 1 >= kolkuPodatociPrv) or (SledenPochetokVtor + 1 >= kolkuPodatociVtor)):
        KrajNaDatoteka = True        
    else:
        PokazatelNaVtorPar = 0
        for i in range(zemeniPodatociPrv - 1):
            if np.log(prvPodatoci.iloc[i + 1, 1]) - np.log(prvPodatoci.iloc[i, 1]) > PragNaSignal:
                Najden = False
                VremePrv = (NapraviData(prvPodatoci.iloc[i, 0]) - datetime.datetime(1970,1,1)).total_seconds()
                if PokazatelNaVtorPar < zemeniPodatociVtor - 1:
                    while not Najden:
                        VremeVtor = (NapraviData(vtorPodatoci.iloc[PokazatelNaVtorPar, 0]) - datetime.datetime(1970,1,1)).total_seconds()
                        if PokazatelNaVtorPar < zemeniPodatociVtor - 2:
                            PostojanaDnevnaDobivka += np.log(vtorPodatoci.iloc[PokazatelNaVtorPar + 1, 1]) - np.log(vtorPodatoci.iloc[PokazatelNaVtorPar, 1])
                            BrPostojaniTrguvanja += 1
    #                    print(VremePrv, ' vtor ', VremeVtor)
                        if VremeVtor > VremePrv + DocenenjePoSignal:
                            Najden = True
                            Dobivka = np.log(vtorPodatoci.iloc[PokazatelNaVtorPar + 1, 1]) - np.log(vtorPodatoci.iloc[PokazatelNaVtorPar, 1])
                            PrinosiPoSignal.append(Dobivka)
                            VremeNaPrinos.append(vtorPodatoci.iloc[PokazatelNaVtorPar, 0])
                            BrTrguvanja += 1
                            DnevnaDobivka += Dobivka
                                                    
                        PokazatelNaVtorPar += 1
                        if PokazatelNaVtorPar > zemeniPodatociVtor - 2:
                            Najden = True
                    
                                                
#        print(' deneska ima ', DnevniTrguvanja, ' trguvanja i ', DnevnaDobivka, ' dobivka  ')                
        print('  trguvanja ', BrTrguvanja, '  a vkupno ', BrPostojaniTrguvanja)
        print('  dobivka ', DnevnaDobivka, ' a postojano ', PostojanaDnevnaDobivka)        
        print(' prosek dobivki ', DnevnaDobivka / BrTrguvanja, '  i postojani ', PostojanaDnevnaDobivka / BrPostojaniTrguvanja)        
    PochetokPrv = SledenPochetokPrv
    PochetokVtor = SledenPochetokVtor

SpisokDobivki = []
for i in range(len(PrinosiPoSignal)):
    SpisokDobivki.append([VremeNaPrinos[i], PrinosiPoSignal[i]])    
    
panda = pd.DataFrame(SpisokDobivki)    
    
writer = pd.ExcelWriter(KajDaSnima + 'dobivki.xlsx')
panda.to_excel(writer, 'Sheet1')
writer.save()    
    
numbins = 30
n, bins, patches = plt.hist(PrinosiPoSignal, numbins, density=True, facecolor='g', alpha=0.75, log = True)
#                    plt.hist(zaHist, 50, density=True, facecolor='g', alpha=0.75, log = True, bins = 'auto')                    
binovi = bins[0:-1]
plt.plot(binovi, n, 'rx')
plt.show()


print('  trguvanja ', BrTrguvanja, '  a vkupno ', BrPostojaniTrguvanja)
print('  dobivka ', DnevnaDobivka, ' a postojano ', PostojanaDnevnaDobivka)
print(' prosek dobivki ', DnevnaDobivka / BrTrguvanja, '  i postojani ', PostojanaDnevnaDobivka / BrPostojaniTrguvanja)