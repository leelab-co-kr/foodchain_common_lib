# -*- coding: utf-8 -*-

from hashlib import md5
from pymongo import MongoClient

def make_md5(s, encoding='utf-8'): 
	return md5(s.encode(encoding)).hexdigest() 


def get_member(mb_table, mb_id ) : 
	if mb_id == None or mb_id == "" :
		row = { 'mb_name': '손님', 'mb_level': 0 , 'mb_id': "" }
	else :
		rows = mb_table.find({ 'mb_id': mb_id })
		for row in rows :
			break
		if row == None :
			row = { 'mb_name': '손님', 'mb_level': 0 , 'mb_id': "" }

	return row

def get_menu( cfg, menu_table, mb ) : 
	menu = {}
	if mb['mb_id'] != '' :
		mb_login = 3
	else :
		mb_login = 2

	where = { '$and': [ 
		{'me_permit': { '$lte': mb['mb_level'] } }
		,{ '$or': [ {'me_display': 1 }, { 'me_display': mb_login } ] } 
		,{ '$or': [ {'me_type2': cfg['cf_type'] }, { 'me_type2': ''} ] } 
		]}
	rows = menu_table.find( where )

	#rows = rows.sort( {'me_order': 1 } )

	menu['total'] = menu_table.find( where ).count()
	i = 0
	for row in rows :
		menu[i] = row
		i += 1
	return menu

def is_permit( co_id, cfg, menu_table, mb ) : 
	if mb['mb_id'] != '' :
		mb_login = 3
	else :
		mb_login = 2

	where = { '$and': [ 
		{'co_id': co_id }
		, {'me_permit': { '$lte': mb['mb_level'] } }
		, { '$or': [  {'me_display': 0 }, {'me_display': 1 }, { 'me_display': mb_login } ] } 
		, { '$or': [ {'me_type2': cfg['cf_type'] }, { 'me_type2': ''} ] } 
		]}
	return menu_table.find( where ).count()

def sql_fetch( _table, _where, _order ) : 
	rows = _table.find( _where )
	cnt = rows.count(  )
	'''
	if cnt > 0 :
		rows = rows.sort( _order )
		'''
	row = None
	for row in rows :
		break
	return row
