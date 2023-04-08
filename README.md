# RINOMINA CANZONI
L'obbiettivo di questo programma è rinominare i file .mp3 utilizzando i metadati salvati al suo interno utilizando una regola a piacere.
È anche possibile editare i metadati principali, aggiungere commenti e cambiare l'immagine di copertina della canzone. 
È possibile cercare immagini online utilizzando [Google-Images-Search](https://pypi.org/project/Google-Images-Search/), quindi se si aggiungono nel file .env nascosto le chiavi del progetto, seguendo la guida lì presente, sarà appunto possibile aggiungere le immagini come desiderato. Al momento non è possibli cercare immagini all'interno del pc

## [Indice](#indice)
- [RINOMINA CANZONI](#rinomina-canzoni)
  - [Indice](#indice)
  - [Utilizzo](#utilizzo)
  - [Esecuzione](#esecuzione)
  - [Compilazione (?)](#compilazione-)
  - [Sviluppo](#sviluppo)
  - [Materiale utilizzato](#materiale-utilizzato)
  - [LICENCES](#licences)

## [Utilizzo](#indice)
Una volta avviato, sarà possibile scegliere la cartella da cui atingere i file .mp3 da editare. (Il programma attingerà automaticamente unicamente ai file .mp3 presenti nella cartella selezionata).
Scegliendo di fare una modifica 

## [Esecuzione](#indice)
Prima dell'esecuzione accertatevi di possedere tutti i pacchetti presenti in [requirements.txt](requirements.txt). Nel caso non dovesse essere in possesso delle chiavi per utilizzare Google-Images-Search o non doveste avere il pacchetto, il programma dovrebbe eseguirsi senza vere interruzioni.

## [Compilazione (?)](#indice)
Anche se non penso sia il termine corretto, per creare il file eseguibile è possibile utilitzzare [auto-py-to-exe](https://github.com/brentvollebregt/auto-py-to-exe), ed è possibile caricare i dati direttamente dal file [py2exe.json](https://github.com/Scarlet06/Rinomina-Canzoni/blob/main/py2exe.json). Prestate attenzione però che in automatico verrà aggiunto il pacchetto Google-Images-Search come `hidden import`. Credo l'esecuzione dovrebbe avvenire con successo anche se il pacchetto non dovesse essere presente nella vostra libreria. Ma per sicurezza, siete avvisati!

## [Sviluppo](#indice)
Lo sviluppo è iniziato diversi anni addietro e la primissima versione è stata fatta con tkinter. Lavorando poi ad un secondo progetto (ancora privato), mi sono trovato motlo meglio ad utilizzare pygame, ed ora ho copiato da lì diverse strutture che sono ora utilizzate! So che ci stanno ancora diversi spaghetti, ma sono contento di questo risultato. L'"impaginazione" segue ancora l'idea avuta con tkinter, ma credo questa renda un po' meglio.

Maybe TO DO list:
- un riproduttore musicale per la canzone che si sta editando in quel momento (play, stop, volume up, volume down... (skip +/- 5 sec?))
- nel caso si volesse rinominare il file con un nome già presente nella cartella, vorrei:
  - poter scegliere se eliminare uno dei due file
  - riprodurre uno dei due file
  - scegliere di editare le due canzoni contemporaneamente?

## [Materiale utilizzato](#indice)
- Per il font dei caratteri speciali, ho deciso d'utilizzare Kazuki Kimura, potete trovare tutti i dettagli a riguardo in nel suo [README.md](Font/README.md) e la sua licenze è [OFL.txt](Font/OFL.txt)
- Le tre immagini [arr_back.png](Images/arr_back.png), [circle.png](Images/circle.png) e [down.png](Images/down.png) sono tutte state prese dal secondo progetto privato di cui ho cita l'esistenza e sono state disegnate da [Ferrixio](https://github.com/ferrixio). Ci tengo anche ad aggiungere che quello che nel codice è la classe `Start` è un'evoluzione della parte del codice sviluppata dallo stesso Ferrixio, nell steso progetto secondario, ovvero la classe `Fexplorer` (L'explorer proposto da Ferrixio).
- Le altre due immagini [Rinomina.ico](Images/Rinomina.ico) e [Rinomina.png](Images/Rinomina.png) sono invece state disegnate da me.

## [LICENCES](LICENSE.md)
Questo progetto è protetto da Apache License 2.0, eccetto per tutto il materiale non di nostra proprietà intellettuale, per cui ciascuno possiede la propria licenza. Per ulteriori dettagli è possibile visionare [NOTICE](NOTICE.md).