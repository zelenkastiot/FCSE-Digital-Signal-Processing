# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 11:56:36 2018

@author: Lasko
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import OptimalParameters as op
import datetime
#import SampleVarianceData as svd
import powerlaw
#import PCA
import math
import csv
import PCAnova as PCA

def is_nan(x):
    return (x is np.nan or x != x)

#############################################
#       Akcii


#podatoci = pd.ExcelFile('/Users/Lasko/podatoci/varijansa/AAP.xlsx', sheetname=0)
#Izvlecheni = podatoci.parse(0)
#    # Ova e za CALL Opcii
#OpenPrice = Izvlecheni.iloc[:,4].real
#ClosePrice = Izvlecheni.iloc[:,1].real
#Vreminja = Izvlecheni.iloc[:,6] # probno za data


#       Akcii
#############################################

#############################################
#       FOREX

#podatoci = svd.podatoci
podatoci = pd.ExcelFile('/Users/Lasko/podatoci/varijansa/2016/EUR_USD_2016.xlsx')
Izvlecheni = podatoci.parse(0)
    # Ova e za CALL Opcii
OpenPrice = Izvlecheni.iloc[:,1].real
ClosePrice = Izvlecheni.iloc[:,2].real
Vreminja = Izvlecheni.iloc[:,0] # probno za data

#       FOREX
#############################################

#print(OpenPrice)
#for i in range(400):
#    print(i, ' ', Vreminja[i].hour, ' den ' ,Vreminja[10 * i].weekday())

KolkuPodatoci = len(OpenPrice)
KolkuPodatoci = 10000

#print(KolkuPodatoci)
LogPrinosi = []

VremenskaRazlika = []




#########################################
#    po den i po saat statistika

KolkuPoDenISaat = np.zeros((7, 24))
PoDenISaatVarijansa = np.zeros((7, 24))
PoDenISaatHistogrami = np.zeros((7, 24, 53))
RealiziranoGama = []
PoDenISaatGama = np.zeros((7, 24))
PrethodenMoment = Vreminja[0]
LogPrinosi = []
for i in range(KolkuPodatoci - 2):    
    TekovenMoment = Vreminja[i + 1]
    if (TekovenMoment.date() == PrethodenMoment.date()) and (TekovenMoment.hour == PrethodenMoment.hour):
        LogPrinosi.append(np.log(OpenPrice[i + 1]) - np.log(OpenPrice[i]))        
    else:
        Varijansa = np.std(LogPrinosi, ddof = 1)
        KolkuPoDenISaat[PrethodenMoment.weekday(), PrethodenMoment.hour] += 1
        PoDenISaatVarijansa[PrethodenMoment.weekday(), PrethodenMoment.hour] += Varijansa
        ImpGama = op.ImpliedGamma(LogPrinosi)
        PoDenISaatGama[PrethodenMoment.weekday(), PrethodenMoment.hour] += ImpGama
        LogPrinosi = []
        KoaNedela = PoDenISaatHistogrami[PrethodenMoment.weekday(), PrethodenMoment.hour, 0] + 1
        PoDenISaatHistogrami[PrethodenMoment.weekday(), PrethodenMoment.hour, KoaNedela] = Varijansa
        PoDenISaatHistogrami[PrethodenMoment.weekday(), PrethodenMoment.hour, 0] = KoaNedela
    PrethodenMoment = TekovenMoment    


#for k in range(4):
#    print(' nova nedela ')
#    for j in range(24):
#        print(' saat ', j)
#        ZaHistogram = []
#        for i in range(52):
#            if PoDenISaatHistogrami[k, j, i + 1] > 0:
#                ZaHistogram.append(PoDenISaatHistogrami[k, j, i + 1])
#        plt.hist(ZaHistogram)   
#        plt.show()     



for i in range(7):
    for j in range(24):
#        print('den', i, ' saat ', j, ' kolku podatoci ', KolkuPoDenISaat[i,j])
        if KolkuPoDenISaat[i, j] != 0:
            PoDenISaatVarijansa[i, j] = PoDenISaatVarijansa[i, j] /  KolkuPoDenISaat[i, j]
            PoDenISaatGama[i, j] = PoDenISaatGama[i, j] /  KolkuPoDenISaat[i, j]            

rezultati = []
PoDenISaatVarijansaMatrica = np.zeros((7, 24, 50))
MatricaNaAktivnost = np.zeros((120, 50))
for i in range(7):
    for j in range(24):
        if (i * 24 + j < 113): 
            greshki = str(i * 24 + j) 
            for k in range(50):            
                PoDenISaatVarijansaMatrica[i, j, k] = PoDenISaatHistogrami.item(i, j, k + 1)
                MatricaNaAktivnost[i * 24 + j, k] = PoDenISaatHistogrami.item(i, j, k + 1)                
#                print('den', i, ' saat ', j, ' nedela ', k, '  vred ', PoDenISaatVarijansaMatrica[i,j,k])
                greshki += '\t' + str(PoDenISaatVarijansaMatrica[i, j, k])
            greshki += '\n'   
            rezultati.append(greshki)
        if (i * 24 + j > 160):
            greshki = str(i * 24 + j - 48) 
            for k in range(50):            
                PoDenISaatVarijansaMatrica[i, j, k] = PoDenISaatHistogrami.item(i, j, k + 1)
                MatricaNaAktivnost[(i - 2) * 24 + j, k] = PoDenISaatHistogrami.item(i, j, k + 1)                
#                print('den', i, ' saat ', j, ' nedela ', k, '  vred ', PoDenISaatVarijansaMatrica[i,j,k])
                greshki += '\t' + str(PoDenISaatVarijansaMatrica[i, j, k])
            greshki += '\n'   
            rezultati.append(greshki)

print(MatricaNaAktivnost)
            
out_f = open('rezultati.csv', 'w')
w = csv.writer(out_f)
for l in rezultati:
    w.writerow(l.strip().split('\t'))
out_f.close()        

#ZgmechenaMatrica = np.zeros((168, 50))
#for i in range(7):
#    for j in range(24):
#        print(PoDenISaatVarijansaMatrica[i, j, :])
#        for k in range(50):
##            if not math.isnan(PoDenISaatVarijansaMatrica.item(i, j, k)):
#            ZgmechenaMatrica[i * 24 + j, k] = PoDenISaatVarijansaMatrica[i, j, k]    
##            if is_nan(ZgmechenaMatrica[i * 24 + j, k]):
##                ZgmechenaMatrica[i * 24 + j, k] = 0
##            print(' saat ', i * 24 + j, ' nedela ', k, ' vrednost ', ZgmechenaMatrica[24 * i + j, k])
#            
#np.nan_to_num(ZgmechenaMatrica)            
            
#for i in range(168):
#    for j in range(50):
##        if is_nan(ZgmechenaMatrica.item(i, j)):
##            ZgmechenaMatrica[i, j] = 0
#            print(' saat ', i, '   nedela ', j, ' vrednost ', ZgmechenaMatrica.item(i, j))


PoDen = np.reshape(MatricaNaAktivnost, (24, 250))

plt.plot(PCA.MeanOfData(PoDen))
plt.title('Ova e sredna aktivnost')
PCA.Crtki()
plt.show()

Obrabotena, Vrednosti, Vektori  = PCA.pca(PoDen)

print(Obrabotena)
print(Vektori)
print(PoDen.shape, Obrabotena.shape, Vektori.shape)



ObrPan = pd.DataFrame(np.real(Obrabotena))
VekPan = pd.DataFrame(np.real(Vektori))
MatPan = pd.DataFrame(np.real(PoDen))
MatPan.to_csv("GodishniPodatoci.csv")
VekPan.to_csv("PCAvektori.csv")
ObrPan.to_csv("PCAmatrica.csv")


#np.savetxt("GodishniPodatoci.csv", MatricaNaAktivnost, delimiter=",")
#np.savetxt("PCAvektori.csv", Vektori, delimiter=",")
#np.savetxt("PCAmatrica.csv", Obrabotena, delimiter=",")

#np.savetxt("NEPOMESobrabotena.csv", Obrabotena, delimiter=",")

#print(Vrednosti)
#print(Obrabotena[0])
#print(Obrabotena[1])
plt.plot(Obrabotena[0], 'r')
plt.plot(Obrabotena[1], 'g')
plt.plot(Obrabotena[2], 'b')
plt.plot(Obrabotena[3], 'm')
plt.plot(Obrabotena[4], 'k')
plt.title('Ova e matricata so PCA')
PCA.Crtki()
plt.show()

plt.plot(Vektori[0], 'r')
plt.plot(Vektori[1], 'g')
plt.plot(Vektori[2], 'b')
plt.plot(Vektori[3], 'm')
plt.plot(Vektori[4], 'k')
plt.title('Ova se glavnite vektori')
PCA.Crtki()
plt.show()


###########################################
# PCA Pomestena i Normirana

#Obrabotena, Vrednosti, Vektori  = PCA.pcaMeanAndNorm(MatricaNaAktivnost)
#
#plt.plot(Obrabotena[0])
#plt.show()
#plt.plot(Obrabotena[1])
#plt.show()
#
#np.savetxt("zgmechena.csv", MatricaNaAktivnost, delimiter=",")
#np.savetxt("obrabotena.csv", Obrabotena, delimiter=",")
#
##print(Vrednosti)
##print(Obrabotena[0])
##print(Obrabotena[1])
#plt.plot(Obrabotena[:, 0], 'r')
#plt.plot(Obrabotena[:, 1], 'g')
#plt.plot(Obrabotena[:, 2], 'b')
#plt.plot(Obrabotena[:, 3], 'm')
#plt.plot(Obrabotena[:, 4], 'k')
#plt.title('Ova e pomestena PCA')
#PCA.Crtki()
#plt.show()

###########################################







# od tuka e skinato

#            
#Denovi = []
#for i in range(7):
#    Den = []
#    for j in range(24):
#        Den.append(PoDenISaatVarijansa[i, j])
#    Denovi.append(Den)    
#    plt.plot(Denovi[i])
#    print('sredna za den ', i, ' ', np.mean(Denovi[i]))           
#plt.xlim(0, 30)    
#plt.legend(('Mon', 'Tue', 'Wed', 'Thu', 'Fri' ,'Sat', 'Sun'))
#plt.title(svd.naslov)    
#plt.show()    
#
#
#
#
#
#############################################
## site podatoci vo eden histogram
##
#PrethodenMoment = Vreminja[0]
#LogPrinosiSkalirani = []
#LogPrinosiObichni = []
##KolkuPodatoci = 1000
#for i in range(KolkuPodatoci - 2):
#    TekovenMoment = Vreminja[i + 1]
#    PominatoVreme = TekovenMoment - PrethodenMoment # vo minuti
#    if (TekovenMoment.date() == PrethodenMoment.date()) and (TekovenMoment.hour != PrethodenMoment.hour):
##        LogPrinosi.append(np.log(OpenPrice[i + 1]) - np.log(OpenPrice[i]))        
#        StandGreshka = 0.5 * (np.sqrt(PoDenISaatVarijansa[PrethodenMoment.weekday(), PrethodenMoment.hour]) + np.sqrt(PoDenISaatVarijansa[TekovenMoment.weekday(), TekovenMoment.hour]))        
#        LogPrinosiSkalirani.append((np.log(OpenPrice[i + 1]) - np.log(OpenPrice[i])) / (np.sqrt(PominatoVreme.total_seconds() / 60) * StandGreshka))               
#    elif (TekovenMoment.date() == PrethodenMoment.date()) and (TekovenMoment.hour == PrethodenMoment.hour):
#        StandGreshka = np.sqrt(PoDenISaatVarijansa[PrethodenMoment.weekday(), PrethodenMoment.hour])
#        LogPrinosiSkalirani.append((np.log(OpenPrice[i + 1]) - np.log(OpenPrice[i])) / (np.sqrt(PominatoVreme.total_seconds() / 60) * StandGreshka))               
#    LogPrinosiObichni.append((np.log(OpenPrice[i + 1]) - np.log(OpenPrice[i])) / (np.sqrt(PominatoVreme.total_seconds() / 60)))                       
#    PrethodenMoment = TekovenMoment    
#
#
#
#num_bins = 100
##counts, bin_edges = np.histogram (LogPrinosi, bins=num_bins, normed=True)
##cdf = np.cumsum(counts)
##plt.plot (bin_edges[1:], cdf/cdf[-1])
##plt.show()
##
##plt.hist(LogPrinosi, bins = num_bins, histtype = 'stepfilled')
##plt.show()
#
#
#print(' voa treba da e arno ')
##Najgolem = max(LogPrinosi)
##Najmal = min(LogPrinosi)
##print(Najgolem, '   ', Najmal)
#
#PozitivniLog = []
#opashka = []
#for i in range(len(LogPrinosiSkalirani)):
#    if LogPrinosiSkalirani[i] > 0:
#        PozitivniLog.append(LogPrinosiSkalirani[i])
#    if LogPrinosiSkalirani[i] > 0.03:
#        opashka.append(LogPrinosiSkalirani[i])    
#        
#        
#Najgolem = max(PozitivniLog)
#KrajnaTochka = np.log10(Najgolem)    
#
#granici = np.logspace(KrajnaTochka - 2.0, KrajnaTochka, num = 100)
##print(granici)
#
#plt.hist(PozitivniLog, bins = granici, log = True)
#plt.show()
#
#
#
#
#
#n, bins, patches = plt.hist(PozitivniLog, bins = granici)
#print(' kolku brojki ', len(n), ' kade se brojkite ', len(bins))
#xniza = []
#for i in range(len(bins) - 1):
#    xniza.append(0.5 * (bins[i] + bins[i + 1]))
#
#plt.plot(xniza, n, 'ro')
#plt.xscale('log')
#plt.yscale('log')        
#plt.show()
#
#samostepenX = []
#samostepenY = []
#for i in range(len(xniza)):
#    if xniza[i] > 0.03:
#        samostepenX.append(xniza[i])
#        samostepenY.append(n[i])
#print('crtam samo stepen ')
#plt.plot(samostepenX, samostepenY, 'ro')
#plt.xscale('log')
#plt.yscale('log')        
#plt.show()
#
#fit = powerlaw.Fit(opashka)
#print('  stepen na opashka ', fit.power_law.alpha)
#
#
#PozitivniLogObichni = []
#for i in range(len(LogPrinosiObichni)):
#    if LogPrinosiObichni[i] > 0:
#        PozitivniLogObichni.append(LogPrinosiObichni[i])
#        
#Najgolem = max(PozitivniLogObichni)
#KrajnaTochka = np.log10(Najgolem)    
#
#granici = np.logspace(KrajnaTochka - 2.0, KrajnaTochka, num = 100)
#
#n, bins, patches = plt.hist(PozitivniLogObichni, bins = granici)
#print(' kolku brojki ', len(n), ' kade se brojkite ', len(bins))
#xniza = []
#for i in range(len(bins) - 1):
#    xniza.append(0.5 * (bins[i] + bins[i + 1]))
#
#plt.plot(xniza, n, 'ro')
#plt.xscale('log')
#plt.yscale('log')        
#plt.show()
#
#
## site podatoci vo eden histogram
#############################################
#
#
######################### 
## Implicirani gami
#
#ImpGama = op.ImpliedGamma(LogPrinosiSkalirani)
#GoleminaNaPaket = 24 * 60
#print(' na den')
#Brojach = 0
#Paket = []
#GamaPrimerok = []
#GamaTochno = []
#for i in range(len(LogPrinosiSkalirani)):
#    Paket.append(LogPrinosiSkalirani[i])
#    Brojach += 1
#    if Brojach > GoleminaNaPaket:
#        GamaPrimerok.append(op.ImpliedGamma(Paket))
#        GamaTochno.append(ImpGama)
#        Brojach = 0
#        Paket = []
#
#print(np.std(GamaPrimerok, ddof = 1))
#
#plt.plot(GamaPrimerok, 'ro')
#plt.plot(GamaTochno, 'g^')
#plt.show()        
#        
#        
#GoleminaNaPaket = 5 * 24 * 60
#print(' na nedela ')
#Brojach = 0
#Paket = []
#GamaPrimerok = []
#GamaTochno = []
#for i in range(len(LogPrinosiSkalirani)):
#    Paket.append(LogPrinosiSkalirani[i])
#    Brojach += 1
#    if Brojach > GoleminaNaPaket:
#        GamaPrimerok.append(op.ImpliedGamma(Paket))
#        GamaTochno.append(ImpGama)
#        Brojach = 0
#        Paket = []
#
#print(np.std(GamaPrimerok, ddof = 1))
#
#plt.plot(GamaPrimerok, 'ro')
#plt.plot(GamaTochno, 'g^')
#plt.show()        
#
#GoleminaNaPaket = 20 * 24 * 60
#print(' na mesec ')
#Brojach = 0
#Paket = []
#GamaPrimerok = []
#GamaTochno = []
#for i in range(len(LogPrinosiSkalirani)):
#    Paket.append(LogPrinosiSkalirani[i])
#    Brojach += 1
#    if Brojach > GoleminaNaPaket:
#        GamaPrimerok.append(op.ImpliedGamma(Paket))
#        GamaTochno.append(ImpGama)
#        Brojach = 0
#        Paket = []
#
#print(np.std(GamaPrimerok, ddof = 1))
#
#plt.plot(GamaPrimerok, 'ro')
#plt.plot(GamaTochno, 'g^')
#plt.show()        
#
# 
# 
#
######################### 
#
#
##########################################
#
############
##   ova e za paketi so ista golemina
#
##GoleminaNaPaket = 60
##ImpliciraniGami = []
##Varijansi = []
##paketi = KolkuPodatoci // GoleminaNaPaket
##for i in range(paketi):
##    Paket = []
##    for j in range(GoleminaNaPaket):
##        Paket.append(LogPrinosi[GoleminaNaPaket * i + j])
##    Varijansa = np.std(Paket, ddof = 1)
##    Varijansi.append(Varijansa)
##    ImpGama = op.ImpliedGamma(Paket)
##    ImpliciraniGami.append(ImpGama)
###    print(ImpGama, '   ', Varijansa)    
#    
#    
############
##   ova e za podatoci po den
#    
#    
##ImpliciraniGami = []
##Varijansi = []
##brojach = 0
##GoleminaNaPaket = 60
##while brojach < KolkuPodatoci:
##    Den = Vreminja[brojach].date()
##    DnevenPaket = []
##    while Den == Vreminja[brojach].date():
##        DnevenPaket.append(LogPrinosi[brojach])
##        brojach = brojach + 1
##    paketi = len(DnevenPaket) // GoleminaNaPaket 
##    ImpliciraniGami = []
##    Varijansi = []       
##    for i in range(paketi):
##        Paket = []
##        j = 0
##        while (GoleminaNaPaket * i + j) < len(DnevenPaket) and (j < GoleminaNaPaket):
##            Paket.append(DnevenPaket[GoleminaNaPaket * i + j])
##            j = j + 1
##        Varijansa = np.std(Paket, ddof = 1)
##        Varijansi.append(Varijansa)
##        ImpGama = op.ImpliedGamma(Paket)
##        ImpliciraniGami.append(ImpGama)
##    plt.subplot(2,1,1)
##    plt.plot(ImpliciraniGami)
##    plt.subplot(2,1,2)
##    plt.plot(Varijansi)
##    plt.xlabel(Den)
##    plt.show()
##    
#
##plt.subplot(4,1,1)
##plt.plot(Vreminja)
##plt.subplot(4,1,2)
##plt.plot(OpenPrice)
##plt.subplot(4,1,3)
##plt.plot(ImpliciraniGami)
##plt.subplot(4,1,4)
##plt.plot(Varijansi)
##plt.show()
#
##den = datetime.date(2018, 6, 27)
##
##for i in range(14):
##    plt.plot(Vreminja, OpenPrice)
##    plt.axis([datetime.datetime.combine(den + datetime.timedelta(days = i), datetime.time(15, 30, 0)), datetime.datetime.combine(den + datetime.timedelta(days = i), datetime.time(22,0, 0)), 130, 150])
##    plt.xlabel(den + datetime.timedelta(days = i))
##    plt.show()
##
#
#
##plt.set_ylim([0, 5])
#
#
############################
## ova e test za Gausova i Studentova
##mu = 0
##sigma = 1
##Povtoruvanja = 1000
##BrojkiVoPrimerok = 1000
##Varijansa = np.zeros(Povtoruvanja)
##for i in range(Povtoruvanja):
##    for j in range(1):
##        Sluchajni = np.random.normal(mu, sigma, BrojkiVoPrimerok)
##        Sredna = np.mean(Sluchajni)
##        Vari = np.std(Sluchajni, ddof = 1)
###        count, bins, ignored = plt.hist(Sluchajni, 30, normed=True)
###        plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
###        print(Sredna,'     ', Vari)
##        Varijansa[i] = Vari
##plt.hist(Varijansa,20)
##
##
##Povtoruvanja = 20
##BrojkiVoPrimerok = 100
##Varijansa = np.zeros(Povtoruvanja)
##for i in range(Povtoruvanja):
##    for j in range(1):
##        Sluchajni = np.random.standard_t(3, BrojkiVoPrimerok)
##        Sredna = np.mean(Sluchajni)
##        Vari = np.std(Sluchajni, ddof = 1)
##        ImpGama = op.ImpliedGamma(Sluchajni)
###        count, bins, ignored = plt.hist(Sluchajni, 30, normed=True)
###        plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
##        print(np.abs(Vari - np.sqrt(3.0)) / np.abs(ImpGama - np.sqrt(3.0)))
##        Varijansa[i] = Vari
##plt.hist(Varijansa,40)
##
#
# 
## voa kje mi trebe. Da go vidam
##   https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.random.normal.html
#
