import pandas as pd
import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import pyromat as pyro
from prettytable import ALL

tabelaA3 = pd.read_csv("termo.csv", sep = ' ')

P2 = 30
P4 = 3
P2 = P2/100
P4 = P4*10
P1 = P4
P3 = P2

h1 = float(tabelaA3.loc[tabelaA3.PRESSAO == P1,'ENTALPV'])
s1 = float(tabelaA3.loc[tabelaA3.PRESSAO == P1,'ENTROPV'])
T1 = float(tabelaA3.loc[tabelaA3.PRESSAO == P1,'TEMPERATURA'])
hL = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTALPL'])
hV = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTALPV'])
sL = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTROPL'])
sV = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTROPV'])
h3 = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTALPL'])
v3 = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'VESPL'])/1000
T2 = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'TEMPERATURA'])
s3 = float(tabelaA3.loc[tabelaA3.PRESSAO == P3,'ENTROPL'])
T4l = float(tabelaA3.loc[tabelaA3.PRESSAO == P4,'TEMPERATURA'])
s4l = float(tabelaA3.loc[tabelaA3.PRESSAO == P4,'ENTROPL'])
s4 = s3
s2 = s1
agua = pyro.get('mp.H2O')
T4 = agua.T_s(p=P4,s=s3)
T4 = T4[0]-273.16
T3 = T2

f1 = plt.figure(1)
ax1 = f1.add_subplot(111)
ax1.set_xlabel('Entropia, s (kJ/kg/K)')
ax1.set_ylabel('Temperatura, T (°C)')
ax1.set_title('Diagrama T-s: Ciclo de Rankine')
cor = 'r'
# Generando a curva: 
Tt,pt = agua.triple()
Tc,pc = agua.critical()
T = np.arange(Tt,Tc,0.1)
sL,sV = agua.ss(T=T)
ax1.plot(sL,T-273.16,'k')
ax1.plot(sV,T-273.16,'k')

# Processo 1-2: 
T = np.array([T1,T2])
s = np.array([s1,s2])
ax1.plot(s,T,cor,linewidth=1.5)

# Processo 2-3: 
T = np.array([T2,T3])
s = np.array([s2,s3])
ax1.plot(s,T,cor,linewidth=1.5)

# Processo 3-4: 
T = np.array([T3,T4+50])
s = np.array([s3,s4])
ax1.plot(s,T,cor,linewidth=1.5)

# Processo 4-4l: 
T = np.array([T4+50,T4l])
s = np.array([s4,s4l])
ax1.plot(s,T,cor,linewidth=1.5)

# Processo 4l-1: 
T = np.array([T4l,T1])
s = np.array([s4l,s1])
ax1.plot(s,T,cor,linewidth=1.5)

# Add some labels
show_text = True
if show_text:
    ax1.text(s1,T1,
    """(1) 
T={0:.1f}°C
s={1:.3f}kJ/kg/K
""".format(float(T1),float(s1)))
    ax1.text(s2+0.3,T2,
    """(2) 
T={0:.1f}°C
s={1:.3f}kJ/kg/K
""".format(float(T2),float(s2)))
    ax1.text(s3+0.7,T3+5,
    """(3) 
T={0:.1f}°C
s={1:.3f}kJ/kg/K""".format(float(T3),float(s3)))
    ax1.text(s4-1,T4+80,
    """(4) 
T={0:.1f}°C
s={1:.3f}kJ/kg/K""".format(float(T4),float(s4)))
    ax1.text(s4l-2.5,T4l+10,
    """(4') 
T={0:.1f}°C
s={1:.3f}kJ/kg/K""".format(float(T4l),float(s4l)))

plt.show()