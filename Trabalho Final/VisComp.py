'''
	Universidade Federal de Sao Carlos
	Bruno Donato Banhos		587460
	Carla Simoes Gama 		613843
'''

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors
import numpy as np

x = []
y = []
z = []
t = []
a = []

def f_to_c(fahrenheit):
    celsius = ((fahrenheit - 32)/9) * 5
    return celsius

fig, ax = plt.subplots()
ax.scatter(x, y)

with open("city_temp.csv") as f:
	for line in f:
		content = line.split("\t")
		t.append(content[0])
		x.append(-float(content[3]))
		y.append(float(content[2]))
		z.append(f_to_c(float(content[1])))
		a.append(float((content[4]).split("\n")[0]))

for i, txt in enumerate(t):
	ax.annotate(txt + ", " + str('%.2f' % z[i]) + "°C" if z[i] > 8.0 or z[i] < -15.0 else "", (x[i],y[i]), size=8)

ax.set_title('Média de temperaturas (°C) no mês de Janeiro em algumas cidades dos EUA')
scatters = plt.scatter(x, y, s=a, c=z, cmap=plt.cm.coolwarm)
plt.colorbar(scatters)
plt.xlabel('Latitude')
plt.ylabel('Longitude')
figManager = plt.get_current_fig_manager()
figManager.resize(*figManager.window.maxsize())

l1 = plt.scatter([],[], s=5, edgecolors='none', color='grey')
l2 = plt.scatter([],[], s=500, edgecolors='none', color='grey')
l3 = plt.scatter([],[], s=1000, edgecolors='none', color='grey')
l4 = plt.scatter([],[], s=1500, edgecolors='none', color='grey')

labels = ["1", "500", "1000", "1500"]

leg = plt.legend([l1, l2, l3, l4], labels, ncol=4, frameon=True, fontsize=12,
handlelength=2, loc = 8, borderpad = 1.2,
handletextpad=1, title='Altitude em metros', scatterpoints = 1, 
bbox_to_anchor=(0.9, 0), borderaxespad=-6.5)

plt.tight_layout(pad=3)
plt.show()
