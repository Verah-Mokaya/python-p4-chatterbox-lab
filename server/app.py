from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages')
def messages():
    return ''

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

@app.route('/messages', methods=['GET', 'POST', 'PATCH', 'DELETE'])
def messages_handler():
    if request.method == 'GET':
        messages = Message.query.all()
        messages_list = [message.to_dict() for message in messages]
        response = make_response(
            jsonify(messages_list),
            200
        )
        return response

    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            content=data.get('content'),
            author=data.get('author')
        )
        db.session.add(new_message)
        db.session.commit()
        response = make_response(
            jsonify(new_message.to_dict()),
            201
        )
        return response

    elif request.method == 'PATCH':
        data = request.get_json()
        message_id = data.get('id')
        message = Message.query.get(message_id)
        if message:
            message.content = data.get('content', message.content)
            message.author = data.get('author', message.author)
            db.session.commit()
            response = make_response(
                jsonify(message.to_dict()),
                200
            )
            return response
        else:
            response = make_response(
                jsonify({'error': 'Message not found'}),
                404
            )
            return response

    elif request.method == 'DELETE':
        data = request.get_json()
        message_id = data.get('id')
        message = Message.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            response = make_response(
                jsonify({'message': 'Message deleted'}),
                200
            )
            return response
        else:
            response = make_response(
                jsonify({'error': 'Message not found'}),
                404
            )
            return response

if __name__ == '__main__':
    app.run(port=5555)
