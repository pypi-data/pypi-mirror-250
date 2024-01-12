import subprocess

def main():
    # Definujte cestu k souboru GUI.py
    python_file_path = "GUI.py"
    
    # Sestavte příkaz pro spuštění souboru GUI.py
    command = ["python", python_file_path]

    try:
        # Spustit soubor GUI.py
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("Soubor GUI.py byl úspěšně spuštěn.")
        else:
            print("Chyba při spouštění souboru GUI.py.")
            print(result.stderr)
    except Exception as e:
        print("Došlo k chybě:", str(e))

if __name__ == "__main__":
    main()
