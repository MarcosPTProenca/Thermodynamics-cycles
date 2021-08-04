import pandas as pd
import numpy as np
from prettytable import PrettyTable
import matplotlib.pyplot as plt
import pyromat as pyro
from prettytable import ALL

tabelaA3 = pd.read_csv("termo.csv", sep = ' ')

Pmax = tabelaA3.loc[tabelaA3['PRESSAO']== tabelaA3['PRESSAO'].max()]
Pmax = float(Pmax['PRESSAO'])
Pmin = tabelaA3.loc[tabelaA3['PRESSAO']== tabelaA3['PRESSAO'].min()]
Pmin = float(Pmin['PRESSAO'])
while True:
    P2 = input("Informe a pressão P2 em kPa: ")
    if P2.isnumeric():
        P2 = float(P2)
        break
    else:
        continue
while P2 > Pmax or P2 < Pmin:
    P2 = float(input("Informe a pressão P2 em kPa: "))
P2 = P2/100
while P2 > Pmax or P2 < Pmin:
    P2 = float(input("Informe a pressão P2 em kPa: "))
    P2 = P2/100
while True:
    P4 = input("Informe a pressão P4 em MPa: ")
    if P4.isnumeric():
        P4 = float(P4)
        break
    else:
        continue
while P4 > Pmax or P4 < Pmin:
    P4 = float(input("Informe a pressão P4 em MPa: "))
P4 = P4*10
while P4 > Pmax or P4 < Pmin:
    P4 = float(input("Informe a pressão P4 em MPa: "))
    P4 = P4*10
print()
def interpo(x,y):
    aux1,aux2 = tabelaA3.loc[(tabelaA3['PRESSAO']-x).abs().argsort()[:2],y]
    aux3,aux4 = tabelaA3.loc[(tabelaA3['PRESSAO']-x).abs().argsort()[:2],'PRESSAO']
    z = aux1 + (aux2-aux1)*(x-aux3)/(aux4-aux3)
    return z
def verifTab(P):
    if P in tabelaA3.PRESSAO.values:
        return True
    else:
        return False
#Convertendo as Ps para bar
P1 = P4
P3 = P2
P4_aux = P4*10**5
P3_aux = P3*10**5
#definicao variaveis:
if verifTab(P1) == False:
    h1 = interpo(P1,'ENTALPV')
    s1 = interpo(P1,'ENTROPV')
    T1 = interpo(P1,'TEMPERATURA')
else:   
    h1 = float(tabelaA3.loc[tabelaA3.PRESSAO == P1,'ENTALPV'])
    s1 = float(tabelaA3.loc[tabelaA3.PRESSAO == P1,'ENTROPV'])
    T1 = float(tabelaA3.loc[tabelaA3.PRESSAO == P1,'TEMPERATURA'])
if verifTab(P2) == False:
    hL = interpo(P2,'ENTALPL')
    hV = interpo(P2,'ENTALPV')
    sL = interpo(P2,'ENTROPL')
    sV = interpo(P2,'ENTROPV')
    h3 = interpo(P2,'ENTALPL')
    v3 = interpo(P2,'VESPL')/1000
    T2 = interpo(P2,'TEMPERATURA')
else:
    hL = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTALPL'])
    hV = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTALPV'])
    sL = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTROPL'])
    sV = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTROPV'])
    h3 = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTALPL'])
    v3 = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'VESPL'])/1000
    T2 = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'TEMPERATURA'])
if verifTab(P3) == False:
    s3 = interpo(P3,'ENTROPL')
else:
    s3 = float(tabelaA3.loc[tabelaA3.PRESSAO == P3,'ENTROPL'])
if verifTab(P4) == False:
    T4l = interpo(P4,'TEMPERATURA')
    s4l = interpo(P4,'ENTROPL')
else:
    T4l = float(tabelaA3.loc[tabelaA3.PRESSAO == P4,'TEMPERATURA'])
    s4l = float(tabelaA3.loc[tabelaA3.PRESSAO == P4,'ENTROPL'])
s4 = s3
s2 = s1
#Encontrando T4
agua = pyro.get('mp.H2O')
T4 = agua.T_s(p=P4,s=s3)
T4 = T4[0]-273.16
T3 = T2
def desenhesqRank(P4,P2):
    print()
    print("\t\t\t\t     | qH")
    print("       (4)\t\t     V\t\t    (1)")
    if P4/10 >= 10:
        print(f"   P4 = {P4/10} Mpa +--------+\tx1 = 1,0")
    else:
        print(f"   P4 = {P4/10} Mpa\t +--------+\tx1 = 1,0")
    print("   +------>------|CALDEIRA|------->-------+")
    print("   ↑   \t\t\t +--------+ \t\t\t  ↓")
    print("   |      \t\t\t\t\t\t\t\t  |")
    print("+-----+\t\t\t\t\t\t\t      +-------+")
    print("|BOMBA|\t\t\t\t\t\t\t      |TURBINA|")
    print("+-----+\t\t\t\t\t\t\t      +-------+")
    print("   |      \t\t\t\t\t\t\t\t  |")
    print("   ↑\t\t\t+-----------+ \t\t\t  ↓")
    print("   +------<-----|CONDENSADOR|------<------+")
    print("          (3)  \t+-----------+\t   (2)")
    print(f"\t\tx3 = 0        | qL     P2 = {P2*100} Kpa, x2 = ?")
    print("\t\t\t\t      V")
    print()
    
def relatorioRank(P1,P2,P4,s1,h1,hL,hV,sL,sV,s2,v3,P4_aux,P3_aux):
    print("Desenho esquemático: Ciclo de Rankine")
    desenhesqRank(P4,P2)
    print('Lista de considerações:')
    print()
    print("* Fluido de trabalho: água")
    print("* Cada componente do ciclo é avaliado como volume de controle")
    print("* Regime permanente")
    print("* A turbina e a bomba operam adiabaticamente")
    print("* A caldeira e o condensador operam à pressão constante")
    print("* Variações de Ec e Ep são desprezíveis")
    print("* Não há trabalho na caldeira e no condensador")
    print("* Processos internamente reversíveis")
    print()
    print('1) Turbina(processo 1->2): expansão adiabática -> isentrópica')
    print()
    print("1ª Lei da Termodinâmica: wt = h1 - h2")
    print("2ª Lei da Termodinâmica: s1 = s2")
    print()
    print(f"* Estado 1: vapor saturado; x1 = 1,0; P1 = {P1/10} Mpa ({P1} bar)")
    print()
    print(f"Tabela A-3 ({P1} bar): h1 = {h1} kJ/kg \t s1 = {s1} kJ/kg*K")
    print()
    print(f"* Estado 2: mistura bifásica; x2 = ?; P2 = {P2*100} Kpa ({P2} bar)")
    print()
    print("-> Encontrando x2:")
    print(f"s2 = s1 = {s1} kJ/kg*K")
    print(f"Tabela A-3 ({P2} bar): hL = {hL} kJ/kg \t sL = {sL} kJ/kg*K")
    print(f"                      hV = {hV} kJ/kg \t sV = {sV} kJ/kg*K")
    print("s2 = sL +x2*(sV-sL) -> x2 = (s2-sL)/(sV-sL)")
    print(f"x2 = ({s2} - {sL})kJ/kg*K/({sV} - {sL})kJ/kg*K")
    x2 = (s1-sL)/(sV-sL)
    print(f'x2 = {x2:.4f}')
    print()
    print("-> Encontrando h2:")
    print(f"h2 = hL + x2*(hV - hL) -> h2 = {hL} kJ/kg + {x2:.4f}*({hV} - {hL}) kJ/kg")
    h2 = hL + x2*(hV-hL)
    print(f'h2 = {h2:.4f} kJ/kg')
    print()
    print("-> Calculando wt:")
    wt = h1-h2
    print(f"wt = h1 - h2 -> wt = {h1:.4f} kJ/kg - {h2:.4f} kJ/kg")
    trac1 = PrettyTable([f"wt = {wt:.4f} kJ/kg"])
    trac1.padding_width = 1
    trac1.hrules = ALL
    print(trac1)
    print("O sinal do trabalho na turbina é positivo, pois \nela realiza trabalho (sai energia do sistema).")
    print()
    print('2) Condensador(processo 2->3): rejeição de calor à P cte')
    print()
    print("1ª Lei da Termodinâmica: qL = h2 - h3")
    print(f"* Estado 3: líquido saturado; x3 = 0; P3 = {P2*100} Kpa ({P2} bar)")
    print()
    print(f"Tabela A-3 ({P3} bar): h3 = {h3} kJ/kg \t v3 = {v3} m3/kg")
    print()
    print("-> Calculando qL:")
    qL = h3-h2
    print(f"qL = h3 - h2 -> qL = {h3} kJ/kg - {h2:.2f} kJ/kg")
    trac2 = PrettyTable([f"qL = {qL:.4f} kJ/kg"])
    trac2.padding_width = 1
    trac2.hrules = ALL
    print(trac2)
    print("O sinal do calor no condensador é negativo, pois\no calor sai do sistema (diminui energia do sistema)\numa vez que o vapor se encontra em um estado energético")
    print("maior que o líquido e para transformar vapor\nem líquido é preciso retirar energia do sistema.")
    print()
    print('3) Bomba(processo 2->3): compressão adiabática -> isentrópica')
    print()
    print("1ª Lei da Termodinâmica: wb = h4 - h3")
    print("2ª Lei da Termodinâmica: s3 = s4")
    print()
    print(f"* Estado 4: líquido comprimido; P4 = {P4/10} Mpa ({P4} bar)")
    print()
    print("-> Calculando wb:")
    wb = v3*(P4_aux-P3_aux)/1000
    print(f'wb = v3*(P4 - P3) -> wb = {v3} m3/kg *({P4_aux} - {P3_aux}) N/m2')
    trac3 = PrettyTable([f'|wb| = {wb:.4f} kJ/kg'])
    trac3.padding_width = 1
    trac3.hrules = ALL
    print(trac3)
    print("O sinal do trabalho na bomba é negativo, pois \npara funcionar a bomba consome trabalho, logo \nenergia é acrescentada ao sistema.")
    print()
    print("-> Encontrando h4:")
    print(f"wb = h4 - h3 -> h4 = wb + h3 -> h4 = {wb:.2f} kJ/kg + {h3} kJ/kg")
    h4 = wb+h3
    print(f"h4 = {h4:.4f} kJ/kg")
    print()
    print('4) Caldeira(processo 4->1): adição de calor à P cte')
    print()
    print("1ª Lei da Termodinâmica: qH = h1 - h4")
    print()
    print(f"qH = h1 - h4 -> qH = {h1} kJ/kg - {h4:.1f} kJ/kg")
    qH = h1-h4
    trac4 = PrettyTable([f'qH = {qH:.4f} kJ/kg'])
    trac4.padding_width = 1
    trac4.hrules = ALL
    print(trac4)
    print("O sinal do calor na caldeira é positivo, visto que \né transferido calor para o sistema (aumenta a energia do sistema).")
    print()
    print("-> Calculando a eficiência térmica:")
    nT = (wt-wb)/qH
    print(f"nT = (wt - |wb|)/qH -> nT = ({wt:.4f} kJ/kg - {wb:.4f} kJ/kg)/{qH:.4f} kJ/kg ")
    trac4 = PrettyTable([f'nT = {nT*100:.2f}%'])
    trac4.padding_width = 1
    trac4.hrules = ALL
    print(trac4)

def diagramaRank(T1,T2,T3,T4,T4l,s1,s2,s3,s4,s4l):
    # Gerando o diagrama
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
    plt.show()
def tabelaRank(T1,T2,T3,T4,P1,P2,P3,P4,s1,s2,s3,s4,sV,sL,h1,h3,hV,hL,P4_aux,P3_aux,v3):
    #Realizando calculos
    x2 = (s1-sL)/(sV-sL)
    h2 = hL + x2*(hV-hL)
    wb = v3*(P4_aux-P3_aux)/1000
    wt = h1-h2
    qL = h3-h2
    h4 = wb+h3
    qH = h1-h4
    nT = (wt-wb)/qH
    #Construindo a tabela de dados
    tab = PrettyTable()
    tab.field_names = [" ","Estado 1", "Estado 2", "Estado 3", "Estado 4"]
    tab.add_row(['Estado','Vsat','Mbifa','Lsat', 'Lcomp'])
    tab.add_row(["P(bar)", f'{P1:.2f}',f'{P2:.2f}',f'{P3:.2f}',f'{P4:.2f}'])
    tab.add_row(["T(°C)", f'{T1:.2f}',f'{T2:.2f}',f'{T3:.2f}',f'{T4:.2f}'])
    tab.add_row(["s(kJ/kg*K) ", f'{s1:.4f}',f'{s2:.4f}',f'{s3:.4f}',f'{s4:.4f}'])
    tab.add_row(["h(kJ/kg)", f'{h1:.2f}',f'{h2:.2f}',f'{h3:.2f}',f'{h4:.2f}'])
    tab.add_row(["x", 1.00,f'{x2:.3f}',0,'-'])
    tab.hrules = ALL
    print(tab.get_string(title="DADOS ENCONTRADOS"))
    tab2 = PrettyTable()
    tab2.header = False
    tab2.add_row(['wt(kJ/kg)',f"{wt:.2f}"])
    tab2.add_row(['qL(kJ/kg)',f"{qL:.2f}"])
    tab2.add_row(['wb(kJ/kg)',f"{wb:.2f}"])
    tab2.add_row(['qH(kJ/kg)',f"{qH:.2f}"])
    tab2.add_row(['nT',f"{nT*100:.2f}%"])
    tab2.padding_width = 1
    tab2.hrules = ALL
    print(tab2)
def relatorioText(P1,P2,P4,s1,h1,hL,hV,sL,sV,s2,v3,P4_aux,P3_aux):
    try:
        arquivo = open('EPC ciclo de Rankine', 'r+')
    except FileNotFoundError:
        arquivo = open('EPC ciclo de Rankine', 'w+')
    arquivo.writelines("Desenho esquemático: Ciclo de Rankine\n")
    arquivo.writelines("\n\t\t     | qH\n")
    arquivo.writelines("       (4)\t     V\t\t    (1)\n")
    if P4/10 >= 10:
        arquivo.writelines(f"   P4 = {P4/10} Mpa +--------+\tx1 = 1,0\n")
    else:
        arquivo.writelines(f"   P4 = {P4/10} Mpa\t +--------+\tx1 = 1,0\n")
    arquivo.writelines("   |------>------|CALDEIRA|------->-------|\n")
    arquivo.writelines("   |   \t\t +--------+ \t\t  |\n")
    arquivo.writelines("   |      \t\t\t\t  |\n")
    arquivo.writelines("+-----+\t\t\t\t      +-------+\n")
    arquivo.writelines("|BOMBA|\t\t\t\t      |TURBINA|\n")
    arquivo.writelines("+-----+\t\t\t\t      +-------+\n")
    arquivo.writelines("   |      \t\t\t\t  |\n")
    arquivo.writelines("   |\t\t+-----------+ \t\t  |\n")
    arquivo.writelines("   |------<-----|CONDENSADOR|------<------|\n")
    arquivo.writelines("          (3)  \t+-----------+\t   (2)\n")
    arquivo.writelines(f"\tx3 = 0        | qL     P2 = {P2*100} Kpa, x2 = ?\n")
    arquivo.writelines("\t\t      V\n\n")
    arquivo.writelines('Lista de considerações:\n\n')
    arquivo.writelines("* Fluido de trabalho: água\n")
    arquivo.writelines("* Cada componente do ciclo é avaliado como volume de controle\n")
    arquivo.writelines("* Regime permanente\n")
    arquivo.writelines("* A turbina e a bomba operam adiabaticamente\n")
    arquivo.writelines("* A caldeira e o condensador operam à pressão constante\n")
    arquivo.writelines("* Variações de Ec e Ep são desprezíveis\n")
    arquivo.writelines("* Não há trabalho na caldeira e no condensador\n")
    arquivo.writelines("* Processos internamente reversíveis\n\n")
    arquivo.writelines('1) Turbina(processo 1->2): expansão adiabática -> isentrópica\n\n')
    arquivo.writelines("1ª Lei da Termodinâmica: wt = h1 - h2\n")
    arquivo.writelines("2ª Lei da Termodinâmica: s1 = s2\n\n")
    arquivo.writelines(f"* Estado 1: vapor saturado; x1 = 1,0; P1 = {P1/10} Mpa ({P1} bar)\n\n")
    arquivo.writelines(f"Tabela A-3 ({P1} bar): h1 = {h1} kJ/kg \t s1 = {s1} kJ/kg*K\n\n")
    arquivo.writelines(f"* Estado 2: mistura bifásica; x2 = ?; P2 = {P2*100} Kpa ({P2} bar)\n\n")
    arquivo.writelines("-> Encontrando x2:\n\n")
    arquivo.writelines(f"s2 = s1 = {s1} kJ/kg*K\n")
    arquivo.writelines(f"Tabela A-3 ({P2} bar): hL = {hL} kJ/kg \t sL = {sL} kJ/kg*K\n")
    arquivo.writelines(f"                      hV = {hV} kJ/kg \t sV = {sV} kJ/kg*K\n")
    arquivo.writelines("s2 = sL +x2*(sV-sL) -> x2 = (s2-sL)/(sV-sL)\n")
    arquivo.writelines(f"x2 = ({s2} - {sL})kJ/kg*K/({sV} - {sL})kJ/kg*K\n")
    x2 = (s1-sL)/(sV-sL)
    arquivo.writelines(f'x2 = {x2:.4f}\n\n')
    arquivo.writelines("-> Encontrando h2:\n\n")
    arquivo.writelines(f"h2 = hL + x2*(hV - hL) -> h2 = {hL} kJ/kg + {x2:.4f}*({hV} - {hL}) kJ/kg\n")
    h2 = hL + x2*(hV-hL)
    arquivo.writelines(f'h2 = {h2:.4f} kJ/kg\n\n')
    arquivo.writelines("-> Calculando wt:\n\n")
    wt = h1-h2
    arquivo.writelines(f"wt = h1 - h2 -> wt = {h1:.4f} kJ/kg - {h2:.4f} kJ/kg\n")
    trac1 = PrettyTable([f"wt = {wt:.4f} kJ/kg"])
    trac1.padding_width = 1
    trac1.hrules = ALL
    arquivo.writelines(f'{trac1}\n')
    arquivo.writelines("O sinal do trabalho na turbina é positivo, pois \nela realiza trabalho (sai energia do sistema).\n\n")
    arquivo.writelines('2) Condensador(processo 2->3): rejeição de calor à P cte\n\n')
    arquivo.writelines("1ª Lei da Termodinâmica: qL = h2 - h3\n\n")
    arquivo.writelines(f"* Estado 3: líquido saturado; x3 = 0; P3 = {P2*100} Kpa ({P2} bar)\n\n")
    arquivo.writelines(f"Tabela A-3 ({P3} bar): h3 = {h3} kJ/kg \t v3 = {v3} m3/kg\n\n")
    arquivo.writelines("-> Calculando qL:\n\n")
    qL = h3-h2
    arquivo.writelines(f"qL = h3 - h2 -> qL = {h3} kJ/kg - {h2:.2f} kJ/kg\n")
    trac2 = PrettyTable([f"qL = {qL:.4f} kJ/kg"])
    trac2.padding_width = 1
    trac2.hrules = ALL
    arquivo.writelines(f'{trac2}\n')
    arquivo.writelines("O sinal do calor no condensador é negativo, pois o\ncalor sai do sistema (diminui energia do sistema)\numa vez que o vapor se encontra em um estado energético\n")
    arquivo.writelines("maior que o líquido e para transformar vapor em \nlíquido é preciso retirar energia do sistema.\n\n")
    arquivo.writelines('3) Bomba(processo 2->3): compressão adiabática -> isentrópica\n\n')
    arquivo.writelines("1ª Lei da Termodinâmica: wb = h4 - h3\n")
    arquivo.writelines("2ª Lei da Termodinâmica: s3 = s4\n\n")
    arquivo.writelines(f"* Estado 4: líquido comprimido; P4 = {P4/10} Mpa ({P4} bar)\n\n")
    arquivo.writelines("-> Calculando wb:\n\n")
    wb = v3*(P4_aux-P3_aux)/1000
    arquivo.writelines(f'wb = v3*(P4 - P3) -> wb = {v3} m3/kg *({P4_aux} - {P3_aux}) N/m2\n')
    trac3 = PrettyTable([f'|wb| = {wb:.4f} kJ/kg'])
    trac3.padding_width = 1
    trac3.hrules = ALL
    arquivo.writelines(f'{trac3}\n')
    arquivo.writelines("O sinal do trabalho na bomba é negativo, pois \npara funcionar a bomba consome trabalho, logo \nenergia é acrescentada ao sistema.\n\n")
    arquivo.writelines("-> Encontrando h4:\n\n")
    arquivo.writelines(f"wb = h4 - h3 -> h4 = wb + h3 -> h4 = {wb:.2f} kJ/kg + {h3} kJ/kg\n")
    h4 = wb+h3
    arquivo.writelines(f"h4 = {h4:.4f} kJ/kg\n\n")
    arquivo.writelines('4) Caldeira(processo 4->1): adição de calor à P cte\n\n')
    arquivo.writelines("1ª Lei da Termodinâmica: qH = h1 - h4\n\n")
    arquivo.writelines(f"qH = h1 - h4 -> qH = {h1} kJ/kg - {h4:.1f} kJ/kg\n")
    qH = h1-h4
    trac4 = PrettyTable([f'qH = {qH:.4f} kJ/kg'])
    trac4.padding_width = 1
    trac4.hrules = ALL
    arquivo.writelines(f'{trac4}\n')
    arquivo.writelines("O sinal do calor na caldeira é positivo, visto que \né transferido calor para o sistema (aumenta a energia do sistema).\n\n")
    arquivo.writelines("-> Calculando a eficiência térmica:\n\n")
    nT = (wt-wb)/qH
    arquivo.writelines(f"nT = (wt - |wb|)/qH -> nT = ({wt:.4f} kJ/kg - {wb:.4f} kJ/kg)/{qH:.4f} kJ/kg \n")
    trac4 = PrettyTable([f'nT = {nT*100:.2f}%'])
    trac4.padding_width = 1
    trac4.hrules = ALL
    arquivo.writelines(f"{trac4}")
    arquivo.close()    
def leiaInt(msg):
    while True:
        try:
            n = int(input(msg))
        except(ValueError,TypeError):
            print('ERRO: digite um numero inteiro valido')
            continue
        except(KeyboardInterrupt):
            print('Usuario preferiu nao digitar esse numero')
            return 0
        else:
            return n
        
def linha(tam = 46):
    return '-' * tam

def cabeçalho(txt):
    print(linha())
    print(txt.center(46))
    print(linha())
    
def menu(lista):
    cabeçalho('MENU: CICLO DE POTÊNCIA RANKINE')
    i=1
    for item in lista:
        print(f'({i}) -> {item}')
        i +=1
    print(linha())
    opc = leiaInt('Sua opcao: ')
    print('\n')
    return opc

def menuR (menu):
    while True:    
        resposta = menu(['Relatório: ciclo de Rankine','Dados: ciclo de Rankine', 'Diagrama T-s: ciclo de Rankine','EPC em txt: ciclo de Rankine','Sair'])
        if resposta == 1:
            relatorioRank(P1,P2,P4,s1,h1,hL,hV,sL,sV,s2,v3,P4_aux,P3_aux)
        elif resposta == 2:
            tabelaRank(T1,T2,T3,T4,P1,P2,P3,P4,s1,s2,s3,s4,sV,sL,h1,h3,hV,hL,P4_aux,P3_aux,v3)
        elif resposta == 3:
            diagramaRank(T1,T2,T3,T4,T4l,s1,s2,s3,s4,s4l)
        elif resposta == 4:
            relatorioText(P1,P2,P4,s1,h1,hL,hV,sL,sV,s2,v3,P4_aux,P3_aux)
            print('Nome arquivo criado: EPC ciclo de Rankine')
        elif resposta == 5:
            print('Fim do programa, obrigado pela visita')
            break
        else:
            print('ERRO! Digite uma opcao valida')
            
menuR(menu)