datadir = "C:\\temp\\"
f=open('C:\\temp\\links.csv','r')
o=open(datadir+"cleaned.csv", "w")
lines = f.readlines()
for line in lines:
	#o.write(line.split("&usd")[0] + "\n")
	mycleanedline = line.split("&usd")[0]
	o.write(mycleanedline + "\n")
o.close()


	

