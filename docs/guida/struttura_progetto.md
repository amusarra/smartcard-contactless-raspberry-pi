Adesso che abbiamo visto dalla superficie cos'è Pyscard e per cosa sarà
utile, cerchiamo di disegnare la struttura del nostro progetto che
implementerà lo scenario introdotto a inizio articolo.

Il diagramma (in notazione UML) di figura 19 mostra package, component e
classi utilizzati per l'implementazione dello scenario che abbiamo
descritto a inizio articolo. Gli elementi del diagramma del nostro
progetto sono quelli evidenziati con il colore giallo ocra e in
particolare:

- **Classi**
    - <a
      href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/master/rpi/gpio/manage_relay.py"
      target="_blank" rel="noopener">ManageRelay</a> (manage_relay.py).
      Classe che gestisce attraverso l'interfaccia GPIO l'attivazione e
      disattivazione dei quattro relè, nonché l'inizializzazione della
      stessa interfaccia GPIO.
    - <a
      href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/master/rpi/smartcard/mongodb/smart_card_access_crud.py"
      target="_blank" rel="noopener">SmartCardAccessCrud</a>
      (smart_card_access_crud.py). Classe che gestisce le operazioni CRUD
      sul database NoSQL MongoDB.
    - <a
      href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/master/rpi/smartcard/mifare/mifare_interface.py"
      target="_blank" rel="noopener">MifareClassicInterface</a>
      (mifare_interface.py). Classe che gestisce la comunicazione con il
      lettore di Smart Card e di conseguenza d'interagire con la Smart
      Card connessa. Le operazioni gestite sono: autenticazione, lettura
      ATR, lettura UID, lettura dalla memoria della carta e scrittura
      sulla memoria della carta.
- **Component**
    - <a
      href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/master/setup_smart_card.py"
      target="_blank" rel="noopener">Setup Smart Card</a>
      (setup_smart_card.py). Script Python che rapprensentata l'entry
      point responsabile del setup della Smart Card e memorizzazione dei
      dati anagrafici dell'ospite sul database MongoDB. Questo script deve
      ricevere in input i parametri necessari per eseguire il setup della
      Smart Card.
    - <a
      href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/master/access_via_smart_card.py"
      target="_blank" rel="noopener">Access via Smart Card</a>
      (access_via_smart_card.py). Script Python che rappresenta l'entry
      point responsabile di governare l'apertura delle porte (attraverso
      l'attivazione dei relè) sulla base della validazione dei dati
      estratti dalla Smart Card. Questo script deve ricevere in input la
      chiave di autenticazione della Smart Card.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/smartcard-contactless-raspberry-pi-uml-diagram-1024x446.jpg"
title="Figura 19 - Package/Component/Class diagram del progetto Smart Card Contactless Raspberry Pi"
class="wp-image-5545 size-large" width="1024" height="446"
alt="Figura 19 - Package/Component/Class diagram del progetto Smart Card Contactless Raspberry Pi" />](https://www.dontesta.it/wp-content/uploads/2022/03/smartcard-contactless-raspberry-pi-uml-diagram-scaled.jpg)
**Figura 19** - Package/Component/Class diagram del progetto Smart Card
Contactless Raspberry Pi

Il package *smartcard* (in verde) fa parte di Pyscard, e i componenti
all'interno sono utilizzati per sfruttare il monitoraggio delle Smart
Card. Utilizzando l'interfaccia <a
href="https://pyscard.sourceforge.io/epydoc/smartcard.CardMonitoring.CardObserver-class.html"
class="reference external">CardObserver</a> siamo in grado di poter
sapere quando la Smart Card viene aggiunta (appoggiata sul lettore) o
rimossa (dal raggio di azione del segnale RF).

Il sequence diagram di figura 20 descrive lo scenario del setup della
Smart Card (vedi Figura 2 - Processo semplificato di accoglienza
dell'ospite in hotel), mostrando le azioni principali e gli eventuali
flussi alternativi. Sempre da questo diagramma possiamo vedere le
relazioni che intercorrono, in termini di messaggi, tra i vari attori,
quest'ultimi sono stati descritti in precedenza e mostrati nel diagramma
di figura 19.

Le azioni decisamente più importanti sono quelle che riguardano l'invio
dei comandi APDU, che riassumendo sono:

1.  <a
    href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/f9ae78638f3eb277ebfc7951fea436da2c6bee44/rpi/smartcard/mifare/mifare_interface.py#L238"
    target="_blank" rel="noopener">Load Authentication Key sulla memoria
    volatile</a>
2.  <a
    href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/f9ae78638f3eb277ebfc7951fea436da2c6bee44/rpi/smartcard/mifare/mifare_interface.py#L78"
    target="_blank" rel="noopener">Autenticazione per accedere al primo
    blocco del settore uno della MIFARE Classic 1K</a>
3.  <a
    href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/f9ae78638f3eb277ebfc7951fea436da2c6bee44/rpi/smartcard/mifare/mifare_interface.py#L213"
    target="_blank" rel="noopener">Richiesta UID</a>
4.  <a
    href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/f9ae78638f3eb277ebfc7951fea436da2c6bee44/rpi/smartcard/mifare/mifare_interface.py#L172"
    target="_blank" rel="noopener">Lettura dell'eventuale precedente
    documentId (numero identificativo del documento di riconoscimento)</a>
5.  <a
    href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/f9ae78638f3eb277ebfc7951fea436da2c6bee44/rpi/smartcard/mifare/mifare_interface.py#L286"
    target="_blank" rel="noopener">Salvataggio del documentId</a>

I link della precedente lista riportano direttamente sul metodo
specifico della classe <a
href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/master/rpi/smartcard/mifare/mifare_interface.py"
target="_blank" rel="noopener">Mifare Classic Interface</a> all'interno
del quale è specificato il contenuto dell'APDU inviata.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/setup_smart_card_sequence-1024x1235.png"
title="Figura 20 - Diagramma di sequenza dell&#39;entry point Setup Smart Card"
class="wp-image-5548 size-large" width="1024" height="1235"
alt="Figura 20 - Diagramma di sequenza dell&#39;entry point Setup Smart Card" />](https://www.dontesta.it/wp-content/uploads/2022/03/setup_smart_card_sequence.png)
**Figura 20** - Diagramma di sequenza dell'entry point Setup Smart Card

Nella fase di setup della Smart Card, prima di inserire i dati
anagrafici dell'ospite sul database, viene eseguita la query utilizzando
il filtro
`{"smartCardId": "f{uid}", "documentId": f"{identification_number}"}`
, in modo che sia possibile verificare che non esista già un documento
con l'associazione smartCardId e documentId (fare riferimento allo step
33 del sequence diagram di figura 20).

Il sequence diagram di figura 21 descrive lo scenario di Accesso alla
stanza tramite Smart Card (vedi Figura 3 - Processo di accesso alla
stanza), mostrando le azioni principali e gli eventuali flussi
alternativi. Sempre da questo diagramma possiamo vedere le relazioni che
intercorrono, in termini di messaggi, tra i vari attori, quest'ultimi
sono stati descritti in precedenza e mostrati nel diagramma di figura 19.

In questo diagramma, tra gli attori in gioco abbiamo anche il componente
<a
href="https://pyscard.sourceforge.io/epydoc/smartcard.CardMonitoring.CardMonitor-class.html"
target="_blank" rel="noopener">Card Monitor</a> di Pyscard, che abbiamo
utilizzato per aggiungere la nostra interfaccia <a
href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/master/rpi/smartcard/mifare/mifare_interface.py#L51"
target="_blank" rel="noopener">Mifare Classic Interface</a> come
observable, in questo modo il Card Monitor richiamerà il metodo <a
href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/blob/f9ae78638f3eb277ebfc7951fea436da2c6bee44/rpi/smartcard/mifare/mifare_interface.py#L312"
target="_blank" rel="noopener">update(self, observable, actions)</a> nel
momento in cui si verificheranno gli eventi di aggiunta o rimozione
della Smart Card. Il metodo update implementa quando descritto in Figura
16 - Mind Map sugli aspetti funzionali che il software dovrà
implementare, di cui le azioni sono evidenti sul sequence diagram a
seguire.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/access_via_smart_card_sequence-1-1024x1047.png"
title="Figura 21 - Diagramma di sequenza per l&#39;entry point Access via Smart Card"
class="wp-image-5552 size-large" width="1024" height="1047"
alt="Figura 21 - Diagramma di sequenza per l&#39;entry point Access via Smart Card" />](https://www.dontesta.it/wp-content/uploads/2022/03/access_via_smart_card_sequence-1.png)
**Figura 21** - Diagramma di sequenza per l'entry point Access via Smart
Card

I dati sono estratti dal database MongoDB utilizzando il filtro
`{"smartCardId": f"{uid}", "documentId":f{identification_number}", "smartCardEnabled": "true"}`,
nel caso non ci siano documenti che rispettino questo filtro, il sistema
negherà l'accesso, alternativamente, sarà aggiornato il documento su
MongDB e attivato il relè corrispondente al numero della stanza
associato all'ospite (fare riferimento allo step 1.7 del sequence
diagram di figura 21).

Molto bene! Una volta descritti i sequence diagram dei nostri due
scenari, direi che potremmo passare all'azione, ovvero, eseguire il
deploy dell'applicazione sul Raspberry Pi 4.