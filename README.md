# Code Prompt Generator

This Python script, `code_prompt_generator.py`, helps you create Markdown files containing code snippets from a specified directory. This is useful for generating prompts for Large Language Models (LLMs) or for documenting codebases in a structured Markdown format.

## Functionality

The script recursively scans a directory for code files and generates a Markdown (`.md`) file.  It includes:

* **Code Extraction:**  Extracts code content from files within the specified directory.
* **Language Detection:**  Automatically detects the programming language based on file extensions and applies appropriate syntax highlighting in the Markdown output.
* **Filtering:**
    * **Exclusion Patterns:**  Allows you to exclude files and directories based on flexible patterns (using `fnmatch`).
    * **Default Blacklists:**  Includes default blacklists for common directories (like `node_modules`, `.git`) and files (like lock files, config files).
    * **Whitelists & Blacklists:**  Provides options to override default whitelists and blacklists for more precise control over included files.
* **Comment Removal:**  Optionally removes comments from the code snippets in the output Markdown.
* **`.env` File Handling:** Offers options for how to handle `.env` files:
    * **Ignore:** Exclude `.env` files entirely.
    * **Names Only:** Include only the variable names from `.env` files (hiding values).
    * **Include Values:** Include the full content of `.env` files (including values).
* **Markdown Output:**  Generates a clean Markdown file with code blocks, making it easy to read and use in various contexts.

## Features

* **Flexible File Filtering:**  Powerful exclusion patterns and customizable whitelists/blacklists.
* **Multi-Language Support:**  Supports syntax highlighting for common programming languages (JavaScript, TypeScript, Svelte, HTML, CSS, JSON, Markdown, Python, Environment files).
* **Comment Removal:**  Clean up code snippets by removing comments.
* **`.env` Handling Options:** Control how sensitive environment information is included.
* **Cross-Platform (Likely):** Designed to work on Windows, macOS, and Linux (though macOS and Linux are currently untested).

## Installation

1. **Clone the repository (optional):**

   If you are using Git, you can clone this repository to your local machine:

   ```bash
   git clone https://github.com/Vanillabacke/codeprompt.git
   cd codeprompt
   ```

2. **Ensure Python is installed:**

   This script requires Python 3.7 or later. If you don't have Python installed, download and install it from [python.org](https://www.python.org/).  **During installation on Windows, make sure to check the "Add Python to PATH" option.**

3. **No external Python packages are required:**

   This script uses only standard Python libraries, so no `pip install` is necessary!

## Usage

Run the script from your terminal using the following command:

```bash
code_prompt_generator.py [options]
```

**Options:**

* `-d`, `--dev-dir <directory>`: The directory to scan for code files. Defaults to the current directory if not provided.
* `-o`, `--output-dir <path>`: The path to the output Markdown file. A timestamp (YYMMDD-HHMM-) will be prepended to the filename. If a directory is specified, it will be created if it doesn't exist. Defaults to `code_prompt.md` in the current directory.
* `-x`, `--exclude <patterns>`:  Comma-separated list of file patterns to exclude. Example: `--exclude=someFile.js,folder/subfolder,*.log`. Uses `fnmatch` patterns. Matches against both relative and absolute file paths.
* `-w`, `--whitelist <patterns>`: Comma-separated list of file patterns to **override** the default whitelist. If specified, only files matching these patterns will be included.
* `-b`, `--blacklist <files>`: Comma-separated list of file names to **override** the default blacklist. If specified, only files matching these names will be excluded.
* `-c`, `--remove-comments`: If set, comments will be removed from the code snippets.
* `-n`, `--include-env`:  Include only variable names from `.env` files (hides values).
* `-v`, `--include-env-values`: Include the full content of `.env` files (including values).  **Mutually exclusive with `--include-env`.**

**Example Usage:**

1. **Generate `code_prompt.md` from the current directory (using all defaults):**

   ```bash
   code_prompt_generator.py
   ```

2. **Generate `my_prompt.md` in the current directory from the `src` directory, excluding `tests` folder:**

   ```bash
   code_prompt_generator.py -d src -o my_prompt.md -x "tests"
   ```

3. **Generate `prompt_no_comments.md` in the "output" directory (which will be created if it doesn't exist) from the `project` directory, removing comments:**

   ```bash
   code_prompt_generator.py -d project -o output/prompt_no_comments.md -c
   ```

4. **Generate prompt including only JavaScript and Svelte files from the `webapp` directory, using short flag for whitelist:**

   ```bash
   code_prompt_generator.py -d webapp -o js_svelte_prompt.md -w "*.js,*.svelte"
   ```

5. **Generate prompt excluding specific blacklisted files, using short flag for blacklist:**

   ```bash
   code_prompt_generator.py -d my_project -o no_lockfiles_prompt.md -b "package-lock.json,yarn.lock"
   ```

6. **Generate prompt including `.env` variable names only, outputting to `env_names_prompt.md`:**

   ```bash
   code_prompt_generator.py -d my_project -o env_names_prompt.md -n
   ```

## Customization

You can customize the script through command-line arguments:

* **File Filtering:** Use `-x`, `-w`, and `-b` flags to precisely control which files are included in the output.
* **Comment Removal:** Use `-c` or `--remove-comments` to remove comments for cleaner code snippets.
* **`.env` Handling:** Choose how `.env` files are processed using `-n` (`--include-env`) or `-v` (`--include-env-values`).

You can also modify the script directly to adjust:

* **Default Blacklists/Whitelists:**  Change `DEFAULT_BLACKLISTED_DIRS`, `DEFAULT_WHITELISTED_FILES`, and `DEFAULT_BLACKLISTED_FILES` in the script to modify the default filtering behavior.
* **Language Mappings:**  Update `EXT_TO_LANG` to add support for more file extensions and languages.
* **Comment Patterns:**  Modify `COMMENT_PATTERNS` to adjust comment removal for different languages or add support for new languages.

## Making the script executable from anywhere (Command Line Access)

To run the `code_prompt_generator.py` script directly from your command line without typing `python` every time, you need to make it accessible in your system's PATH.  Here are two methods for Windows, and instructions for macOS and Linux:

### Windows

**Method 1: Direct Python Script Execution (Recommended for simple setup)**

1. **Ensure Python is associated with `.py` files and "Add Python to PATH" was checked during Python installation.** (See Installation step 2).

2. **Make the script executable (optional but recommended):**

   * Open `code_prompt_generator.py` in a text editor.
   * Add the following line as the very first line of the file (called a "shebang" line):

     ```python
     #!python
     ```

   * Save the file. This line tells Windows to use the Python interpreter to run this script.

3. **Add the script's directory to your PATH environment variable:**

   * **Locate the script's directory:**  Find the folder where you saved `code_prompt_generator.py`. For example, if you cloned the repository to `C:\tools\code-prompt-generator`, that's your script's directory.

   * **Open System Environment Variables:**
      * Press the **Windows key**, type "env", and select "Edit the system environment variables".
      * In the "System Properties" window, click the "Environment Variables..." button.

   * **Edit the "Path" variable:**
      * In the "System variables" section (or "User variables" if you only want it for your user), find the variable named "Path" and select it.
      * Click "Edit...".

   * **Add the script's directory:**
      * Click "New" and paste or type the full path to the directory where you saved `code_prompt_generator.py`.
      * For example: `C:\tools\code-prompt-generator`
      * Click "OK" on all open windows to save the changes.

   * **Restart your command prompt (and potentially your computer):**  The changes to the PATH variable might not be reflected in already open command prompt windows. Close and reopen your command prompt, or restart your computer for the changes to take full effect.

4. **Run from command line:**

   Now, you should be able to open a command prompt in *any* directory and run the script by simply typing:

   ```bash
   code_prompt_generator.py [options]
   ```

**Method 2: Using a `codeprompt.bat` file (Alternative method)**

1. **Choose a location for the `codeprompt.bat` file:** It's recommended to place this `.bat` file in a custom directory like `C:\tools`. You will need to ensure this directory is added to your system's PATH environment variable. Creating `C:\tools` if it doesn't exist is also a good practice.

2. **Create `codeprompt.bat`:**
   * Open Notepad or any plain text editor.
   * Paste the following lines into the editor, **adjusting the path to `code_prompt_generator.py` to the actual location where you saved the script:**

     ```batch
     @echo off
     python C:\path\to\your\script\code_prompt_generator.py %*
     ```
     **Example (if `code_prompt_generator.py` is in `C:\tools`):**
     ```batch
     @echo off
     python C:\tools\code_prompt_generator.py %*
     ```
   * Save the file as `codeprompt.bat` in the directory you chose in step 1 (e.g., `C:\tools\codeprompt.bat`).  **Make sure to select "All Files" as the "Save as type" to prevent it from being saved as `codeprompt.bat.txt`.**

3. **Ensure the directory containing `codeprompt.bat` is in your PATH environment variable:**
   * If you chose a new directory (like `C:\tools`), follow the steps in **Method 1, step 3** to add this directory (e.g., `C:\tools`) to your system's PATH environment variable.

4. **Run from command line:**

   Now, you should be able to open a command prompt in *any* directory and run the script by simply typing:

   ```bash
   codeprompt [options]
   ```

### macOS and Linux (Untested - Use with caution)

1. **Make the script executable:**

   * Open your terminal.
   * Navigate to the directory where you saved `code_prompt_generator.py` using the `cd` command (e.g., `cd ~/Documents/code-prompt-generator`).
   * Make the script executable using the `chmod` command:

     ```bash
     chmod +x code_prompt_generator.py
     ```
     This command adds execute permissions to the script file.

   * **Add a shebang line (recommended):**
     * Open `code_prompt_generator.py` in a text editor (like `nano`, `vim`, or a GUI editor).
     * Add one of the following lines as the very first line of the file, depending on how Python is installed on your system:

       ```python
       #!/usr/bin/env python3  # Recommended - uses environment's python3
       ```
       *OR (if `python3` doesn't work)*
       ```python
       #!/usr/bin/env python   # Uses environment's default python (might be python2 or python3)
       ```
       *OR (if you know the exact path to your python3 executable, find it using `which python3`)*
       ```python
       #!/usr/bin/python3  # Replace with the actual path if needed, e.g., #!/usr/local/bin/python3
       ```
     * Save the file.

2. **Add the script's directory to your PATH environment variable:**

   * **Locate the script's directory:** Find the full path to the directory containing `code_prompt_generator.py`. For example, if you saved it in `~/Documents/code-prompt-generator`, the path is `/Users/YourUsername/Documents/code-prompt-generator` (or `/home/YourUsername/Documents/code-prompt-generator` on Linux). You can use `pwd` command in the terminal when you are in the script's directory to get the full path.

   * **Edit your shell configuration file:**  You need to modify your shell's configuration file to add the directory to the PATH.  Common shell configuration files are:
      * **Bash:** `~/.bashrc` or `~/.bash_profile`
      * **Zsh:** `~/.zshrc`
      * (Other shells might use `~/.profile` or similar)

      Choose the appropriate file for your shell (if you're unsure, try `~/.bashrc` first for Bash or `~/.zshrc` for Zsh).

   * **Open the configuration file in a text editor:**  For example, using `nano`:

     ```bash
     nano ~/.bashrc  # Or nano ~/.zshrc, etc.
     ```

   * **Add the directory to the PATH variable:**  Add the following line to the *end* of the file. Replace `/path/to/your/script/directory` with the actual path you found in step 2.

     ```bash
     export PATH="$PATH:/path/to/your/script/directory"
     ```
     For example: `export PATH="$PATH:~/Documents/code-prompt-generator"`

   * **Save and close the file.** (In `nano`, press `Ctrl+X`, then `Y` to save, then Enter).

   * **Apply the changes:**  You need to reload your shell configuration file or restart your terminal for the changes to take effect. Run one of the following commands in your terminal:

     ```bash
     source ~/.bashrc   # If you edited ~/.bashrc
     source ~/.zshrc   # If you edited ~/.zshrc
     # Or restart your terminal window
     ```

3. **Run from terminal:**

   Now, you should be able to open a terminal in *any* directory and run the script by simply typing:

   ```bash
   code_prompt_generator.py [options]
   ```

**Troubleshooting (macOS/Linux):**

* **"Command not found":** If you still get "command not found" after following these steps:
    * Double-check that you added the correct directory path to your PATH variable in the correct shell configuration file.
    * Ensure you used `export PATH="$PATH:/your/path"` correctly (including the `$PATH:` part).
    * Make sure you sourced the configuration file (`source ~/.bashrc` or similar) or restarted your terminal.
    * Verify that the script file is indeed executable (`chmod +x`) and has a correct shebang line.
    * Try using the full path to the script in the PATH variable instead of just the directory (e.g., `export PATH="$PATH:/path/to/your/script/directory/code_prompt_generator.py"` - less common, but might work in some cases).

* **Permissions issues:** If you get "Permission denied" errors, double-check that you used `chmod +x` correctly.

**Important Note for macOS/Linux Testing:**

Please test these macOS and Linux instructions and provide feedback!  Let me know if they work correctly or if any adjustments are needed. Your feedback will help improve the documentation for other users.

## Platform Compatibility

* **Windows:**  Tested and confirmed to work on Windows.
* **macOS:**  Likely to work on macOS, but **currently untested**.
* **Linux:** Likely to work on Linux distributions, but **currently untested**.

The script uses standard Python libraries and file path handling, which are generally cross-platform. However, if you encounter any issues on macOS or Linux, please report them!

## Contributing

Contributions are welcome! If you find bugs, have feature requests, or want to improve the script, please feel free to:

1. Fork the repository.
2. Create a branch for your changes.
3. Commit your changes and push them to your fork.
4. Submit a pull request.