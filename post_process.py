import re
from database import *


# line is processed through vietocr
# here not using fuzzy

def correct_food_name_vi(food_name_vi:str):
	_regrex = r'[^a-z0-9A-Z_ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễếệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ ]'
	food_name_vi = food_name_vi.upper()
	food_name_vi = re.sub(_regrex, '', food_name_vi).strip()
	return food_name_vi.lower()

def one_bbx_1line(line: list, fuzzy, translator):
	text = line[0]
	text = text.lower()
	if is_redundant_info(text) or is_address(text) or not is_food_vn(text) or not re.search(not_dot_pattern, text):
		return False

	# here is food with no price
	text = fuzzy(text) # correct words
	text = correct_food_name_vi(text)
	translated_text = translator(text)
	
	return (text.upper(), translated_text.upper(), 'NOT GIVEN')

def two_bbx_1line(line: list, fuzzy, translator):
	text1, text2 = line[0].lower(), line[1].lower()
	if is_redundant_info(text1) or is_address(text1) or is_redundant_info(text2) or is_address(text2):
		return False # Here are 2 redundant bbx

	case = is_price(text1)
	if case: # if text1 is the price
		# food_vn = text2 # text 2 might be food
		food_vn = correct_food_name_vi(text2)
		if not is_food_vn(food_vn):
			return False
		price_corrected = correct_price(text1, case)
		food_vn = fuzzy(food_vn) # correct words
		translated_text = translator(food_vn)
		return (food_vn.upper(), translated_text.upper(), price_corrected)
	case = is_price(text2)		
	if case: # or if  text2 is the price
		# food_vn = text1
		food_vn = correct_food_name_vi(text1)
		if not is_food_vn(food_vn):
			return False
		price_corrected = correct_price(text2, case)
		food_vn = fuzzy(food_vn) # correct words
		translated_text = translator(food_vn)
		return (food_vn.upper(), translated_text.upper(), price_corrected)

	else: # If both are not price, these two boxes are noise
		return False

def many_bbx_1line(line: list, fuzzy, translator): # Only solve the case one food goes with many prices (size s, m, l)
	text = [t.lower() for t in line]
	price_ls = []
	price_ls_corrected = []
	for t in text:
		if is_redundant_info(t) or is_address(t):
			return False
		case = is_price(t)
		if case:
			price_ls.append(t)
			price_ls_corrected.append(correct_price(t, case))

	if len(price_ls) == 0: # no price founded
		return False

	for price in price_ls:
		text.remove(price) # remove all prices in original list
	# remove all food text containning dots
	food_vn_ls = []
	for food in text:
		if re.search(not_dot_pattern, food) and is_food_vn(food):
			food = correct_food_name_vi(food)
			food_vn_ls.append(food)

	# check whether the list contains 1 food or more
	if len(food_vn_ls) != 1 : # if more than 1 food or no food, giveup!
		return False

	# else there is only one food left
	food_vn = food_vn_ls[0]
	food_vn = fuzzy(food_vn) # correct words
	translated_text = translator(food_vn)

	if len(price_ls_corrected) == 1:
		return (food_vn.upper(), translated_text.upper(), price_ls_corrected[0]) 

	# Sort the price
	price_ls_corrected.sort()
	# print("Here inside function: ", food_vn, price_ls_corrected)
	# elif 2: size S, size M
	if len(price_ls_corrected) == 2:
		return [(food_vn.upper()+' SIZE S',translated_text.upper()+' SIZE S',price_ls_corrected[0]),
				(food_vn.upper()+' SIZE M',translated_text.upper()+' SIZE M',price_ls_corrected[1])]
	# elif 3: size S, size M, size L		
	if len(price_ls_corrected) == 3:
		return [(food_vn.upper()+' SIZE S', translated_text.upper()+' SIZE S', price_ls_corrected[0]),
				(food_vn.upper()+' SIZE M', translated_text.upper()+' SIZE M', price_ls_corrected[1])
				(food_vn.upper()+' SIZE L', translated_text.upper()+' SIZE L', price_ls_corrected[2])]
	return False


'''
term1 = 'cá chim ... .'
print(re.search(not_dot_pattern, term1))
'''

def correct_price(text: str, case: int):
	if case == 1:
		text = text.replace(' ', '').replace('k', '000').replace('o','0')
		text_emp = ''
		for t in text:
			if t.isdecimal():
				text_emp += t
			else:
				break
		return text_emp

	elif case == 2:
		text = text.replace(' ', '').replace('.', '').replace('o','0')
		text_emp = ''
		for t in text:
			if t.isdecimal():
				text_emp += t
			else:
				break
		return text_emp

	elif case == 3:
		return 'NOT GIVEN'

	elif case == 4:
		text = text.replace(' ', '').replace('o','0')
		text += '000'
		return text

	else:
		return False

def is_price(text: str):
	if re.fullmatch(price_pattern1, text):
		return int(1)
	elif re.fullmatch(price_pattern2, text):
		return int(2)
	elif re.fullmatch(price_pattern3, text):
		return int(3)
	elif re.fullmatch(price_pattern4, text):
		return int(4)
	else:
		return False

def is_redundant_info(term: str):
	return any(e in term for e in Database.redundant)

def is_address(term: str):
	return re.match(address_pattern, term)

def is_food_vn(term: str):
	return any(e in term for e in Database.vietnamese_pattern)
