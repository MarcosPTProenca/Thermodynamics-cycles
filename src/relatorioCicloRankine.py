import pandas as pd
import numpy as np
from prettytable import PrettyTable
from prettytable import ALL
tabelaA3 = pd.read_csv("termo.csv", sep = ' ')
P2 = 30
P4 = 3
P2 = P2/100
P1 = P4*10
P4 = P4*10
P3 = P2
P4_aux = P4*10**5
P3_aux = P3*10**5
#definicao variaveis:
h1 = float(tabelaA3.loc[tabelaA3.PRESSAO == P1,'ENTALPV'])
s1 = float(tabelaA3.loc[tabelaA3.PRESSAO == P1,'ENTROPV'])
hL = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTALPL'])
hV = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTALPV'])
sL = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTROPL'])
sV = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTROPV'])
h3 = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'ENTALPL'])
s3 = float(tabelaA3.loc[tabelaA3.PRESSAO == P3,'ENTROPL'])
T4l = float(tabelaA3.loc[tabelaA3.PRESSAO == P4,'TEMPERATURA'])
s4l = float(tabelaA3.loc[tabelaA3.PRESSAO == P4,'ENTROPL'])
v3 = float(tabelaA3.loc[tabelaA3.PRESSAO == P2,'VESPL'])/1000
s4 = s3
s2 = s1
def relatorio(P1,P2,P4,s1,h1,hL,hV,sL,sV,s2):
    try:
        arquivo = open('EPC', 'r+')
    except FileNotFoundError:
        arquivo = open('EPC', 'w+')
    arquivo.writelines("Desenho esquemático: Ciclo de Rankine\n")
    arquivo.writelines("\n\t\t     | qH\n")
    arquivo.writelines("       4\t     V\t\t    1\n")
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
    arquivo.writelines("          3  \t+-----------+\t   2\n")
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
    arquivo.writelines(f"x2 = ({s2} - {sL})/({sV} - {sL})\n")
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
    arquivo.writelines("O sinal do calor na caldeira é posivito, visto que \né transferido calor para o sistema (aumenta a energia do sistema).\n\n")
    arquivo.writelines("-> Calculando a eficiência térmica:\n\n")
    nT = (wt-wb)/qH
    arquivo.writelines(f"nT = (wt - wb)/qH -> nT = ({wt:.4f} kJ/kg - {wb:.4f} kJ/kg)/{qH:.4f} kJ/kg \n")
    trac4 = PrettyTable([f'nT = {nT*100:.2f}%'])
    trac4.padding_width = 1
    trac4.hrules = ALL
    arquivo.writelines(f"{trac4}\n")
    arquivo.close()
relatorio(P1,P2,P4,s1,h1,hL,hV,sL,sV,s2)  
