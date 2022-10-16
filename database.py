# Address, welcome term
class Database:
	redundant = [
		'xin',
		'chào',
		'mừng',
		'cảm',
		'thời',
		'phục',
		'hân',
		'rất',
		'2022',
		'menu',
		'qn',
		'quy nhơn',
		'giao',
		'sỉ',
		'lẻ',
		'cửa',
		'quán',
		'nhánh',
		'hệ',
		'khách',
		'nhà',
		'phố',
		'vỉa',
		'ẩm',
		'món',
		'dđ',
		'sđt',
		'giải',
		'địa chỉ',
		'address',
		'khác',
		'cô',
		'bà',
		'dì',
		'cậu',
		'khai',
		'các',
		'VAT'
	]
	vietnamese_pattern = [
		'à',
		'á',
		'ã',
		'ạ',
		'ả',
		'ă',
		'ắ',
		'ằ',
		'ẳ',
		'ẵ',
		'ặ',
		'â',
		'ấ',
		'ầ',
		'ẩ',
		'ẫ',
		'ậ',
		'è',
		'é',
		'ẹ',
		'ẻ',
		'ẽ',
		'ê',
		'ề',
		'ế',
		'ể',
		'ễ',
		'ệ',
		'đ',
		'ì',
		'í',
		'ĩ',
		'ỉ',
		'ị',
		'ò',
		'ó',
		'õ',
		'ọ',
		'ỏ',
		'ô',
		'ố',
		'ồ',
		'ổ',
		'ỗ',
		'ộ',
		'ơ',
		'ớ',
		'ờ',
		'ở',
		'ỡ',
		'ợ',
		'ù',
		'ú',
		'ũ',
		'ụ',
		'ủ',
		'ư',
		'ứ',
		'ừ',
		'ử',
		'ữ',
		'ự',
		'ỳ',
		'ỵ',
		'ỷ',
		'ỹ',
		'ý',
		'coca',
		'soda',
		'pepsi',
		'chocolate',
		'strong bow',
		'heineken'
	]
def check_a_phone(self):
	pass


# price pattern
part = r'(/phần|/đĩa|/dĩa|/chén|/con|/ly|/cái|/hũ|/bịch|/bịch nhỏ|/bịch lớn|/người|/cây|/tô|/lít|/kg|/lon|/chai)?'
missing_part = r'(/phân|/phan|/đìa|/đia|/dia|/dìa|/chen|/chẽn|/cãi|/hù|/hu|/bich|/ngưỡi|/ngươi|)?'
# One: ex: 5k, 123k, 7k/ly 
price_pattern1 = r'\s?\d[\do]?[\do]?\s?k\s?' + part + missing_part
# Two: ex: 30.000, 20.000 đ/con
price_pattern2 = r'\s?\d[\do]?[\do]?\s?[\.\,]([\do]){3}\s?đ?\s?' + part + missing_part
# Three: free
price_pattern3 = r'\s?theo\s?thời\s?(vụ|giá)\s?[(]?k?g?[)]?|\s?miễn\s?phí\s?'
# Foure: ex 5, 12, 13
price_pattern4 = r'\s?\d{1,3}\s?'
# not dot pattern
not_dot_pattern = r'^[^.]+$'
# address
address_pattern = r'(\d{1,3})?\s?(nguyễn|lê|trần|phạm|hoàng|ngô|đào|cao|kha|dương|cù|võ|trương|lê|hồ|chế)\s'


