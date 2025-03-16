from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains  # Importation de ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Fonction pour attendre qu'un élément soit présent sur la page
def attendre_element(xpath, timeout=10):
    try:
        # Attendre que l'élément soit visible
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    except:
        return None

# Spécifie le chemin du WebDriver Firefox (geckodriver)
geckodriver_path = "/usr/local/bin/geckodriver"  # Le chemin correct vers geckodriver

# Initialise le WebDriver de Firefox
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service)

# Ouvre WhatsApp Web
driver.get("https://web.whatsapp.com")

# Demander à l'utilisateur de scanner le QR Code
print("Scanner le QR Code avec ton téléphone...")
input("Appuie sur Entrée une fois que tu as scanné le QR Code...")

# Une fois que l'utilisateur a scanné le QR Code et appuyé sur Entrée, on continue
print("QR Code scanné, tu es maintenant connecté!")

# 🔍 Recherche de la barre de recherche
print("🔍 Recherche de la barre de recherche...")
search_box = attendre_element(
    "//div[@aria-label='Search' and @contenteditable='true'] | "
    "//div[@aria-label='Rechercher' and @contenteditable='true'] | "
    "//input[@aria-label='Search'] | "
    "/html/body/div[1]/div/div/div[3]/div/div[3]/div/div[1]/div/div[2]/div[2]/div/div"
)

if search_box:
    print("✅ Barre de recherche trouvée !")
else:
    print("❌ ERREUR : Impossible de trouver la barre de recherche.")
    driver.quit()
    exit()

# Cliquez pour activer la barre de recherche
search_box.click()

# ✅ Rechercher le groupe
groupe_nom = "Ethical"  # Nom du groupe modifié
search_box.send_keys(groupe_nom)

# Attendre que la recherche se termine et que le groupe apparaisse
timeout = 30  # Attendre jusqu'à 30 secondes
groupe_trouve = False
while timeout > 0:
    # Recherche les groupes dont le nom commence par "Ethical"
    group_elements = driver.find_elements(By.XPATH, f"//span[starts-with(@title, '{groupe_nom}')]")
    if group_elements:
        print(f"✅ Groupe trouvé !")
        groupe_trouve = True
        break
    else:
        print("⏳ Attente du groupe...")
        time.sleep(1)
        timeout -= 1

if not groupe_trouve:
    print(f"❌ ERREUR : Impossible de trouver un groupe commençant par '{groupe_nom}'.")
    driver.quit()
    exit()

# Appuyez sur Entrée pour entrer dans la discussion
group_elements[0].click()  # Clique sur le premier groupe trouvé
time.sleep(2)  # Attendre que la discussion se charge

# 🔍 Recherche de l'élément pour les numéros
print("🔍 Recherche des informations du groupe...")
info_group_xpath = "/html/body/div[1]/div/div/div[3]/div/div[4]/div/header/div[2]/div[2]/span"
info_group_element = attendre_element(info_group_xpath)

if info_group_element:
    print("✅ Information du groupe trouvée !")
else:
    print("❌ ERREUR : Impossible de trouver les informations du groupe.")
    driver.quit()
    exit()

# Simuler un survol (hover) de la souris sur l'élément pour afficher les numéros
print("🔍 Simuler le survol de la souris pour afficher les numéros...")
actions = ActionChains(driver)
actions.move_to_element(info_group_element).perform()  # Survoler l'élément
time.sleep(2)  # Attendre que l'effet de survol prenne effet

# Récupérer les numéros affichés
num_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div/div[3]/div/div[4]/div/header/div[2]/div[2]/span")

# Vérifier si des numéros ont été trouvés
if num_elements:
    print("✅ Numéros de téléphone trouvés !")
    # Crée ou ouvre un fichier texte pour enregistrer les numéros
    with open("numéros_telefoniques.txt", "w") as f:
        for num in num_elements:
            num_text = num.text
            print(f"Numéro trouvé : {num_text}")
            f.write(num_text + "\n")  # Écrire chaque numéro sur une nouvelle ligne dans le fichier
else:
    print("❌ Aucun numéro trouvé.")

# Ferme le navigateur après quelques secondes
time.sleep(5)  # Attendre quelques secondes
driver.quit()
