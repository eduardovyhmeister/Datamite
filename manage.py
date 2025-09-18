#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def _parse_files_env(value: str):
    if not value:
        return []
    # support comma-separated list or single path (file or directory)
    parts = [p.strip() for p in value.split(',') if p.strip()]
    expanded = []
    for p in parts:
        p = os.path.abspath(os.path.expanduser(p))
        if os.path.isdir(p):
            # add PDFs in directory
            for name in os.listdir(p):
                if name.lower().endswith('.pdf'):
                    expanded.append(os.path.join(p, name))
        else:
            expanded.append(p)
    return expanded


def create_vector_db_if_configured():
    project_id = os.getenv('VECTORDB_ID')
    upload_folder = os.getenv('UPLOAD_FOLDER')
    files_env = os.getenv('FILE_PATHS') or os.getenv('FILE_PATH')
    files_to_process = _parse_files_env(files_env)

    if not project_id or not upload_folder or not files_to_process:
        return  # silently skip if not configured

    try:
        from LangGraphChatLogic.data.document_handling import load_project_documents
        load_project_documents(
            project_id=project_id,
            files_to_process=files_to_process,
            collection_name=project_id,
        )
        print(f"Vector DB ensured for project {project_id}. Files: {len(files_to_process)}")
    except Exception as exc:
        print(f"Failed to initialize vector DB: {exc}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datamite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Run DB initialization only when starting the dev server, once
    if 'runserver' in sys.argv and os.environ.get('RUN_MAIN') == 'true':
        create_vector_db_if_configured()

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
