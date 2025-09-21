"""
Documentation loader module for loading DOCS.md content.
"""
from pathlib import Path


def load_docs(docs_file: str = "DOCS.md") -> str:
    """
    Load documentation content from a markdown file.

    Args:
        docs_file: Path to the documentation file (default: "DOCS.md")

    Returns:
        Documentation content as string, or fallback content if file not found.
    """
    try:
        current_dir = Path.cwd()
        docs_path = current_dir / docs_file

        if not docs_path.exists():
            for i in range(3):
                parent_dir = current_dir.parents[i] if i < len(current_dir.parents) else None
                if parent_dir:
                    potential_path = parent_dir / docs_file
                    if potential_path.exists():
                        docs_path = potential_path
                        break

        # Read the documentation file
        if docs_path.exists():
            with open(docs_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
                return content if content else get_fallback_docs()
        else:
            print(f"Warning: {docs_file} not found. Using fallback documentation.")
            return get_fallback_docs()

    except Exception as e:
        print(f"Error loading documentation from {docs_file}: {e}")
        return get_fallback_docs()


def get_fallback_docs() -> str:
    """
    Fallback documentation content when DOCS.md is not available.

    Returns:
        Default documentation content as string.
    """
    return """# Ghala Webhooks Service

This service handles **Ghala webhooks**, verifies authenticity, and dispatches events to plugins.

## Repository

Clone the project:
```bash
git clone https://github.com/erickweyunga/ghala-hooks
cd ghala-hooks
```
"""

def get_app_description() -> str:
    """
    Get the application description from DOCS.md or fallback content.

    Returns:
        Documentation content for use in FastAPI app description.
    """
    return load_docs()
