# Dettagli sulle carte MIFARE Classic 1K

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
rel="noopener">ISO/IEC 14443A</a> (caratteristiche
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
rel="noopener">NXP (CRYPTO1)</a> per l'autenticazione e
la crittografia che è stato
<span style="text-decoration: underline;">rotto nel 2008</span>.

Dopo l'ultima frase immagino che vi stiate domandando: **perché scrivere
allora un articolo su questa Smart Card?** 

La risposta è abbastanza semplice. Questa è una delle <a
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
**Figura 4** - Struttura della memoria della Mifare Classic 1K (dal
datasheet NXP MIFARE Classic EV1 1K
https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf)

Prima di poter compiere operazioni di lettura o scrittura sui blocchi di
memoria, è necessario eseguire prima un'autenticazione tramite la chiave
del settore del blocco. In genere tutte le chiavi (A e B) sono impostate
su valore `FFFFFFFFFFFFh` in fase di produzione del chip (e in ogni caso
la documentazione fornita al momento dell'acquisto fornisce indicazioni
sulle chiavi di accesso e su come eseguire la modifica).

La tabella mostrata in figura 5 rappresenta la mappa della memoria con
in evidenza il range degli indirizzi per i *Data Blocks* e i *Trailer
Block* per ogni settore. Questa mappa sarà utile nel momento in cui
dovremo leggere e scrivere sui data blocks.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/mifare_1K_memory_map-2-1024x602.jpg"
title="Figura 5 - Memory Map della MIFARE Classic 1K completa di range d&#39;indirizzi dei blocchi"
class="wp-image-5521 size-large" width="1024" height="602"
alt="Figura 5 - Memory Map della MIFARE Classic 1K completa di range d&#39;indirizzi dei blocchi" />](https://www.dontesta.it/wp-content/uploads/2022/03/mifare_1K_memory_map-2.jpg)
**Figura 5** - Memory Map della MIFARE Classic 1K completa di range
d'indirizzi dei blocchi

Dopo questa sorvolata sulle caratteristiche principali della MIFARE
Classic 1K che sono di nostro interesse per il nostro obiettivo,
possiamo andare avanti ed esplorare il modo su come comunicare con la
carta per le operazioni di autenticazione, lettura e scrittura.