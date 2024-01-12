import os
import subprocess
import platform
import requests
import re
from tqdm.auto import tqdm
from urllib.parse import urlparse

class S5CmdRunner:
    """
    A class that provides methods for interacting with s5cmd, a command-line tool for efficient S3 data transfer.

    Attributes:
        s5cmd_path (str): The path to the s5cmd executable.

    Methods:
        __init__(): Initializes the S5CmdRunner object.
        has_s5cmd() -> bool: Checks if s5cmd is available.
        get_s5cmd() -> None: Downloads and installs s5cmd if it is not available.
        call_function(command: str, *args): Calls a function with the specified command and arguments.
        download_file(file_uri) -> str: Downloads a file from a URI to a temporary local path.
        generate_s5cmd_file(s3_uris, dest_dir) -> str: Generates a command file for s5cmd with the specified S3 URIs and destination directory.
        download_from_s3_list(s3_uris, dest_dir): Downloads multiple files from S3 using s5cmd.
        is_local_file(path) -> bool: Checks if a file path is a local file.
        download_from_url(url) -> str: Downloads a file from a URL to a temporary local path.
        cp(from_str, to_str): Copies a file from a local path or URL to an S3 URI or vice versa using s5cmd.
        mv(from_str, to_str): Moves a file from a local path to an S3 URI or vice versa using s5cmd.
        run(txt_uri): Runs s5cmd with a command file specified by a local path, URL, or S3 URI.
    """
    def __init__(self):
        self.s5cmd_path = os.path.expanduser('~/s5cmd')
        if not self.has_s5cmd():
            self.get_s5cmd()

    def has_s5cmd(self) -> bool:
        return os.path.exists(self.s5cmd_path) and os.access(self.s5cmd_path, os.X_OK)

    def get_s5cmd(self) -> None:
        arch = platform.machine()
        s5cmd_url = ""

        if arch == 'x86_64':
            s5cmd_url = "https://huggingface.co/kiriyamaX/s5cmd-backup/resolve/main/s5cmd_2.2.2_Linux-64bit/s5cmd"
        elif arch == 'aarch64':
            s5cmd_url = "https://huggingface.co/kiriyamaX/s5cmd-backup/resolve/main/s5cmd_2.2.2_Linux-arm64/s5cmd"
        else:
            raise ValueError("Unsupported architecture")

        subprocess.run(["wget", "-O", self.s5cmd_path, s5cmd_url])
        subprocess.run(["chmod", "+x", self.s5cmd_path])

    def call_function(self, command: str, *args, capture_output=False):
        """
        :param capture_output: If True, the function will return a subprocess.Popen object (to reroute stdout and stderr)
        """
        if capture_output:
            try:
                process = subprocess.Popen([command, *args], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                return process
            except Exception as e:
                print(f"Error starting subprocess: {e}")
                return None
        else:
            subprocess.run([command, *args])


    def generate_s5cmd_file(self, s3_uris, dest_dir):
        command_file_path = '/tmp/s5cmd_commands.txt'
        with open(command_file_path, 'w') as file:
            for s3_uri in s3_uris:
                command = f"cp {s3_uri} {dest_dir}/{os.path.basename(s3_uri)}\n"
                file.write(command)
        return command_file_path

    def download_from_s3_list(self, s3_uris, dest_dir, simplified_print=True):
        if not self.has_s5cmd():
            raise RuntimeError("s5cmd is not available")

        command_file_path = self.generate_s5cmd_file(s3_uris, dest_dir)
        
        if simplified_print:
            process = self.call_function(self.s5cmd_path, "run", command_file_path, capture_output=True)
            if process and process.stdout:
                with tqdm(total=len(s3_uris), desc="downloading files") as pbar:
                    for line in process.stdout:
                        if "cp" in line:
                            pbar.update(1)
                process.wait()
            else:
                print("Failed to start s5cmd subprocess with output capture.")
        else:
            self.call_function(self.s5cmd_path, "run", command_file_path)

    
    def is_local_file(self, path):
        return os.path.isfile(path)    


    def get_filename_from_url(self, url):
        """
        Extract the filename from a URL.

        Args:
            url (str): The URL to parse.

        Returns:
            str: The filename extracted from the URL.
        """
        parsed_url = urlparse(url)
        return os.path.basename(parsed_url.path)
    

    def download_file(self, uri):
        """
        Download a file from a URI (S3 or HTTP/HTTPS URL) to a temporary local path, preserving the filename.

        Args:
            uri (str): The URI of the file to download, can be an S3 URI or a URL.

        Returns:
            str: The local path of the downloaded file.
        """
        if uri.startswith('s3://'):
            local_filename = self.get_filename_from_url(uri)  # Use the S3 key as the filename
            local_path = os.path.join('/tmp', local_filename)
            self.call_function(self.s5cmd_path, "cp", uri, local_path)
        elif re.match(r'https?://', uri):
            local_filename = self.get_filename_from_url(uri)
            local_path = os.path.join('/tmp', local_filename)
            response = requests.get(uri)
            response.raise_for_status()
            with open(local_path, 'wb') as file:
                file.write(response.content)
        else:
            raise ValueError("Unsupported URI scheme")
        return local_path
    

    def mv(self, from_str, to_str):
        """
        Move a file from a local path to an S3 URI or from an S3 URI to a local path.

        Args:
            from_str (str): The source file path or S3 URI.
            to_str (str): The destination file path or S3 URI.
        """
        if not self.has_s5cmd():
            raise RuntimeError("s5cmd is not available")

        self.call_function(self.s5cmd_path, "mv", from_str, to_str)


    def cp(self, from_str, to_str):
        """
        Copy a file from a local path or URI (S3 or URL) to an S3 URI or from an S3 URI to a local path.
        Warns if a file is being uploaded as a file name instead of into a folder.

        Args:
            from_str (str): The source file path or URI.
            to_str (str): The destination file path or S3 URI.
        """
        if not self.has_s5cmd():
            raise RuntimeError("s5cmd is not available")

        if re.match(r'https?://', from_str) or from_str.startswith('s3://'):
            from_str = self.download_file(from_str)

        if os.path.isfile(from_str) and not to_str.endswith('/'):
            # Check if the source is a file and the destination does not end with a slash
            file_extension = os.path.splitext(from_str)[1]
            if file_extension:  # Check if source has a file extension
                print(f"Warning: '{from_str}' is being uploaded as a file name '{to_str}' instead of into a folder.")

        self.call_function(self.s5cmd_path, "cp", from_str, to_str)


     
    def run(self, txt_uri):
        """
        Run s5cmd with a command file specified by a local path, URL, or S3 URI.

        Args:
            txt_uri (str): The path, URL, or S3 URI of the command file.
        """
        if not self.has_s5cmd():
            raise RuntimeError("s5cmd is not available")

        if not self.is_local_file(txt_uri):
            txt_uri = self.download_file(txt_uri)

        self.call_function(self.s5cmd_path, "run", txt_uri)



if __name__ == '__main__':
    # Example usage:
    runner = S5CmdRunner()
    runner.run('s3://your-bucket/path-to-your-file.txt')
    # Or
    runner.run('http://example.com/path-to-your-file.txt')
