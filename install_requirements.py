import os
import subprocess

packages = [
    "asgiref==3.8.1",
    "Django==5.1.1",
    "gunicorn==23.0.0",
    "packaging==24.1",
    "sqlparse==0.5.1",
    "whitenoise==6.7.0",
    "django-cors-headers",
    "djangorestframework",
    "Pillow>=10.0.0",
    "requests",
    "PyJWT"
]

def install_packages():
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call(['pip', 'install', package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e}")
            return False
    return True

if __name__ == "__main__":
    print("Starting package installation...")
    if install_packages():
        print("All packages installed successfully!")
    else:
        print("Some packages failed to install. Please check the errors above.")