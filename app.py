from flask import Flask, render_template, request
from transformers import pipeline
app = Flask(__name__)
generator = pipeline("text-generation", model="gpt2")
def generate_story(prompt):
    try:
        result = generator(prompt, max_length=250, num_return_sequences=1, clean_up_tokenization_spaces=True)
        story = result[0]["generated_text"]
        story = story.replace("\n", " ").strip()
        if '.' in story:
            story = story[:story.rfind('.') + 1]
        return story
    except Exception as e:
        return f"Error: {e}"
@app.route("/", methods=["GET", "POST"])
def index():
    story = ""
    if request.method == "POST":
        prompt = request.form.get("prompt", "")
        if prompt:
            story = generate_story(prompt)
    return render_template("index.html", story=story)
if __name__ == "__main__":
    app.run(debug=True)
