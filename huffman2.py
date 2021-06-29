#!/usr/local/bin/python3
import sys
import argparse

class Tree:
	def __init__(self,Value_left,Value_right,Value_current):
		self.left = Value_left
		self.right = Value_right
		self.Value_current = Value_current
	
	def get_current(self): 
		return self.Value_current

	def set_current(self,current):
		self.current = current

	def get_left(self):
		return self.left
	
	def get_right(self):
		return self.right

	def set_left(self,left):
		self.left = left

	def set_right(self,right):
		self.right = right

class Huffman(Tree):
	def __init__(self):
		self.tree = None
		self.list_of_char = None
		self.data = None
		self.info = ''

	def set_tree(self,tree):
		self.tree = tree
	
	def get_tree(self):
		return self.tree
	
	def set_list_of_char(self,list_char):
		self.list_of_char = list_char

	def get_list_of_char(self):
		return self.list_of_char

	def set_data(self,data):
		self.data = data
	
	def get_data(self):
		return self.data

	def set_info(self,info):
		self.info = info
	
	def get_info(self):
		return self.info

def build_tree(text_input):
    
	characters = '\'"AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz 1234567890!@#$%^&*()-_+={}[]\|<>,.?/~`\n'
	
	count_char = []
	node = []
	
	for i in characters:
		if i in text_input:
			count_char.append([i,text_input.count(i)])
	
	count_char.sort(key = lambda x: x[1])

	for i in count_char:
		node.append(Tree(None,None,i))

	tree = node
	
	while(len(tree))>1:
		if(isinstance(tree[0].get_current(),list) and isinstance(tree[1].get_current(),list)):
			newCurrent = tree[0].get_current()[1] + tree[1].get_current()[1]
			if(tree[0].get_current()[1] <= tree[1].get_current()[1]):
				newLeft,newRight = tree[0],tree[1]
			else:
				newLeft,newRight = tree[1],tree[0]
			
			newTree = Tree(newLeft,newRight,newCurrent)
			tree.append(newTree)
			tree.remove(newTree.get_left())
			tree.remove(newTree.get_right())
		
		elif(isinstance(tree[0].get_current(),int) and isinstance(tree[1].get_current(),int)):
			newCurrent = tree[0].get_current() + tree[1].get_current()
			if(tree[0].get_current() <= tree[1].get_current()):
				newLeft,newRight = tree[0],tree[1]
			else:
				newLeft,newRight = tree[1],tree[0]
		
			newTree = Tree(newLeft,newRight,newCurrent)
			tree.append(newTree)
			tree.remove(newTree.get_left())
			tree.remove(newTree.get_right())
		
		elif(isinstance(tree[0].get_current(),int) and isinstance(tree[1].get_current(),list)):
			newCurrent = tree[0].get_current() + tree[1].get_current()[1]
			if(tree[0].get_current() <= tree[1].get_current()[1]):
				newLeft,newRight = tree[0],tree[1]
			else:
				newLeft,newRight = tree[1],tree[0]
			
			newTree = Tree(newLeft,newRight,newCurrent)
			tree.append(newTree)
			tree.remove(newTree.get_left())
			tree.remove(newTree.get_right())
		
		elif(isinstance(tree[0].get_current(),list) and isinstance(tree[1].get_current(),int)):
			newCurrent = tree[0].get_current()[1] + tree[1].get_current()
			if(tree[0].get_current()[1] <= tree[1].get_current()):
				newLeft,newRight = tree[0],tree[1]
			else:
				newLeft,newRight = tree[1],tree[0]
			
			newTree = Tree(newLeft,newRight,newCurrent)
			tree.append(newTree)
			tree.remove(newTree.get_left())
			tree.remove(newTree.get_right())
		
		tree.sort(key=lambda x : x.get_current() if(isinstance(x.get_current(), int)) else x.get_current()[1])
	
	obj = Huffman()
	obj.set_tree(tree[0])
	obj.set_list_of_char(count_char)
	obj.set_data([tree[0],count_char])
	return (tree[0],count_char)

def traverse_tree(data,left,right,Value,total_letter_list):
	if(len(total_letter_list) == len(data[1])):
		return total_letter_list
	if left:
		Value=Value+'0'
	if right:
		Value=Value+'1'

	if(isinstance(data[0].get_current(),int)):
		if(isinstance(data[0].get_left().get_current(),list)):
			for i in data[1]:
				if(i[0] == data[0].get_left().get_current()[0]):
					if[i[0],str(Value)+'0'] not in total_letter_list:
						total_letter_list.append([i[0],str(Value) + '0'])
		if(isinstance(data[0].get_right().get_current(),list)):
			for i in data[1]:
				if(i[0] == data[0].get_right().get_current()[0]):
					if[i[0],str(Value)+'1'] not in total_letter_list:
						total_letter_list.append([i[0],str(Value) + '1'])
		return traverse_tree([data[0].get_left(),data[1]],True,False,Value,total_letter_list) or traverse_tree([data[0].get_right(),data[1]],False,True,Value,total_letter_list)  

def get_encoded_text(text,charecters_list):
	encoded_text = ''
	for char in text:
		for i in charecters_list:
			if char == i[0]:
				encoded_text += i[1]
		
	return encoded_text

def encode(input_file, output_file):
	print("encoding ", input_file, output_file)
	
	with open(input_file,'r+') as inp_file,open(output_file,'wb') as out_file:
		text = inp_file.read()
		text = text
		
		tree = build_tree(text)
		
		code_list = traverse_tree(tree,None,None,'',[])
		
		obj1 = Huffman()
		obj1.set_tree(tree)
		obj1.set_list_of_char(code_list)
		
		
		dictonary = {}
		for i in code_list:
			dictonary.update({i[0]:i[1]})
		sorted_dict = sorted(dictonary.items(), key=lambda x: len(x[1]),reverse =True)
		for i in sorted_dict:
			if(i[0] == '\n'):
				out_file.write("\N" + ":" +i[1]+" ")	
				continue
			out_file.write(i[0] + ":" +i[1]+" ")
		encoded = get_encoded_text(text,code_list)
		out_file.write('\n')
		out_file.write(encoded)

		
	
def decode(input_file, output_file):
	print("decoding ", input_file, output_file)
	
	with open(input_file,'r') as inp_file,open(output_file,'w') as out_file:
		dic = {}
		file_info = inp_file.readlines()
		codes = file_info[0].split(' ')
		binary = file_info[1]
		out_str = ''
		for i in codes:
			if len(i) <= 1:
				codes.remove(i)
		
		for i in codes:	
			kv = i.split(':')
			if(len(kv[0]) == 0):
				kv[0] = ' '
			dic.update({kv[1]:kv[0]})
		sorted_dict = sorted(dic.items(), key=lambda x: len(x[0]),reverse =True)
		
		while(len(binary) != 0):
			for i in sorted_dict:
				l = len(i[0])
				if(i[0] == (binary[0:l])):
					if(i[1] == '\\N'):
						out_file.write('\n')
						binary = binary[l:]	
						continue
					out_file.write(i[1])
					binary = binary[l:]		
		
		out_file.write(out_str)

	
def get_options(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(description="Huffman compression.")
	groups = parser.add_mutually_exclusive_group(required=True)
	groups.add_argument("-e", type=str, help="Encode files")
	groups.add_argument("-d", type=str, help="Decode files")
	parser.add_argument("-o", type=str, help="Write encoded/decoded file", required=True)
	options = parser.parse_args()
	return options


if __name__ == "__main__":
	options = get_options()
	if options.e is not None:
		encode(options.e, options.o)
	if options.d is not None:
		decode(options.d, options.o)
