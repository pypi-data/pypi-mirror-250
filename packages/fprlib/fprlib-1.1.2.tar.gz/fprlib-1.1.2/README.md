# Inštalacija (za Windows)

- odpreš CMD
- vtipkaš : pip install fprlib
- v .py datoteko vpišeš : import fprlib as fp

# Seznam ukazov

- cfit : uporabno za fitanje krivulj
- mprint : uporabno za printanje matrik

# Primer uporabe funkcije cfit

```Python
import fprlib #as fp
import numpy as np

x_data = [-6.62934E-1,-6.36725E-1,-6.12907E-1,-5.99908E-1,-5.93818E-1,-5.86678E-1,-5.82887E-1,-5.77581E-1,-5.73450E-1,-5.71544E-1,-5.69519E-1,-5.67124E-1,-5.64384E-1,-5.60124E-1,-5.57659E-1,-5.55432E-1,-5.53430E-1,-5.51513E-1,-5.49471E-1,-5.47633E-1,-5.45375E-1,-5.43347E-1,-5.41005E-1,-5.38391E-1,-5.36362E-1,-5.33630E-1,-5.29340E-1,-5.22832E-1,-5.14236E-1,-5.09088E-1,-4.96033E-1,-4.82724E-1,-4.28678E-1,+1.08242E+0,+1.87425E+0,+3.86342E+0,+4.79353E+0,+6.52731E+0,+7.85109E+0,+8.31908E+0,+8.98060E+0,+1.02541E+1,+1.04246E+1,+1.04806E+1]
y_data = [-1.54238E+1,-8.77151E+0,-4.78847E+0,-3.18064E+0,-2.56410E+0,-1.94406E+0,-1.65661E+0,-1.29949E+0,-1.05447E+0,-9.50160E-1,-8.45721E-1,-7.30154E-1,-6.07445E-1,-4.35915E-1,-3.46365E-1,-2.71186E-1,-2.08004E-1,-1.51217E-1,-9.44567E-2,-4.64407E-2,+8.65516E-3,+5.47404E-2,+1.04184E-1,+1.54969E-1,+1.91395E-1,+2.36552E-1,+2.99386E-1,+3.78305E-1,+4.58030E-1,+4.95166E-1,+5.63105E-1,+6.05569E-1,+6.62091E-1,+6.70630E-1,+6.71116E-1,+6.71733E-1,+6.71947E-1,+6.72297E-1,+6.72552E-1,+6.72637E-1,+6.72751E-1,+6.72968E-1,+6.72991E-1,+6.73010E-1]
sez = ["a","b","c"]
p = [-1,-10,1]

def funkcija(x, dol, sir, c):
    return dol*np.exp(sir*x)+c

fprlib.cfit(funkcija, x_data, y_data,sez,p)
```

# Razlaga ***CFIT***

> ## fprlib.cfit(\<funkcija\>, \<X podatki\>, \<Y podatki\>, \<imena spremenljivk\>=None, \<začetne vrednosti\>=None)

### Obvezne spemenljivke:

1. \<funkcija\> : Vstavi funkcijo oziroma njeno "ime" ampak ***obvezno brez citatov!***
2. \<x podatki\> : Vstavi seznam X koordinat meritev.
3. \<y podatki\> : Vstavi seznam Y koordinat meritev.

### Neobvezne spremeljike:

1. \<imena spremenljivk\> : Seznam imen spremenljivk v funkciji, v primeru da seznam ni podan, bodo spremenljivke oštevilčene.
2. \<začetne vrednosti\> : Seznam začetnih vrednosti, ki jih uporabi program za oceno. ***Sicer neobvezno, se lahko pokaže, da program vrne slab fit, če niso začetne vrednosti dobro uganjene!***

## Funkcija:

Da bi naš program lahko karkoli računal moramo predpisati fizikalno funkcijo, za katero menimo, da lepo opiše pojav. Opmnimo, da so imena spremenljivk poljubna, vendar če se nekje uporabi spremenljivka z istim imenom, posledično pomeni, da ti dve vrednosti morata biti enaki:

> def \<funkcija\>(x, a, b, c, d)
>    
>‎return f(x,a,b,c,d)

nato moramo definirati podatke za x in y v obliki *python seznama (list-a)*.
Dodatno lahko definiramo še imena spremenljivk v seznamu, npr.:

> sez = ["prva spremenljivka" , "druga_spremeljivka", "tretja spremenljivka", "karkoli_kakorkoli", 1 ]

***Opomba*** : določeni znaki niso dovoljeni. Npr.: "-".

***Opomba*** : knjižnica avtomatično umakne presledke iz vseh besedil, seveda pa prej vse pretvori v besedila, kakor preveri če je ime spremenljivke podvojeno!

ter definiramo seznam začetnih vrednosti npr.:

> p = [ 1 , 2 , 3 , 4.231E-3 ]

***Opomba*** : na prvem mestu v seznamih "sez" in "p" mora biti ime oz. začetna vrednost, ki odgovarja spremenljivki "a" iz formule, ter na drugem mestu teh seznamov vrednosti, ki pripadajo spremenljivki "b" iz formule.

# Primer ampak prilagojen razlagi

```python
sez = ["prva spremenljivka" , "druga_spremeljivka", "tretja spremenljivka", "karkoli_kakorkoli", 1 ]
p = [-1,-10,1,0]

def funkcija(x, a, b, c, d):
    return a*np.exp(b*x+d)+c

fprlib.cfit(funkcija, x_data, y_data,sez,p)
```

> -| Fit values |----------------------------------------
>
>fit_prvaspremenljivka : -5.099442181457673e-06
> 
>fit_druga_spremeljivka : -23.779394915909464
> 
>fit_tretjaspremenljivka : 0.8452948803956754
> 
>fit_karkoli_kakorkoli : -0.7635025821425597
>
>
>
>-| Parameter standard deviation values |---------------
>
>
>
>fit_prvaspremenljivka stdev (1 sigma) : 8.648790074428476
> 
>fit_druga_spremeljivka stdev (1 sigma) : 0.45025382355777877
> 
>fit_tretjaspremenljivka stdev (1 sigma) : 0.054671981396874514
> 
>fit_karkoli_kakorkoli stdev (1 sigma) : 1696026.9841948354
> 
>
> 
>-| Graph |---------------------------------------------
