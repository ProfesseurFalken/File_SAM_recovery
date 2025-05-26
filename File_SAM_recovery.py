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

def extract_images_from_sam(file_path, output_path):
    """
    Recherche et extrait les images potentielles (JPEG, PNG) dans un fichier .sam.
    Sauvegarde les images dans le dossier de sortie.
    """
    try:
        with open(file_path, 'rb') as file:
            content = file.read()
        
        # Signatures d'images courantes
        jpeg_signature = b'\xFF\xD8'
        png_signature = b'\x89\x50\x4E\x47'
        extracted_images = []
        
        # Recherche des signatures JPEG
        jpeg_positions = [i for i in range(len(content)) if content[i:i+2] == jpeg_signature]
        for idx, pos in enumerate(jpeg_positions):
            # Cherche la fin du fichier JPEG (FF D9)
            end_pos = content.find(b'\xFF\xD9', pos)
            if end_pos != -1:
                image_data = content[pos:end_pos+2]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = f"{output_path}/extracted_image_{timestamp}_{idx+1}.jpg"
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_data)
                extracted_images.append(image_path)

        # Recherche des signatures PNG
        png_positions = [i for i in range(len(content)) if content[i:i+4] == png_signature]
        for idx, pos in enumerate(png_positions):
            # Cherche la fin du fichier PNG (IEND chunk: 00 00 00 00 49 45 4E 44 AE 42 60 82)
            end_pos = content.find(b'\x00\x00\x00\x00\x49\x45\x4E\x44\xAE\x42\x60\x82', pos)
            if end_pos != -1:
                image_data = content[pos:end_pos+12]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                image_path = f"{output_path}/extracted_image_{timestamp}_{idx+1}.png"
                with open(image_path, 'wb') as img_file:
                    img_file.write(image_data)
                extracted_images.append(image_path)

        return extracted_images if extracted_images else "Aucune image trouvée."
    except Exception as e:
        return f"Erreur lors de l'extraction des images : {e}"

def get_file_metadata(file_path):
    """
    Récupère les métadonnées de date (création, modification) du fichier.
    """
    try:
        creation_time = os.path.getctime(file_path)
        modification_time = os.path.getmtime(file_path)
        creation_date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
        modification_date = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
        return f"Date de création : {creation_date}\nDate de modification : {modification_date}"
    except Exception as e:
        return f"Erreur lors de la récupération des métadonnées : {e}"

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

def save_output(content, output_path, prefix="recovered_sam"):
    """
    Sauvegarde le contenu extrait dans un fichier avec un horodatage.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"{output_path}/{prefix}_{timestamp}.txt"
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Contenu sauvegardé dans {output_file}"
    except Exception as e:
        return f"Erreur lors de la sauvegarde : {e}"

def main():
    parser = argparse.ArgumentParser(description="Outil de récupération pour fichiers .sam d'Ami Pro")
    parser.add_argument("file_path", help="Chemin vers le fichier .sam (ou disque pour TestDisk)")
    parser.add_argument("--mode", choices=["text", "binary", "images", "metadata", "testdisk", "all"], default="text",
                        help="Mode : text (extraire texte brut), binary (analyser données binaires), images (extraire images), metadata (dates du fichier), testdisk (récupérer fichier supprimé), all (tous sauf testdisk)")
    parser.add_argument("--output", default="output", help="Dossier pour sauvegarder les résultats")
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.makedirs(args.output)

    results = []
    
    if args.mode in ["text", "all"]:
        print("Extraction du texte brut...")
        text_result = extract_text_from_sam(args.file_path)
        print("Texte extrait :\n", text_result)
        save_result = save_output(text_result, args.output, "text")
        results.append(save_result)

    if args.mode in ["binary", "all"]:
        print("Analyse des données binaires...")
        binary_result = analyze_sam_binary(args.file_path)
        if isinstance(binary_result, list):
            print("Segments lisibles trouvés :")
            for i, chunk in enumerate(binary_result, 1):
                print(f"Segment {i}: {chunk}")
            save_result = save_output('\n'.join(binary_result), args.output, "binary")
            results.append(save_result)
        else:
            print(binary_result)
            results.append(binary_result)

    if args.mode in ["images", "all"]:
        print("Extraction des images...")
        image_result = extract_images_from_sam(args.file_path, args.output)
        if isinstance(image_result, list):
            print("Images extraites :")
            for img in image_result:
                print(f"- {img}")
            results.append(f"Images sauvegardées : {', '.join(image_result)}")
        else:
            print(image_result)
            results.append(image_result)

    if args.mode in ["metadata", "all"]:
        print("Récupération des métadonnées de date...")
        metadata_result = get_file_metadata(args.file_path)
        print(metadata_result)
        save_result = save_output(metadata_result, args.output, "metadata")
        results.append(save_result)

    if args.mode == "testdisk":
        print("Lancement de TestDisk pour récupération...")
        testdisk_result = run_testdisk(args.file_path)
        print(testdisk_result)
        save_result = save_output(testdisk_result, args.output, "testdisk")
        results.append(save_result)

    print("\nRésumé des opérations :")
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
