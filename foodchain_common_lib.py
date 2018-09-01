# -*- coding: utf-8 -*-
import os
import sys
import urllib.request
import json
import socket
import requests
import datetime

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

def get_local_ip_addr() :
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	ipaddr = s.getsockname()[0]
	s.close()
	return ipaddr

"""
Transaction status push 
host : http://아이피:8001
base_key :
access_token :
"""
def put_txion_status( host, base_key , access_token ) :

	local_addr = get_local_ip_addr()
	now = datetime.datetime.now()
	nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S')
	doc = {'addr':local_addr, 'datetime':nowDatetime}
	headers = { 
		'Authorization': 'Basic %s' % make_md5(base_key) , 
		'access-token': '%s' % make_md5(access_token)
	} 
	
	r = requests.post( host+'/txion_status',  json=doc , headers=headers) 
	return r.content
'''
Python에서 주소좌표변환 api를 호출
'''
def get_addr2gps( naver, addr ) :
	client_id = naver['NAVER_MAP_CLIENT_ID']
	client_secret = naver['NAVER_MAP_CLIENT_SECRET'] 
	encText = urllib.parse.quote( addr )
	url = "https://openapi.naver.com/v1/map/geocode?query=" + encText # json 결과
	# url = "https://openapi.naver.com/v1/map/geocode.xml?query=" + encText # xml 결과
	request = urllib.request.Request(url)
	request.add_header("X-Naver-Client-Id",client_id)
	request.add_header("X-Naver-Client-Secret",client_secret)
	response = urllib.request.urlopen(request)
	rescode = response.getcode()
	if(rescode==200):
		response_body = response.read()
		res = json.loads(response_body.decode('utf-8'))
		res = res['result']['items']
		res = res[0]['point']
		return str(res['y']) + "," + str(res['x'])
	else:
		return ""
