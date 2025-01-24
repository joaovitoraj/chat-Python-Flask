from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

# Recebe mensagens e retransmite para todos os clientes conectados
@socketio.on('message')
def handle_message(data):
    message = data['message']
    sender_name = data['senderName']
    print(f'Mensagem recebida de {sender_name}: {message}')
    
    # Retransmitir mensagem com o nome do remetente
    emit('message', {'message': message, 'senderName': sender_name}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
