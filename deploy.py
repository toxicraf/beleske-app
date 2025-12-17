#!/usr/bin/env python3
"""
Skripta za automatski deploy na PythonAnywhere
- Push-uje promene na GitHub
- Pull-uje na PythonAnywhere preko API-ja (scheduled task)
- Reload-uje aplikaciju
"""
import os
import subprocess
import sys
import argparse
import requests
from getpass import getpass

# PythonAnywhere API endpoint
RELOAD_API_URL = "https://www.pythonanywhere.com/api/v0/user/{username}/webapps/{domain}/reload/"

def get_git_status():
    """Proverava da li postoje uncommitted promene"""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None

def commit_and_push(message="Auto-deploy from Cursor"):
    """Commit-uje i push-uje promene na GitHub"""
    try:
        # Proveri da li postoji Git repozitorijum
        subprocess.run(["git", "status"], check=True, capture_output=True)
        
        # Dodaj sve promene
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit
        subprocess.run(["git", "commit", "-m", message], check=True)
        
        # Push
        result = subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
        print("✅ Promene su push-ovane na GitHub")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Greška pri Git operaciji: {e}")
        return False
    except FileNotFoundError:
        print("❌ Git nije instaliran ili nije u PATH-u")
        return False

def reload_pythonanywhere(username, api_token):
    """Reload-uje aplikaciju na PythonAnywhere preko API-ja"""
    domain = f"{username}.pythonanywhere.com"
    url = RELOAD_API_URL.format(username=username, domain=domain)
    
    try:
        response = requests.post(url, headers={"Authorization": f"Token {api_token}"})
        if response.status_code == 200:
            print("✅ Aplikacija je reload-ovana na PythonAnywhere")
            return True
        else:
            print(f"❌ Greška pri reload-u: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Greška pri API pozivu: {e}")
        return False

def safe_input(prompt, default=None):
    """Bezbedan input koji radi i u non-interactive modu"""
    try:
        return input(prompt)
    except (EOFError, KeyboardInterrupt):
        return default if default else ""

def main():
    parser = argparse.ArgumentParser(description='Deploy aplikacije na PythonAnywhere')
    parser.add_argument('-m', '--message', help='Commit poruka', default='Auto-deploy from Cursor')
    parser.add_argument('-y', '--yes', action='store_true', help='Automatski potvrdi sve (non-interactive)')
    parser.add_argument('--no-reload', action='store_true', help='Ne reload-uj aplikaciju')
    args = parser.parse_args()
    
    print("🚀 PythonAnywhere Auto-Deploy\n")
    
    # Proveri Git status
    changes = get_git_status()
    if not changes:
        print("ℹ️  Nema promena za commit")
        if not args.yes:
            response = safe_input("Da li želiš da reload-uješ aplikaciju bez commit-a? (y/n): ", "n")
            if response.lower() != 'y':
                return
    else:
        print(f"📝 Pronađene promene:\n{changes}\n")
        if args.yes:
            should_commit = True
        else:
            response = safe_input("Da li želiš da commit-uješ i push-uješ promene? (y/n): ", "n")
            should_commit = response.lower() == 'y'
        
        if should_commit:
            if not args.yes:
                message = safe_input("Unesi commit poruku (Enter za default): ", args.message)
                if not message:
                    message = args.message
            else:
                message = args.message
            
            if not commit_and_push(message):
                return
    
    # PythonAnywhere reload
    if args.no_reload:
        print("⏭️  Preskačem reload (--no-reload flag)")
        return
    
    username = os.environ.get('PYTHONANYWHERE_USERNAME')
    api_token = os.environ.get('PYTHONANYWHERE_API_TOKEN')
    
    if not username:
        if args.yes:
            print("⚠️  PYTHONANYWHERE_USERNAME nije postavljen. Preskačem reload.")
            return
        username = safe_input("Unesi PythonAnywhere username: ", "")
    if not api_token:
        if args.yes:
            print("⚠️  PYTHONANYWHERE_API_TOKEN nije postavljen. Preskačem reload.")
            return
        try:
            api_token = getpass("Unesi PythonAnywhere API token: ")
        except (EOFError, KeyboardInterrupt):
            print("\n⚠️  API token nije unet. Preskačem reload.")
            return
    
    if username and api_token:
        # Reload aplikacije
        print("\n🔄 Reload-ujem aplikaciju na PythonAnywhere...")
        reload_pythonanywhere(username, api_token)
        
        # Instrukcije za pull
        site_path = os.environ.get('PYTHONANYWHERE_SITE_PATH', '/home/toxicraf/mysite')
        print(f"\n📥 Sledeći korak: Pull-uj promene na PythonAnywhere")
        print(f"   Idi na PythonAnywhere → Consoles → Bash")
        print(f"   Pokreni: cd {site_path} && git pull origin main")
        print(f"   Zatim: Web tab → Reload")
    else:
        print("⚠️  Nisu uneti username ili API token. Preskačem reload.")
        print("\n💡 Za automatski reload, postavi environment varijable:")
        print("   PYTHONANYWHERE_USERNAME=toxicraf")
        print("   PYTHONANYWHERE_API_TOKEN=your_token_here")
        print("\n   Ili pokreni sa: python deploy.py -y")

if __name__ == "__main__":
    main()

