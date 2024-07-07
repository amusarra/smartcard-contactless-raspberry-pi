# Introduzione

Le [Smart Card](https://it.wikipedia.org/wiki/Smart_card) fanno parte ormai da tempo del nostro quotidiano: 
dalla [SIM (Subscriber Identity Module)](https://it.wikipedia.org/wiki/Carta_SIM) del cellulare, alla carta di
credito, come sistema di fidelizzazione, per accedere ai locali e come mezzo per fruire dei servizi della pubblica
amministrazione.

Integrare sistemi di autenticazione basati su Smart Card nei propri sistemi e applicazioni, credo che possa essere
un'attività molto interessante per chi programma e l'aspetto a mio avviso più coinvolgente è la vicinanza con quelli
che amo definire bonariaménte **"pezzi di ferro"**.

Quasi due anni fa ho scritto l'articolo [Raspberry Pi – Un esempio di applicazione della TS-CNS](https://www.dontesta.it/2020/07/17/raspberry-pi-esempio-applicazione-ts-cns-smartcard), 
dove mostravo come poter creare un sistema di accesso utilizzando la propria TS-CNS; in questo articolo vedremo
invece come mettere insieme: [Raspberry Pi](https://www.raspberrypi.org/), modulo da quattro relè, lettore di Smart
Card e [MIFARE Classic 1K](https://en.wikipedia.org/wiki/MIFARE) contactless Smart Card per poi armonizzare il tutto,
sviluppando il software necessario allo scopo di realizzare un sistema di accesso.

Per lo sviluppo del progetto è necessario toccare un numero considerevole di argomenti e cercherò di trattare i
principali con il giusto livello di profondità, in caso contrario l’articolo assumerebbe delle dimensioni notevoli.
Mi impegnerò a lasciare tutti i riferimenti utili per ogni vostro approfondimento.

A questo punto direi d’iniziare; mettetevi comodi e munitevi della giusta concentrazione perché la lettura di questo
articolo sarà abbastanza impegnativa ma spero interessante.