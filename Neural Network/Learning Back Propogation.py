
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

import matplotlib.pyplot as plt

learningRate = 0.1

i = 1.5
w = 0.8
y = 0.8
a = lambda: i * w
C = lambda: (a() - y) ** 2

# dCdw = lambda: dadw * dCda()

def dCdw():
    """
    dC/dw ==>
        da/dw = i = 1.5
        dC/da = 2(a-y) = 2((i*w)-y)
        (da/dw) * (dC/da) = (1.5 * 2) * ((i*w)-y) = 3((i*w)-y)
        3((i*w)-y) = 3(iw) - 3y
        3*i*w - 3*y
        (3*1.5)*w - (3*0.8)
        = 4.5w - 2.4
        "wMultiple" = 4.5, "slopeBias" = 2.4
    """
    
    dadw = i

    wMultiple = (dadw * 2) * i
    slopeBias = (dadw * 2) * y

    return wMultiple, slopeBias

# print(
#     f"i:{i} \n" + 
#     f"w:{round(w,3)} \n" + 
#     f"y:{y} \n" + 
#     f"a:{round(a(),3)} \n" + 
#     f"C:{round(C(),3)} \n"
# )

plotW = []
plotC = []

for _ in range(15):

    wMultiple, slopeBias = dCdw()
    # print(f"{wMultiple, slopeBias}")

    w -= (learningRate * (wMultiple * w)) - (learningRate * slopeBias)
    
    plotW.append(w)
    plotC.append(C())

# print(
#     f"i:{i} \n" + 
#     f"w:{round(w,3)} \n" + 
#     f"y:{y} \n" + 
#     f"a:{round(a(),3)} \n" + 
#     f"C:{round(C(),3)} \n"
# )

fig, axes = plt.subplots(2)
fig.tight_layout()

axes[0].set_title("Weight / time")
axes[0].plot(plotW)

axes[1].set_title("Cost / time")
axes[1].plot(plotC)

plt.show()