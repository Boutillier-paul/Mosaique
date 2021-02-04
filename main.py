#Auteur : BOUTILLIER Paul
#TP : A

import cv2
import os
import numpy as np
import random
import math


global tabPetitesImages
tabPetitesImages = []

#BONUS - Prend un screen d'une video toutes les 3 secondes
def screenOfVideo(cheminVideo):
    #Lire la vidéo à un chemin donné
    cam = cv2.VideoCapture(cheminVideo)

    try:
        #Création d'un dossier
        if not os.path.exists('img'):
            os.makedirs('img')

        #On ressort une erreur s'il n'est pas créé
    except OSError:
        print("Erreur")

    #Frame
    currentframe = 0
    frameParSeconde = cam.get(cv2.CAP_PROP_FPS)
    i = 0

    while (True):

        ret, frame = cam.read()

        if ret:
            if currentframe % (frameParSeconde * 3) == 0:
                #Si la vidéo continue, on créé des images
                name = './img/frame' + str(i) + '.jpg'
                print('En cours de création...' + name)

                #Ecriture des images extraites
                cv2.imwrite(name, frame)

                i += 1

            #On ajoute 1 au compteur Frame
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

#Sous - programme permettant de modifier les images et de conserver leur nom et couleur moyenne dans un tableau global pour un dossier donné
def question4 (str1, taillePetitesImages):

    #Pour toutes les images dans le dossier contenu dans str1
    for i in range(len(os.listdir(str1))):

        img = cv2.imread(str1+"/frame"+str(i)+".jpg")
        dim = img.shape

        #Découpage en image carré
        image = img[0:dim[0], int(dim[1] / 2) - int(dim[0] / 2):int(dim[1] / 2) + int(dim[0] / 2)]

        #Resize avec la taille souhaitée
        image = cv2.resize(image, (taillePetitesImages, taillePetitesImages))

        #Sauvegarde des petites images
        cv2.imwrite('imgPlusPetites/img'+str(i)+".jpg", image)

        #Définition de la couleur moyenne de la petite image
        couleurMoy = couleurMoyenne(image, image.shape[0])

        #Création des données à entrer dans le tableau global
        val = ["imgPlusPetites/img"+str(i)+".jpg", couleurMoy]

        #On entre les données dans le tableau (nom et couleur)
        tabPetitesImages.append(val)

#Sous - programme retournant la couleur moyenne d'une image pour une taille donnée
def couleurMoyenne(image,x):

    r, g, b = 0, 0, 0

    #Si l'image n'est qu'un seul pixel
    if x == 1:
        r, g, b = image

    else:
        for i in range(x):
            for j in range(x):
                r0, g0, b0 = image[i, j]

                r += r0
                g += g0
                b += b0

        #On calcul la moyenne pour chaque valeur
        r /= (x*x)
        g /= (x*x)
        b /= (x*x)

    couleurMoy=np.array([int(r), int(g), int(b)])

    return couleurMoy


#Sous - programme permettant de remplir la mosaique
def remplirMosaique(imageRetaillee):

    for i in range(imageRetaillee.shape[0]):

        if i == 1:
            mosaique = img_concat_horizontal
        if i != 0 and i != 1:
            mosaique = np.concatenate((mosaique, img_concat_horizontal), axis=0)

        for j in range(imageRetaillee.shape[1]):
            meulleurScore = 1000000
            pixel = imageRetaillee[i, j]

            couleurMoy = couleurMoyenne(pixel, 1)
            score1 = couleurMoy[0]+couleurMoy[1]+couleurMoy[2]

            tabChoix = list()

            for x in range(len(tabPetitesImages)):
                couleurMoyPetiteImage = tabPetitesImages[x][1]
                score2 = couleurMoyPetiteImage[0] + couleurMoyPetiteImage[1] + couleurMoyPetiteImage[2]

                score2 = abs(score1-score2)

                if score2 < meulleurScore:
                    meulleurScore = score2
                    indice = x

            img = cv2.imread(tabPetitesImages[indice][0])
            tabChoix.append(img)

            if len(tabChoix) != 0:
                indice = len(tabChoix)-1
                randomNb = random.randint(0, indice)

                if j == 0:
                    img_concat_horizontal = tabChoix[randomNb]
                else:
                    img_concat_horizontal = np.concatenate((img_concat_horizontal, tabChoix[randomNb]), axis=1)

    return mosaique


#_____MAIN_____

#On récupère les images de la vidéo
cheminVideo = ".mp4"
#screenOfVideo(cheminVideo)

#taille des petites images
taille = 40

#Lecture de l'image à reproduire
img_a_reproduire = cv2.imread('imgAReproduire.jpg')

#Affichage de la taille de l'image
dimensions = img_a_reproduire.shape

#On récupère les données et on divise par la taille les dimensions (on garde la partie entière)
hauteur = int(dimensions[0]/10)
largeur = int(dimensions[1]/10)

#Redimmensionnement de l'image
img_a_reproduire_resized = cv2.resize(img_a_reproduire, (largeur, hauteur))

#LES IMAGES DU DOSSIERS "img" DOIVENT S'APPELER "frame"+numero (en commencant par 0)
question4("img", taille)

#Création de la mosaique
print("Création de la mosaïque... veuillez patientez...")
mosaique = remplirMosaique(img_a_reproduire_resized)

#Sauvegarde de la mosaique
cv2.imwrite("mosaique.jpg", mosaique)
print("Mosaïque sauvegardé sous le nom de : mosaique.jpg")

