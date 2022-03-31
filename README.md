# Lapem
Lecteur Audio Pour Ecole Maternelle
La documentation se trouve sur le [Wiki](https://github.com/ckl67/lapem/wiki)

# Mode de connexion
   
## Mode : Point d'accès : 

La Led Rouge reste allumée

    @IP : 10.3.141.1
    SSID : ssid=LapemNetwork
    Mot de Passe  : secret_password

Cette action peut se faire à travers le scipt
    bash scl2ap.sh

## Mode Client : 

La Led Rouge clignote

    @IP : votre réseau

Cette action peut se faire à travers le scipt

    bash sap2cl.sh
    
# Quelques comandes en ssh:

Pensez à tuer le process qui tourne en tâches de fond

    ps -ef | grep lapem 
    sudo kill -9 [process]
    
# Principe

Lapem va jouer les fichiers : "audio.mp3" ou "audio.wav".

Une fois connecté sur le lecteur réseau duLapem, cette connexion va vous permettre 
*  de copier des fichiers musique .mp3 ou .wav et de les renommer.
      Lapem va jouer de préférence le fichier "audio.mp3".
      Si ce fichier n'existe pas, Lapem va jouer le fichier "audio.wav"
      Si nécessaire vous pouvez utilez le programme "Audacity" pour  
      convertir les fichiers ".mp3" en  fichier ".wav"

*  d'ajuster le volume de lecture à travers le fichier volume.cfg

l'accès au Lapem se fait à travers connexion ssh ou samba

    login : pi
    password: raspberry

