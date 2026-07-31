# ai_stylist_backend.py
import pandas as pd
import pickle

# Load dataset
df = pd.read_csv("ai_stylist_full_dataset.csv")

# Add a body shape column if missing
def estimate_body_shape(height, weight, gender):
    bmi = weight / ((height / 100) ** 2)
    if gender.lower() == 'female':
        if bmi < 18.5:
            return 'rectangle'
        elif bmi < 24:
            return 'pear'
        elif bmi < 28:
            return 'hourglass'
        else:
            return 'apple'
    else:
        if bmi < 20:
            return 'rectangle'
        elif bmi < 25:
            return 'triangle'
        elif bmi < 30:
            return 'inverted'
        else:
            return 'oval'

# Add body_shape column if not present
if 'body_shape' not in df.columns:
    df['body_shape'] = df.apply(
        lambda row: estimate_body_shape(row['height_cm'], row['weight_kg'], row['gender']),
        axis=1
    )

def time_color_hint(time_of_day):
    """Return color tone suggestion for time of day."""
    t = str(time_of_day).lower()
    if t in ['morning', 'day']:
        return "lighter / pastel tones recommended"
    if t == 'evening':
        return "vibrant / bright tones recommended"
    if t == 'night':
        return "darker / richer tones recommended"
    return "neutral tones recommended"

def recommend_outfits(gender, height, weight, skin_tone, event_type,
                      dress_code=None, time_of_day=None, style_preference=None, top_n=3):
    """Return top outfit recommendations based on multiple filters."""
    user_body_shape = estimate_body_shape(height, weight, gender)
    candidates = df.copy()
    candidates = candidates[candidates['gender'].str.lower() == gender.lower()].copy()

    def score_row(row):
        score = 0
        if row['event_type'].lower() == event_type.lower():
            score += 3
        if dress_code and row['dress_code'].lower() == dress_code.lower():
            score += 2
        if time_of_day and row['time_of_day'].lower() == time_of_day.lower():
            score += 1
        if style_preference and row['style_preference'].lower() == style_preference.lower():
            score += 2
        if row['skin_tone'].lower() == skin_tone.lower():
            score += 1
        if 'body_shape' in row and row['body_shape'].lower() == user_body_shape.lower():
            score += 2
        return score

    candidates['score'] = candidates.apply(score_row, axis=1)
    candidates = candidates.sort_values(by='score', ascending=False)
    top = candidates.head(top_n)

    # If no match found, pick random
    if top['score'].max() == 0:
        top = df[df['gender'].str.lower() == gender.lower()].sample(n=min(top_n, len(df)))

    return top, user_body_shape

# Optional pickle save (for other integrations)
with open("ai_stylist_model.pkl", "wb") as f:
    pickle.dump({"df": df}, f)

print("✅ Backend loaded successfully (ai_stylist_backend.py)")
