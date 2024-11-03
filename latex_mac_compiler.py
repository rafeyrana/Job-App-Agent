import subprocess
import os
import re

def update_tlmgr():
    """Update tlmgr and its packages."""
    try:
        subprocess.run(
            ["sudo", "tlmgr", "update", "--self", "--all"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
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
    
    for package in packages:
        try:
            subprocess.run(
                ["sudo", "tlmgr", "install", package],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {package}: {e.stderr.decode() if e.stderr else ''}")

def latex_to_pdf(tex_file, pdf_name="output.pdf"):
    """Convert LaTeX to PDF with proper error handling."""
    # Get the directory of the tex file
    output_directory = os.path.dirname(os.path.abspath(tex_file))
    if not output_directory:
        output_directory = "."
    
    # Ensure all required packages are installed
    print("Checking and installing required packages...")
    update_tlmgr()
    install_required_packages()
    
    # Expected output PDF path
    pdf_file_path = os.path.join(output_directory, pdf_name)
    
    try:
        # Run pdflatex twice to resolve references
        for i in range(2):
            process = subprocess.Popen(
                ["pdflatex", "-interaction=nonstopmode", "-output-directory", output_directory, tex_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print("LaTeX Compilation Error:")
                print(stdout)
                print(stderr)
                if "Emergency stop" in stdout:
                    log_file = os.path.join(output_directory, os.path.splitext(os.path.basename(tex_file))[0] + ".log")
                    if os.path.exists(log_file):
                        with open(log_file, 'r') as f:
                            print("\nDetails from log file:")
                            print(f.read())
                return False
        
        # Check if PDF was generated
        generated_pdf = os.path.join(output_directory, os.path.splitext(os.path.basename(tex_file))[0] + ".pdf")
        if os.path.exists(generated_pdf):
            # Rename if necessary
            if generated_pdf != pdf_file_path:
                os.rename(generated_pdf, pdf_file_path)
            print(f"PDF generated successfully at: {pdf_file_path}")
            return True
        else:
            print("PDF generation failed")
            return False
            
    except Exception as e:
        print(f"Error during compilation: {str(e)}")
        return False
    finally:
        # Clean up auxiliary files
        for ext in [".aux", ".log", ".out"]:
            aux_file = os.path.join(output_directory, os.path.splitext(os.path.basename(tex_file))[0] + ext)
            try:
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            except OSError:
                pass

if __name__ == "__main__":
    latex_file = "resume.tex"
    latex_to_pdf(latex_file, pdf_name="example.pdf")