# 🇮🇹 💬 CHAT P2P (Peer-to-Peer) con Interfaccia Grafica.

## 👨‍💻 Autore: Cristian Buttaro.
Questa è un'applicazione di Chat Peer-to-Peer (P2P) scritta in **_Python_**, con un'interfaccia moderna realizzata con **CustomTkinter**. <br>Consente a più utenti di chattare tra loro tramite connessione socket, **senza bisogno di un server centrale**.


## 🧰 Requisiti.
Essendo stata scritta in Python, è ovvio che si deve avere Python nella versione 3.8 o superiore, in quanto sono necessarie le seguenti librerie:
- _`customtkinter`_;
- _`tkinter`_ (_già incluso in Python_);
- _`urllib.request`_ (_già incluso_);
- _`socket`_, _`threading`_, _`datetime`_, _`platform`_, _`sys`_, _`os`_(_già inclusi_);<br>
Quindi, laddove non fosse presente, bisogna installare CustomTkinter:

```bash
pip install customtkinter
```


## 🚀 Avvio dell'applicazione.
L'avvio dell'applicazione prevede la creazione di un peer; per effettuare la connessione tra due o più peer, bisogna crearne ulteriori.<br>
In virtù di questo bisogna seguire la seguente procedura.
1. Bisogna assicurarsi che tutti i peer si trovano sulla **stessa rete** (_LAN o internet con IP pubblico_);
2. Per avviare il programma:

```bash
python p2pchat.py
```

3. Inserire il proprio **username** nella finestra di dialogo iniziale.


## 🖥️ Funzionalità dell'interfaccia.
- **HEADER**: Mostra l'username e la porta in ascolto.
- **IP LOCALE E PUBBLICO**: Visibili nella parte alta della finestra.
- **MESSAGGI**:
    - I propri messaggi compaiono a destra, con sfondo verde.
    - Quelli ricevuti vengono posizionati a sinistra.
    - I messaggi di sistema sono centrati.
- **LISTA DEI PEER CONNESSI**: laterale, aggiornata dinamicamente agli ingressi dei nuovi peer.
- **INPUT DEI MESSAGGI**:
    - Scrivere nella casella inferiore.
    - Premere `Invio` per inviare.
    - `Shift+Invio`per andare a capo.


## 🌐 Come effettuare la connessione a un peer.
1. Recuperare l'indirizzo **_IP:PORTA_** del peer a cui ci si vuole collegare; se si fa su un unico dispositivo e si aprino più peer con più terminali, basta usare il bottone **📋 Copia IP** del peer a cui ci si vuole collegare.
2. Bisogna inserire nel campo sotto alla chat (ad esempio: `192.168.1.5:5000`); si può anche usare **📥 Incolla IP**, dato che l'indirizzo IP:PORTA è negli appunti.
3. Cliccando su **🔗 Connetti a peer**, l'utente effettua la connessione a quel peer desiderato.


## 🎨 Tema grafico.
Si può cambiare l'aspetto tra il tema **_light_** e **_dark_** cliccando sul pulsante **🌞 Cambia Tema 🌙**.


## 🔊 Notifiche audio.
Si può avere un suono per ogni messaggio che si invia, ma ciò dipende da ogni sistema operativo:
- **Windows**: suono di sistema.
- **macOS**: suono `Pop.aiff`.
- **Linux/Unix o Altri**: stampa `🔔 Nuovo messaggio` nel terminale.


## ❌ Uscita dall'app.
Si può chiudere l'app, chiudendo direttamente la finestra della GUI.
Con la chiusura della finestra di quel determinato peer, vengono terminate le connessioni con gli altri peer, in modo sicuro; così anche se si ha un unico peer attivo.


## 📁 Struttura del progetto.
```
p2pchat.py     #Codice sorgente principale dell'applicazione
README.md      #Documentazione e guida d'uso
```


## ⚠️ Avvertenze
- Nessuna cifratura è implementata: la comunicazione, difatti, **_non è sicura_** per uso pubblico.
- L'app è pensata per test, esercitazione o uso in reti locali; si può provare ad utilizzarla/implementarla per una connessione a più dispositivi, con reti differenti.


## 📌 Possibili miglioramenti futuri:
- 🔒 Cifratura end-to-end dei messaggi (AES/RSA);
- 📁 Invio file e immagini;
- 👤 Aggiunta avatar o colori personalizzati per utenti;
- 🌍 Visualizzazione geolocalizzazione peer.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# 🇬🇧 💬 P2P Chat with Graphical Interface. 
## 👨‍💻 Author: Cristian Buttaro.
This is a **_Python_** Peer-to-Peer (P2P) Chat application with a modern interface built using **CustomTkinter**.<br>It allows multiple users to chat with each other via socket connection, **without the need for a central server**.


## 🧰 Requirements.
Since it’s written in Python, you’ll need Python version 3.8 or higher. The following libraries are required:
- _`customtkinter`_;
- _`tkinter`_ (_already included with Python_);
- _`urllib.request`_ (_already included_);
- _`socket`_, _`threading`_, _`datetime`_, _`platform`_, _`sys`_, _`os`_(_all included_);<br>
So, if not already installed, you need to install CustomTkinter:

```bash
pip install customtkinter
```


## 🚀 Launching the Application.
Launching the application creates a peer; to establish a connection between two or more peers, additional ones must be created.<br>
Therefore, the following procedure should be followed.
1. Ensure all peers are on the **same network** _LAN or internet with public IP_);
2. To run the program:

```bash
python p2pchat.py
```

3. Enter your **username** in the initial dialog window.


## 🖥️ Interface Features.
- **HEADER**: Displays the username and listening port.
- **LOCAL AND PUBLIC IP**: Shown at the top of the window.
- **MESSAGES**:
    - Your messages appear on the right, with a green background.
    - Received messages appear on the left.
    - System messages are centered.
- **CONNECTED PEERS LIST**: Displayed on the side and dynamically updated as new peers join.
- **MESSAGE INPUT**:
    - Type in the input box at the bottom.
    - Press `Enter` to send.
    - Press `Shift+Enter` for a new line.


## 🌐 How to Connect to a Peer.
1. Obtain the **_IP:PORTA_** address of the peer you want to connect to. If you’re running multiple peers on a single device using multiple terminals, just use the **📋 Copia IP** button on the peer you want to connect to.
2. Enter the address in the field below the chat (e.g. 192.168.1.5:5000). You can also use **📥 Incolla IP** if the IP:PORT is already copied.
3. Click on **🔗 Connetti a peer** to initiate the connection.


## 🎨 Graphic Theme.
You can switch between the **_light_** and **_dark_** theme by clicking the **🌞 Cambia Tema 🌙** button.


## 🔊 Audio Notifications.
A sound can play for each sent message, depending on the operating system:
- **Windows**:  system sound;
- **macOS**: `Pop.aiff` sound.
- **Linux/Unix o Altri**: stampa `🔔 Nuovo messaggio` in the terminal.


## ❌ Exiting the App.
You can exit the app by simply closing the GUI window.<br>
When a peer window is closed, all its connections to other peers are safely terminated—even if it’s the only active peer left.


## 📁 Project Structure.
```
p2pchat.py     #Main source code of the application
README.md      #Documentation and usage guide
```


## ⚠️ Warnings.
- NNo encryption is implemented: communication is **not secure** for public use.
- The app is intended for testing, practice, or use on local networks; it can also be adapted/extended for multi-device use across different networks.


## 📌 Possible Future Improvements:
- 🔒 End-to-end encryption of messages (AES/RSA);
- 📁 File and Image transfer;
- 👤 Adding avantars or custom colors for users;
- 🌍 Peer geolocation display.
