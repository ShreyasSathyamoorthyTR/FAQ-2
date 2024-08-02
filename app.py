from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from utils import  execute_query,access_cache,update_cache,get_data_in_format_areas,capital_each

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def main_page():
    areas_wrong_format = execute_query('SELECT area FROM area_new')
    practice_areas = get_data_in_format_areas(areas_wrong_format)
    cache = [{}]
    update_cache(cache)
    return render_template('index.html', areas=practice_areas)

@app.route('/', methods=['POST'])
def subareas():
    cache = access_cache()
    selected_sub_area = request.form.get('sub_area')
    question_count = request.form.get('question_count')
    cache[0]["question_count"] = str(question_count)
    practice_area = cache[0].get("selected_practice_areas", "")  
    prompt1 = (f"Please generate a list of {question_count} frequently asked questions and answers about {selected_sub_area} that falls under {practice_area} in the law field. Each question should be formatted in an <h1> tag and each answer should be formatted in an <h2> tag. Ensure the questions and answers address various aspects relevant to clients seeking legal assistance, including how different practice areas and sub-practice areas of law firms manage these issues.")
    cache[0]["prompt1"] = prompt1
    cache[0]["selected_sub_practice_areas"] = capital_each(selected_sub_area)
    if len(cache[0]["selected_sub_practice_areas"].strip()) <= 2:
        cache[0]["prompt1"] = prompt1.replace(" that falls under ", "")
        cache[0]['prompt2'] = ""
    else:
        cache[0]['prompt2'] = (f'''Does {selected_sub_area} come under {practice_area}? <h1>Yes</h1><If the answer is yes, the content ends here <h1>No</h1><h2>Under Which practice area does that sub practice area come under, specify only the practice area name</h2>''')
    update_cache(cache)
    return cache[0]

@socketio.on('message')
def handle_message(message):
    cache = access_cache()
    cache[0]["selected_practice_areas"] = message
    update_cache(cache)
    query = "SELECT specific_category FROM prompt_areas WHERE area = %s"
    subareas = execute_query(query, (message,))
    if subareas:
        subareas = subareas[0][0]
    emit('response', {'items': subareas})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
