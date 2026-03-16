<utilities>
The following command line utilities are pre-installed in the sandbox and ready to use via the `shell` tool to complete related tasks:

- manus-render-diagram <input_file> <output_file>
  Description: Render diagram files (.mmd, .d2, .puml, .md) to PNG format
  Example: `$ manus-render-diagram path/to/input.mmd path/to/output.png`

- manus-md-to-pdf <input_file> <output_file>
  Description: Convert Markdown file to PDF format
  Example: `$ manus-md-to-pdf path/to/input.md path/to/output.pdf`

- manus-speech-to-text <input_file>
  Description: Transcribe speech/audio files (.mp3, .wav, .mp4, .webm) to text
  Example: `$ manus-speech-to-text path/to/interview.mp3`

- manus-mcp-cli <command> [args...]
  Description: Interact with Model Context Protocol (MCP) servers
  Example: `$ manus-mcp-cli --help`

- manus-upload-file <input_file> [input_file_2 ...]
  Description: Upload one or more files to S3 and get direct public URLs for MCP or API invocations
  Example: `$ manus-upload-file path/to/file1.png path/to/file2.pdf`

- manus-export-slides <slides_uri> <output_format>
  Description: Export slides from manus-slides://{version_id} URI to specified format (.pdf, .ppt)
  Example: `$ manus-export-slides manus-slides://2tvrCaJBV8I6gabDLa4YCL pdf`
</utilities>
