from flask import request

app = Flask(__name)
@app.route("/main", methods=["POST"], strict_slashes=False)

def handle_guess():
    to_handle_data = request.get_json()
    db = SQLAlchemy()
    db.session.add(new_todo)
    db.session.commit()

    return 'Processed fine!', 201

if __name__ == '__main__':
    app.run(host='10.194.180.160')
