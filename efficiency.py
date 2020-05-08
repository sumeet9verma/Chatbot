import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
data = np.loadtxt('chats_storage.txt', delimiter=",",
                  usecols=[3])
out=list(data)
out_new=[int(i) for i in out]
k=Counter(out_new)
# print(k)
names = list(k.keys())
values = list(k.values())
efficiency=((values[1])/(values[0]+values[1]))*100
eff=int(efficiency)
print("efficiency of chatbot:",eff,"%")