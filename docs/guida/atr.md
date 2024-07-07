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
**Figura 11** - Dettagli estratti sull'ATR della Smart Card MIFARE Classic
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
**Figura 12** - Esempio di output del comando pcsc_scan che mostra le
informazioni estratte dalla Smart Card, in questo caso CIE