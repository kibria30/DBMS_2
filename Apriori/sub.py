# ele2 = [('I1', 'I2'), ('I1', 'I3'), ('I1', 'I5'), ('I2', 'I3'), ('I2', 'I4'), ('I2', 'I5')]
ele = ['I1', 'I2', 'I3', 'I4', 'I5']
ele2 = []

def convert(ele):
    ele2 = [(i,) for i in ele]
    return ele2

print(type(ele[0]))
for i in ele:
    if type(i) != tuple:
        ele2 = convert(ele)

print(ele2)
print(type(ele2[0]))
ele3 = set()
for i in range(len(ele2)-1):
    for j in range(i+1, len(ele2)):
        temp = set(ele2[i] + ele2[j])
        temp = sorted(tuple((temp)))
        if(len(temp))==len(ele2[0])+1:
            ele3.add(tuple(temp))

for i in ele3:
    print(i)