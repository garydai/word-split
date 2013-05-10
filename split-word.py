#coding: utf-8
import sys
#print sys.getdefaultencoding()
import codecs
#print u'Hello world! 你好，世界！'

import collections
dic=collections.defaultdict(lambda:1)
#隐藏状态
states = {'s':0, 'e':1, 'm':2, 'a':3}
transition_probility = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]
initial_probility = {'b':0.0, 'm':0.0, 'e':0.0, 's':0.0}
emit_probility = {'b':{}, 'm':{}, 'e':{}, 's':{}}
transition_probility = {
'b':{'b':0.0}, 'b':{'m':0.19922840916814916 }, 'b':{'e':0.8007715908318509}, 'b':{'s':0.0},
'm':{'b':0.0}, 'b':{'m':0.47583202978061256  }, 'b':{'e':0.5241679702193874 }, 'b':{'s':0.0},
'e':{'b':0.6309567616935934}, 'b':{'m':0.0 }, 'b':{'e':0.0}, 'b':{'s':0.36904323830640656},
's':{'b':0.6343402140354506}, 'b':{'m':0.0 }, 'b':{'e':0.0}, 'b':{'s':0.36565844303914763},
}
#def create_emit_matrix(word):

#该函数错的,不能只有一个词语决定转移函数,要根据句子的分词情况,e->s也是有概率的
def create_transiton_matrix(word):
	global transition_probility_count
	global initial_probility
	global transition_probility
	#单字
	if len(word) == 1:
		initial_probility['s'] = initial_probility['s'] + 1
	#多字	
	if len(word) > 1:
		initial_probility['b'] = initial_probility['b'] + 1


def LoadDic(filename):
	count = 0
	trie = {}
	for line in file(filename):
		word, frq = line.split(' ')[0:2]
		#统计词频率
		word = word.decode('utf-8')
		dic[word] = int(frq) + 1
		count += (int(frq) + 1)
		create_transiton_matrix(word)
		if len(word) == 1:
			if trie.has_key(word):
				trie[word]['s'] = 	trie[word]['s'] + 1
				trie[word]['sum'] = trie[word]['sum'] + 1
			else:
				trie[word] = {'s':1.0, 'b':0.0, 'e':0.0, 'm':0.0, 'sum':1.0, 'char':word}
			continue
		i = 0
		for c in word:
			if trie.has_key(c):
				if i == 0:
					trie[c]['b'] = trie[c]['b'] + 1
				elif i < len(word) - 2:
					trie[c]['m'] = trie[c]['m'] + 1
				elif i == len(word) - 1:
					trie[c]['e'] = trie[c]['e'] + 1
				trie[c]['sum'] = trie[c]['sum'] + 1
			else:
				if i == 0:
					trie[c] = {'s':0.0, 'b':1.0, 'e':0.0, 'm':0.0, 'sum':1.0, 'char':c}
				elif i < len(word) - 2:
					trie[c] = {'s':0.0, 'b':0.0, 'e':0.0, 'm':1.0, 'sum':1.0, 'char':c}
				elif i == len(word) - 1:
					trie[c] = {'s':0.0, 'b':0.0, 'e':1.0, 'm':0.0, 'sum':1.0, 'char':c}
			i = i + 1
	global emit_probility
	for c in trie:
		emit_probility['s'][c] = trie[c]['s'] / trie[c]['sum']
		emit_probility['b'][c] = trie[c]['b'] / trie[c]['sum']
		emit_probility['e'][c] = trie[c]['e'] / trie[c]['sum']		
		emit_probility['m'][c] = trie[c]['m'] / trie[c]['sum']

#	print emit_probility
	f = open('test.txt', 'w+')
	for i in emit_probility:
		for j in emit_probility[i]:
			string = u'%s%f\n'%(j,emit_probility[i][j])
			f.write(string.encode('utf-8'))
	
	summ = initial_probility['s'] + initial_probility['b'] 
	initial_probility['b'] = initial_probility['b'] / summ
	initial_probility['s'] = initial_probility['s'] / summ	
	print initial_probility['b'] ,initial_probility['s'] 
	#print trie		
	dic[u'_t_'] = count


def SplitWord(ipt):

	count = dic[u'_t_']
	l = len(ipt)
	#初始状态
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
						#记录前匹配index
						idx[i] = j
				if(j == 0 and j != i):
					#print frqmax, dic[word] / count
					if(frqmax < 1.0 * dic[word] / count):
						frqmax = 1.0 * dic[word] / count
						idx[i] = j	
			j = j + 1
		dp[i] = frqmax

	#print dp
	#print idx

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
		print w[w_len - i - 1], '|',

	print ''

if __name__ == '__main__':
	LoadDic('dict.txt')
	for line in file('word-test.txt'):
		line = line.replace('\n', '')
		SplitWord(line.decode('utf-8'))



