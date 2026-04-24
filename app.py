from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assistant IA UDB</title>
    <style>
        body, html { margin: 0; padding: 0; height: 100%; font-family: Arial, sans-serif; overflow: hidden; }
        .main-layout { display: flex; height: 100vh; width: 100vw; }
        .website-container { flex: 7; border-right: 2px solid #ccc; }
        .udb-iframe { width: 100%; height: 100%; border: none; }
        .sidebar-assistant { flex: 3; display: flex; flex-direction: column; background: #f9f9f9; min-width: 350px; }
        .sidebar-header { padding: 15px; background: #fff; border-bottom: 1px solid #ddd; display: flex; align-items: center; gap: 10px; }
        .sidebar-logo { height: 60px; width: auto; }
        .sidebar-chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .msg-bubble { padding: 10px 15px; border-radius: 15px; max-width: 85%; font-size: 14px; line-height: 1.4; }
        .user { align-self: flex-end; background: #007bff; color: white; }
        .ai { align-self: flex-start; background: #eee; color: #333; white-space: pre-wrap; }
        .sidebar-input-area { padding: 15px; display: flex; gap: 10px; border-top: 1px solid #ddd; background: #fff; }
        input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 5px; }
        button { padding: 10px 15px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }

        /* ADAPTATION TELEPHONE - SOLUTION FORCEE */
@media (max-width: 768px) {
    body, html {
        overflow: hidden; /* Empêche la page entière de bouger */
        height: 100%;
    }
    .main-layout { 
        flex-direction: column; 
        height: 100vh;
    }
    .website-container { 
        flex: none; 
        height: 30vh; /* On réduit encore un peu le site */
    }
    .sidebar-assistant { 
        flex: 1; 
        height: 70vh;
        position: relative; /* Important pour le placement de l'input */
    }
    .sidebar-chat-box {
        height: calc(70vh - 70px); /* On laisse pile la place pour l'input */
        overflow-y: auto;
        padding-bottom: 80px; /* Espace de sécurité */
    }
    .sidebar-input-area {
        position: fixed; /* SOLUTION RADICALE : Fixé au bas de l'écran */
        bottom: 0;
        left: 0;
        right: 0;
        width: 100%;
        background: #fff;
        z-index: 9999; /* Toujours au-dessus du reste */
        border-top: 2px solid #007bff;
        padding: 10px;
        /* Ajoute la marge ici directement */
        padding-bottom: 25px; 
        box-sizing: border-box;
        
    }
}
    </style>
</head>
<body>
    <div class="main-layout">
        <div class="website-container">
            <iframe src="https://udb-sn.com/index.php?u=Presentation" class="udb-iframe"></iframe>
        </div>
        <div class="sidebar-assistant">
            <div class="sidebar-header">
                <img src="https://udb-sn.com/images/logo.png" class="sidebar-logo">
                <div><strong>Assistant IA UDB</strong></div>
            </div>
            <div id="chat-box" class="sidebar-chat-box">
                <div class="msg-bubble ai">Bienvenue ! Comment puis-je vous aider ?</div>
            </div>
            <div class="sidebar-input-area">
                <input type="text" id="user-input" placeholder="Posez votre question..." onkeydown="if(event.key === 'Enter') sendMessage()">
                <button onclick="sendMessage()">➤</button>
            </div>
        </div>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const chatBox = document.getElementById('chat-box');
            if (!input.value.trim()) return;

            const query = input.value;
            chatBox.innerHTML += `<div class="msg-bubble user">${query}</div>`;
            
            const aiMsg = document.createElement('div');
            aiMsg.className = 'msg-bubble ai';
            aiMsg.innerText = "Recherche en cours...";
            chatBox.appendChild(aiMsg);

            input.value = "";
            chatBox.scrollTop = chatBox.scrollHeight;

            try {
                const response = await fetch("http://13.39.8.176:8000/ask", {
                    method: "POST",
                    mode: "cors", // Ajoute cette ligne
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ query: query })
                });

                const reader = response.body.getReader();
                aiMsg.innerText = ""; 

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    aiMsg.innerText += new TextDecoder().decode(value);
                    chatBox.scrollTop = chatBox.scrollHeight;
                }
            } catch (e) {
                aiMsg.innerText = "Erreur : Le serveur ne répond pas.";
            }
        }
    </script>
</body>
</html>
    ''')

if __name__ == "__main__":
    app.run()
