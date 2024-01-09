import scipy as sp
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import statistics as st
import uncertainties as un
from uncertainties import ufloat
from uncertainties.umath import *
from decimal import *
#------------------------------------------------------------------------
#------------------------------------------------------------------------

def FindLocalExtremes(arr2, arr): 
    if len(arr) != len(arr2):
        print("Error: list lengths do not match!")
        return
    if len(arr) <3:
        print("Error: List is too short")
    
    n = len(arr)
    mx = [] 
    mn = [] 
    #First point
    if(arr[0] > arr[1]): 
        mx.append((arr2[0], arr[0])) 
    elif(arr[0] < arr[1]): 
        mn.append((arr2[0], arr[0]))
    #Last point
    if(arr[-1] > arr[-2]): 
        mx.append((arr2[n-1], arr[n-1])) 
    elif(arr[-1] < arr[-2]): 
        mn.append((arr2[n-1], arr[n-1])) 
    #All inside points
    for i in range(1, n-1): 
        if(arr[i-1] > arr[i] < arr[i + 1]): 
            mn.append((arr2[i],arr[i])) 
        elif(arr[i-1] < arr[i] > arr[i + 1]): 
            mx.append((arr2[i],arr[i]))
    return (mx,mn)

#------------------------------------------------------------------------
def mprint(matrix):
    s = [[str(e) for e in row] for row in matrix]
    lens = [max(map(len, col)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print ('\n'.join(table))
    print()
    
#------------------------------------------------------------------------
def cfit(func, x_data, y_data, s=None, p0=None):
    tl = len(x_data)
    if len(s) != len(set(s)):
        print("Varable name is duplicated!")
        pass
    
    for i in range(len(s)):
        s[i] = str(s[i]).replace(" ","")
        
    if s == None:
        s = []
    if tl != len(y_data):
        print("Data lists are not of equal length!")
        pass
    elif tl <= 2:
        print("Data lists do not contain enough data points!")
        pass
    
    def y_compile():
        global cfit_n
        global y_model_compile
        y_model_compile = ""
        y_model_compile = "x_model,"
        for i in cfit_n:
            if i != list(cfit_n)[-1]:
                y_model_compile += str(i + ",")
            else:
                y_model_compile += str(i)
        return y_model_compile

        
    globals()["cfit_n"] = dict()
    globals()["y_model_compile"] = ""
    globals()["cfit_list"] = []
    global cfit_n
    global y_model_compile
    x_data = np.asarray(x_data)
    y_data = np.asarray(y_data)

    par, cov = curve_fit((func), x_data, y_data, p0)
    if len(s) != len(par):
        for i in range(1,len(par)+1):
            s.append(i)
    
    for i in range(len(par)):
        globals()[f"fit_{s[i]}"] = float(par[i])
        cfit_n[f"fit_{s[i]}"] = float(par[i])
        cfit_list = float(par[i])



    x_model = np.linspace(min(x_data),max(x_data),100)
    y_model_compile = y_compile()
    y_model = eval( f"func("+ y_model_compile +")" )

    plt.plot(x_data, y_data, "o", label="data")
    plt.plot(x_model, y_model, "-", label="fit")
    plt.legend()
    print("\n-| Fit values |----------------------------------------\n" )
    for i in cfit_n:
        print(str(i) + " : "+ str(cfit_n[i]))
    print("\n-| Parameter standard deviation values |---------------\n" )
    m = np.sqrt(np.diag(cov))
    for i in range(len(m)):
        print(list(cfit_n.keys())[i] + " stdev (1 sigma) : " + str(m[i]))

    print("\n-| Graph |---------------------------------------------\n" )
    plt.show()

#------------------------------------------------------------------------

def DataToFloat(l, tag):
    if not isinstance(l, list):
        print("Error, first input isn't a list!")
        return
    elif not isinstance(tag,str):
        print("Error, second input isn't a string!")
        return
    elif isinstance(l,list) and isinstance(tag,str):
        for i in range(len(l)):
            if not ( isinstance(l[i], int) or isinstance(l[i], float)):
                print("Error, list contains non-numerical objects!")
                return
        return ufloat(st.mean(l), st.stdev(l)/sqrt(len(l)), tag)
    
#------------------------------------------------------------------------

def ErrorCalc(func, var, latex_print=False):
    rezultat = func()
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Pripravi seznam vseh ufloat-ov potrebnih za konstrukcijo matrik
    seznam = []
    for i in var:
        seznam = seznam + [var[i]]
    seznam = seznam + [rezultat]

    # Konstruira matrike
    array_cov = un.covariance_matrix(seznam)
    array_cor = un.correlation_matrix(seznam)

    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Izpis rezultatov programa

    print("----------------------------------------------------------------------------------------------------------------------------------------\nVhodni podatki : \n")
    for i in var:
        print(repr(var[i]))
    print("----------------------------------------------------------------------------------------------------------------------------------------\nObčutljivostni koeficient : \n")
    for i in var:
        print(i + " : " + str(abs(rezultat.derivatives[var[i]])))
    print("----------------------------------------------------------------------------------------------------------------------------------------\nPrispevek negotovosti : \n")
    for (var, error) in rezultat.error_components().items():
        print( "{}: {}".format(var.tag, error))
    print("----------------------------------------------------------------------------------------------------------------------------------------\nmatrike se zapišejo v isti vrsti kot spremenljivke v 'dictionary'-ju torej prvi stolpec predstavlja prvo zapisano vrednost kakor tudi prva vrstica predstavlja prvo zapisano vrednost.\n----------------------------------------------------------------------------------------------------------------------------------------\nCorrelation matrix : \n")
    matrix_print(array_cor)
    print("----------------------------------------------------------------------------------------------------------------------------------------\nCovariance matrix : \n")
    matrix_print(array_cov)
    print("----------------------------------------------------------------------------------------------------------------------------------------\nRezultat : " + str(repr(rezultat)) + "\n" + "95% prepričanost : " + str(rezultat.s*2) + "\n\n\n") 
    if latex_print:
        print("---LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print---\n----------------------------------------------------------------------------------------------------------------------------------------\nVhodni podatki : \n")
        for i in var:
            print(repr("{:L}".format(var[i])))
        print("----------------------------------------------------------------------------------------------------------------------------------------\nRezultat : " + str("{:L}".format(rezultat)) + "\n\n---LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print-LaTeX print---")
