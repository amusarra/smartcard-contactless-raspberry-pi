# Smart Card Contactless Raspberry Pi
[![Antonio Musarra's Blog](https://img.shields.io/badge/maintainer-Antonio_Musarra's_Blog-purple.svg?colorB=6e60cc)](https://www.dontesta.it)
[![Twitter Follow](https://img.shields.io/twitter/follow/antonio_musarra.svg?style=social&label=%40antonio_musarra%20on%20Twitter&style=plastic)](https://twitter.com/antonio_musarra)

This is a project linked to an article that I will shortly publish on my [blog](https://www.dontesta.it). When described 
in this README it should be enough to make you understand the intentions of this project, the rest I leave to your 
curiosity.

This project was born with the aim of providing a complete example (hardware and software) on how it is possible to 
create a simple access system using contactless Smart Cards and the Raspberry Pi. The figure below shows the hardware 
diagram of the Smart Card access solution.

The scenario I created is the one that each of us experiences almost every day, that is, with our hands a Smart Card 
to gain access to an opening, which could for example be a door to a hotel room.

![Hardware diagram of the Smart Card access solution](docs/images/hardware_diagram_smartcard_access_raspberry_pi_1.jpg)

Figure 1 - Hardware diagram of the Smart Card access solution (Smart Card icon from https://www.smartcardfocus.com/)

The [MIFARE Classic® 1K](https://www.nxp.com/docs/en/data-sheet/MF1S50YYX_V1.pdf) contactless is predicated on 
**NXP MF1 IC S50**, which is connected to a coil with a couple of turns then embedded into the plastic to make the 
passive contactless open-end credit. The communication layer (MIFARE RF Interface) complies with part 2 and three 
of the [ISO/IEC14443A](https://en.wikipedia.org/wiki/ISO/IEC_14443) standard. This type of card is a good choice for 
classic applications such as public transport ticketing and can also be used for several other applications 
(door opening systems and the like). 

The Smart Card Reader must be compliant with the standards indicated in the diagram in figure 1. In my case I used 
the [Bit4id miniLector CIE](https://shop.bit4id.com/prodotto/minilector-cie/) reader connected to the Raspberry Pi via 
the USB port. The technical name of the reader I used is: BIT4ID miniLector AIR NFC v3.

A four-relay module managed through the [GPIO](https://en.wikipedia.org/wiki/General-purpose_input/output) ports is 
connected to the Raspberry Pi. In our scenario, the relays represent the actuators necessary to open the doors of the 
hotel where we are guests.

Figure 2 illustrates the simplified process (in [BPMN](https://www.bpmn.org/) notation) of what happens when a guest is 
received by the hotel staff. Of the whole process, only the service task (indicated in red) is the object of the 
software implementation.

![Guest Receiving Process](docs/images/guest_receiving_process.jpg)

Figure 2 - Simplified process of receiving the guest at the hotel.

The process of figure 3 instead shows what happens when the guest asks to enter his room through the use of the 
electronic key by placing it on the reader. Of the whole process, only the service task (indicated in red) is the 
object of the software implementation.

![Room access process](docs/images/room_access_process.jpg)

Figure 3 - Room access process

The software of this project written in Python implements the service tasks indicated in the processes of figure 2 and 
figure 3. In particular, the entry points are:

1. `setup_smart_card.py`. Python script that implements the service task indicated in the process of figure 2. 
This script receives a series of input data (number of identity document, room number, name and surname of the 
guest). Of the received data, some are stored on the Smart Card (identity document number) and others on the 
database (in this case MongoDB).
2. `access_via_smart_card.py`. Python script that implements the service task indicated in the process of 
figure 3. This script extracts from the Smart Card the identification of the same and the number of the identity 
document, then uses this data to understand if the guest can have access to his room.

Table 1 shows the data managed by the Smart Card. The UID is actually proper to the Smart Card, however, the 
Identification Number attribute is written during the setup phase by the `setup_smart_card.py` script and read during the access 
request phase by the `access_via_smart_card.py` script.

| Attribute Name        | Description                                                                      | Type     | 
|:----------------------|:---------------------------------------------------------------------------------|:---------| 
| UID                   | Smart Card ID assigned by the manufacturer. In this case we use the 4-byte NUID. | Byte(4)  |
| Identification Number | Number (which can also be alphanumeric) of the guest's identity document.        | Byte(16) |

Table 1 - Data that is stored on the Smart Card.

Table 2 shows the data managed by the database (MondoDB). The scope column indicates which python script used (for 
reading or writing) the attribute, therefore, identifies on which process it is used (setup procedure or access 
procedure).

Console 3 shows the document created on the database during the Smart Card setup phase. Console 5 shows the document 
updated when requesting access via the Smart Card.

| Attribute Name    | Scope                                         | Description                                                               | Type                                  | 
|:------------------|:----------------------------------------------|:--------------------------------------------------------------------------|:--------------------------------------| 
| createDate        | setup_smart_card.py                           | Date when document/record was registered on the system.                   | Date Time with Time Zone (ISO Format) |
| modifiedDate      | access_via_smart_card.py                      | Date whose purpose is to track each document / record update.             | Date Time with Time Zone (ISO Format)                   |
| firstAccess       | access_via_smart_card.py                      | Date representing the first access to the system via the Smart Card.      | Date Time with Time Zone (ISO Format)                         |
| lastAccess        | access_via_smart_card.py                      | Date representing the last access to the system via the Smart Card.       | Date Time with Time Zone (ISO Format)                                |
| smartCardInitDate | setup_smart_card.py                           | Date when the Smart Card was registered on the system.                    | Date Time with Time Zone (ISO Format)                                |
| smartCardId       | setup_smart_card.py, access_via_smart_card.py | UID (4 byte) of the Smart Card                                            | String                                                               |
| smartCardEnabled  | setup_smart_card.py, access_via_smart_card.py | Indicates if the Smart Card is enabled (true), false otherwise.           | Boolean                                                              |
| documentId        | setup_smart_card.py, access_via_smart_card.py | Number (which can also be alphanumeric) of the guest's identity document. | String                                                               |
| roomNumber        | setup_smart_card.py, access_via_smart_card.py | Number of the assigned room                                               | Int                                                                       |
| countAccess       | setup_smart_card.py, access_via_smart_card.py | Number of successful accesses.                                            | Int                                                                       |
| firstName         | setup_smart_card.py                           | Name of the guest to whom the Smart Card is assigned.                     | String                                                                    |
| lastName          | setup_smart_card.py                           | Lastaname of the guest to whom the Smart Card is assigned.                | String                                                                    |

Table 2 - Data that is stored on the database (MongoDB).


## 1. Hardware Requirements

1. [Raspberry Pi 4 Model B 8GByte RAM](https://www.melopero.com/shop/raspberry-pi/boards/raspberry-pi-4-model-b-8gb/?src=raspberrypi)
2. [MicroSD Card (min 8GByte)](https://www.raspberrypi.com/documentation/computers/getting-started.html#sd-card-for-raspberry-pi)
3. [Elegoo 4 Channel DC 5V Modulo Relay](https://amzn.to/3rkr4uw)
4. [Bit4id miniLector CIE](https://shop.bit4id.com/prodotto/minilector-cie/)
5. [Mifare Classic 1K](https://amzn.to/3vkAifZ)
6. [Mifare Classic 1K RfId Tag](https://amzn.to/3BReSbF)

## 2. Software Requirements

1. [Raspberry Pi OS (64bit)](https://www.raspberrypi.com/documentation/computers/os.html#introduction)
2. [Python 3.9.x](https://www.raspberrypi.com/documentation/computers/os.html#python)
3. [Docker 20.10.12](https://docs.docker.com/engine/install/debian/)
4. [Development Tools (make, gcc)](https://packages.debian.org/bullseye/build-essential) (install or update via `sudo apt install build-essential`)

## 3. Wiring diagram of the solution
Figure 4 shows the wiring diagram for connecting the four relay module to the GPIO pins of the Raspberry Pi 4. I 
remember that the Smart Card reader is connected via USB to the Raspberry Pi 4, for this reason it has not been 
included in the wiring diagram.

![Wiring diagram Raspberry Pi and Relays Module](docs/images/wiring_diagram_solution.png)

Figure 4 - Wiring diagram Raspberry Pi and Relays Module

## 4. Quick-start
The fundamental steps to be able to try the solution immediately are indicated below.
1. Login to your Raspberry Pi
2. Clone project, install the python requirements and prepare MongoDB
3. Smart Card Initialization
4. Run the Smart Card Access Tool

To perform the reading and writing operations on the Smart Card, an authentication key is required, the default value 
is `FFFFFFFFFFFF`. This key must be passed to both Python scripts via the `-a` or `--authentication-key` option. For 
details on accepted options, use the `-h` or `--help` option.

```bash
# 1. Clone the repository
$ git clone https://github.com/amusarra/smartcard-contactless-raspberry-pi.git
$ cd smartcard-contactless-raspberry-pi

# 2. Install the Python requirements
$ make

# 3. Docker pull and run MongoDB 4.4.12
$ docker pull mongo:4.4.12
$ docker run -d -p 27017-27019:27017-27019 --name mongodb mongo:4.4.12

# 4. Check MongoDB logs and howto access to the MongoDB console (optional task)
$ docker exec -it mongodb bash

# Inside the MongoDB Docker Container
root@0d21da235b0d:/# mongo
```
Console 1 - Clone project, install the python requirements and prepare MongoDB


```bash
# 1. Smart Card Initialization
#   a) Store Identity document number (example: identity card, driving license, 
#      social security number, passport number) on Smart Card
#   b) Association of the Smart Card to the specific person and assignment of the room.
$ cd smartcard-contactless-raspberry-pi

# Setup Smart Card for Antonio Musarra with identity card DA789876DF and assign room number one (1) 
$ ./setup_smart_card.py -a FFFFFFFFFFFF -i DA789876DF -s --firstname Antonio --lastname Musarra -r 1
```
Console 2 - Smart Card Initialization


![Smart Card Init Tool](docs/images/initialize_smart_card_1.png)
Figure 1 - Run the Smart Card Init Tool to init the first Smart Card

```bash
# 1. Run the mongo console from Docker Container
root@0d21da235b0d:/# mongo

# 2. Use the SmartCardAccessCrudDB and view the SmartCardAccess collection
> use SmartCardAccessCrudDB
> db.SmartCardAccess.find().pretty()
{
	"_id" : ObjectId("62195fbf93c42ff88754734e"),
	"createDate" : "2022-02-25T23:01:19.682355Z",
	"firstname" : "Antonio",
	"lastname" : "Musarra",
	"documentId" : "DA789876DF",
	"smartCardEnabled" : "true",
	"smartCardId" : "B4 90 90 1E",
	"smartCardInitDate" : "2022-02-25T23:01:19.682582Z",
	"roomNumber" : 1,
	"countAccess" : 0
}
```
Console 3 - Check entry on MongoDB

```bash
# 1. Start the Smart Card Access Tool
#   a) Read the Identification Number from Smart Card
#   b) Check on MongoDB if the Smart Card is paired and enabled
#   c) If the association is valid then it opens the door of the room to 
#      which the card is associated. Opening corresponds to the activation 
#      of the relay which is deactivated after five seconds.
$ cd smartcard-contactless-raspberry-pi

# Run the Smart Card Access Tool
$ ./access_via_smart_card.py -a FFFFFFFFFFFF
```
Console 4 - Run the Smart Card Access Tool

![Run Smart Card Access Tool](docs/images/run_smart_card_access_tool_1.png)
Figure 2 - Run the Smart Card Access Tool

```bash
> db.SmartCardAccess.find().pretty()
{
	"_id" : ObjectId("62195fbf93c42ff88754734e"),
	"createDate" : "2022-02-25T23:01:19.682355Z",
	"firstname" : "Antonio",
	"lastname" : "Musarra",
	"documentId" : "DA789876DF",
	"smartCardEnabled" : "true",
	"smartCardId" : "B4 90 90 1E",
	"smartCardInitDate" : "2022-02-25T23:01:19.682582Z",
	"roomNumber" : 1,
	"countAccess" : 5,
	"firstAccess" : "2022-02-25T23:15:36.523275Z",
	"lastAccess" : "2022-02-25T23:27:33.645680Z",
	"modifiedDate" : "2022-02-25T23:27:33.645727Z"
}
{
	"_id" : ObjectId("62196645c6b265cd472d58ca"),
	"createDate" : "2022-02-25T23:29:09.869289Z",
	"firstname" : "Valentina",
	"lastname" : "Musarra",
	"documentId" : "MU589876XD",
	"smartCardEnabled" : "true",
	"smartCardId" : "13 9E 55 73",
	"smartCardInitDate" : "2022-02-25T23:29:09.869317Z",
	"roomNumber" : 2,
	"countAccess" : 3,
	"firstAccess" : "2022-02-25T23:29:18.392172Z",
	"lastAccess" : "2022-02-25T23:29:40.846213Z",
	"modifiedDate" : "2022-02-25T23:29:40.846276Z"
}
```
Console 5 - Data display to check for updates following accesses
