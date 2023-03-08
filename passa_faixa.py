from numpy import (pi, exp, linspace, absolute, angle, cos, sin)
from matplotlib.pyplot import (plot, show, title, xlabel, ylabel, subplots, scatter)
from scipy import io


def H(z):
    return ((z - exp(1j * 7 * pi / 50)) * (z - exp(-1j * 7 * pi / 50))) / (
        ((z - 0.9) ** 2))


def dif(n):
    global sinal
    global aux
    if n == 0:
        aux[0] = sinal[0]
        return aux[0]
    elif n == 1:
        aux[1] = sinal[1] - ((2 * cos(7 * pi / 50)) * sinal[0]) + (1.8 * aux[0])
        return aux[1]
    else:
        aux[n] = sinal[n] - ((2 * cos(7 * pi / 50)) * sinal[n - 1]) + sinal[n - 2] + (
            (1.8 * aux[n - 1]) - (0.81 * aux[n - 2])
        )
        return aux[n]


# Diagrama de polos e zeros:

t = linspace(0, 2 * pi, 1000)
x = cos(t)
y = sin(t)

figure, axes = subplots(1)
axes.plot(x, y, color='cyan')
axes.set_aspect(1)
xlabel("Eixo Real")
ylabel("Eixo imaginário")
scatter(cos(7 * pi / 50), sin(7 * pi / 50), marker='o', color='black')
scatter(cos(7 * pi / 50), sin(-7 * pi / 50), marker='o', color='black')
scatter(0.9, 0, marker='x', color='black')
title("Círculo Complexo Unitário")
show()

# Amplitude e Fase da resposta em Frequência do Sistema:

dom = linspace(-2 * pi, 2 * pi, 10000)

plot(dom, absolute(H(exp(1j * dom))), color='red')
title("Resposta em Frequência H(e^j$\omega$)")
xlabel("Frequência angular $\omega$")
ylabel("Magnitude")
show()

plot(dom, angle(H(exp(1j * dom)), deg=True), color='blue')
title("Resposta em Frequência H(e^j$\omega$)")
xlabel("Frequência angular $\omega$")
ylabel("Fase (graus)")
show()

# Implementação do filtro sobre o sinal de ECG:

variaveis = io.loadmat("noisy_ecg_data_2.mat")
sinal = variaveis['noisy_ecg2']
sinal = sinal.ravel()
dom_2 = linspace(0, sinal.shape[0], sinal.shape[0])
plot(dom_2, sinal, color='red')
title("Sinal de ECG ruidoso (todas as amostras)")
xlabel("Amostras (n)")
ylabel("Amplitude")
show()

aux = list(0 for i in range(sinal.shape[0]))

dom_3 = linspace(0, 500, 500)
plot(dom_3, sinal[:500], color='red')
title("Sinal de ECG ruidoso (500 amostras)")
xlabel("Amostras (n)")
ylabel("Amplitude")
show()

sinal_filtrado = list(dif(a) for a in range(5000))
plot(dom_2, sinal_filtrado, color='blue')
title("Sinal de ECG filtrado (todas as amostras)")
xlabel("Amostras (n)")
ylabel("Amplitude")
show()

sinal_filtrado_2 = sinal_filtrado[:500]
plot(dom_3, sinal_filtrado_2, color='blue')
title("Sinal de ECG filtrado (500 amostras)")
xlabel("Amostras (n)")
ylabel("Amplitude")
show()
