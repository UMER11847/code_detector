import io
import zipfile

import requests


SUPPORTED_EXTENSIONS = (
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".cpp",
    ".c",
    ".cs",
    ".php",
    ".go",
)


def get_repository_files(repo_url):
    """
    Download a public GitHub repository as a ZIP file
    and extract supported source-code files.
    """

    parts = repo_url.rstrip("/").split("/")

    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL.")

    owner = parts[-2]
    repo_name = parts[-1]

    zip_url = (
        f"https://github.com/{owner}/{repo_name}/archive/refs/heads/main.zip"
    )

    response = requests.get(zip_url, timeout=30)

    # Some repositories use master instead of main
    if response.status_code == 404:

        zip_url = (
            f"https://github.com/{owner}/{repo_name}/archive/refs/heads/master.zip"
        )

        response = requests.get(zip_url, timeout=30)

    if response.status_code != 200:

        raise ValueError(
            "Unable to download repository. "
            "Make sure the repository is public and the URL is correct."
        )

    files = []

    with zipfile.ZipFile(io.BytesIO(response.content)) as archive:

        for file_path in archive.namelist():

            if not file_path.lower().endswith(SUPPORTED_EXTENSIONS):
                continue

            # Skip hidden/system directories
            if "/.git/" in file_path or "/node_modules/" in file_path:
                continue

            try:

                code = archive.read(file_path).decode("utf-8")

                files.append(
                    {
                        "name": file_path,
                        "code": code,
                    }
                )

            except (UnicodeDecodeError, KeyError):

                continue

    return files
