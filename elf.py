#!/usr/bin/env python3
# author: vap0r
# github: github.com/qq53

import struct
import os

def choose(d, i):
	for k,v in d.items():
		if v == i:
			return k
	return ''

def choose_bit(d, i):
	result = ''
	for k,v in d.items():
		if v & i:
			result += k
	return result

def get_cstr(s):
	s = s.decode('ascii')
	return s[:s.find('\x00')]

def trace_elf(cmd):
	return os.popen(cmd).readlines()

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

		td = {
			'NULL': 0,
			'LOAD': 1,
			'DYNAMIC': 2,
			'INTERP': 3,
			'NOTE': 4,
			'SHLIB': 5,
			'PHDR': 6,
			'TLS': 7,
			'NUM': 8,
			'LOOS': 0x60000000,
			'GNU_EH_FRAME': 0x6474e550,
			'GNU_STACK': 0x6474e551,
			'GNU_RELRO': 0x6474e552,
			'SUNWBSS': 0x6ffffffa,
			'SUNWSTACK': 0x6ffffffb
		}
		dtemp['type'] = choose(td, temp[0])

		fd = {
			'X': 1<<0,
			'W': 1<<1,
			'R': 1<<2,
			'o': 0x0ff00000,
			'p': 0xf0000000
		}
		dtemp['flags'] = choose_bit(fd,temp[1])[::-1]
		dtemp['offset'] = hex(temp[2])
		dtemp['vaddr'] = hex(temp[3])
		dtemp['paddr'] = hex(temp[4])
		dtemp['filesz'] = hex(temp[5])
		dtemp['memsz'] = hex(temp[6])
		dtemp['align'] = hex(temp[7])

		header['ph'].append(dtemp)

	f.close()
	f = open(tmpf, 'rb')
	soff = int(header['shoff'],16)
	d = f.read()
	data = d[soff:]

	i = int(header['shstrndx'],16)
	if header['class'] == '32':
		l = struct.calcsize('10I')
		temp = struct.unpack('10I',data[i*l:i*l+l])
	elif header['class'] == '64':
		l = struct.calcsize('2I4Q2I2Q')
		temp = struct.unpack('2I4Q2I2Q',data[i*l:i*l+l])
	soff = temp[4]
	size = temp[5]
	tbl = d[soff:soff+size]

	header['sh'] = []

	rodata_addr = ''
	rodata_size = ''
	for i in range(int(header['shnum'],16)):
		if header['class'] == '32':
			l = struct.calcsize('10I')
			temp = struct.unpack('10I',data[i*l:i*l+l])
		elif header['class'] == '64':
			l = struct.calcsize('2I4Q2I2Q')
			temp = struct.unpack('2I4Q2I2Q',data[i*l:i*l+l])
		dtemp = {}
		dtemp['name'] = get_cstr(tbl[temp[0]:])
		td = {
			'NULL': 0,
			'PROGBITS': 1,
			'SYMTAB': 2,
			'STRTAB': 3,
			'RELA': 4,
			'HASH': 5,
			'DYNAMIC': 6,
			'NOTE': 7,
			'NOBITS': 8,
			'REL': 9,
			'SHLIB': 10,
			'DYNSYM': 11,
			'INIT_ARRAY': 14,
			'FINI_ARRAY': 15,
			'PREINIT_ARRAY': 16,
			'GROUP': 17,
			'SYMTAB_SHNDX': 18,
			'NUM': 19,
			'LOOS': 0x60000000,
			'GNU_ATTRIBUTES': 0x6ffffff5,
			'GNU_HASH': 0x6ffffff6,
			'GNU_LIBLIST': 0x6ffffff7,
			'CHECKSUM': 0x6ffffff8,
			'SUMW_move': 0x6ffffffa,
			'SUNW_COMDAT': 0x6ffffffb,
			'SUNW_syminfo': 0x6ffffffc,
			'GNU_verdef': 0x6ffffffd,
			'GNU_verneed': 0x6ffffffe,
			'GNU_versym': 0x6fffffff,
		}
		dtemp['type'] = choose(td,temp[1])

		fd = {
			'W': 1<<0,
			'A': 1<<1,
			'X': 1<<2,
			'M': 1<<4,
			'S': 1<<5,
			'I': 1<<6,
			'L': 1<<7,
			'O': 1<<8,
			'G': 1<<9,
			'T': 1<<10,
			'o': 0x0ff00000,
			'p': 0xf0000000,
		}
		dtemp['flags'] = choose_bit(fd,temp[2])[::-1]
		dtemp['addr'] = hex(temp[3])
		dtemp['offset'] = hex(temp[4])
		dtemp['size'] = hex(temp[5])
		dtemp['link'] = hex(temp[6])
		dtemp['info'] = hex(temp[7])
		dtemp['addralign'] = hex(temp[8])
		dtemp['entsize'] = hex(temp[9])
		if dtemp['name'] == '.rodata':
			rodata_addr = str(int(dtemp['addr'],16))
			rodata_size = str(int(dtemp['size'],16))

		header['sh'].append(dtemp)

	cmd = ' '.join(['./tracer/tracer'+header['class'],tmpf,rodata_addr,rodata_size])
	header['pss'] = trace_elf(cmd)

	return header

def print_var(var):
	t = type(var)
	if t == type([]):
		for i in var:
			print_var(i)
	elif t == type({}):
		for k,v in var.items():
			print(k,':')
			print_var(v)
	else:
		print(var)

if __name__ == '__main__':
	print_var(elf('tracer/test32'))
