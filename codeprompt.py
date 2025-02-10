import os
import sys
import argparse
import re
from fnmatch import fnmatch
import datetime  # Import the datetime module

DEFAULT_BLACKLISTED_DIRS = {'node_modules', 'archive', '.git', '.vscode', '.appwrite', 'static', '.svelte-kit'}
DEFAULT_WHITELISTED_FILES = {'*.js', '*.ts', '*.svelte', '*.html', '*.css', '*.json', '*.md', '*.py', '*.env'}
DEFAULT_BLACKLISTED_FILES = {'package-lock.json', 'yarn.lock', '.DS_Store', '.prettierrc.json', '.prettierignore', 'tsconfig.json', 'README.md', '.gitignore', 'code_prompt'}

EXT_TO_LANG = {
    ".js": "javascript",
    ".ts": "typescript",
    ".svelte": "svelte",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".md": "markdown",
    ".py": "python",
    ".env": "env"
}

COMMENT_PATTERNS = {
    "javascript": r'//.*|/\*[\s\S]*?\*/',
    "typescript": r'//.*|/\*[\s\S]*?\*/',
    "svelte": r'<!--[\s\S]*?-->',  # Svelte uses HTML comments
    "html": r'<!--[\s\S]*?-->',
    "css": r'/\*[\s\S]*?\*/',
    "python": r'#.*',
    "env": r'#.*'
}

def is_whitelisted(file, whitelisted_files):
    return any(fnmatch(file, pattern) for pattern in whitelisted_files) if whitelisted_files else True

def is_blacklisted(file, blacklisted_files):
    return file in blacklisted_files

def remove_comments(content, lang):
    if lang in COMMENT_PATTERNS:
        return re.sub(COMMENT_PATTERNS[lang], '', content, flags=re.MULTILINE)
    return content

def gather_files(root_dir, output_file, exclude_patterns, include_env_mode,
                 whitelisted_files, blacklisted_files, remove_comments_flag):
    try:
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for root, dirs, files in os.walk(root_dir):
                dirs[:] = [d for d in dirs if d not in DEFAULT_BLACKLISTED_DIRS and not d.startswith('.')]

                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, root_dir)

                    # Check if the file/path is excluded
                    if any(fnmatch(rel_path, pattern) or fnmatch(file_path, pattern) for pattern in exclude_patterns):
                        continue

                    if is_blacklisted(file, blacklisted_files) or not is_whitelisted(file, whitelisted_files):
                        continue

                    if os.path.abspath(file_path) == os.path.abspath(output_file):
                        continue

                    ext = os.path.splitext(file)[1]
                    lang = EXT_TO_LANG.get(ext, "plaintext")

                    try:
                        with open(file_path, 'r', encoding='utf-8') as in_f:
                            content = in_f.read()

                            if file == ".env":
                                if include_env_mode == "names_only":
                                    # Only keep the variable names in .env
                                    lines = content.splitlines()
                                    content = "\n".join(line.split("=", 1)[0] for line in lines if "=" in line)
                                elif include_env_mode == "ignore":
                                    continue  # Skip the .env file

                            if remove_comments_flag:
                                content = remove_comments(content, lang)

                            out_f.write(f"## {rel_path}\n\n")
                            out_f.write(f"```{lang}\n{content}\n```\n\n")
                    except UnicodeDecodeError:
                        print(f"UnicodeDecodeError: Skipping {file_path}")
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
    except Exception as e:
        print(f"Error writing to file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a Markdown file containing code snippets from a directory.",
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("-d", "--dev-dir", default=os.getcwd(),
                        help="The directory to scan for code files (default: current directory).")
    parser.add_argument("-o", "--output-dir", default="code_prompt.md",
                        help="The path to the output Markdown file.\nA timestamp (YYMMDD-HHMM-) will be prepended to the filename. If a directory is specified, it will be created if it doesn't exist.")
    parser.add_argument("-x", "--exclude", default="",
                        help="A comma-separated list of file patterns to exclude from the output.\n"
                             "  Example: --exclude=someFile.js,folder/subfolder,folder/someFile.js\n"
                             "  Uses fnmatch patterns (similar to glob patterns).\n"
                             "  Matches against both the relative and absolute file paths.")

    parser.add_argument("-w", "--whitelist", default="",
                        help="A comma-separated list of file patterns to *override* the default whitelist.\n"
                             "  If specified, *only* files matching these patterns will be included.")
    parser.add_argument("-b", "--blacklist", default="",
                        help="A comma-separated list of file names to *override* the default blacklist.\n"
                             "  If specified, *only* files matching these names will be excluded.")

    parser.add_argument("-c", "--remove-comments", action="store_true",
                        help="If set, comments will be removed from the code snippets in the output.")

    env_group = parser.add_mutually_exclusive_group()
    env_group.add_argument("-n", "--include-env", action="store_true",
                        help="If set, only includes the variable names (left side of '=') from .env files.\n"
                             "  This hides the values of environment variables in the output.")
    env_group.add_argument("-v", "--include-env-values", action="store_true",
                        help="If set, includes the entire contents of .env files, including the variable values.")


    args = parser.parse_args()

    dev_dir = args.dev_dir
    output_file = args.output_dir # Corrected variable name to match argparse definition
    exclude_patterns = [p.strip() for p in args.exclude.split(",") if p.strip()]
    remove_comments_flag = args.remove_comments

    if args.include_env:
        include_env_mode = "names_only"
    elif args.include_env_values:
        include_env_mode = "values"
    else:
        include_env_mode = "ignore"

    # Override whitelists and blacklists if provided
    whitelisted_files = set([p.strip() for p in args.whitelist.split(",") if p.strip()]) if args.whitelist else DEFAULT_WHITELISTED_FILES
    blacklisted_files = set([p.strip() for p in args.blacklist.split(",") if p.strip()]) if args.blacklist else DEFAULT_BLACKLISTED_FILES

    # Generate timestamp
    timestamp = datetime.datetime.now().strftime("%y%m%d-%H%M-")

    # Split path
    output_dir, output_name = os.path.split(output_file)

    # Add code_prompt to the filename if it is not there
    if "code_prompt" not in output_name:
      filename = "code_prompt.md"
    else:
      filename = output_name

    # Create output directory
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
        except OSError as e:
            print(f"Could not create output directory: {e}")
            sys.exit(1)

    # Contruct path
    output_file = os.path.join(output_dir, timestamp + filename)

    if not os.path.isdir(dev_dir):
        print(f"Invalid directory: {dev_dir}")
        sys.exit(1)

    gather_files(dev_dir, output_file, exclude_patterns, include_env_mode,
                 whitelisted_files, blacklisted_files, remove_comments_flag)
    print(f"Markdown prompt created: {os.path.abspath(output_file)}")