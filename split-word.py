#coding: utf-8
import sys
print sys.getdefaultencoding()
import codecs
print u'Hello world! 你好，世界！'

import collections
dic=collections.defaultdict(lambda:1)

def LoadDic():
	count = 0
	for line in file('SogouLabDic.dic'):
		word, frq = line.split('\t')[0:2]
		dic[word.decode('utf-8')] = int(frq) + 1
		count += (int(frq) + 1)
	dic[u'_t_'] = count


def SplitWord(ipt):

	count = dic[u'_t_']
	l = len(ipt)
	dp = [1.0 / count for i in range(l)]
	idx = [-1 for i in range(l)]
	#print p
	for i in range(l):
		if(i):
			dp[i] *= dp[i - 1]

	for i in range(l):
		j = 0
		frqmax = dp[i]
		while j <= i:
			word = ipt[j:i+1]
			#前面有匹配到的词或匹配自身
			if(dic[word] != 1 or i == j):
				if(j > 0):
					if(frqmax < dp[j - 1] * dic[word] / count):
						frqmax = dp[j - 1] * dic[word] / count
						idx[i] = j
				if(j == 0 and j != i):
					if(frqmax < dp[j] * dic[word] / count):
						frqmax = dp[j] * dic[word] / count
						idx[i] = j	
			j = j + 1
		dp[i] = frqmax

	print dp
	print idx

	w = []
	i = l - 1
	while i >= 0:
		if(idx[i] != -1):
			w.append(ipt[idx[i]: i + 1])
			i = idx[i] - 1
		else:
			w.append(ipt[i:i + 1])	
			i = i - 1

	w_len = len(w)
	for i in range(w_len):
		print w[w_len - i - 1]


if __name__ == '__main__':
	LoadDic()
	s = u"从一个人"
	SplitWord(s)



