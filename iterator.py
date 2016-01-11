f=open('iwant.txt','r')
g=open('links.txt','w')
for line in f.readlines():
	print line
	g.write(line+"\n")

f.close()
g.close()
# for line in g.writelines():
