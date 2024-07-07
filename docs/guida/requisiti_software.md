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
    rel="nofollow">Development Tools (make, gcc)</a> (install or update
    via `sudo apt install build-essential`)

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
di <a href="https://www.linkedin.com/in/mauro-cicolella-0b107076/"
target="_blank" rel="noopener">Mauro Cicolella</a>.