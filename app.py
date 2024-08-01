


from flask import Flask,render_template, request

from utils import  establish_connection,close_connection,access_cache,update_cache,get_data_in_format_areas,get_data_in_format_subareas,capital_each

app = Flask(__name__)

@app.route('/')
def main_page():
    cur,conn=establish_connection()
    cur.execute('SELECT area FROM area_new')
    areas_wrong_format=cur.fetchall()
    practice_areas=get_data_in_format_areas(areas_wrong_format)
    dic={"practice_areas":practice_areas,
         "selected_practice_areas":"",
         "sub_practice_areas":[],
         "selected_sub_practice_areas":"",
         "question_count":"",
         "prompt1":"",
         "prompt2":"",
         "prompt3":""}
    cache=(access_cache())
    cache=[(dic)]
    update_cache(cache)
    close_connection(cur,conn)
    return render_template('index.html',areas=practice_areas)


@app.route('/', methods=['POST'])
def subareas():
    cur,conn=establish_connection()
    area=request.form.get('main_area')
    cache=(access_cache())
    cache[0]["selected_practice_areas"]=area
    if area in cache[0]['practice_areas']:
        cur.execute(f"SELECT specific_category FROM area_new WHERE area='{capital_each(area)}'")
        subareas=cur.fetchall()
        cache[0]["sub_practice_areas"]=get_data_in_format_subareas(subareas[0][0][0])
    else:
        cache[0]["sub_practice_areas"]=[]
    update_cache(cache)
    close_connection(cur,conn)
    selected_sub_area=request.form.get('sub_area')
    question_count=request.form.get('question_count')
    cache=(access_cache())
    cache[0]["selected_sub_practice_areas"]=selected_sub_area
    cache[0]["question_count"]=str(question_count)
    prompt=f"Give {question_count} FAQ question and answer for {selected_sub_area} under {cache[0]["selected_practice_areas"]} practice area"
    if len((cache[0]["selected_sub_practice_areas"]).strip())<=2:
        prompt=prompt.replace(" under ","")
        cache[0]["prompt2"]=""
        cache[0]["prompt3"]=""
        cache[0]["prompt3"]=""
    else:
        cache[0]["prompt2"]=f"does {selected_sub_area} comes under {cache[0]["selected_practice_areas"]}?"   #second p tag first word
        cache[0]["prompt3"]=f"{selected_sub_area} comes under which practice area?"   #first strong tag
    cache[0]["prompt1"]=prompt
    return cache

if __name__ == '__main__':
    app.run(port=5001)
