import subprocess
import os
from typing import List, Union

def run_command(command: List[str]) -> Union[str, None]:
    """Helper function to run a shell command and return its output or None on error."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {" ".join(command)}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"Command not found: {command[0]}")
        return None

def manus_render_diagram(input_file: str, output_file: str) -> Union[str, None]:
    """Renders diagram files to PNG format.
    Example: manus_render_diagram('path/to/input.mmd', 'path/to/output.png')
    """
    command = ['manus-render-diagram', input_file, output_file]
    print(f"Executing: {" ".join(command)}")
    return run_command(command)

def manus_md_to_pdf(input_file: str, output_file: str) -> Union[str, None]:
    """Converts a Markdown file to PDF format.
    Example: manus_md_to_pdf('path/to/input.md', 'path/to/output.pdf')
    """
    command = ['manus-md-to-pdf', input_file, output_file]
    print(f"Executing: {" ".join(command)}")
    return run_command(command)

def manus_speech_to_text(input_file: str) -> Union[str, None]:
    """Transcribes speech/audio/video files to text.
    Example: manus_speech_to_text('path/to/interview.mp3')
    """
    command = ['manus-speech-to-text', input_file]
    print(f"Executing: {" ".join(command)}")
    return run_command(command)

def manus_mcp_cli(command_args: List[str]) -> Union[str, None]:
    """Interacts with Model Context Protocol (MCP) servers.
    Example: manus_mcp_cli(['--help'])
    """
    command = ['manus-mcp-cli'] + command_args
    print(f"Executing: {" ".join(command)}")
    return run_command(command)

def manus_upload_file(input_files: List[str]) -> Union[str, None]:
    """Uploads one or more files to S3 and returns direct public URLs.
    Example: manus_upload_file(['path/to/file1.png', 'path/to/file2.pdf'])
    """
    command = ['manus-upload-file'] + input_files
    print(f"Executing: {" ".join(command)}")
    return run_command(command)

def manus_export_slides(slides_uri: str, output_format: str) -> Union[str, None]:
    """Exports slides from a manus-slides://{version_id} URI to a specified format.
    Example: manus_export_slides('manus-slides://2tvrCaJBV8I6gabDLa4YCL', 'pdf')
    """
    command = ['manus-export-slides', slides_uri, output_format]
    print(f"Executing: {" ".join(command)}")
    return run_command(command)

# Example Usage (uncomment to test)
# if __name__ == "__main__":
#     # Create dummy files for testing
#     with open("test.md", "w") as f:
#         f.write("# Test Markdown\n\nThis is a test document.")
#     with open("test.mmd", "w") as f:
#         f.write("graph TD; A-->B;")

#     print("\n--- Testing manus_md_to_pdf ---")
#     pdf_output = manus_md_to_pdf("test.md", "test.pdf")
#     if pdf_output: print(f"PDF created: test.pdf")

#     print("\n--- Testing manus_render_diagram ---")
#     diagram_output = manus_render_diagram("test.mmd", "test.png")
#     if diagram_output: print(f"Diagram rendered: test.png")

#     print("\n--- Testing manus_mcp_cli ---")
#     mcp_help = manus_mcp_cli(["--help"])
#     if mcp_help: print(f"MCP CLI Help:\n{mcp_help[:200]}...") # Print first 200 chars

#     # Clean up dummy files
#     os.remove("test.md")
#     if os.path.exists("test.pdf"): os.remove("test.pdf")
#     if os.path.exists("test.png"): os.remove("test.png")
