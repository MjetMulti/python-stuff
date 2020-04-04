from copy import deepcopy
import json

class Box:
	def __init__(self, row_pos = 0, col_pos = 0, width = 3, height = 3, has_border = False, content = None):
		self.row_pos = row_pos
		self.col_pos = col_pos
		self.width = width
		self.height = height
		self.has_border = has_border # the border is NOT included in width (or height)
		if content == None:
			self.clearBox()
		else:
			self.content = content
	def clearBox(self):
		self.content = [[' ' for i in range(self.width)] for j in range(self.height)]
	def addContent(self, row, col, text):
		text_list = list(text)
		if (col + len(text)) <= self.width:
			for i in range(len(text)):
				self.content[row][col + i] = text_list[i]
		

class Display:
	code_quote = "```"
	total_width = 62
	total_height = 22
	border_pieces = {"start" : ['·'],
					 "corners" : ['┌','┐','┘','└'],
					 "intersections" : ['├','┬','┤','┴','┼'],
					 "sides" : ['│','─']
					}
	top_line = border_pieces["corners"][0] + border_pieces["sides"][1] * (total_width - 2) + border_pieces["corners"][1] + '\n'
	bottom_line = border_pieces["corners"][3] + border_pieces["sides"][1] * (total_width - 2) + border_pieces["corners"][2] + '\n'
	fill_lines = border_pieces["sides"][0] + ' ' * (total_width-2) + border_pieces["sides"][0] + '\n'
	empty_box = top_line + fill_lines * (total_height - 2) + bottom_line
	
	def __init__(self, my_box = None, content = {}):
		if my_box == None:
			self.my_box = list(self.empty_box)
		else:
			self.my_box = my_box
		self.content = content
		for i in self.content:
			self.content[i] = Box(**(self.content[i]))		
	
	def boxInBox(self,row_start,row_stop,col_start,col_stop):
		complist = [item for sublist in self.border_pieces for item in self.border_pieces[sublist]]
		self.my_box[row_start * (self.total_width + 1) + col_start] = self.border_pieces["start"][0]
		for i_row in range(row_start, row_stop + 1):
			if (i_row == row_start) or (i_row == row_stop):
				for i_col in range(col_start, col_stop + 1):
					self.insertBorderCharacter(i_row, i_col, self.border_pieces, complist, True)
			else:
				self.insertBorderCharacter(i_row, col_start, self.border_pieces, complist, True)
				self.insertBorderCharacter(i_row, col_stop, self.border_pieces, complist, True)

	def insertBorderCharacter(self, row, col, border_pieces, border_pieces_list, should_iterate):
		hilf = 0
		if ((((row - 1) >= 0) and (self.my_box[(row-1)*(self.total_width+1)+col] in border_pieces_list)) and # all four sides
			(((row + 1) <= self.total_height-1) and (self.my_box[(row+1)*(self.total_width+1)+col] in border_pieces_list)) and
			(((col - 1) >= 0) and (self.my_box[row*(self.total_width+1)+col-1] in border_pieces_list)) and
			(((col + 1) <= self.total_width-1) and (self.my_box[row*(self.total_width+1)+col+1] in border_pieces_list))):
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["intersections"][4]
			if should_iterate:
				self.insertBorderCharacter(row - 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row + 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col - 1, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col + 1, border_pieces, border_pieces_list, False)
		elif ((((row + 1) <= self.total_height-1) and (self.my_box[(row+1)*(self.total_width+1)+col] in border_pieces_list)) and # not top
			(((col - 1) >= 0) and (self.my_box[row*(self.total_width+1)+col-1] in border_pieces_list)) and
			(((col + 1) <= self.total_width-1) and (self.my_box[row*(self.total_width+1)+col+1] in border_pieces_list))):
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["intersections"][1]
			if should_iterate:
				self.insertBorderCharacter(row + 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col - 1, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col + 1, border_pieces, border_pieces_list, False)
		elif ((((row - 1) >= 0) and (self.my_box[(row-1)*(self.total_width+1)+col] in border_pieces_list)) and #not right
			(((row + 1) <= self.total_height-1) and (self.my_box[(row+1)*(self.total_width+1)+col] in border_pieces_list)) and
			(((col - 1) >= 0) and (self.my_box[row*(self.total_width+1)+col-1] in border_pieces_list))):
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["intersections"][2]
			if should_iterate:
				self.insertBorderCharacter(row - 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row + 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col - 1, border_pieces, border_pieces_list, False)
		elif ((((row - 1) >= 0) and (self.my_box[(row-1)*(self.total_width+1)+col] in border_pieces_list)) and # not bottom
			(((col - 1) >= 0) and (self.my_box[row*(self.total_width+1)+col-1] in border_pieces_list)) and
			(((col + 1) <= self.total_width-1) and (self.my_box[row*(self.total_width+1)+col+1] in border_pieces_list))):
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["intersections"][3]
			if should_iterate:
				self.insertBorderCharacter(row - 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col - 1, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col + 1, border_pieces, border_pieces_list, False)
		elif ((((row - 1) >= 0) and (self.my_box[(row-1)*(self.total_width+1)+col] in border_pieces_list)) and #not left
			(((row + 1) <= self.total_height-1) and (self.my_box[(row+1)*(self.total_width+1)+col] in border_pieces_list)) and
			(((col + 1) <= self.total_width-1) and (self.my_box[row*(self.total_width+1)+col+1] in border_pieces_list))):
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["intersections"][0]
			if should_iterate:
				self.insertBorderCharacter(row - 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row + 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col + 1, border_pieces, border_pieces_list, False)
		elif ((((row + 1) <= self.total_height-1) and (self.my_box[(row+1)*(self.total_width+1)+col] in border_pieces_list)) and # right bot
			(((col + 1) <= self.total_width-1) and (self.my_box[row*(self.total_width+1)+col+1] in border_pieces_list))):
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["corners"][0]
			if should_iterate:
				self.insertBorderCharacter(row + 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col + 1, border_pieces, border_pieces_list, False)
		elif ((((row + 1) <= self.total_height-1) and (self.my_box[(row+1)*(self.total_width+1)+col] in border_pieces_list)) and# left bot
			(((col - 1) >= 0) and (self.my_box[row*(self.total_width+1)+col-1] in border_pieces_list))):
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["corners"][1]
			if should_iterate:
				self.insertBorderCharacter(row + 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col - 1, border_pieces, border_pieces_list, False)
		elif ((((row - 1) >= 0) and (self.my_box[(row-1)*(self.total_width+1)+col] in border_pieces_list)) and # left top
			(((col - 1) >= 0) and (self.my_box[row*(self.total_width+1)+col-1] in border_pieces_list))):
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["corners"][2]
			if should_iterate:
				self.insertBorderCharacter(row - 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col - 1, border_pieces, border_pieces_list, False)
		elif ((((row - 1) >= 0) and (self.my_box[(row-1)*(self.total_width+1)+col] in border_pieces_list)) and # top right
			(((col + 1) <= self.total_width-1) and (self.my_box[row*(self.total_width+1)+col+1] in border_pieces_list))):
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["corners"][3]
			if should_iterate:
				self.insertBorderCharacter(row - 1, col, border_pieces, border_pieces_list, False)
				self.insertBorderCharacter(row, col + 1, border_pieces, border_pieces_list, False)
		elif (((row - 1) >= 0) and (self.my_box[(row-1)*(self.total_width+1)+col] in border_pieces_list)): # top
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["sides"][0]
			if should_iterate:
				self.insertBorderCharacter(row - 1, col, border_pieces, border_pieces_list, False)
		elif (((row + 1) <= self.total_height-1) and (self.my_box[(row+1)*(self.total_width+1)+col] in border_pieces_list)): # bot
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["sides"][0]
			if should_iterate:
				self.insertBorderCharacter(row + 1, col, border_pieces, border_pieces_list, False)
		elif (((col - 1) >= 0) and (self.my_box[row*(self.total_width+1)+col-1] in border_pieces_list)): # left
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["sides"][1]
			if should_iterate:
				self.insertBorderCharacter(row, col - 1, border_pieces, border_pieces_list, False)
		elif (((col + 1) <= self.total_width-1) and (self.my_box[row*(self.total_width+1)+col+1] in border_pieces_list)): # right
			self.my_box[row * (self.total_width + 1) + col] = border_pieces["sides"][1]
			if should_iterate:
				self.insertBorderCharacter(row, col + 1, border_pieces, border_pieces_list, False)
		else:
			pass

	def insertContent(self): # return value can be used to print the box
		for i in self.content:
			obj = self.content[i]
			if isinstance(obj,Box):
				for j in range(obj.height):
					self.my_box[(((obj.row_pos + j) * (self.total_width + 1)) + obj.col_pos) : (((obj.row_pos + j) * (self.total_width + 1)) + obj.col_pos + obj.width)] = obj.content[j]
				self.boxInBox(obj.row_pos -1, obj.row_pos + obj.height,obj.col_pos - 1, obj.col_pos + obj.width)
		return "".join(self.my_box)
		
	def saveBox(self):
		hilf = deepcopy(vars(self))
		for i in hilf["content"]:
			if isinstance(hilf["content"][i],Box):
				hilf["content"][i] = vars(hilf["content"][i])
			else:
				del hilf["content"][i]
		with open("boxsavefile.txt", "w", encoding = 'utf-8') as file:
			json.dump(hilf, file, indent=4)
