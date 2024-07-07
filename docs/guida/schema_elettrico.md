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
**Figura 14** - Schema elettrico di collegamento tra il Raspberry Pi e il
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
**Figura 15** - Output del comando pinout, utile per verificare la
piedinatura del GPIO e altre informazione sul layout hardware e
componenti