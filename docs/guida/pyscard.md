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
**Figura 18** - Architettura di Pyscard

Pyscard sarà di aiuto per:

1.  Eseguire la connessione al lettore di Smart Card e alla MIFARE
    Classic 1K
2.  Filtrare le connessioni alle sole MIFARE Classic 1K tramite l'ATR
3.  Inviare i comandi APDU
4.  Ricevere le risposte ai comandi APDU
5.  Intercettare gli eventi di aggiunta e rimozione Smart Card dal
    lettore