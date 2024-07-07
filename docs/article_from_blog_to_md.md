\[:it\]Le
<a href="https://it.wikipedia.org/wiki/Smart_card" target="_blank"
rel="noopener"><strong>Smart Card</strong></a> fanno parte ormai da
tempo del nostro quotidiano: dalla
<a href="https://it.wikipedia.org/wiki/Carta_SIM" target="_blank"
rel="noopener">SIM</a> (*Subscriber Identity Module*) del cellulare,
alla carta di credito, come sistema di fidelizzazione, per accedere ai
locali e come mezzo per fruire dei servizi della pubblica
amministrazione.

Integrare sistemi di autenticazione basati su Smart Card nei propri
sistemi e applicazioni, credo che possa essere un'attività molto
interessante per chi programma e l'aspetto a mio avviso più coinvolgente
è la vicinanza con quelli che amo definire bonariaménte **"pezzi di
ferro"**.

Quasi due anni fa ho scritto l'articolo <a
href="https://www.dontesta.it/2020/07/17/raspberry-pi-esempio-applicazione-ts-cns-smartcard/"
target="_blank" rel="noopener">Raspberry Pi – Un esempio di applicazione
della TS-CNS</a>, dove mostravo come poter creare un sistema di accesso
utilizzando la propria TS-CNS; in questo articolo vedremo invece come
mettere insieme <a href="https://www.raspberrypi.org/" target="_blank"
rel="noopener">Raspberry Pi</a>, modulo da quattro relè, lettore di
Smart Card e
<a href="https://en.wikipedia.org/wiki/MIFARE" target="_blank"
rel="noopener">MIFARE Classic 1K</a> contactless Smart Card per poi
armonizzare il tutto con il software necessario allo scopo di realizzare
un sistema di accesso.

Per lo sviluppo del progetto è necessario toccare un numero
considerevole di argomenti e cercherò di trattare i principali con il
giusto livello di profondità, in caso contrario l’articolo assumerebbe
delle dimensioni notevoli. Mi impegnerò a lasciare tutti i riferimenti
utili per ogni vostro approfondimento.

A questo punto direi d’iniziare; mettetevi comodi e munitevi della
giusta concentrazione perché la lettura di questo articolo sarà
abbastanza impegnativa ma spero interessante.

## 1. Descrizione dello scenario

Credo d'intuire quale potrebbe essere il vostro pensiero in questo
momento. **Che tipo di *Sistema di Accesso* andremo a realizzare?**

Vorrei implementare qualcosa che tutti almeno una volta abbiamo usato.
Un comunissimo scenario di *Sistema di Accesso* lo abbiamo vissuto tutti
accedendo alla nostra camera di albergo grazie alla Smart Card (o chiave
elettronica) consegnata al momento dell'accoglienza. La figura a seguire
mostra lo schema hardware della soluzione che andremo a realizzare.

\[caption id="" align="aligncenter" width="2523"\]<img
src="https://github.com/amusarra/smartcard-contactless-raspberry-pi/raw/master/docs/images/hardware_diagram_smartcard_access_raspberry_pi_1.jpg"
title="Figura 1 - Schema hardware della soluzione di accesso (Smart Card icon da https://www.smartcardfocus.com/)"
width="2523" height="1383"
alt="Figura 1 - Schema hardware della soluzione di accesso" /> Figura
1 - Schema hardware della soluzione di accesso (Smart Card Reader icon
da https://www.smartcardfocus.com/)

La <a
href="https://www.nxp.com/products/rfid-nfc/mifare-hf/mifare-classic:MC_41863"
target="_blank" rel="noopener">MIFARE Classic® 1K contactless si basa su
NXP MF1 IC S50</a>. Questa tipologia di carta è una buona scelta per
applicazioni classiche come la biglietteria dei trasporti pubblici,
servizi di fidelizzazione e può essere utilizzata anche per molte altre
applicazioni come sistemi di apertura porte e simili.

Il lettore di Smart Card deve essere conforme a standard indicati nello
schema di figura 1. Nel mio caso ho utilizzato il lettore
<a href="https://shop.bit4id.com/en/prodotto/minilector-cie/"
target="_blank" rel="noopener">CIE Bit4id miniLector</a> collegato al
Raspberry Pi tramite la porta USB. Il nome tecnico del lettore che ho
utilizzato è: BIT4ID miniLector AIR NFC v3.

Al Raspberry Pi è collegato un modulo di quattro relè gestito tramite le
porte
<a href="https://it.wikipedia.org/wiki/General_Purpose_Input/Output"
target="_blank" rel="noopener"><strong>GPIO</strong></a>. Nel nostro
scenario,<span style="text-decoration: underline;"> i relè rappresentano
gli attuatori necessari per aprire le porte dell'hotel dove siamo
ospiti</span>.

Appurato che il nostro scenario è quello di un sistema di accesso per
consentire agli ospiti di un hotel di accedere alle proprie stanze
attraverso una Smart Card, vediamo quali sono i due processi che portano
al raggiungimento di questo obiettivo.

La figura 2 illustra il processo semplificato (in notazione
<a href="https://www.bpmn.org/" target="_blank" rel="noopener">BPMN</a>)
di ciò che accade quando un ospite viene ricevuto dal personale
dell'hotel. Dell'intero processo, solo il *Service Task* (indicato in
rosso) sarà l'oggetto dell'implementazione del software.

<img
src="https://github.com/amusarra/smartcard-contactless-raspberry-pi/raw/master/docs/images/guest_receiving_process.jpg"
class="size-large" width="3156" height="1686"
alt="Figura 2 - Processo semplificato di accoglienza dell&#39;ospite in hotel." />
Figura 2 - Processo semplificato di accoglienza dell'ospite in hotel.

Il processo di figura 3 mostra invece cosa succede quando l'ospite
chiede di entrare nella sua camera tramite l'uso della chiave
elettronica appoggiandola sul lettore. Dell'intero processo, solo i
Service Task (indicati in rosso) saranno oggetto dell'implementazione
del software.

<img
src="https://github.com/amusarra/smartcard-contactless-raspberry-pi/raw/master/docs/images/room_access_process.jpg"
class="size-large" width="3156" height="1686"
alt="Figura 3 - Processo di accesso alla stanza" /> Figura 3 - Processo
di accesso alla stanza

Credo che tutti i processi illustrati (in figura 2 e figura 3) in
notazione BPMN siano abbastanza esplicativi da non richiedere ulteriori
approfondimenti. I Service Task sono gli elementi che saranno oggetto di
nostro interesse per l'implementazione del software che fin da questo
momento possiamo dividere in due macro componenti le cui responsabilità
devono essere:

1.  il setup della Smart Card (o chiave elettronica) in fase di
    registrazione dell'ospite presso la struttura alberghiera.
    All'interno della Smart Card sarà memorizzato l'identificativo di un
    documento di riconoscimento dell'ospite, sul database del sistema di
    gestione dell'albergo saranno invece memorizzati i dati anagrafici
    insieme ad altri dati necessari per associare la chiave elettronica
    all'ospite e alla stanza a lui assegnata;
2.  la verifica che la chiave elettronica sia abilitata e associata
    all'ospite e alla stanza a cui consentire l'accesso.

 

## 2. Qualche dettaglio sulla MIFARE Classic 1K

MIFARE è un marchio registrato di
<a href="https://www.nxp.com/" target="_blank" rel="noopener">NXP
Semiconductors</a>. I prodotti MIFARE sono circuiti integrati ampiamente
utilizzati per l'utilizzo in Smart Card senza contatto e molte altre
applicazioni in tutto il mondo. La gamma MIFARE comprende circuiti
integrati per la realizzazione di tessere contactless e lettori per la
comunicazione con esse.

Il nome MIFARE racchiude diversi tipi di Smart Card senza contatto,
quella utilizzata in questo scenario rientra nel tipo *Classic*. Si
tratta di schede di memoria a logica cablata che solo parzialmente sono
conformi allo standard
<a href="https://it.wikipedia.org/wiki/ISO/IEC_14443" target="_blank"
rel="noopener"><strong>ISO/IEC 14443A</strong></a> (caratteristiche
fisiche, potenza e interfaccia del segnale radio, inizializzazione e
anticollisione), poiché utilizzano un set di comandi proprietari invece
del protocollo
<a href="https://www.iso.org/standard/73599.html" target="_blank"
rel="noopener">ISO/IEC 14443-4</a> di alto livello e non sono conformi
al formato frame
<a href="https://www.iso.org/standard/73598.html" target="_blank"
rel="noopener">ISO/IEC 14443-3</a> e nelle comunicazioni crittografate
usano un <span style="text-decoration: underline;">protocollo di
sicurezza proprietario</span>
<a href="https://en.wikipedia.org/wiki/Crypto-1" target="_blank"
rel="noopener"><strong>NXP (CRYPTO1)</strong></a> per l'autenticazione e
la crittografia che è stato
<span style="text-decoration: underline;">rotto nel 2008</span>.

Dopo l'ultima frase immagino che vi stiate domandando: **perché scrivere
allora un articolo su questa Smart Card?** La risposta è abbastanza
semplice. Questa è una delle <a
href="https://it.wikipedia.org/wiki/Smart_card#Smart_card_a_sola_memoria"
target="_blank" rel="noopener">Smart Card a sola memoria</a> più diffuse
e semplici da usare, e per il tipo di scenario qui presentato, la
possibilità di scoprire "facilmente" la chiave di autenticazione è
secondario, inoltre, questo è articolo prettamente didattico.

La MIFARE Classic 1K dispone di 1024 byte di memoria
(<a href="https://it.wikipedia.org/wiki/EEPROM" target="_blank"
rel="noopener"><strong>EEPROM</strong></a>) suddivisa in 16 segmenti;
ogni settore è protetto da due chiavi che vengono chiamate A e B. In
tutti i tipi di carta, 16 byte a settore sono riservati alle chiavi e
alle condizioni d’accesso e non possono essere utilizzati per i dati
dell’utente; inoltre, i primi 16 byte contengono il
<span style="text-decoration: underline;">numero di serie univoco</span>
e di sola lettura. In questo modo la memoria disponibile si riduce a 752
byte.

Data l'altissima diffusione di questa tipologia di Smart Card e le
versioni "cinesi" esistenti, dubito che non ci siano numeri di serie
duplicati, visto anche che i byte dedicati alla memorizzazione del
numero di serie sono quattro.

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/mifare_classic_1k_memory_organization_MF1S50YYX_V1-1024x1047.png"
title="Figura 4 - Struttura della memoria della Mifare Classic 1K (dal datasheet NXP MIFARE Classic EV1 1K https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf)"
class="wp-image-5504 size-large" width="1024" height="1047"
alt="Figura 4 - Struttura della memoria della Mifare Classic 1K (dal datasheet NXP MIFARE Classic EV1 1K https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf)" />](https://www.dontesta.it/wp-content/uploads/2022/03/mifare_classic_1k_memory_organization_MF1S50YYX_V1.png)
Figura 4 - Struttura della memoria della Mifare Classic 1K (dal
datasheet NXP MIFARE Classic EV1 1K
https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf)

Prima di poter compiere operazioni di lettura o scrittura sui blocchi di
memoria, è necessario eseguire prima un'autenticazione tramite la chiave
del settore del blocco. In genere tutte le chiavi (A e B) sono impostate
su valore `FFFFFFFFFFFFh` in fase di produzione del chip (e in ogni caso
la documentazione fornita al momento dell'acquisto fornisce indicazioni
sulle chiavi di accesso e su come eseguire la modifica).

La tabella mostrata in figura 5 rappresenta la mappa della memoria con
in evidenza il range degli indirizzi per i *Data Blocks* e i *Trailer
Block *per ogni settore. Questa mappa sarà utile nel momento in cui
dovremo leggere e scrivere sui data blocks.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/mifare_1K_memory_map-2-1024x602.jpg"
title="Figura 5 - Memory Map della MIFARE Classic 1K completa di range d&#39;indirizzi dei blocchi"
class="wp-image-5521 size-large" width="1024" height="602"
alt="Figura 5 - Memory Map della MIFARE Classic 1K completa di range d&#39;indirizzi dei blocchi" />](https://www.dontesta.it/wp-content/uploads/2022/03/mifare_1K_memory_map-2.jpg)
Figura 5 - Memory Map della MIFARE Classic 1K completa di range
d'indirizzi dei blocchi

Dopo questa sorvolata sulle caratteristiche principali della MIFARE
Classic 1K che sono di nostro interesse per il nostro obiettivo,
possiamo andare avanti ed esplorare il modo su come comunicare con la
carta per le operazioni di autenticazione, lettura e scrittura.

 

## 3. I misteriosi pacchetti APDU

La comunicazione delle informazioni tra la carta e il lettore è resa
possibile grazie allo scambio di pacchetti detti **APDU** (*Application
Protocol Data Unit*); essi rappresentano l’unità di comunicazione tra il
lettore e la carta e la loro struttura è ben definita da
<a href="https://www.iso.org/obp/ui/#iso:std:iso-iec:7816:-4:ed-4:v1:en"
target="_blank" rel="noopener"><strong>ISO/IEC 7816-4 Organization,
security and commands for interchange</strong></a>.

**Esistono due tipi di APDU: quelli di comando e quelli di risposta**. I
primi richiedono un set di attributi attraverso cui il lettore è in
grado di sapere quali operazioni compiere e quali dati inviare, i
secondi contengono il risultato dell’operazione richiesta con in coda
l'esito dell'operazione.

La tabella di figura 6 mostra la struttura dei comandi APDU che
attraverso il lettore di Smart Card possiamo inviare alla carta MIFARE.

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/structure_of_request_command_apdu-1-1024x751.jpg"
class="wp-image-5520 size-large" width="1024" height="751"
alt="Figura 6 - Struttura dei comandi APDU" />](https://www.dontesta.it/wp-content/uploads/2022/03/structure_of_request_command_apdu-1-scaled.jpg)
Figura 6 - Struttura dei comandi APDU

 

La tabella di figura 7 mostra un esempio di comando APDU per ottenere
l'UID della MIFARE Classic 1K, la cui lunghezza è pari a 4 byte (vedi
attributo Le). A fronte dei comandi inviati, riceviamo sempre una
risposta che ha la struttura indicata dalla tabella di figura 8.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/apdu_command_for_request_uid-1024x464.jpg"
class="size-large wp-image-5514" width="1024" height="464"
alt="Figura 7 - Comando per ottenere l&#39;UID della Smart Card MIFARE Classic 1K" />](https://www.dontesta.it/wp-content/uploads/2022/03/apdu_command_for_request_uid.jpg)
Figura 7 - Comando per ottenere l'UID della Smart Card MIFARE Classic 1K

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/structure_of_response_command_apdu-1-1024x521.jpg"
title="Figura 8 - Struttura di risposta APDU"
class="wp-image-5522 size-large" width="1024" height="521"
alt="Figura 8 - Struttura di risposta APDU" />](https://www.dontesta.it/wp-content/uploads/2022/03/structure_of_response_command_apdu-1.jpg)
Figura 8 - Struttura di risposta APDU

 

La tabella di figura 9 mostra la risposta ottenuta a fronte del comando
APDU per richiedere l'UID (vedi figura 7) la cui lunghezza dell'UID è
pari a 4 byte più 2 byte che segnalano l’esito del comando. L’UID è
restituito con il byte meno significativo
(<a href="https://it.wikipedia.org/wiki/Bit_meno_significativo"
target="_blank" rel="noopener">LSB</a>) a sinistra e quello più
significativo
(<a href="https://it.wikipedia.org/wiki/Bit_pi%C3%B9_significativo"
target="_blank" rel="noopener">MSB</a>) a destra (quindi usa il sistema
<a href="https://it.wikipedia.org/wiki/Ordine_dei_byte" target="_blank"
rel="noopener">little-endian</a>).

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/apdu_response_of_the_command_uid-1-1024x651.jpg"
title="Figura 9 - Risposta del comando APDU per ottenere l&#39;UID della MIFARE Classic 1K"
class="wp-image-5523 size-large" width="1024" height="651"
alt="Figura 9 - Risposta del comando APDU per ottenere l&#39;UID della MIFARE Classic 1K" />](https://www.dontesta.it/wp-content/uploads/2022/03/apdu_response_of_the_command_uid-1.jpg)
Figura 9 - Risposta del comando APDU per ottenere l'UID della MIFARE
Classic 1K

 

Confrontando i valori di **SW1** e **SW2** (*Status Word*) con quelli
riportati dalla tabella mostrata in figura 10 è possibile evincere se
l'esecuzione del comando è andato a buon fine.

**Attenzione**. I valori di SW1 e SW2 fanno riferimento al comando per
ottenere l'UID della carta; questi valori potrebbero essere diversi per
altre classi di comando, in particolare nei casi di errore.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/response_apdu_command_uid_sw1_sw2-1024x388.jpg"
class="size-large wp-image-5517" width="1024" height="388"
alt="Figura 10 - Codici di risposta APDU comando UID" />](https://www.dontesta.it/wp-content/uploads/2022/03/response_apdu_command_uid_sw1_sw2-scaled.jpg)
Figura 10 - Codici di risposta APDU comando UID

Per maggiori dettagli sui comandi ed eventuali estensioni, consiglio
sempre di consultare il datasheet della
<a href="https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf"
target="_blank" rel="noopener">MIFARE Classic 1K</a>. I comandi APDU di
nostro interesse per implementare lo scenario descritto nella parte
introduttiva dell'articolo, sono:

- comando per ottenere l'UID della carta;
- comando per leggere i dati da un determinato settore e blocco;
- comando per scrivere dati su un determinato settore e blocco della
  carta.

 

## 4. Cos'è l'Answer to reset o ATR

La prima risposta di una Smart Card inserita in un lettore si chiama
<a href="https://en.wikipedia.org/wiki/Answer_to_reset" target="_blank"
rel="noopener"><strong>ATR</strong></a> (*Answer to reset*). Lo scopo
dell'ATR è descrivere i parametri di comunicazione supportati, la natura
e lo stato della carta. L'ottenimento di un ATR viene spesso utilizzato
come prima indicazione che questa sia operativa, e il suo contenuto
viene esaminato come prima prova che sia del tipo appropriato per un
determinato utilizzo. <span style="text-decoration: underline;">Il
lettore di Smart Card, il driver del lettore e il sistema operativo
utilizzeranno questi parametri per stabilire una comunicazione con la
scheda.</span>

L'ATR è descritto dallo standard
<a href="https://it.wikipedia.org/wiki/ISO/IEC_7816" target="_blank"
rel="noopener"><strong>ISO/IEC 7816-3</strong></a>. I primi byte
dell'ATR descrivono i parametri elettrici, seguiti da byte che
descrivono le interfacce di comunicazione disponibili e i rispettivi
parametri. Questi byte di interfaccia sono quindi seguiti da byte
storici che non sono standardizzati e sono utili per trasmettere
informazioni proprietarie come il tipo di scheda, la versione del
software integrato o lo stato della scheda. Infine questi byte storici
sono eventualmente seguiti da un byte di checksum.

Potremmo riassumere che l'**ATR contiene "un sacco di dati" che ci
dicono vita morte e miracoli della Smart Card**. Per esempio, scopriamo
di più sull'ATR
`3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 01 00 00 00 00 6A` 
utilizzando il tool <a
href="https://smartcard-atr.apdu.fr/parse?ATR=3B8F8001804F0CA000000306030001000000006A"
target="_blank" rel="noopener">Smart card ATR parsing</a> sviluppato da
<a href="https://ludovicrousseau.blogspot.com/" target="_blank"
rel="noopener">Ludovic Rousseau</a>. La figura a seguire mostra le
informazioni estratte alcune delle quali:

- tipo di Smart Card e in questo caso si tratta della MIFARE Classic 1K;
- produttore della Smart Card e in questo caso NXP;
- standard tecnologici;
- protocolli di comunicazione e in questo caso T=0 (orientato al byte,
  che costituisce l'unità minima di informazione scambiata) e T=1
  (orientato al blocco di byte, grazie al quale la velocità di accesso è
  maggiore), protocollo solitamente utilizzato di default quando
  disponibile e supportato anche dal lettore.

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/mifare_classic_1k_atr_parsing-1024x1487.png"
class="size-large wp-image-5529" width="1024" height="1487"
alt="Figura 11 - Dettagli estratti sull&#39;ATR della Smart Card MIFARE Classic 1K" />](https://www.dontesta.it/wp-content/uploads/2022/03/mifare_classic_1k_atr_parsing.png)
Figura 11 - Dettagli estratti sull'ATR della Smart Card MIFARE Classic
1K

 

Ludovic Rousseau ha fatto un ottimo lavoro tracciando dal 2002 un <a
href="http://ludovic.rousseau.free.fr/softwares/pcsc-tools/smartcard_list.txt"
target="_blank" rel="noopener">gran numero di ATR</a> costruendo un vero
e proprio database. Così facendo è possibile identificare una Smart Card
dato il suo ATR. All'interno della lista sono presenti anche le
"nostrane Smart Card" come la **TS-CNS**
(<a href="https://www.agid.gov.it/it/piattaforme/carta-nazionale-servizi"
target="_blank" rel="noopener"><em>Tessera Sanitaria - Carta Nazionale
Servizi</em></a>) e **CIE**
(<a href="https://developers.italia.it/it/cie/" target="_blank"
rel="noopener"><em>Carta d'Identità Elettronica</em></a>). È possibile
utilizzare il comando `pcsc_scan` per ottenere informazioni di dettaglio
sulla Smart Card, le stesse illustrate in figura 11. La figura 12 mostra
l'output del comando menzionato da cui è possibile dedurre che la Smart
Card analizzata è una CIE.

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/output_of_pcsc_scan_smart_card_cie-1024x656.png"
class="size-large wp-image-5532" width="1024" height="656"
alt="Figura 12 - Esempio di output del comando pcsc_scan che mostra le informazioni estratte dalla Smart Card, in questo caso CIE" />](https://www.dontesta.it/wp-content/uploads/2022/03/output_of_pcsc_scan_smart_card_cie.png)
Figura 12 - Esempio di output del comando pcsc_scan che mostra le
informazioni estratte dalla Smart Card, in questo caso CIE

 

## 5. Requisiti Hardware

Realizzare lo scenario descritto richiede il recupero di una serie di
"pezzi di ferro".

1.  <a
    href="https://www.melopero.com/shop/raspberry-pi/boards/raspberry-pi-4-model-b-8gb/?src=raspberrypi"
    rel="nofollow">Raspberry Pi 4 Model B 8GByte RAM</a>
2.  <a
    href="https://www.raspberrypi.com/documentation/computers/getting-started.html#sd-card-for-raspberry-pi"
    rel="nofollow">MicroSD Card (min 8GByte)</a>
3.  <a href="https://amzn.to/3rkr4uw" rel="nofollow">Elegoo 4 Channel DC 5V
    Modulo Relay</a>
4.  <a href="https://amzn.to/3hKuZ1k" target="_blank" rel="noopener">Jumper
    Wire Cable Cavo F2F female to female</a>
5.  <a href="https://shop.bit4id.com/prodotto/minilector-cie/"
    rel="nofollow">Bit4id miniLector CIE</a>
6.  <a href="https://amzn.to/3vkAifZ" rel="nofollow">Mifare Classic 1K</a>
7.  <a href="https://amzn.to/3BReSbF" rel="nofollow">Mifare Classic 1K RFID
    Tag</a> (opzionale)

Per quanto riguarda il Raspberry Pi è possibile optare per la versione
con 4GByte di RAM ma è importante installare come sistema operativo
l'ultima versione di <a
href="https://www.raspberrypi.com/documentation/computers/os.html#introduction"
target="_blank" rel="noopener">Raspberry Pi OS</a> affinché sia
supportato il lettore di Smart Card Bit4id miniLector CIE e questo
grazie alla versione 1.4.34-1 della libreria libccid (check via
`apt info libccid`).

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/debian_apt_info_libccid.png"
class="size-full wp-image-5533" width="1021" height="816"
alt="Figura 13 - Dettaglio del driver libccid necessario per interoperabilità tra Sistema Operativo e lettore di Smart Card" />](https://www.dontesta.it/wp-content/uploads/2022/03/debian_apt_info_libccid.png)
Figura 13 - Dettaglio del driver libccid necessario per interoperabilità
tra Sistema Operativo e lettore di Smart Card

Nel caso in cui abbiate già un lettore di Smart Card o vogliate
acquistarne un diverso modello, consiglio di consultare la
<a href="https://ccid.apdu.fr/ccid/shouldwork.html" target="_blank"
rel="noopener">lista dei lettori di Smart Card supportati dal driver
libccid</a>.

 

## 6. Requisiti Software

Così come abbiamo bisogno dell'hardware, è necessario che siano
soddisfatti una serie di requisiti software, quali:

1.  <a
    href="https://www.raspberrypi.com/documentation/computers/os.html#introduction"
    rel="nofollow">Raspberry Pi OS (64bit)</a>
2.  <a
    href="https://www.raspberrypi.com/documentation/computers/os.html#python"
    rel="nofollow">Python 3.9.x</a> (distribuito e installato di default
    con Raspberry Pi OS)
3.  <a href="https://docs.docker.com/engine/install/debian/"
    rel="nofollow">Docker 20.10.12</a>
4.  <a href="https://packages.debian.org/bullseye/build-essential"
    rel="nofollow">Development Tools (make, gcc)</a> (install or update
    via `sudo apt install build-essential`)

Per questo genere di scenari
<span style="text-decoration: underline;">non è assolutamente necessario
provvedere all'installazione del sistema operativo in versione
Desktop</span>, consiglio pertanto di preparare e usare l'immagine di
<a href="https://www.raspberrypi.com/software/operating-systems/"
target="_blank" rel="noopener">Raspberry Pi OS Lite (64bit)</a>. Per
coloro che avessero bisogno di una guida su come installare questo
sistema operativo, consiglio di seguire la guida ufficiale <a
href="https://www.raspberrypi.com/documentation/computers/getting-started.html#installing-the-operating-system"
target="_blank" rel="noopener">Installing the Operating System</a>.

L'installazione di Docker potrebbe essere anche opzionale; personalmente
preferisco installare il database in forma di container. Più in avanti
vedremo quale database ho scelto per questa soluzione.

Per approfondimenti sul tema Docker, consiglio la lettura del libro
<a href="https://amzn.to/3tiyO1W" target="_blank" rel="noopener">Docker:
Sviluppare e rilasciare software tramite container</a> di
<a href="https://www.linkedin.com/in/serena-sensini/" target="_blank"
rel="noopener">Serena Sensini</a> e la visione delle
<a href="https://www.youtube.com/watch?v=wAyUdtQF05w" target="_blank"
rel="noopener">Pillole di Docker</a> sul canale YouTube
di <a href="https://www.linkedin.com/in/mauro-cicolella-0b107076/"
target="_blank" rel="noopener">Mauro Cicolella</a>.

 

## 7. Schema elettrico della soluzione

Una volta ottenuto l'hardware (indicato in precedenza), possiamo
procedere con il collegamento del modulo dei quattro relè
all'interfaccia GPIO con l'ausilio dei jumper femmina-femmina.

La figura 14 mostra lo schema elettrico di collegamento tra il modulo a
quattro relè e il Raspberry Pi. Ricordo che il lettore di Smart Card è
collegato via USB al Raspberry Pi. Utilizzando i jumper e seguendo lo
schema, il risultato sarà assicurato.
<span style="text-decoration: underline;">È preferibile eseguire
l'operazione di collegamento lasciando il proprio Raspberry Pi spento e
scollegato dalla fonte di alimentazione.</span>

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/schematic_smart_card_contactless_raspberry_pi-1024x724.png"
class="size-large wp-image-5584" width="1024" height="724"
alt="Figura 14 - Schema elettrico di collegamento tra il Raspberry Pi e il modulo da quattro relè" />](https://www.dontesta.it/wp-content/uploads/2022/03/schematic_smart_card_contactless_raspberry_pi.png)
Figura 14 - Schema elettrico di collegamento tra il Raspberry Pi e il
modulo da quattro relè

 

Per ogni dubbio sulla disposizione dei pin del connettore J8 del
Raspberry, consultare l'output del comando `pinout` (vedi figura 15)
prima di procedere con l'operazione di collegamento, oppure, puntate il
vostro browser su <a href="https://pinout.xyz" target="_blank"
rel="noopener">pinout.xyz</a>.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/output_of_the_pinout_command_on_rpi-1024x663.png"
class="size-large wp-image-5536" width="1024" height="663"
alt="Figura 15 - Output del comando pinout, utile per verificare la piedinatura del GPIO e altre informazione sul layout hardware e componenti " />](https://www.dontesta.it/wp-content/uploads/2022/03/output_of_the_pinout_command_on_rpi.png)
Figura 15 - Output del comando pinout, utile per verificare la
piedinatura del GPIO e altre informazione sul layout hardware e
componenti

 

## 8. Progettare il software

È arrivato il momento di saltare dall'hardware al software cercando di
delineare ciò che dovremo implementare con l'obiettivo di soddisfare i
requisiti espressi in forma di diagrammi BPMN (vedi figura 2 e figura
3). Ricordo che solo quanto espresso dai Service Task deve essere
realizzato in forma di software.

Cerchiamo di identificare il **cosa** dovrà essere soddisfatto dal punto
di vista funzionale per poi passare al **come** gli aspetti funzionali
dovranno essere implementati. La tabella mostrata in figura 16
(trasposizione di una classica Mind Map), descrive gli aspetti
funzionali che il software che andremo a realizzare deve implementare.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_functions_software-1024x584.png"
class="size-large wp-image-5539" width="1024" height="584"
alt="Figura 16 - Mind Map sugli aspetti funzionali che il software dovrà implementare" />](https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_functions_software.png)
Figura 16 - Mind Map sugli aspetti funzionali che il software dovrà
implementare

Il software deve prevedere due entry point, ed esattamente quelli
indicati all'interno della tabella di figura 16, le cui responsabilità
devo essere:

- **Setup Smart Card**: entry point la cui principale responsabilità è
  quella di "formattare" la Smart Card (o chiave elettronica) con i dati
  personali dell'ospite e in questo caso il numero del documento
  d'identità, inoltre, creare l'associazione tra chiave elettronica,
  ospite e stanza a lui assegnata. Una volta eseguiti i task di questo
  entry point (vedi figura 16), la Smart Card potrà essere consegnata
  all'ospite.
- **Gestione Accesso Porte** entry point la cui principale
  responsabilità è quella di garantire l'accesso (apertura della porta
  della stanza) solo a coloro che hanno in possesso una Smart Card
  valida, aggiornando i dati di accesso sul database. La Mind Map di
  figura 16 mostra i singoli task che devono essere eseguiti da questo
  specifico entry point.

 

Più volte è stato fatto riferimento all'esistenza di un database, bene,
adesso cerchiamo di capire quali sono i dati da esso trattati e le
responsabilità dei due entry point in merito al trattamento di questi
dati. La tabella di figura 17 mostra la struttura dati del documento che
descrive l'associazione ospite, Smart Card e stanza assegnata e traccia
i dati degli eventi d'inizializzazione e accesso.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_table_guest_access_document-1024x1806.png"
class="size-large wp-image-5543" width="1024" height="1806"
alt="Figura 17 - Struttura dati che descrive l&#39;associazione ospite, smart card e stanza assegnata e traccia i dati gli eventi di inizializzazione e accesso" />](https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_table_guest_access_document.png)
Figura 17 - Struttura dati che descrive l'associazione ospite, smart
card e stanza assegnata e traccia i dati degli eventi d'inizializzazione
e accesso

La tabella mostra un'informazione importante per ogni attributo del
documento, ovvero, lo scope, quindi l'entry point, con evidenza del
diritto di accesso: (r -read) lettura o (w - write) scrittura.

## 9. Implementare il software

Adesso che il **cosa **è chiaro, vediamo il **come**, rispondendo alle
domande a seguire:

1.  Quale linguaggio usare per implementare lo scenario che abbiamo
    descritto all'inizio dell'articolo? **Python**
2.  Esiste qualche libreria Python per la costruzione di applicazioni
    basate su Smart Card?
    <a href="https://pyscard.sourceforge.io/index.html" target="_blank"
    rel="noopener"><strong>Pyscard</strong></a>
3.  Quale tipo di database usare per la memorizzazione dei dati?
    <a href="https://www.mongodb.com/" target="_blank"
    rel="noopener"><strong>MongoDB</strong></a>
    (<a href="https://it.wikipedia.org/wiki/NoSQL" target="_blank"
    rel="noopener">NoSQL</a> database)
4.  Esiste qualche libreria Python per operare con MongoDB?
    <a href="https://pymongo.readthedocs.io/en/stable/" target="_blank"
    rel="noopener"><strong>PyMongo</strong></a>
5.  Esiste qualche libreria Python per interagire con l'interfaccia GPIO
    del Raspberry
    Pi? **<a href="https://pypi.org/project/RPi.GPIO/" target="_blank"
    rel="noopener"><span class="pl-v">RPi</span>.<span
    class="pl-v">GPIO</span></a>**

Da questa lista le cose da fare sono parecchie e lo spazio per vederle
tutte nel dettaglio in questo articolo non c'è. Direi quindi di
focalizzare la nostra attenzione sui componenti da realizzare rimanendo
ad alto livello, senza scendere nello specifico del codice.

**Non vi allarmate!** Il progetto è già stato sviluppato prima di
scrivere questo articolo e disponibile sul mio repository GitHub
<a href="https://github.com/amusarra/smartcard-contactless-raspberry-pi"
target="_blank" rel="noopener">Smart Card Contactless Raspberry Pi</a>.

**Nota su MongoDB**. È necessario preparare un'instanza di MongoDB sul
proprio Raspberry Pi affinche la soluzione funzioni nel modo corretto.
Le scelte sono due: container docker o installazione classica
direttamente sul sistema operativo. Personalmente ho scelto la strada di
Docker (vedi 6. Requisiti Software), per cui, una volta
<a href="https://docs.docker.com/engine/install/debian/" target="_blank"
rel="noopener">installato Docker sul proprio Raspberry Pi OS</a>, i
passi per tirare su un'istanza MongoDB 4.4.12 sono quelli indicati a
seguire.

 

    [code lang="bash" toolbar="true" title="Console 1 - Pull dell&#039;immagine MongoDB 4.4.12 e run del container"]
    # 1. Docker pull e run MongoDB 4.4.12
    $ docker pull mongo:4.4.12
    $ docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:4.4.12

    # 2. Verifica che l'istanza sia su e accesso alla console bash (task opzionale)
    $ docker exec -it mongodb bash

    # 3. Avvio della console MongoDB (task opzionale)
    root@0d21da235b0d:/# mongo
    [/code]

Nel caso in cui preferiate perseguire la seconda strada, il blog di
MongoDB riporta la procedura completa sull'articolo <a
href="https://www.mongodb.com/developer/how-to/mongodb-on-raspberry-pi/"
target="_blank" rel="noopener">Install &amp; Configure MongoDB on the
Raspberry Pi</a>.

 

### 9.1 Cos'è Pyscard

**Pyscard**, Python Smart Card library, è un modulo Python che aggiunge
il supporto per le Smart Card facilitando la costruzione di applicazioni
che hanno la necessità di utilizzare la tecnologia delle Smart Card.

Pyscard supporta la piattaforma Microsoft Windows utilizzando i
componenti <a
href="https://docs.microsoft.com/en-us/previous-versions/windows/desktop/secsmart/microsoft-base-smart-card-cryptographic-service-provider"
target="_blank" rel="noopener">Microsoft Smart Card Base</a>, Linux e
macOS utilizzando <a href="https://pcsclite.apdu.fr/" target="_blank"
rel="noopener">PCSC-lite</a>. Il diagramma di figura 18 mostra
l'architettura Pyscard (box in verde). Il modulo <a
href="https://pyscard.sourceforge.io/epydoc/smartcard.scard.scard-module.html"
class="reference external">smartcard.scard</a> è il wrapper di WinSCard
API (*smart card base components*). Il modulo
<a href="https://pyscard.sourceforge.io/epydoc/index.html"
class="reference external">smartcard</a> è un vero e proprio framework
costruito su PC/SC API.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/architecture_of_the_pyscard_library-1024x931.jpg"
title="Figura 18 - Architettura di Pyscard"
class="wp-image-5554 size-large" width="1024" height="931"
alt="Figura 18 - Architettura di Pyscard" />](https://www.dontesta.it/wp-content/uploads/2022/03/architecture_of_the_pyscard_library-scaled.jpg)
Figura 18 - Architettura di Pyscard

Pyscard sarà di aiuto per:

1.  Eseguire la connessione al lettore di Smart Card e alla MIFARE
    Classic 1K
2.  Filtrare le connessioni alle sole MIFARE Classic 1K tramite l'ATR
3.  Inviare i comandi APDU
4.  Ricevere le risposte ai comandi APDU
5.  Intercettare gli eventi di aggiunta e rimozione Smart Card dal
    lettore

###  

### 9.2 Struttura del progetto software

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
Figura 19 - Package/Component/Class diagram del progetto Smart Card
Contactless Raspberry Pi

 

Il package *smartcard* (in verde) fa parte di Pyscard, e i componenti
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
Figura 20 - Diagramma di sequenza dell'entry point Setup Smart Card

Nella fase di setup della Smart Card, prima di inserire i dati
anagrafici dell'ospite sul database, viene eseguita la query utilizzando
il filtro
`{`<span class="pl-s">`"smartCardId"`</span>`: `<span class="pl-s">`f"`<span class="pl-s1"><span class="pl-kos">`{`</span>`uid`<span class="pl-kos">`}`</span></span>`"`</span>`, `<span class="pl-s">`"documentId"`</span>`: `<span class="pl-s">`f"`<span class="pl-s1"><span class="pl-kos">`{`</span>`identification_number`<span class="pl-kos">`}`</span></span>`"`</span>`}`
, in modo che sia possibile verificare che non esista già un documento
con l'associazione smartCardId e documentId (fare riferimento allo step
33 del sequence diagram di figura 20).

Il sequence diagram di figura 21 descrive lo scenario di Accesso alla
stanza tramite Smart Card (vedi Figura 3 - Processo di accesso alla
stanza), mostrando le azioni principali e gli eventuali flussi
alternativi. Sempre da questo diagramma possiamo vedere le relazioni che
intercorrono, in termini di messaggi, tra i vari attori, quest'ultimi
sono stati descritti in precedenza e mostrati nel diagramma di figura
19.

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
Figura 21 - Diagramma di sequenza per l'entry point Access via Smart
Card

I dati sono estratti dal database MongoDB utilizzando il filtro
`{"smartCardId": f"{uid}", "documentId":f{identification_number}", "smartCardEnabled": "true"}`,
nel caso non ci siano documenti che rispettino questo filtro, il sistema
negerà l'accesso, alternativamente, sarà aggiornato il documento su
MongDB e attivato il relè corrispondente al numero della stanza
associato all'ospite (fare riferimento allo step 1.7 del sequence
diagram di figura 21).

Molto bene! Una volta descritti i sequence diagram dei nostri due
scenari, direi che potremmo passare all'azione, ovvero, eseguire il
deploy dell'applicazione sul Raspberry Pi 4.

 

## 10. Deploy e test del software sul Raspberry Pi

Ci siamo! È arrivato il momento d'installare il progetto software sul
Raspberry Pi e verificare che tutto funzioni così per com'è stato
ideato. Il deployment diagram della figura a seguire mostra tutti i
componenti del nostro sistema di accesso.

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/system_deployment_on_raspberry-1024x891.png"
class="size-large wp-image-5562" width="1024" height="891"
alt="Figura 22 - Deployment diagram del sistema di accesso via Smart Card Contactless su Raspberry Pi" />](https://www.dontesta.it/wp-content/uploads/2022/03/system_deployment_on_raspberry.png)
Figura 22 - Deployment diagram del sistema di accesso via Smart Card
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

 

    [code lang="bash" toolbar="true" title="Console 2 - Installazione del progetto software"]
    # Accesso al Raspberry Pi via SSH
    $ ssh amusarra@192.168.238.169

    # Clone del repository GitHub del progetto
    $ git clone https://github.com/amusarra/smartcard-contactless-raspberry-pi.git

    # Installazione delle dipendenze Python
    $ cd smartcard-contactless-raspberry-pi
    $ make
    [/code]

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
Figura 23 - Installazione delle dipendenze Python tramite il comando
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
Figura 24 - Tabella dei parametri d'input per lo script Python
setup_smart_card.py

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_script_access_via_smart_card-1024x265.png"
title="Figura 25 - Tabella dei parametri d&#39;input per lo script Python access_via_smart_card.py"
class="wp-image-5573 size-large" width="1024" height="265"
alt="Figura 25 - Tabella dei parametri d&#39;input per lo script Python access_via_smart_card.py" />](https://www.dontesta.it/wp-content/uploads/2022/03/mind_map_script_access_via_smart_card.png)
Figura 25 - Tabella dei parametri d'input per lo script Python
access_via_smart_card.py

La figura 26 mostra un esempio di come si presenta l'help in linea dello
script `setup_smart_card.py` attivato utilizzando l'opzione `--help` (o
`-h`).

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/setup_smart_card.py_help_option-1024x618.png"
class="size-large wp-image-5574" width="1024" height="618"
alt="Figura 26 - Come si presenta l&#39;help in line dello script setup_smart_card.py" />](https://www.dontesta.it/wp-content/uploads/2022/03/setup_smart_card.py_help_option.png)
Figura 26 - Come si presenta l'help in linea dello script
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
Figura 27 - Registrazione Smart Card MIFARE Classic 1K con i dati
dell'ospite

Dopo la registrazione della Smart Card e la consegna all'ospite,
quest'ultimo può usare la Smart Card per accedere alla propria stanza
assegnata in fase di registrazione, che ricordo essere la numero due.

 

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/smart_card_registration_data_on_mongodb_1-1024x974.png"
class="size-large wp-image-5577" width="1024" height="974"
alt="Figura 28 - Documento registrato su MongoDB a fronte del processo di registrazione Smart Card" />](https://www.dontesta.it/wp-content/uploads/2022/03/smart_card_registration_data_on_mongodb_1.png)
Figura 28 - Documento registrato su MongoDB a fronte del processo di
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
Figura 29 - Richiesta di accesso via Smart Card MIFARE Classic 1K

L'output mostrato dalla figura 29 evidenzia anche un accesso non
riuscito perché in questo caso la Smart Card presentata non è registrata
sul sistema. Gli screencast a seguire mostrano i due entry point in
azione: setup_smart_card.py e access_via_smart_card.py.

<a href="https://asciinema.org/a/475795" target="_blank"
rel="noopener"><img src="https://asciinema.org/a/475795.svg"
title="Screencast 1 - Processo di registrazione Smart Card in azione"
width="1223" height="784"
alt="Screencast 1 - Processo di registrazione Smart Card in azione" /></a>
Screencast 1 - Processo di registrazione Smart Card in azione

 

<a href="https://asciinema.org/a/475797" target="_blank"
rel="noopener"><img src="https://asciinema.org/a/475797.svg"
title="Screencast 2 - Processo di accesso alla stanza via Smart Card in azione"
width="1223" height="784"
alt="Screencast 2 - Processo di accesso alla stanza via Smart Card in azione" /></a>
Screencast 2 - Processo di accesso alla stanza via Smart Card in azione

Dopo i due screencast che mostrano il sistema di accesso in azione,
possiamo affermare che il nostro lavoro di analisi, progettazione e
implementazione sia arrivato al termine, raggiungendo anche l'obiettivo
prefissato.

## 11. Conclusioni

Ringrazio tutti voi per essere arrivati “incolumi” alla fine di questo
lungo percorso sperando di non essere stato noioso e di essere riuscito
nell’intento di rendere interessanti gli argomenti trattati oltre che a
spingere la vostra curiosità in avanti.

Potrei lasciarvi un compito per casa: **come aprire la porta di casa
utilizzando la propria CIE o TS-CNS**.

Mi sarebbe piaciuto approfondire maggiormente alcuni degli argomenti
trattati, come per esempio il framework Pyscard e alcune sezioni del
codice Python sviluppato. Nell’attesa di pubblicare altri articoli di
approfondimento, vi chiedo di scrivere le vostre impressioni, esperienze
o altro di cui vorreste qualche approfondimento utilizzando i commenti
all’articolo oppure condividendo attraverso i classici canali social.

Sempre nell'ottica Open Source, il progetto
<a href="https://github.com/amusarra/smartcard-contactless-raspberry-pi"
target="_blank" rel="noopener">Smart Card Contactless Raspberry Pi</a>
pubblicato sul mio repository GitHub, contiene all'interno della
directory <a
href="https://github.com/amusarra/smartcard-contactless-raspberry-pi/tree/master/docs"
target="_blank" rel="noopener">docs</a> i seguenti elementi:

- il file diagrams.drawio contenente diagrammi e tabelle. File che
  potete aprire con <a href="https://app.diagrams.net/" target="_blank"
  rel="noopener">Draw.io</a>
- il file SCH_Smart_Card_Contactless_Raspberry_Pi_2022-03-11.json dello
  schema elettrico che potete aprire con
  <a href="https://easyeda.com/" target="_blank"
  rel="noopener">EasyEDA</a>
- i file UML \*.puml di <a href="https://plantuml.com/" target="_blank"
  rel="noopener">PlantUML</a> che contengono i sequence diagram

 

## 12. Risorse

Come di consueto lascio una serie di risorse che ritengo utili ai fini
dell’approfondimento degli argomenti trattati nel corso di questo
articolo.

- Attuatori per maker
  – <a href="https://amzn.to/3slHmE9" target="_blank"
  rel="noopener">https://amzn.to/3slHmE9</a>
- Raspberry Pi. La guida completa
  – <a href="https://amzn.to/2RpYZWh" target="_blank"
  rel="noopener">https://amzn.to/2RpYZWh</a>
- Docker: Sviluppare e rilasciare software tramite container
  – <a href="https://amzn.to/3tiyO1W" target="_blank"
  rel="noopener">https://amzn.to/3tiyO1W</a> 
  di <a href="https://www.linkedin.com/in/serena-sensini/" target="_blank"
  rel="noopener">Serena Sensini</a>
- Valutiamo se continuare a usare Docker o passare a Podman
  – <a href="https://www.theredcode.it/podman/what-is-podman/"
  target="_blank"
  rel="noopener">https://www.theredcode.it/podman/what-is-podman/</a>
- Pillole di Docker
  – <a href="https://www.youtube.com/watch?v=wAyUdtQF05w" target="_blank"
  rel="noopener">https://www.youtube.com/watch?v=wAyUdtQF05w</a> di <a href="https://www.linkedin.com/in/mauro-cicolella-0b107076/"
  target="_blank" rel="noopener">Mauro Cicolella</a>
- Raspberry PI GPIO – Tutti i segreti del pinout – <a
  href="https://www.moreware.org/wp/blog/2021/04/09/raspberry-pi-gpio-tutti-i-segreti-del-pinout/"
  target="_blank"
  rel="noopener">https://www.moreware.org/wp/blog/2021/04/09/raspberry-pi-gpio-tutti-i-segreti-del-pinout/</a>
- Smart cards – A short illustrated guide ( Feb. 2022) - <a
  href="https://www.thalesgroup.com/en/markets/digital-identity-and-security/technology/smart-cards-basics"
  target="_blank"
  rel="noopener">https://www.thalesgroup.com/en/markets/digital-identity-and-security/technology/smart-cards-basics</a>
- Hacking Mifare Classic Cards - <a
  href="https://www.blackhat.com/docs/sp-14/materials/arsenal/sp-14-Almeida-Hacking-MIFARE-Classic-Cards-Slides.pdf"
  target="_blank"
  rel="noopener">https://www.blackhat.com/docs/sp-14/materials/arsenal/sp-14-Almeida-Hacking-MIFARE-Classic-Cards-Slides.pdf</a>
- How to Crack Mifare Classic Cards -
  <a href="https://firefart.at/post/how-to-crack-mifare-classic-cards/"
  target="_blank"
  rel="noopener">https://firefart.at/post/how-to-crack-mifare-classic-cards/</a>
- A Practical Attack on the MIFARE Classic -
  <a href="https://arxiv.org/pdf/0803.2285.pdf" target="_blank"
  rel="noopener">https://arxiv.org/pdf/0803.2285.pdf</a>
-  ACR122U Application Programming Interface - <a
  href="https://www.acs.com.hk/download-manual/419/API-ACR122U-2.04.pdf"
  target="_blank"
  rel="noopener">https://www.acs.com.hk/download-manual/419/API-ACR122U-2.04.pdf</a>

\[:\]
