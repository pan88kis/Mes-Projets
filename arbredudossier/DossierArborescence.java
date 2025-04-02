package arbredudossier;
import java.io.File;
import java.util.Scanner;
/* Avant de le compiler rassure toi que la version de javac et java soient pareils*/
public class DossierArborescence {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        System.out.print("Entrez le chemin du dossier : ");
        String chemin = scanner.nextLine();

        System.out.print("Entrez la hauteur maximale d'affichage : ");
        int hauteur = scanner.nextInt();

        System.out.print("Voulez-vous afficher les fichiers/dossiers cachés ? (oui/non) : ");
        boolean afficherCaches = scanner.next().equalsIgnoreCase("oui");

        File dossier = new File(chemin);

        if (dossier.exists() && dossier.isDirectory()) {
            afficherArborescence(dossier, 0, hauteur, afficherCaches);
        } else {
            System.out.println("Le chemin spécifié n'est pas un dossier valide.");
        }

        scanner.close();
    }

    public static void afficherArborescence(File dossier, int niveau, int hauteurMax, boolean afficherCaches) {
        if (niveau > hauteurMax) {
            return;
        }

        for (int i = 0; i < niveau; i++) {
            System.out.print("  ");
        }
        System.out.println("|- " + dossier.getName());

        File[] fichiers = dossier.listFiles();
        if (fichiers != null) {
            for (File fichier : fichiers) {
                if (!afficherCaches && fichier.isHidden()) {
                    continue;
                }

                if (fichier.isDirectory()) {
                    afficherArborescence(fichier, niveau + 1, hauteurMax, afficherCaches);
                } else {
                    for (int i = 0; i < niveau + 1; i++) {
                        System.out.print("  ");
                    }
                    System.out.println("|- " + fichier.getName());
                }
            }
        }
    }
}
