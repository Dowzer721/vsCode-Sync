
import sys
sys.path.append("C:\\Users\\Luke\\Documents\\Learning Python\\")
import LukeLibrary as LL

import matplotlib.pyplot as plt

learningRate = LL.randomFloat(0.01, 0.1) # 0.01

i = LL.randomFloat(0.0, 5.0) # 1.5
w = LL.randomFloat() # 0.8
y = LL.randomFloat(0.0, 5.0) # 0.8
a = lambda: i * w
C = lambda: (a() - y) ** 2

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

plotW = []
plotC = []

loopCount = max(50, int(1.25 / learningRate))
for _ in range(loopCount):

    wMultiple, slopeBias = dCdw()
    # print(f"{wMultiple, slopeBias}")

    w -= (learningRate * (wMultiple * w)) - (learningRate * slopeBias)
    
    plotW.append(w)
    plotC.append(C())

fig, axes = plt.subplots(2)
fig.tight_layout()
fig.canvas.set_window_title(f"Learning Rate:{learningRate}, Ideal Weight:{round(y/i,2)}, Final Weight:{round(plotW[-1],2)}")

axes[0].set_title("Weight / time")
axes[0].plot(plotW)

axes[1].set_title("Cost / time")
axes[1].plot(plotC)

plt.show()