import psycopg2

hostname='localhost'
database='dump'
username='postgres'
pwd='password'
port_id=5432


extracted_data_cache = {}

from flask import session, request

def establish_connection():
    conn=psycopg2.connect(host=hostname, dbname=database, user=username, password=pwd, port=port_id)
    cur = conn.cursor()
    conn.autocommit= True
    return cur,conn

def close_connection(cur,conn):
    cur.close()
    conn.close()
    
def access_cache():
    session_id = session.get('session_id')
    extracted_data = extracted_data_cache.get(session_id, [])
    return extracted_data

def update_cache(extracted_data):
    session_id = request.cookies.get('session_id')
    extracted_data_cache[session_id] = extracted_data

def get_data_in_format_areas(area):
    areas=[]
    [areas.append(i[0]) for i in area]
    return areas

def get_data_in_format_subareas(are):
    areas=[]
    for i in list((are).split(',')):
        areas.append((capital_each((i[1:-1].capitalize()).replace('-'," "))))
    return areas
        
def capital_each(text):
    return (" ").join(i.capitalize() for i in text.split(" "))
