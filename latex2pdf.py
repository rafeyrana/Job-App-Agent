import subprocess
import os

def cleanup_auxiliary_files(base_path):
    """Clean up auxiliary files generated during LaTeX compilation."""
    auxiliary_extensions = ['.aux', '.log', '.out', '.toc', '.lof', '.lot', '.fls', '.fdb_latexmk']
    
    for ext in auxiliary_extensions:
        aux_file = base_path + ext
        try:
            if os.path.exists(aux_file):
                os.remove(aux_file)
        except OSError as e:
            print(f"Warning: Could not remove {aux_file}: {e}")

def latex_to_pdf(tex_file, output_pdf=None):
    """Convert LaTeX file to PDF."""
    try:
        # Get the directory and base filename
        directory = os.path.dirname(os.path.abspath(tex_file))
        base_name = os.path.splitext(os.path.basename(tex_file))[0]
        
        # If no output_pdf specified, use the same name as tex_file
        if output_pdf is None:
            output_pdf = os.path.join(directory, base_name + '.pdf')
        
        # Ensure output directory exists
        os.makedirs(directory, exist_ok=True)
        
        # Run pdflatex twice to resolve references
        for _ in range(2):
            process = subprocess.Popen(
                ['pdflatex', '-interaction=nonstopmode', 
                 '-output-directory', directory, tex_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                print("LaTeX Compilation Error:")
                print(stdout)
                print(stderr)
                # If compilation fails, check log file for details
                log_file = os.path.join(directory, base_name + '.log')
                if os.path.exists(log_file):
                    with open(log_file, 'r') as f:
                        print("\nDetails from log file:")
                        print(f.read())
                return False
        
        # Check if PDF was generated
        default_pdf = os.path.join(directory, base_name + '.pdf')
        if os.path.exists(default_pdf):
            # Rename if necessary
            if default_pdf != output_pdf:
                os.rename(default_pdf, output_pdf)
            print(f"✓ PDF generated successfully at: {output_pdf}")
            return True
        else:
            print("✗ PDF generation failed")
            return False
            
    except Exception as e:
        print(f"Error during compilation: {str(e)}")
        return False
    
    finally:
        # Clean up auxiliary files
        cleanup_auxiliary_files(os.path.join(directory, base_name))

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python latex2pdf.py <input.tex> [output.pdf]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    latex_to_pdf(input_file, output_file)