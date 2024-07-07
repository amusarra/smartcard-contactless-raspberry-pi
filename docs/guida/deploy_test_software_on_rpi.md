Ci siamo! È arrivato il momento d'installare il progetto software sul
Raspberry Pi e verificare che tutto funzioni così per com'è stato
ideato. Il deployment diagram della figura a seguire mostra tutti i
componenti del nostro sistema di accesso.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/system_deployment_on_raspberry-1024x891.png"
class="size-large wp-image-5562" width="1024" height="891"
alt="Figura 22 - Deployment diagram del sistema di accesso via Smart Card Contactless su Raspberry Pi" />](https://www.dontesta.it/wp-content/uploads/2022/03/system_deployment_on_raspberry.png)
**Figura 22** - Deployment diagram del sistema di accesso via Smart Card
Contactless su Raspberry Pi

Assumiamo a questo punto che tutti i requisiti software indicati in
precedenza siano tutti soddisfatti (fare riferimento a 6. Requisiti
Software). Per installare il progetto software sul Raspberry Pi occorre
seguire i seguenti passi:

1.  accedere in ssh alla Raspberry Pi;
2.  decidere una locazione dove installare il progetto software. Non ci
    sono restrizioni; nel mio caso ho preferito usare la home del mio
    account;
3.  eseguire il clone del repository del progetto;
4.  eseguire l'installazione delle dipendenze Python.

Per ambienti di sviluppo o test è possibile pensare di fare ricorso alla
creazione di quella che viene definita nel mondo Python,
<a href="https://docs.python.org/3/tutorial/venv.html" target="_blank"
rel="noopener">Virtual Environments</a>.


```bash
# Accesso al Raspberry Pi via SSH
ssh amusarra@192.168.238.169

# Clone del repository GitHub del progetto
git clone https://github.com/amusarra/smartcard-contactless-raspberry-pi.git

# Installazione delle dipendenze Python
cd smartcard-contactless-raspberry-pi
make
```
**Console 2** - Installazione del progetto software

Il comando `make` non fa altro che procedere con l'installazione delle
dipendenze Python specificate sul file <a
href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/master/requirements.txt"
target="_blank" rel="noopener">requirements.txt</a> utilizzando
<a href="https://pypi.org/project/pip/" target="_blank"
rel="noopener">pip</a>. La figura 23 mostra il processo d'installazione
delle dipendenze Python sul Raspberry Pi. Ultimata l'installazione, è
possibile eseguire il test vero e proprio del software. Prima di
eseguire il test occorre accertarsi che dal punto di vista hardware sia
tutto regolare controllando tutti i collegamenti (vedi schema
elettrico), compreso il collegamento del lettore di Smart Card via USB.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/install_rpi_access_system_via_smart_card_1-1024x626.png"
class="size-large wp-image-5568" width="1024" height="626"
alt="Figura 23 - Installazione delle dipendenze Python tramite il comando make" />](https://www.dontesta.it/wp-content/uploads/2022/03/install_rpi_access_system_via_smart_card_1.png)
**Figura 23** - Installazione delle dipendenze Python tramite il comando
make

Ormai dovremmo sapere quali sono gli entry point da utilizzare, sia
quello per il setup della Smart Card, sia quello che avvia il controllo
degli accessi. Entrambi gli entry point, quindi gli script Python,
devono essere avviati specificando una serie di parametri. Le due
tabelle a seguire mostrano i parametri d'input dei due script:
`setup_smart_card.py` e `access_via_smart_card.py`.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_script_setup_smart_card-1024x582.png"
class="size-large wp-image-5572" width="1024" height="582"
alt="Figura 24 - Tabella dei parametri d&#39;input per lo script Python setup_smart_card.py" />](https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_script_setup_smart_card.png)
**Figura 24** - Tabella dei parametri d'input per lo script Python
setup_smart_card.py

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_script_access_via_smart_card-1024x265.png"
title="Figura 25 - Tabella dei parametri d&#39;input per lo script Python access_via_smart_card.py"
class="wp-image-5573 size-large" width="1024" height="265"
alt="Figura 25 - Tabella dei parametri d&#39;input per lo script Python access_via_smart_card.py" />](https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_script_access_via_smart_card.png)
**Figura 25** - Tabella dei parametri d'input per lo script Python
access_via_smart_card.py

La figura 26 mostra un esempio di come si presenta l'help in linea dello
script `setup_smart_card.py` attivato utilizzando l'opzione `--help` (o
`-h`).

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/setup_smart_card.py_help_option-1024x618.png"
class="size-large wp-image-5574" width="1024" height="618"
alt="Figura 26 - Come si presenta l&#39;help in line dello script setup_smart_card.py" />](https://www.dontesta.it/wp-content/uploads/2022/03/setup_smart_card.py_help_option.png)
**Figura 26** - Come si presenta l'help in linea dello script
setup_smart_card.py

A questo punto siamo davvero pronti. Il primo step è la registrazione
della Smart Card per il nuovo ospite Mario Rossi il cui documento
d'identità ha il numero MU589876XD e al quale assegnamo la stanza numero
due.

Prima di avviare la registrazione, prendiamo la Smart Card poggiandola
sul lettore. Il comando da avviare per la registrazione è:
`./setup_smart_card.py -a FFFFFFFFFFFF -i MU589876XD -s --firstname Mario --lastname Rossi -r 2`

Se tutto va per il verso giusto, l'output ottenuto in console dovrebbe
essere quello mostrato dalla figura a seguire.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/setup_smart_card_run_1-1024x511.png"
class="size-large wp-image-5576" width="1024" height="511"
alt="Figura 27 - Registrazione Smart Card MIFARE Classic 1K con i dati dell&#39;ospite " />](https://www.dontesta.it/wp-content/uploads/2022/03/setup_smart_card_run_1.png)
**Figura 27** - Registrazione Smart Card MIFARE Classic 1K con i dati
dell'ospite

Dopo la registrazione della Smart Card e la consegna all'ospite,
quest'ultimo può usare la Smart Card per accedere alla propria stanza
assegnata in fase di registrazione, che ricordo essere la numero due.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/smart_card_registration_data_on_mongodb_1-1024x974.png"
class="size-large wp-image-5577" width="1024" height="974"
alt="Figura 28 - Documento registrato su MongoDB a fronte del processo di registrazione Smart Card" />](https://www.dontesta.it/wp-content/uploads/2022/03/smart_card_registration_data_on_mongodb_1.png)
**Figura 28** - Documento registrato su MongoDB a fronte del processo di
registrazione Smart Card

Avviamo adesso il programma del controllo degli accessi utilizzando il
comando: `./access_via_smart_card.py -a FFFFFFFFFFFF`. Avviato il
programma, questo resta in attesa di leggere la Smart Card. Poggiando la
Smart Card registrata poc'anzi, l'ospite dovrebbe riuscire ad accedere
alla sua stanza, così come mostra la figura a seguire.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/smart_card_access_control_1-1024x570.png"
class="size-large wp-image-5578" width="1024" height="570"
alt="Figura 29 - Richiesta di accesso via Smart Card MIFARE Classic 1K" />](https://www.dontesta.it/wp-content/uploads/2022/03/smart_card_access_control_1.png)
**Figura 29** - Richiesta di accesso via Smart Card MIFARE Classic 1K

L'output mostrato dalla figura 29 evidenzia anche un accesso non
riuscito perché in questo caso la Smart Card presentata non è registrata
sul sistema. Gli screencast a seguire mostrano i due entry point in
azione: setup_smart_card.py e access_via_smart_card.py.

<a href="https://asciinema.org/a/475795" target="_blank"
rel="noopener"><img src="https://asciinema.org/a/475795.svg"
title="Screencast 1 - Processo di registrazione Smart Card in azione"
width="1223" height="784"
alt="Screencast 1 - Processo di registrazione Smart Card in azione" /></a>
**Screencast 1** - Processo di registrazione Smart Card in azione

<a href="https://asciinema.org/a/475797" target="_blank"
rel="noopener"><img src="https://asciinema.org/a/475797.svg"
title="Screencast 2 - Processo di accesso alla stanza via Smart Card in azione"
width="1223" height="784"
alt="Screencast 2 - Processo di accesso alla stanza via Smart Card in azione" /></a>
**Screencast 2** - Processo di accesso alla stanza via Smart Card in azione

Dopo i due screencast che mostrano il sistema di accesso in azione,
possiamo affermare che il nostro lavoro di analisi, progettazione e
implementazione sia arrivato al termine, raggiungendo anche l'obiettivo
prefissato.