# Lapem
Lecteur Audio Pour Ecole Maternelle
La documentation se trouve dans le répertoire documents : "principle.md"

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

Lapem va jouer le fichier : "audio.wav".
Si nécessaire vous pouvez utilez le programme "Audacity" pour convertir les fichiers audio en  fichier ".vaw"

l'accès au Lapem se fait à travers connexion ssh ou samba
    login : pi
    password: raspberry

Cette connexion va vous permettre 
* de copier des fichiers musique et de renommer le fichier transféré en "audio.wav"
* d'ajuster le volume de lecture à travers le fichier volume.cfg