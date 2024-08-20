# Lapem
Lecteur Audio Pour Ecole Maternelle
La documentation se trouve sur le [Wiki](https://github.com/ckl67/lapem/wiki)

# Mode de connexion
   
## Mode : Point d'accès : 

    @IP : 10.3.141.1
    SSID : ssid=LapemNetwork
    Mot de Passe  : secret_password
    
# Principe

Lapem va jouer les fichiers : "audio.mp3" ou "audio.wav".

# Accès réseau au Lapem

L'accès au Lapem se fait à travers connexion Samba 
avec smb://10.3.141.1/lapem (Linux) ou \10.3.141.1\lapem (Windows).
    login : pi
    password: raspberry

cette connexion va vous permettre 
*  de copier des fichiers musique .mp3 ou .wav et de les renommer.
      Lapem va jouer de préférence le fichier "audio.mp3".
      Si ce fichier n'existe pas, Lapem va jouer le fichier "audio.wav"
      Si nécessaire vous pouvez utilez le programme "Audacity" pour  
      convertir les fichiers ".mp3" en  fichier ".wav"

*  d'ajuster le volume de lecture à travers le fichier volume.cfg


# Quelques comandes en ssh:

Pensez à tuer le process qui tourne en tâches de fond

    ps -ef | grep lapem 
    sudo kill -9 [process]
