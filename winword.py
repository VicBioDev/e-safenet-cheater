from pathlib import Path
import os
import sys
import subprocess
import random
import time


# Define chunk size
chunk_size = 1024  # You can adjust this value as per your requirement


def is_encrypted(file_path: Path):
    search_string = "Esafenet".encode("ascii")
    with file_path.open("rb") as file:
        first_chunk = file.read(chunk_size)
        if search_string in first_chunk:
            print(
                f"Found '{search_string.decode()}' at the beginning of file: {file_path}"
            )
            return True
        else:
            print(
                f"'{search_string.decode()}' not found at the beginning of file: {file_path}"
            )
            return False


def is_encrypted_powershell(file_path: Path, search_string="Esafenet"):
    encrypted_extensions = [
        ".txt",
        ".csv",
        ".jpg",
        ".gif",
        ".png",
        ".bmp",
        ".jpeg",
        ".tiff",
        ".docx",
        ".xlsx",
        ".pptx",
        ".pdf",
        ".doc",
        ".xls",
        ".ppt",
    ]
    file_extension = file_path.suffix.lower()
    if file_extension not in encrypted_extensions:
        print(f"Found normal file: {file_path}")
        return False

    ps_script = f"""
        $filePath = "{file_path}"
        $chunkSize = 1024
        $searchString = "{search_string}"

        # Attempt to read the first chunk of the file
        try {{
            $fileStream = [System.IO.File]::OpenRead($filePath)
            $bytes = New-Object Byte[] $chunkSize
            $numBytesRead = $fileStream.Read($bytes, 0, $chunkSize)
            $fileStream.Close()

            if ($numBytesRead -eq 0) {{
                Write-Host "No data read from file."
                exit
            }}

            # Converting bytes to string for comparison
            $firstChunkAsString = [System.Text.Encoding]::ASCII.GetString($bytes)

            return $firstChunkAsString.Contains($searchString)
        }} catch {{
            Write-Host "An error occurred."
            exit
        }}
    """

    # Running the PowerShell script from Python
    try:
        result = subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout.strip()
        is_found = output.lower() == "true"
        if is_found:
            print(f"Found encrypted file: {file_path}")
            return True
        print(f"Found normal file: {file_path}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Unknown file: {file_path}")
        return False


def decrypt_file(file_path: Path):
    print(f"Decrypting file: {file_path.absolute()}")

    # Read binary content of file in chunks and write to output file
    temp_file_path = file_path.with_suffix(f"{file_path.suffix}.temp")
    with file_path.open("rb") as input_file, temp_file_path.open("wb") as output_file:
        while True:
            # Read a chunk of data from the input file
            chunk = input_file.read(chunk_size)

            # Break the loop if no more data is left to read
            if not chunk:
                break

            # Write the chunk of data to the output file
            output_file.write(chunk)

    # Get file properties
    file_stat = os.stat(file_path)
    create_time = file_stat.st_ctime
    modified_time = file_stat.st_mtime

    # Rename the original file to encrypted file using PowerShell command
    encrypted_file_path = file_path.with_suffix(f".encrypted{file_path.suffix}")
    subprocess.run(
        [
            "powershell",
            "Rename-Item",
            f'"{file_path.absolute()}"',
            f'"{encrypted_file_path.absolute()}"',
        ]
    )

    # Update file properties of the final file
    os.utime(temp_file_path, (create_time, modified_time))

    # wait a random time less than 1 second
    wait_time = random.uniform(0, 1)
    time.sleep(wait_time)

    # Rename the temp file to the final file using PowerShell command
    subprocess.run(
        [
            "powershell",
            "Rename-Item",
            f'"{temp_file_path.absolute()}"',
            f'"{file_path.absolute()}"',
        ]
    )


if __name__ == "__main__":

    # Get file path from CLI argument
    input_paths = [Path(arg) for arg in sys.argv[1:]]

    # Decrypt the file if it is encrypted
    for input_path in input_paths:
        if not input_path.exists():
            print(f"File not found: {input_path}")
            continue

        if input_path.is_file() and is_encrypted_powershell(input_path):
            decrypt_file(input_path)

        if input_path.is_dir():
            for file in input_path.rglob("*"):
                if file.is_file() and is_encrypted_powershell(file):
                    decrypt_file(file)

    # Wait for user input before exiting
    input("Press Enter to exit...")
