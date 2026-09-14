import os


def detect_language(filename):
    """
    Detect programming language from a file extension.
    """

    extension = os.path.splitext(filename)[1].lower()

    language_map = {
        ".py": "python",
        ".js": "javascript",
        ".jsx": "javascript",
        ".ts": "typescript",
        ".tsx": "typescript",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".cs": "csharp",
        ".php": "php",
        ".go": "go",
    }

    return language_map.get(extension, "text")
