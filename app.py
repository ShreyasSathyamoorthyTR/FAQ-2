from flask import Flask,render_template, request

from utils import  establish_connection,close_connection,access_cache,update_cache,get_data_in_format_areas,get_data_in_format_subareas,capital_each

app = Flask(__name__)

@app.route('/')
def main_page():
    cur,conn=establish_connection()
    cur.execute('SELECT area FROM area_new')
    areas_wrong_format=cur.fetchall()
    practice_areas=get_data_in_format_areas(areas_wrong_format)
    dic={"practice_areas":practice_areas}
    cache=(access_cache())
    cache=[(dic)]
    update_cache(cache)
    close_connection(cur,conn)
    return render_template('index.html',areas=practice_areas)


@app.route('/', methods=['POST'])
def subareas():
    area=request.form.get('main_area')
    cache=(access_cache())
    cache[0]["selected_practice_areas"]=area
    selected_sub_area=request.form.get('sub_area')
    question_count=request.form.get('question_count')
    cache[0]["selected_sub_practice_areas"]=selected_sub_area
    cache[0]["question_count"]=str(question_count)
    cache[0]["prompt1"]=f"Please generate a list of 10 frequently asked questions and answers about {selected_sub_area} that falls under {area} in the law field. Each question should be formatted in an <h1> tag and each answer should be formatted in an <h2> tag. Ensure the questions and answers address various aspects relevant to clients seeking legal assistance, including how different practice areas and sub-practice areas of law firms manage these issues."
    if len((cache[0]["selected_sub_practice_areas"]).strip())<=2:
        cache[0]["prompt1"]=cache[0]["prompt1"].replace(" that falls under ","")
        cache[0]['prompt2']=""
    else:
        cache[0]['prompt2']=f'''Does {selected_sub_area} come under {area}? <h1>Yes</h1><!-- If the answer is yes, the content ends here --><h1>No</h1><h2>Under Which practice area does that sub practice area come under, specify only the practice area name</h2>'''   
    update_cache(cache)
    return cache[0]

if __name__ == '__main__':
    app.run(port=5001)


