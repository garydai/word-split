#coding: utf-8
import sys
#print sys.getdefaultencoding()
import codecs
#print u'Hello world! 你好，世界！'
import math

import collections
dic=collections.defaultdict(lambda:1)

transition_probility = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]
initial_states = {'b':0.0, 'm':0.0, 'e':0.0, 's':0.0}
emit_probility = {'b':{}, 'm':{}, 'e':{}, 's':{}}
transition_probility = {
'b':{'b':0.0, 'm':0.19922840916814916 , 'e':0.8007715908318509, 's':0.0},
'm':{'b':0.0, 'm':0.47583202978061256 , 'e':0.5241679702193874 , 's':0.0},
'e':{'b':0.6309567616935934, 'm':0.0 , 'e':0.0, 's':0.36904323830640656},
's':{'b':0.6343402140354506, 'm':0.0 , 'e':0.0, 's':0.36565844303914763},
}
#def create_emit_matrix(word):

#该函数错的,不能只有一个词语决定转移函数,要根据句子的分词情况,e->s也是有概率的
def create_ini_states(word, freq):
	global transition_probility_count
	global initial_states
	global transition_probility
	#单字
	if len(word) == 1:
		initial_states['s'] = initial_states['s'] + freq
	#多字	
	if len(word) > 1:
		initial_states['b'] = initial_states['b'] + freq


def LoadDic(filename):
	count = 0
	trie = {}
	for line in file(filename):
		word, frq = line.split(' ')[0:2]
		#统计词频率
		word = word.decode('utf-8')
		dic[word] = int(frq) + 1
		count += (int(frq) + 1)
		create_ini_states(word, float(frq))
		if len(word) == 1:
			if trie.has_key(word):
				trie[word]['s'] = 	trie[word]['s'] + float(frq)
				trie[word]['sum'] = trie[word]['sum'] + float(frq)
			else:
				trie[word] = {'s':float(frq), 'b':1.0, 'e':1.0, 'm':1.0, 'sum':float(frq), 'char':word}
			continue
		i = 0
		for c in word:
			if trie.has_key(c):
				if i == 0:
					trie[c]['b'] = trie[c]['b'] + float(frq)
				elif i < len(word) - 1:
					trie[c]['m'] = trie[c]['m'] + float(frq)
				elif i == len(word) - 1:
					trie[c]['e'] = trie[c]['e'] + float(frq)
				trie[c]['sum'] = trie[c]['sum'] + float(frq)
			else:
				if i == 0:
					trie[c] = {'s':1.0, 'b':float(frq), 'e':1.0, 'm':1.0, 'sum':float(frq), 'char':c}
				elif i < len(word) - 1:
					trie[c] = {'s':1.0, 'b':1.0, 'e':1.0, 'm':float(frq), 'sum':float(frq), 'char':c}
				elif i == len(word) - 1:
					trie[c] = {'s':1.0, 'b':1.0, 'e':float(frq), 'm':1.0, 'sum':float(frq), 'char':c}
			i = i + 1
	#print trie[u'啊']
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
	
	summ = initial_states['s'] + initial_states['b'] 
	initial_states['b'] = initial_states['b'] / summ
	initial_states['s'] = initial_states['s'] / summ	
	#print initial_states['b'] ,initial_states['s'] 
	#print trie		
	dic[u'_t_'] = count


def Viterbi(initial_states, emit_probility, transition_probility, sentence):
	#print transition_probility
	p = []
	trace = []
	for char in sentence:
		p.append({'s':0.0, 'b':0.0, 'e':0.0, 'm':0.0})
		trace.append({'s':'0', 'b':'0', 'e':'0', 'm':'0'})
	states = 'besm'
	for i in range(len(sentence)):
		if i == 0:
			p[0]['s'] = math.log(emit_probility['s'][sentence[0]]) + math.log(initial_states['s'])
			p[0]['b'] = math.log(emit_probility['b'][sentence[0]]) + math.log(initial_states['b'])
		else:
			for now_states in states:
				for last_stete in states:
					if transition_probility[last_stete][now_states] == 0.0 or emit_probility[now_states][sentence[i]] == 0:
						continue
					#上一个状态没到达
					if p[i - 1][last_stete] == 0:
						continue

					if p[i][now_states] == 0.0:
						p[i][now_states] = p[i - 1][last_stete] \
											+ math.log(emit_probility[now_states][sentence[i]]) \
											+ math.log(transition_probility[last_stete][now_states])
						trace[i][now_states] = last_stete
					else:
						if p[i - 1][last_stete] + math.log(emit_probility[now_states][sentence[i]]) \
							+ math.log(transition_probility[last_stete][now_states]) > p[i][now_states]:
							trace[i][now_states] = last_stete
							p[i][now_states] = p[i - 1][last_stete] + math.log(emit_probility[now_states][sentence[i]]) \
							+ math.log(transition_probility[last_stete][now_states])
	#print p
	#print emit_probility['s'][u'啊']
	#print emit_probility['b'][u'啊']
	char  = 's'
	prot = p[len(sentence) - 1]['s']

	#print p
	for state in states:
		if prot < p[len(sentence) - 1][state]:
			prot = p[len(sentence) - 1][state]
			char = state
	output_state = ''
	for i in range(len(sentence)- 1, -1, -1):
	#	if char == 'e': 
		#	print '|'
		#if char == 's': 
		#	print '|'
		#if char == 'b':
		#	print '|'
		#print sentence[i]
		#print char, trace[i][char]		
		#print char
		output_state = char + output_state 
		char = trace[i][char]
	j = 0
	s = ''
	for i in output_state:
		if i == 'b' or i == 's' :
			s =  s +  '|' + sentence[j]
		elif i == 's' or i == 'e':
			s = s + sentence[j] + '|'
		else:
			s =  s + sentence[j] 
		print 's', emit_probility['s'][sentence[j]]
		print 'b', emit_probility['b'][sentence[j]]
		print 'e', emit_probility['e'][sentence[j]]
		print 'm', emit_probility['m'][sentence[j]]
		j = j + 1
		emit_probility
	print s
	print p
	print output_state


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
		#line  = '你好啊朋友'
		SplitWord(line.decode('utf-8'))
		Viterbi(initial_states, emit_probility, transition_probility, line.decode('utf-8'))



