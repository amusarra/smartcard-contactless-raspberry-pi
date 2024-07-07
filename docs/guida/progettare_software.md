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
**Figura 16** - Mind Map sugli aspetti funzionali che il software dovrà
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
**Figura 17** - Struttura dati che descrive l'associazione ospite, smart
card e stanza assegnata e traccia i dati degli eventi d'inizializzazione
e accesso

La tabella mostra un'informazione importante per ogni attributo del
documento, ovvero, lo scope, quindi l'entry point, con evidenza del
diritto di accesso: (r -read) lettura o (w - write) scrittura.