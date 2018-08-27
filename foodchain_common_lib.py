from hashlib import md5
from pymongo import MongoClient

def make_md5(s, encoding='utf-8'): 
	return md5(s.encode(encoding)).hexdigest() 


def get_member(mb_table, mb_id ) : 
	rows = mb_table.find({ 'mb_id': mb_id })
	for row in rows :
		break
	return row