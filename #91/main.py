from flask import Flask, render_template
import extcolors


def extract(image_path: str) -> list:
    colors = extcolors.extract_from_path(image_path)
    return [color[0] for color in colors[0]]


app = Flask(__name__)


@app.route('/')
def homepage():
    colors = extract('123.jpg')
    return render_template('trial.html', colors=colors)


if __name__ == '__main__':
    app.run(debug=True)
