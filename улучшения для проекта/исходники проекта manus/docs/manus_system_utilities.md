# Manus System Utilities: Command Line Tools

This document provides a detailed overview of the command-line utilities pre-installed in the Manus sandbox environment. These utilities extend the agent's capabilities by providing specialized functionalities for file conversion, media processing, and interaction with external services. All descriptions are presented in English, reflecting their native language within the system.

## 1. `manus-render-diagram`

**Description**: Renders diagram files (Mermaid, D2, PlantUML, Markdown with diagram syntax) to PNG format.

**Usage**: `$ manus-render-diagram <input_file> <output_file>`

**Example**: `$ manus-render-diagram path/to/input.mmd path/to/output.png`

**Input File Formats**: `.mmd` (Mermaid), `.d2` (D2), `.puml` (PlantUML), `.md` (Markdown with embedded diagram syntax).

**Output File Format**: `.png`

## 2. `manus-md-to-pdf`

**Description**: Converts a Markdown file to PDF format.

**Usage**: `$ manus-md-to-pdf <input_file> <output_file>`

**Example**: `$ manus-md-to-pdf path/to/input.md path/to/output.pdf`

**Input File Format**: `.md`

**Output File Format**: `.pdf`

## 3. `manus-speech-to-text`

**Description**: Transcribes speech/audio/video files (.mp3, .wav, .mp4, .webm) to text.

**Usage**: `$ manus-speech-to-text <input_file>`

**Example**: `$ manus-speech-to-text path/to/interview.mp3`

**Input File Formats**: `.mp3`, `.wav`, `.mp4`, `.webm`

**Output**: Transcribed text (printed to stdout).

## 4. `manus-mcp-cli`

**Description**: Interacts with Model Context Protocol (MCP) servers. This is a command-line interface for advanced interactions with the MCP, which can be used for various purposes including managing model context, invoking specific model capabilities, or integrating with external MCP-compliant services.

**Usage**: `$ manus-mcp-cli <command> [args...]`

**Example**: `$ manus-mcp-cli --help` (to view available commands and arguments)

## 5. `manus-upload-file`

**Description**: Uploads one or more files to an S3-compatible storage service and returns direct public URLs for MCP or API invocations. This is useful for making generated or processed files accessible externally.

**Usage**: `$ manus-upload-file <input_file> [input_file_2 ...]`

**Example**: `$ manus-upload-file path/to/file1.png path/to/file2.pdf`

**Output**: Public URLs for the uploaded files (printed to stdout).

## 6. `manus-export-slides`

**Description**: Exports slides from a `manus-slides://{version_id}` URI to a specified format (.pdf, .ppt). This utility is used after a presentation has been generated internally by the `slides` tool and needs to be exported into a standard document format.

**Usage**: `$ manus-export-slides <slides_uri> <output_format>`

**Example**: `$ manus-export-slides manus-slides://2tvrCaJBV8I6gabDLa4YCL pdf`

**Input URI Format**: `manus-slides://{version_id}`

**Output Formats**: `pdf`, `ppt`
