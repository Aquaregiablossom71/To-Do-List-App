from flask import Flask, render_template, request
import ai_stylist_backend as stylist

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        gender = request.form['gender']
        height = int(request.form['height'])
        weight = int(request.form['weight'])
        skin_tone = request.form['skin_tone']
        event_type = request.form['event_type']
        dress_code = request.form['dress_code']
        time_of_day = request.form['time_of_day']
        style_preference = request.form['style_preference']

        # Get recommendations from backend
        top_results, body_shape = stylist.recommend_outfits(
            gender=gender,
            height=height,
            weight=weight,
            skin_tone=skin_tone,
            event_type=event_type,
            dress_code=dress_code,
            time_of_day=time_of_day,
            style_preference=style_preference,
            top_n=3
        )

        color_hint = stylist.time_color_hint(time_of_day)

        # Convert DataFrame to list of dicts for easy rendering
        if top_results is not None:
            outfit_list = top_results.to_dict(orient='records')
        else:
            outfit_list = []

        return render_template(
            'result.html',
            body_shape=body_shape,
            color_hint=color_hint,
            outfits=outfit_list
        )

    except Exception as e:
        return render_template('result.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
