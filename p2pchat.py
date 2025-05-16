#LIBRERIE USATE
import socket #Fornisce strumenti per comunicazioni di rete via socket TCP/IP.
import threading #Permette di creare e thread per eseguire codice in parallelo (ad esempio, ascolto in background).
from datetime import datetime #Per gestire date e orari, utile per il timestamp dei messaggi.
import customtkinter as ctk #Libreria GUI basata su Tkinter ma con stile moderno e personalizzabile (per tema white/dark).
from tkinter import simpledialog, messagebox #Dialoghi semplici per input utente e finestre di avviso.
import tkinter as tk #Libreria standard GUI Tkinter per widget di base (Listbox, Label, Frame ed etc.).
import platform #Fornisce informazioni sul sistema operativo in uso (per notifiche sonore diverse).
import os #Interazioni con il sistema operativo.
import sys #Accesso a variabili e funzioni di sistema, usata per controllare piattaforma in uso.
import urllib.request #Per effettuare richieste HTTP (qui per ottenere IP pubblico tramite api ipify).

# Controlla il sistema operativo in uso per definire una funzione di notifica sonora adatta.
if sys.platform.startswith("darwin"):
    #Se il sistema operativo è macOS (darwin).
    import subprocess #Importa il modulo per eseguire comandi di sistema.
    def notify():
        #Riproduce il suono di sistema "Pop" tramite il comando 'afplay'.
        subprocess.call(["afplay", "/System/Library/Sounds/Pop.aiff"])
elif sys.platform.startswith("win"):
    #Se il sistema operativo è Windows (win).
    import winsound #Importa il modulo per generare suoni di sistema.
    def notify():
        #Emette il beep di sistema predefinito.
        winsound.MessageBeep()
else:
    #Per altri sistemi (linux, Unix, etc.).
    def notify():
        #Stampa un'emoji campanella e mesaggio di notifica sulla console.
        print("🔔 Nuovo messaggio")

#Classe per creare i tooltip informativi al passaggio del mouse su un widget.
class ToolTip:
    #Inizializza il tooltip associandolo a un widget e al testo da mostrare.
    def __init__(self, widget, text):
        self.widget = widget #Widget a cui associare il tooltip (ad esempio un bottone, una label, etc.).
        self.text = text #Testo che verrà mostrato nel tooltip.
        self.tip_window = None #Variabile che conterrà la finestra tooltip (quando visibile, posizionando il puntatore su un messaggio).
        #Collego gli eventi del mouse: quando entra nel widget mostro il tooltip, quando esce lo nascondo.
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    #Fa vedere il tooltip quando il mouse entra nel widget.
    def show_tip(self, event=None):
        #Se il tooltip è già mostrato, non faccio nulla.
        if self.tip_window:
            return
        #Ottengo la posizione attuale del cursore nel widget (bbox "insert" tipicamente per Text o Entry).
        x, y, _, _ = self.widget.bbox("insert")
        #Calcolo la posizione assoluta dello tooltip (vicino al widget + offset).
        x += self.widget.winfo_rootx() + 20
        y += self.widget.winfo_rooty() + 20
        #Creo una nuova finestra top-level senza bordi e senza la barra del titolo per il tooltip.
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True) #Rimuove decorazioni della finestra.
        tw.wm_geometry(f"+{x}+{y}") #Posiziona la finestra alle coordinate calcolate.
        #Creo una label all'interno della finestra con testo e stile personalizzato per il tooltip.
        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#333333",
            foreground="white",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9, "italic"),
            padx=5,
            pady=3,
            wraplength=300 #Limito la larghezza del tooltip, con ritorno a capo automatico.
        )
        label.pack(ipadx=1) #Inserisce la label nella finestra tooltip con un piccolo padding interno.

    #Nasconde il tooltip quando il mouse esce dal widget.
    def hide_tip(self, event=None):
        #Se la finestra del tooltip è visibile, la chiudo/distruggo per nasconderla.
        if self.tip_window:
            self.tip_window.destroy()
        self.tip_window = None #Resetto la variabile della finestra del tooltip a None.

#Classe principale che gestisce la chat P2P, l'interfaccia e le connessioni.
class PeerToPeerChat:
    #Inizializza socket, GUI, connessioni e layout iniziale.
    def __init__(self, host='0.0.0.0', port=0):
        self.peers = {} #Dizionario per memorizzare le connessioni socket verso i peer connessi.
        self.usernames = {} #Dizionario per associare a ogni socket il nome utente del peer.
        #Mostra una finestra di dialogo per chiedere all'utente il proprio nome (username).
        self.username = simpledialog.askstring("Nome utente", "Inserisci il tuo username:")
        if not self.username:
            #Se non viene inserito un nome, mostra un avviso e termina il proramma.
            messagebox.showwarning("Input mancante", "Nome utente obbligatorio.")
            exit(1)

        self.host = host #Indirizzo IP su cui mettere in ascolto il server (di default imposto '0.0.0.0' per tutte le interfacce).
        self.port = port #Porta su cui ascoltare (0 significa che il sistema deciderà automaticamente una porta disponibile).

        #Creo un socket TCP IPv4 per accettare le connessioni in entrata.
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Permetto il riutilizzo immediato della porta se il programma viene riavviato.
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Associo il socket all'indirizzo IP e porta specificati.
        self.listener.bind((host, port))
        #Aggiorno la porta assegnata (utile se era 0 e il sistema ha assegnato una porta disponibile).
        self.port = self.listener.getsockname()[1]
        #Metto il socket in ascolto (in background) per nuove connessioni.
        self.listener.listen()
        #Avvio un thread in background per accettare nuove connessioni, senza bloccare la GUI.
        threading.Thread(target=self.accept_connections, daemon=True).start()

        #Provo a ottenere l'indirizzo IP locale della macchina.
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
        except:
            local_ip = 'localhost'#Se fallisce, uso localhost come fallback.
        #Provo a ottenere l'indirizzo IP pubblico usando un servizio web esterno (api ipify).
        try:
            external_ip = urllib.request.urlopen('https://api.ipify.org', timeout=5).read().decode('utf8')
        except:
            external_ip = 'N/D' #Se non riesco, segno come non disponibile.

        self.theme = "light" #Tema di default per la GUI (light mode).
        ctk.set_appearance_mode(self.theme) #Applico il tema a customtkinter.
        ctk.set_default_color_theme("green") #Imposto il tema colori di default a "green".

        #Creo la finestra principale dell'app con customtkinter.
        self.root = ctk.CTk()
        self.copy_in_progress = False #Flag per evitare più copie di seguito negli appunti di testo.
        #Imposto il titolo della finestra con username e porta in cui si è in ascolto.
        self.root.title(f"Chat P2P - {self.username} (Porta: {self.port})")
        #Imposto la dimensione iniziale della finestra.
        self.root.geometry("800x900")
        #Configuro il colore di sfondo della finestra.
        self.root.configure(bg="#f0f2f5")
        #Imposto la dimensione minima della finestra.
        self.root.minsize(700, 800)
        #Configuro il layout della finestra con righe e colonne ridimensionabili.
        self.root.rowconfigure(2, weight=2)
        self.root.columnconfigure(0, weight=1)

        #Creo una label di intestazione con testo di benvenuto e informazioni utente.
        self.header_label = ctk.CTkLabel(self.root, text=f"Benvenuto, {self.username}! (Porta: {self.port})", font=("Segoe UI", 22, "bold"))
        #Posiziono la label nella griglia, spanning su su 3 colonne, allineata a sinistra con padding.
        self.header_label.grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(15, 5))

        #Creo un frame trasparente per contenere le info sugli IP e i bottoni.
        ip_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        #Posiziono il frame sotto la header, spanning su 3 colonne, con padding.
        ip_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=20, pady=(0, 5))
        #Configuro la griglia interna del frame con pesi per le colonne (per il ridimensionamento).
        ip_frame.columnconfigure(0, weight=3) #Colonna 0 più larga (Info IP)
        ip_frame.columnconfigure(1, weight=1) #Colonna 1 (Bottone Copia IP)
        ip_frame.columnconfigure(2, weight=1) #Colonna 2 (Bottone Cambio Tema)

        #Preparo la stringa IP: porta locale per la copia negli appunti.
        ip_info = f"{local_ip}:{self.port}"
        #Label che mostra l'indirizzo IP locale e pubblico.
        self.ip_label = ctk.CTkLabel(ip_frame, text=f"📡 IP locale: {local_ip} | IP pubblico: {external_ip}", font=("Segoe UI", 12))
        #Posiziono la label nella colonna 0 allineata a sinistra.
        self.ip_label.grid(row=0, column=0, sticky="w")

        #Bottone per copiare negli appunti l'indirizzo IP locale e porta.
        self.copy_button = ctk.CTkButton(ip_frame, text="📋 Copia IP", command=lambda: self.copy_to_clipboard(ip_info), height=30)
        #Posiziono il bottone nella colonna 1, allineato a destra con paddding orizzontale.
        self.copy_button.grid(row=0, column=1, sticky="e", padx=5)

        #Bottone per cambiare il tema grafico (light/dark).
        self.theme_button = ctk.CTkButton(ip_frame, text="🌞 Cambia Tema 🌙", command=self.toggle_theme, height=30)
        #Posiziono il bottone nella colonna 2, allineato a destra con padding. 
        self.theme_button.grid(row=0, column=2, sticky="e", padx=5)

        #Creo un frame principale per contenere i messaggi e la lista dei peer connessi, con angoli arrotondati.
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=15)
        #Posiziono il frame in griglia alla riga 2, spanning su 3 colonne, con padding.
        self.main_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=15, pady=(0, 10))
        #Configuro righe e colonne del frame per ridimensionamento (più spazio ai messaggi).
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=4) #Colonna messaggi più larga.
        self.main_frame.columnconfigure(1, weight=1) #Colonna per la lista dei peer più stretta.

        #Creo un frame scrollabile per contenere i messaggi, con angoli arrotondati e colore di sfondo in base al tema.
        self.message_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            corner_radius=10,
            fg_color="#f5f5f5" if self.theme == "light" else "#1e1e1e",
            height=550
        )
        #Posiziono il frame scrollabile dei messaggi nella griglia (riga 0, colonna 0),
        #con opzioni sticky per espandersi in tutte le direzioni (nsew),
        #con padding orizzontale e verticale per distanziarlo dagli altri elementi.
        self.message_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 15), pady=10)

        #Creo una label sopra la lista dei peer connessi, con icona e testo,
        #allineata a sinistra (anchor="w") e font in grassetto dimensione 14.
        self.peer_list_label = ctk.CTkLabel(self.main_frame, text="👥 Peer connessi:", anchor="w", font=("Segoe UI", 14, "bold"))
        #Posiziono la label nella griglia a riga 0, colonna 1, con sticky top e sinistra (new),
        #con padding a sinistra e in alto per distanziarla.
        self.peer_list_label.grid(row=0, column=1, sticky="new", padx=10, pady=(10, 0))

        #Creo una Listbox Tkinter standard per mostrare la lista dei peer connessi,
        #con colori di sfondo e testo adattati al tema (light/dark),
        #con colori personalizzati per selezione, font e aspetto senza bordi.
        self.peer_listbox = tk.Listbox(
            self.main_frame,
            bg="#ffffff" if self.theme == "light" else "#1e1e1e",
            fg="black" if self.theme == "light" else "white",
            selectbackground="#cce5ff" if self.theme == "light" else "#3a3a3a",
            selectforeground="black",
            font=("Segoe UI", 12),
            relief="flat",
            borderwidth=0,
            highlightthickness=0
        )
        #Posiziono la listbox nella griglia a riga 0, colonna 1, con sticky in tutte le direzioni,
        #con padding per distanziarla dai bordi e dalla label sopra.
        self.peer_listbox.grid(row=0, column=1, sticky="nsew", padx=10, pady=(40, 10))

        #Creo una textbox customtkinter per l'input del messaggio da inviare,
        #con altezza 60 pixel, angoli arrotondati, font e colore del testo/sfondo in base al tema,
        #con word wrap abilitato per andare a capo automaticamente.
        self.entry = ctk.CTkTextbox(
            self.root,
            height=60,
            corner_radius=10,
            font=("Segoe UI", 12),
            wrap="word",
            fg_color="#ffffff" if self.theme == "light" else "#1e1e1e",
            text_color="black" if self.theme == "light" else "white"
        )
        #Posiziono la textbox nella griglia sotto i messaggi, spanning su 3 colonne,
        #con sticky orizzontale e padding su tutti i lati tranne sotto.
        self.entry.grid(row=3, column=0, columnspan=3, sticky="ew", padx=20, pady=(10, 0))
        #Associo l'evento "Premere Invio" per inviare il messaggio.
        self.entry.bind("<Return>", self.send_message_event)
        #Blocca l'invio di una nuova riga quando si preme Shift+Invio, per permettere di andare a capo (non fa nulla).
        self.entry.bind("<Shift-Return>", lambda e: None)

        #Creo un bottone customtkinter per inviare il messaggio,
        #con icona, testo, altezza, font in grassetto e angoli arrotondati.
        self.send_button = ctk.CTkButton(self.root, text="📩 Invia", command=self.send_message, height=45, font=("Segoe UI", 14, "bold"), corner_radius=12)
        #Posiziono il bottone in griglia sotto la textbox, spanning su 3 colonne,
        #con sticky orizzontale e padding.
        self.send_button.grid(row=4, column=0, columnspan=3, sticky="ew", padx=20, pady=(5, 15))

        #Creo un campo di input customtkinter per inserire manualmente l'indirizzo IP e la porta,
        #a cui connettersi, con placeholder, font e colori adattati al tema.
        self.connect_entry = ctk.CTkEntry(
            self.root,
            placeholder_text="IP:PORTA",
            font=("Segoe UI", 12),
            fg_color="#ffffff" if self.theme == "light" else "#121212",
            text_color="black" if self.theme == "light" else "white"
        )
        #Posiziono il campo nella griglia sotto il bottone Invia, spanning su 2 colonne,
        #con sticky orizzontale e padding.
        self.connect_entry.grid(row=5, column=0, columnspan=2, sticky="ew", padx=20, pady=(0, 10))

        #Creo un bottone per incollare il testo dagli appunti nella connect_entry,
        #con icona e testo.
        self.paste_button = ctk.CTkButton(self.root, text="📥 Incolla IP", command=self.manual_paste)
        #Posiziono il bottone nella stessa riga, colonna 2, allineato a destra,
        #con padding orizzontale e verticale.
        self.paste_button.grid(row=5, column=2, sticky="e", padx=(0, 20), pady=(0, 10))

        #Creo un bottone per tentare la connessione al peer specificato nella connect_entry,
        #con icona, testo e angoli arrotondati.
        self.connect_button = ctk.CTkButton(self.root, text="📲 Connetti a peer", command=self.connect_to_peer_ui, corner_radius=10)
        #Posiziono il bottone nella riga successiva, spanning su 3 colonne,
        #con sticky orizzontale e padding.
        self.connect_button.grid(row=6, column=0, columnspan=3, sticky="ew", padx=20, pady=(0, 10))

        #Imposto la funzione di callback da chiamare quando l'utente chiude la finestra del programma,
        #per chiudere socket e pulire le risorse prima di uscire.
        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        #Avvio il ciclo principale dell'interfaccia grafica (bloccante fino a chiusura).
        self.root.mainloop()
    #Mostra un messaggio formattato nella finestra della chat.
    def display_message(self, msg, tag="peer", timestamp=""):
        #Divide il messaggio in due parti: header (ad esempio l'username) e corpo del messaggio.
        parts = msg.split(": ", 1)
        header, body = (parts[0], parts[1]) if len(parts) > 1 else (msg, "")
        is_dark = self.theme == "dark" #Controlla se il tema corrente è scuro.

        #Imposta colori e allineamento in base al tipo di messaggio.
        if tag == "own":
            #Messaggi inviati dall'utente stesso (allineati a destra, colori chiari o scuri).
            bg_color = "#dcf8c6" if not is_dark else "#3a5f3a"
            fg_color = "black" if not is_dark else "white"
            anchor = "e"   #Ancora (allineamento) a destra.
            justify = "right" #Giustifica il testo a destra.
        elif tag == "system":
            #Messaggi di sistema (allineati al centro, con colore diverso per evidenziare).
            bg_color = "#ffe0b2" if not is_dark else "#44475a"
            fg_color = "black" if not is_dark else "white"
            anchor = "center"
            justify = "center"
        else:
            #Messaggi ricevuti dai peer (allineati a siistra).
            bg_color = "#ffffff" if not is_dark else "#2c2f33"
            fg_color = "black" if not is_dark else "white"
            anchor = "w"
            justify = "left"

        if tag != "system":
            #Per messaggi normali, creo un "bubble" contenitore con background colorato.
            bubble = tk.Frame(self.message_frame, bg=bg_color, padx=10, pady=6, bd=0, relief="flat", highlightthickness=0)
            #Label per il nome del mittente, in grassetto.
            sender = tk.Label(bubble, text=header, font=("Segoe UI", 9, "bold"), fg=fg_color, bg=bg_color, anchor=anchor, justify=justify)
            #Label per il contenuto del messaggio.
            content = tk.Label(bubble, text=body, font=("Segoe UI", 11), fg=fg_color, bg=bg_color, wraplength=600, justify=justify)
            #Label per il timestamp del messaggio, in grigio chiaro.
            timestamp_label = tk.Label(bubble, text=timestamp, font=("Segoe UI", 8), fg="lightgray", bg=bg_color, anchor=anchor, justify=justify)
            #Posiziono le label nel bubble, con allineamento definito.
            sender.pack(anchor=anchor)
            content.pack(anchor=anchor)
            timestamp_label.pack(anchor=anchor)
            #Posiziono il bubble nella finestra messaggi, con padding e fill orizzontale.
            bubble.pack(anchor=anchor, padx=10, pady=4, fill='x')
            #Aggiungo un tooltip al bubble che mostra il timestamp completo al passaggio del mouse.
            ToolTip(bubble, f"Inviato alle {timestamp}")
        else:
            #Per messaggi di sistema, creo una label semplice, centrata, in corsivo.
            sys_label = tk.Label(self.message_frame, text=msg, bg=bg_color, fg=fg_color, font=("Segoe UI", 10, "italic"), anchor="center", padx=10, pady=5)
            sys_label.pack(anchor="center", fill='x', padx=10, pady=5)

        #Aggiorna la GUI per mostrare subito i messaggi e scrolla automaticamente in fondo.
        self.message_frame.update_idletasks()
        self.message_frame._parent_canvas.yview_moveto(1.0)
    
    #Cambia il tema dell'interfaccia (chiaro/scuro).
    def toggle_theme(self):
        #Cambia il tema da light a dark o viceversa.
        self.theme = "dark" if self.theme == "light" else "light"
        #Aggiorna il tema di customtkinter di conseguenza.
        ctk.set_appearance_mode(self.theme)

    #Incolla negli input il contenuto copiato negli appunti di sistema.
    def manual_paste(self):
        try:
            #Prova a leggere dagli appunti del sistema e incollare nel campo di connect_entry.
            data = self.root.clipboard_get().strip()
            self.connect_entry.delete(0, tk.END) #Cancella contenuto precedente.
            self.connect_entry.insert(0, data) #Inserisce nuovo testo.
        except:
            #Ignora errori se non riesce (ad esempio appunti vuoti o non testo).
            pass
    
    #Copia un testo specificato negli appunti con protezione da doppio clic.
    def copy_to_clipboard(self, text):
        #Previene copia multiple troppo ravvicinate.
        if self.copy_in_progress:
            return
        self.copy_in_progress = True
        self.root.clipboard_clear() #Pulisce gli appunti.
        self.root.clipboard_append(text) #Copia il testo passato negli appunti.
        self.root.update() #Aggiorna la GUI per riflettere la modifica.
        #Dopo 200 millisecondi resetta il flag per permettere nuove copie.
        self.root.after(200, lambda: setattr(self, 'copy_in_progress', False))
    
    # Accetta nuove connessioni in entrata e avvia un thread per ognuna
    def accept_connections(self):
        #Loop infinito per accettare connessioni in ingresso.
        while True:
            conn, addr = self.listener.accept() #Accetto una nuova connessione, ottengo socket e indirizzo peer.
            self.peers[conn] = addr #Salvo la connessione nel dizionario peers.
            #Invio al peer connesso il mio utente e porta con un messaggio speciale.
            conn.send(f"__username__:{self.username}@{self.port}".encode())
            #Creo un thread separato per ricevere messaggi da questo peer senza bloccare il main thread.
            threading.Thread(target=self.receive_messages, args=(conn,), daemon=True).start()

    #Recupera IP e porta dalla GUI e tenta la connessione a un peer remoto.
    def connect_to_peer_ui(self):
        try:
            ip_port = self.connect_entry.get().strip() #Prendo l'indirizzo IP e la porta inserito nella UI.
            ip, port = ip_port.split(":")  #Splitto in IP e porta.
            self.connect_to_peer(ip, int(port)) #Provo a connettermi al peer.
        except Exception as e:
            #Se errore, mostro una finestra di errore con il messaggio di errore.
            messagebox.showerror("Errore", f"Formato non valido o connessione fallita: {e}")

    #Stabilisce una connessione socket a un peer e inizia la ricezione dei messaggi.
    def connect_to_peer(self, ip, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creo un nuovo socket TCP IPv4.
        s.connect((ip, port)) #Provo a connettermi al peer specificato.
        self.peers[s] = (ip, port) #Salvo la connessione nel dizionario peers.
        #Invio il mio utente e porta al peer appena connesso.
        s.send(f"__username__:{self.username}@{self.port}".encode())
        #Avvio un thread per ricevere messaggi da questo peer.
        threading.Thread(target=self.receive_messages, args=(s,), daemon=True).start()
        #Mostro un messaggio di sistema nella chat che indica la connessione riuscita.
        self.display_message(f"Connesso a {ip}:{port}", tag="system")
        #Aggiorno la lista dei peer visibile nella GUI.
        self.update_peer_list()

    #Evento legato al tasto Invio: invia messaggio se non è Shift+Invio.
    def send_message_event(self, event):
        #Controlla se il tasto Shift è premuto; se sì non invia il messaggio (per permettere invio a capo).
        if event.state & 0x0001:
            return
        self.send_message() #Invia il messaggio.
        return "break" #Blocca la gestione predefinita 

     #Invia il messaggio scritto a tutti i peer connessi e lo visualizza localmente.
    def send_message(self):
        content = self.entry.get("1.0", ctk.END).strip() #Prende il testo scritto dall'utente.
        if not content:
            return #Se il contenuto è vuoto, non viene inviato nulla.
        timestamp = datetime.now().strftime("%H:%M") #Ottiene l'orario corrente per il timestamp.
        full_msg = f"{self.username}: {content}"  #Prepara il messaggio completo da inviare.
        self.display_message(full_msg, tag="own", timestamp=timestamp) #Mostra il messaggio nella chat locale.
        #Invio il messaggio a tutti i peer connessi.
        for peer in list(self.peers.keys()):
            try:
                peer.send(full_msg.encode())
            except:
                continue #Se fallisce l'invio a qualche peer, continua senza interrompere.
        self.entry.delete("1.0", ctk.END) #Pulisce la textbox dopo l'invio.

    #Riceve messaggi da un singolo peer, gestisce nomi e disconnessioni.
    def receive_messages(self, conn):
        #Loop infinito per ricevere messaggi da un singolo peer.
        while True:
            try:
                data = conn.recv(1024) #Riceve dati dal peer (massimo 1024 byte).
                if not data:
                    break #Se la connessione si chiude (dati vuoti), esce dal loop.
                message = data.decode() #Decodifica il messaggio ricevuto.
                if message.startswith("__username__:"):
                    #Se il messaggio è un identificativo utente speciale, aggiorna il dizionario usernames.
                    name_info = message.split(":", 1)[1]
                    self.usernames[conn] = name_info
                    self.update_peer_list() #Aggiorna la lista dei peer visibile nella GUI.
                else:
                    #Messaggi normali vengono mostrato nella chat con timestamp e suono di notifica.
                    timestamp = datetime.now().strftime("%H:%M")
                    self.display_message(message, tag="peer", timestamp=timestamp)
                    notify() #Suono di notifica.
            except:
                break #In caso di errore, esce dal loop.
        #Quando il peer si disconnette, mostra messaggio informativo nella chat.
        name = self.usernames.get(conn, "sconosciuto")
        self.display_message(f"[INFO] Il peer '{name}' si è disconnesso.", tag="system")
        conn.close() #Chiude la connessione socket.
        #Rimuove la connessione dai dizionari peers ed usernames.
        if conn in self.peers:
            del self.peers[conn]
        if conn in self.usernames:
            del self.usernames[conn]
        self.update_peer_list() #Aggiorna la lista dei peer connessi.

    #Aggiorna visivamente la lista dei peer connessi nella listbox.
    def update_peer_list(self):
        self.peer_listbox.delete(0, tk.END) #Pulisce la listbox dei peer connessi.
        #Per ogni peer connesso inserisce il nome utente o l'indirizzo IP:PORTA nella listbox. 
        for conn, addr in self.peers.items():
            name = self.usernames.get(conn, f"{addr[0]}:{addr[1]}")
            self.peer_listbox.insert(tk.END, name)

    # Chiude correttamente socket, connessioni e finestra principale all’uscita
    def close_app(self):
        #Chiude tutte le connessioni socket verso i peer.
        for peer in self.peers:
            try:
                peer.close()
            except:
                pass
        self.listener.close() #Chiude il socket in ascolto.
        self.root.destroy() #Distrugge/Chiude la finestra GUI.

#Se questo file è eseguito come script principale, avvia l'applicazione.
if __name__ == "__main__":
    PeerToPeerChat()