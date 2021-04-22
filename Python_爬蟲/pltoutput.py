import matplotlib.pyplot as plt

print('Start----------------------')
fp = open('plt/Beauty.txt', 'r', encoding='UTF-8')
content = fp.read()
str = content
fp.close()

print(str)

#0-22.5
A=plt.bar(str,alpha=0.9, width = 0.8, facecolor = 'SkyBlue', edgecolor = 'Black', label='one', lw=1)

def createLabels(data):
    for item in data:
        height = item.get_height()
        plt.text(
            item.get_x()+item.get_width()/2., 
            height*1.05, 
            '%d' % int(height),
            ha = "center",
            va = "bottom",
        )
createLabels(A)


plt.xlim(0,2001)
plt.ylim(0,40)
plt.title("Data")
plt.xlabel("Time")
plt.ylabel("Size")
plt.show()
