
#Recuperer les coordonnées des lieux à visiter de Pau
def getCoordsFromFile():
    chemin_fichier = 'data/kebabCoord.txt'
    kebabsCoord = {}

    with open(chemin_fichier, 'r') as fichier:
        for ligne in fichier:

            # Diviser la ligne en fonction du caractère ':'
            parts = ligne.split(':')
            
            # Extraire le nom et les coordonnées
            snack_name = parts[0].strip()
            coordinates = eval(parts[1].strip())
            kebabsCoord[snack_name] = coordinates


    return(kebabsCoord)


#Calculer les nouvelles coordonnées du personnage en fonction de sa vitesse et de sa destination, se deplace à vol d'oiseau
def calculateNewCoord(currentCoord, destination, speed):
    speed = speed * 0.00005
    # Calculer la différence entre les coordonnées actuelles et la destination
    diff_x = destination[0] - currentCoord[0]
    diff_y = destination[1] - currentCoord[1]
    
    #Calculer la distance qu'il reste à parcourir
    distance_squared = (diff_x**2 + diff_y**2)**0.5

    if distance_squared > 0:
        magnitude = distance_squared**0.5
    else:
        magnitude = 1.0
        
    #Normaliser la direction
    unit_vector = [diff_x / magnitude, diff_y / magnitude]

    #Mettre à jour les coordonées avec la direction et la vitesse
    currentCoord[0] += unit_vector[0] * speed
    currentCoord[1] += unit_vector[1] * speed

    return currentCoord