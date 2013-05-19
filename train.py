#coding: utf-8
def transport():

	f = open('train_script.txt', 'w+')
	for line in file('msr_train.txt'):
		line = line.decode('utf-8')
		t = ''
		for char in line:
			if char != u'/' and char != u'B' and char != u'E' and char != u'S' and char != u'M':
				t = t + char;
		f.write(t.encode('utf-8'));

def train():
	
if __name__ == '__main__':
	train('train_script.txt')

