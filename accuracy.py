
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
data = np.loadtxt('feedback.txt', delimiter=",",  
                  usecols=[2])
out=list(data)
#print(out)
out_new=[int(i) for i in out]
#print(out_new)
k=Counter(out_new)
#print(k)
acc=['good','average','bad']
#count=[values[0],values[1],values[2]]
names = list(k.keys())
#print(names)
values = list(k.values())
#print(values)
total_sum=values[0]+values[1]+values[2]
accuracy1=(values[0]/total_sum)*100
print("good",accuracy1)
accuracy2=(values[1]/total_sum)*100
print("average",accuracy2)
accuracy3=(values[2]/total_sum)*100
print("bad",accuracy3)

plt.bar(0,accuracy1,tick_label=names[0])
plt.bar(1,accuracy2,tick_label=names[1])
plt.bar(2,accuracy3,tick_label=names[2])
plt.xticks(range(0,3),names)
plt.savefig('feedback.png')
plt.xlabel('parameters of accuracy')
plt.ylabel('percentage of accuracy')
plt.legend(acc)

#plt.legend(count)
opacity = 0.5
bar_width = 0.30
plt.show()
