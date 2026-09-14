from github_utils import get_repository_files


repo_url = "https://github.com/psf/requests"

files = get_repository_files(repo_url)

print(f"Found {len(files)} source files")

for file in files[:5]:
    print(file["name"])
