# Aplicação utilizando sockets para desenvolver chat em tempo real com Flask

## Descrição
Esta aplicação implementa um chat em tempo real desenvolvido utilizando Flask e Sockets. Com dela, é possível enviar e receber mensagens instantaneamente entre os usuários conectados, sem a necessidade de atualizar a página.

## Pré-requisitos
### Obrigatórios
O que é necessário para rodar o projeto:
- Python 3.13.1
- Navegador atualizado
- ngrok
- Biblioteca flask e extensão flask_socketio

### Versões utilizadas
- bidict==0.23.1
- blinker==1.9.0
- click==8.1.8
- colorama==0.4.6
- dnspython==2.7.0
- eventlet==0.38.2
- Flask==3.1.0
- Flask-SocketIO==5.5.1
- greenlet==3.1.1
- h11==0.14.0
- itsdangerous==2.2.0
- Jinja2==3.1.5
- MarkupSafe==3.0.2
- redis==5.2.1
- simple-websocket==1.1.0
- Werkzeug==3.1.3
- wsproto==1.2.0

## Instalação Local
Passo a passo para rodar o projeto na rede interna:
1. Certifique-se de que o seu navegador esteja atualizado

2. Verifique a versão do Python que você tem instalado. Para isso, abra o cmd e digite: 
```bash
python -v
```
Caso não tenha o Python instalado, visite a [página oficial](https://www.python.org/) e instale.
 
3. Clone o repositório:
   ```bash
   git clone https://github.com/usuario/repo.git
   ```
   Caso não saiba usar o Git, visite [visite este tutorial](https://rogerdudler.github.io/git-guide/index.pt_BR.html).

4. Instale a biblioteca *flask* e a extensão *flask_socketio*:
```bash
   pip install flask flask-socketio
   ```

5. Crie uma pasta para armazenar a aplicação e, dentro dela, crie o arquivo _app.py_. Nesse arquivo, importe as bibliotecas necessárias, defina uma rota para servir a interface do chat e configure o comportamento dos WebSockets para o envio de mensagens:
```python
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
@app.route('/')
def index():
    return render_template('index.html')
@socketio.on('message')
def handle_message(data):
    message = data['message']
    sender_name = data['senderName']
    print(f'Mensagem recebida de {sender_name}: {message}')
    emit('message', {'message': message, 'senderName': sender_name}, broadcast=True)
if __name__ == '__main__':
    socketio.run(app, debug=True)
```

6. Dentro do mesmo diretório do app.py, crie uma pasta chamada _templates_ e, nela, um arquivo _index.html_. Esse arquivo será responsável pela interface do chat:
```html
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chat em Tempo Real</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    <script src="//cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
</head>
<body>
    <div id="login-screen">
        <h1>Bem-vindo ao Chat</h1>
        <input id="username" type="text" placeholder="Digite seu nome">
        <button onclick="enterChat()">Entrar</button>
    </div>
    <main id="window" style="display: none;">
        <section id="chat-view">
            <div id="chat-box-display" class="chat-box"></div>
            <section id="chat-box-input">
                <input id="message" class="input" type="text" placeholder="Digite sua mensagem">
                <button class="send-button" onclick="sendMessage()">Enviar</button>
            </section>
        </section>
    </main>
    <script>
        const socket = io();
        let username = '';
        function enterChat() {
            const inputUsername = document.getElementById('username').value.trim();
            if (inputUsername) {
                username = inputUsername;
                document.getElementById('login-screen').style.display = 'none';
                document.getElementById('window').style.display = 'block';
            } else {
                alert('Por favor, insira seu nome para entrar no chat.');
            }
        }
        const usernameInput = document.getElementById('username');
        usernameInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                enterChat();
            }
        });
        socket.on('message', function(data) {
            const { message, senderName } = data;
            const chatBoxDisplay = document.getElementById('chat-box-display');
            const messageElement = document.createElement('div');
            const sender = document.createElement('strong');
            sender.textContent = senderName + ': ';
            messageElement.appendChild(sender);
            messageElement.appendChild(document.createTextNode(message));
            messageElement.className = senderName === username ? 'send-message-bubble' : 'message-bubble';
            chatBoxDisplay.appendChild(messageElement);
            chatBoxDisplay.scrollTop = chatBoxDisplay.scrollHeight;
        });
        function sendMessage() {
            const inputField = document.getElementById('message');
            const message = inputField.value.trim();
            if (message) {
                socket.emit('message', { message, senderName: username });
                inputField.value = '';
            } else {
                alert('Por favor, digite uma mensagem antes de enviar.');
            }
        }
        const inputField = document.getElementById('message');
        inputField.addEventListener('keydown', function(event) {
            if (event.key === 'Enter') {
                event.preventDefault();
                sendMessage();
            }
        });
    </script>
</body>
</html>
```
7. Agora, retorne ao diretório onde está o arquivo _app.py_ e crie uma nova pasta chamada _static_.

8. Dentro da pasta _static_ crie o arquivo _style.css_, que irá estilizar a nossa aplicação:
```css
#login-screen {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #C8C2BF;
}

#login-screen h1 {
    margin-bottom: 20px;
}

#username {
    width: 300px;
    height: 40px;
    padding: 10px;
    margin-bottom: 10px;
    border: 2px solid #CCC;
    border-radius: 20px; 
    outline: none;
    text-align: center;
    font-size: 16px;
}

#username:focus {
    border-color: #7E9E53;
}

#login-screen button {
    width: 150px;
    height: 40px;
    border: none;
    border-radius: 20px; 
    background-color: #7E9E53;
    color: white;
    font-size: 16px;
    cursor: pointer;
}

#login-screen button:hover {
    background-color: #6C8A45;
}

body {
    margin: 0;
    padding: 0;
    background-color: #C8C2BF; 
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}

#window {
    position: relative;
    width: 840px;
    height: 640px;
    background-color: #FFF; 
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
    overflow: hidden; 
}

#chat-view {
    position: relative;
    height: 100%;
    display: flex;
    flex-direction: column;
}

#chat-box-display {
    flex: 1;
    padding: 1em;
    font-size: .9em;
    display: flex;
    flex-direction: column;
    overflow-y: auto; 
    background-color: #FFF; 
}

.send-message-bubble {
    align-self: flex-end; 
    margin: .5em 0;
    padding: .5em 1em;
    border-radius: 1.5em;
    background-color: #2D2E2C; 
    color: #FFF;
    max-width: 60%;
    word-wrap: break-word; 
}

.message-bubble {
    align-self: flex-start;
    margin: .5em 0;
    padding: .5em 1em;
    border-radius: 1.5em;
    background-color: #A62F60;
    color: #FFF;
    max-width: 60%;
    word-wrap: break-word;
}

#chat-box-input {
    display: flex;
    padding: .5em;
    background-color: #F0F0F0; 
    border-top: 1px solid #CCC;
}

.input {
    flex: 1;
    height: 2em;
    padding: 0 .5em;
    border: 1px solid #CCC;
    border-radius: 4px;
    margin-right: .5em;
}

.send-button {
    width: 80px;
    height: 2em;
    background-color: #7E9E53;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
```

9. Por fim, volte a pasta onde está o arquivo _app.py_, abra o cmd e digite:
```bash
python app.py
```

10. Pronto, agora é só abrir o navegador e digitar o endereço `http://127.0.0.1:5000`


### Acesso externo

1. Para que o chat seja acessado em outra rede, crie uma conta no [ngrok](https://ngrok.com/).

2. Na tela Inicial, desça até a seção _Connect_, selecione a aba _Download_ e clique no botão de _Download_ para baixar o executável.

3. Descompacte a pasta e abra o executável. Após clicar, irá abrir uma janela do cmd com diversas informações e aguardando o próximo comando.

4. Volte na página inicial do site do ngrok, e no mesmo local onde foi realizado o download, você encontrará um comando com o seu token logo abaixo. Copie tudo, cole na janela do cmd que foi aberta e tecle enter.

    O comando é neste formato: `ngrok config add-authtoken ########SEU_TOKEN_AQUI########`

5. Em seguida, digite na mesma janela do cmd o código informando seu endereço local e tecle enter:
```bash
ngrok http http://127.0.0.1:5000/
```

6. Logo abrirá uma interação com duas colunas: _Session Status_ e _Online_.

7. Na ultima linha da coluna _Online_, estará o endereço que você deve copiar para acessar a rede. Copie-o e abra no navegador em qualquer dispositivo que o chat já estará funcionando.

### Interface Web
Depois de concluir as etapas anteriores, ao acessar `http://127.0.0.1:4040`, você poderá visualizar todas as conexões e solicitações realizadas durante o uso da aplicação.

## Autoria e Contribuições
Este projeto foi desenvolvido por:
- [João Vitor Araújo](https://www.linkedin.com/in/joaovitoraj/)
- [Rafael Valverde](https://github.com/Rafousz)

Com contribuição de: [Jansen Alves](http://github.com/janseealves/)

