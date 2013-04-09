#coding= utf-8
import sys
print sys.getdefaultencoding()
reload(sys)
sys.setdefaultencoding('utf-8')

s = "中文"
print s

count = 0
for line in file('SogouLabDic.dic'):
	word, frq = line.split('\t')[0:2]
	dic = {}
	dic[word] = int(frq)
	count += int(frq)
	#print dic[word]
#print count


inputstring = "明天去开会"
print inputstring

l = len(inputstring) 
p = [1.0 / count for i in range(l)]
#print p
for i in range(l):
	if(i):
		p[i] *= p[i - 1]
#print p

for i in range(l):
	j = 0
	while j <= i:
		word = inputstring[j:]
		j = j + 1
	#	print word
