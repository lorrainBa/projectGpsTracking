
def getCoordKebab():
    # Définir le chemin du fichier texte
    chemin_fichier = './../data/kebabCoord.txt'

    # Initialiser la liste de listes
    kebabsCoord = {}

    # Lire le fichier et extraire les données
    with open(chemin_fichier, 'r') as fichier:
        for ligne in fichier:
            # Diviser la ligne en fonction du caractère ':'
            parts = ligne.split(':')
            
            # Extraire le nom et les coordonnées
            snack_name = parts[0].strip()
            coordinates = eval(parts[1].strip())  # Utiliser eval pour convertir la chaîne en une liste

            # Ajouter au dictionnaire
            kebabsCoord[snack_name] = coordinates


    return(kebabsCoord)


def calculateNewCoord(currentCoord, destination, speed):
    speed = speed * 0.00005
     # Calculer la différence entre les coordonnées actuelles et la destination
    diff_x = destination[0] - currentCoord[0]
    diff_y = destination[1] - currentCoord[1]
    
    # Calculer la magnitude pour déterminer la distance totale à parcourir
    distance_squared = (diff_x**2 + diff_y**2)**0.5

    if distance_squared > 0:
        magnitude = distance_squared**0.5
    else:
        magnitude = 1.0
        
    # Calculer le vecteur unitaire (direction à suivre)
    unit_vector = [diff_x / magnitude, diff_y / magnitude]

    # Mettre à jour les coordonnées actuelles avec un pas spécifié
    currentCoord[0] += unit_vector[0] * speed
    currentCoord[1] += unit_vector[1] * speed

    return currentCoord