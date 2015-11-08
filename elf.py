#!/usr/bin/python3
# author: vap0r
# github: github.com/qq53

import struct

def choose(d, i):
	for k,v in d.items():
		if v == i:
			return k
	return ''

def elf(tmpf):
	f = open(tmpf, 'rb')
	header = {}
	magic = [i for i in f.read(16)]
	
	if magic[0] != 127 or magic[1] != ord('E') or magic[2] != ord('L') or magic[3] != ord('F'):
		return None

	header['class'] = choose({'32':1,'64':2}, magic[4])
	header['encoding'] = choose({'little':1,'big':2}, magic[5])
	header['OS ABI'] = choose({'UNIX System V ABI':0,'HP-UX':1,'GNU':3}, magic[7])
	header['ABI'] = choose({'UNIX System V ABI':0,'HP-UX':1,'GNU':3}, magic[8])

	if header['class'] == '32':
		temp = f.read(struct.calcsize('2H5I6H'))
		temp = struct.unpack('2H5I6H',temp)
	elif header['class'] == '64':
		temp = f.read(struct.calcsize('2HI3LI6H'))
		temp = struct.unpack('2HI3QI6H',temp)

	td = {
		'Relocatable': 1,
		'Executable': 2,
		'Shared object': 3,
		'Core': 4
	}
	header['type'] = choose(td, temp[0]) + ' file'

	md = {
		'Intel 80386': 3,
		'AMD x86-64 architecture': 62,
	}
	header['machine'] = choose(md, temp[1])
	header['version'] = temp[2]
	header['entry'] = hex(temp[3])
	header['phoff'] = hex(temp[4])
	header['shoff'] = hex(temp[5])
	header['flags'] = hex(temp[6])
	header['ehsize'] = hex(temp[7])
	header['phentsize'] = hex(temp[8])
	header['phnum'] = hex(temp[9])
	header['shentsize'] = hex(temp[10])
	header['shnum'] = hex(temp[11])
	header['shstrndx'] = hex(temp[12])

	header['ph'] = []
	for i in range(int(header['phnum'],16)):
		if header['class'] == '32':
			temp = f.read(struct.calcsize('8I'))
			temp = struct.unpack('8I',temp)
		elif header['class'] == '64':
			temp = f.read(struct.calcsize('2I6Q'))
			temp = struct.unpack('2I6Q',temp)
		dtemp = {}
		dtemp['type'] = hex(temp[0])
		dtemp['offset'] = hex(temp[1])
		dtemp['vaddr'] = hex(temp[2])
		dtemp['paddr'] = hex(temp[3])
		dtemp['filesz'] = hex(temp[4])
		dtemp['memsz'] = hex(temp[5])
		dtemp['flags'] = hex(temp[6])
		dtemp['align'] = hex(temp[7])

		header['ph'].append(dtemp)

	return header

if __name__ == '__main__':
	for k,v in elf('test').items():
		if type(v) == type([]):
			for dl in v:
				for k1,v1 in dl.items():
					print('\t',k1,':',v1)
				print('\n')
		else:
			print(k,':',v)
