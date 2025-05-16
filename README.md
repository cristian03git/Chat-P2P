# 💬 CHAT P2P - Peer-to-Peer con Interfaccia Grafica.

Questa è un'applicazione di Chat Peer-to-Peer (P2P) scritta in **_Python_**, con un'interfaccia moderna realizzata con **CustomTkinter**. Consente a più utenti di chattare tra loro tramite connessione socket, **senza bisogno di un server centrale**.


## 🧰 Requisiti.
Essendo stata scritta in Python, è ovvio che si deve avere Python nella versione 3.8 o superiore, in quanto sono necessarie le seguenti librerie:
- _`customtkinter`_;
- _`tkinter`_ (_già incluso in Python_);
- _`urllib.request`_ (_già incluso_);
- _`socket`_, _`threading`_, _`datetime`_, _`platform`_, _`sys`_, _`os`_(_già inclusi_);
Quindi, laddove non fosse presente, bisogna installare CustomTkinter:

```bash
pip install customtkinter
```


## 🚀 Avvio dell'applicazione.
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


## 📁 Struttura del progetto
```
p2pchat.py     # Codice sorgente principale dell'applicazione
README.md      # Documentazione e guida d'uso
```


## ⚠️ Avvertenze
- Nessuna cifratura è implementata: la comunicazione, difatti, **_non è sicura_** per uso pubblico.
- L'app è pensata per test, esercitazione o uso in reti locali; si può provare ad utilizzarla/implementarla per una connessione a più dispositivi, con reti differenti.


## 📌 Possibili miglioramenti futuri:
- 🔒 Cifratura end-to-end dei messaggi (AES/RSA)
- 📁 Invio file e immagini
- 👤 Aggiunta avatar o colori personalizzati per utenti
- 🌍 Visualizzazione geolocalizzazione peer


## 👨‍💻 Autore: Cristian Buttaro.