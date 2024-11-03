import subprocess
import os

def update_tlmgr():
    """Update tlmgr and its packages."""
    try:
        print("Updating TeX Live Manager...")
        subprocess.run(
            ["sudo", "tlmgr", "update", "--self", "--all"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error updating tlmgr: {e.stderr.decode() if e.stderr else ''}")
        return False

def install_required_packages():
    """Install all required packages for the resume template."""
    packages = [
        "preprint",  # Contains fullpage.sty
        "collection-latexextra",
        "collection-fontsrecommended",
        "enumitem",
        "hyperref",
        "fancyhdr",
        "babel",
        "marvosym",
        "titlesec",
        "tabularx"
    ]
    
    print("Installing required LaTeX packages...")
    for package in packages:
        try:
            subprocess.run(
                ["sudo", "tlmgr", "install", package],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"✓ Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error installing {package}: {e.stderr.decode() if e.stderr else ''}")

def setup_latex_environment():
    """Main function to set up the LaTeX environment."""
    print("Setting up LaTeX environment...")
    
    # Update package manager
    if update_tlmgr():
        print("✓ Successfully updated TeX Live Manager")
    else:
        print("✗ Failed to update TeX Live Manager")
        return False
    
    # Install required packages
    install_required_packages()
    
    print("\nLatex environment setup complete!")
    return True

if __name__ == "__main__":
    setup_latex_environment()