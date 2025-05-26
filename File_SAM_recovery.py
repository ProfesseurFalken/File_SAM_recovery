import re
import binascii
import subprocess
import argparse
import os
from datetime import datetime

def extract_text_from_sam(file_path):
    """
    Extrait le texte brut d'un fichier .sam potentiellement corrompu.
    Ignore les données binaires non lisibles.
    """
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            text = content.decode('ascii', errors='ignore')
            cleaned_text = re.sub(r'[^\x20-\x7E\n\r]+', '', text)
            return cleaned_text.strip()
    except Exception as e:
        return f"Erreur lors de l'extraction du texte : {e}"

def analyze_sam_binary(file_path, max_bytes=1000):
    """
    Analyse les données binaires d'un fichier .sam et extrait les segments lisibles.
    Affiche une représentation hexadécimale des premiers octets.
    """
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
            hex_data = binascii.hexlify(content[:max_bytes]).decode('ascii')
            print(f"Premiers {max_bytes} octets en hexadécimal :\n{hex_data}\n")
            text_chunks = []
            for i in range(0, len(content), 100):
                chunk = content[i:i+100].decode('ascii', errors='ignore')
                if any(c.isprintable() for c in chunk):
                    text_chunks.append(chunk.strip())
            return text_chunks
    except Exception as e:
        return f"Erreur lors de l'analyse binaire : {e}"

def run_testdisk(disk):
    """
    Exécute TestDisk pour tenter de récupérer un fichier .sam supprimé ou écrasé.
    Nécessite que TestDisk soit installé et accessible dans le PATH.
    """
    try:
        result = subprocess.run(
            ["testdisk", "/log", disk],
            capture_output=True,
            text=True,
            timeout=300
        )
        return f"Résultat de TestDisk :\n{result.stdout}"
    except FileNotFoundError:
        return "Erreur : TestDisk n'est pas installé ou n'est pas dans le PATH."
    except subprocess.TimeoutExpired:
        return "Erreur : TestDisk a dépassé le temps d'exécution."
    except Exception as e:
        return f"Erreur lors de l'exécution de TestDisk : {e}"

def save_output(content, output_path):
    """
    Sauvegarde le contenu extrait dans un fichier avec un horodatage.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_path}/recovered_sam_{timestamp}.txt"
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Contenu sauvegardé dans {output_file}"
    except Exception as e:
        return f"Erreur lors de la sauvegarde : {e}"

def main():
    parser = argparse.ArgumentParser(description="Outil de récupération pour fichiers .sam d'Ami Pro")
    parser.add_argument("file_path", help="Chemin vers le fichier .sam (ou disque pour TestDisk)")
    parser.add_argument("--mode", choices=["text", "binary", "testdisk"], default="text",
                       help="Mode : text (extraire texte brut), binary (analyser données binaires), testdisk (récupérer fichier supprimé)")
    parser.add_argument("--output", default="output", help="Dossier pour sauvegarder les résultats")
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if args.mode == "text":
        print("Extraction du texte brut...")
        result = extract_text_from_sam(args.file_path)
        print("Texte extrait :\n", result)
        save_result = save_output(result, args.output)
        print(save_result)

    elif args.mode == "binary":
        print("Analyse des données binaires...")
        result = analyze_sam_binary(args.file_path)
        if isinstance(result, list):
            print("Segments lisibles trouvés :")
            for i, chunk in enumerate(result, 1):
                print(f"Segment {i}: {chunk}")
            save_result = save_output('\n'.join(result), args.output)
            print(save_result)
        else:
            print(result)

    elif args.mode == "testdisk":
        print("Lancement de TestDisk pour récupération...")
        result = run_testdisk(args.file_path)
        print(result)
        save_result = save_output(result, args.output)
        print(save_result)

if __name__ == "__main__":
    main()
