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
**Figura 13** - Dettaglio del driver libccid necessario per interoperabilità
tra Sistema Operativo e lettore di Smart Card

Nel caso in cui abbiate già un lettore di Smart Card o vogliate
acquistarne un diverso modello, consiglio di consultare la
<a href="https://ccid.apdu.fr/ccid/shouldwork.html" target="_blank"
rel="noopener">lista dei lettori di Smart Card supportati dal driver
libccid</a>.