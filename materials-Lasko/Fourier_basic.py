#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 11:20:51 2020

@author: Lasko
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack as furie


pochetok = -10
kraj = 10
BrPrimeroci = 64
PolovinaBrPrim = BrPrimeroci / 2
vreme = np.linspace(pochetok, kraj, BrPrimeroci)

# Dirakov impuls
Dirak = np.zeros(BrPrimeroci)
Dirak[PolovinaBrPrim] = 1

# Skok funkcija
Skok = np.zeros(BrPrimeroci)
Skok[PolovinaBrPrim:] = 1


# Sinusoida
Omega0 = 2
Sinusna = np.sin(vreme * Omega0)

# Eksponencijalna funkcija koja pochnuva vo 0

SechenaEksp = np.exp(-vreme) * Skok

# crtaj skok funkcija
plt.plot(vreme, Skok)
plt.xlabel(' n ')
plt.ylabel(' x[n] ')

# najdi FFT  na Dirakov impuls
FurDirak = furie.fft(Dirak)
frekvencii = np.linspace(-np.pi, np.pi, BrPrimeroci)

# crtaj spektar na Dirakov impuls
plt.figure()
plt.plot(frekvencii, abs(FurDirak))
plt.xlabel(' k ')
plt.ylabel(' X[k] ')

# crtaj sinusna funkcija
plt.figure()
plt.plot(vreme, Sinusna)
plt.xlabel(' n ')
plt.ylabel(' x[n] ')

# crtaj spektar na sinusna funkcija
plt.figure()
plt.stem(frekvencii, abs(furie.fftshift(furie.fft(Sinusna))))
plt.xlabel(' k ')
plt.ylabel(' X[k] ')


# crtaj sechena ekspon.
plt.figure()
plt.plot(vreme, SechenaEksp)
plt.xlabel(' n ')
plt.ylabel(' x[n] ')

# crtaj spektar na sechena eksp. funkcija
plt.figure()
plt.stem(frekvencii, abs(furie.fftshift(furie.fft(SechenaEksp))))
plt.xlabel(' k ')
plt.ylabel(' X[k] ')
