# I misteriosi pacchetti APDU

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
**Figura 6** - Struttura dei comandi APDU

La tabella di figura 7 mostra un esempio di comando APDU per ottenere
l'UID della MIFARE Classic 1K, la cui lunghezza è pari a 4 byte (vedi
attributo Le). A fronte dei comandi inviati, riceviamo sempre una
risposta che ha la struttura indicata dalla tabella di figura 8.

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/apdu_command_for_request_uid-1024x464.jpg"
class="size-large wp-image-5514" width="1024" height="464"
alt="Figura 7 - Comando per ottenere l&#39;UID della Smart Card MIFARE Classic 1K" />](https://www.dontesta.it/wp-content/uploads/2022/03/apdu_command_for_request_uid.jpg)
**Figura 7** - Comando per ottenere l'UID della Smart Card MIFARE Classic 1K

[<img
src="https://www.dontesta.it/wp-content/uploads/2022/03/structure_of_response_command_apdu-1-1024x521.jpg"
title="Figura 8 - Struttura di risposta APDU"
class="wp-image-5522 size-large" width="1024" height="521"
alt="Figura 8 - Struttura di risposta APDU" />](https://www.dontesta.it/wp-content/uploads/2022/03/structure_of_response_command_apdu-1.jpg)
**Figura 8** - Struttura di risposta APDU

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
**Figura 9** - Risposta del comando APDU per ottenere l'UID della MIFARE
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
**Figura 10** - Codici di risposta APDU comando UID

Per maggiori dettagli sui comandi ed eventuali estensioni, consiglio
sempre di consultare il datasheet della
<a href="https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf"
target="_blank" rel="noopener">MIFARE Classic 1K</a>. I comandi APDU di
nostro interesse per implementare lo scenario descritto nella parte
introduttiva dell'articolo, sono:

- comando per ottenere l'UID della carta;
- comando per leggere i dati da un determinato settore e blocco;
- comando per scrivere dati su un determinato settore e blocco della carta.