import fire
import uvicorn
import os
from multiprocessing import freeze_support

from colab_easy_ui.ColabEasyUI import ColabEasyUI


# app = ColabEasyUI.get_instance("upload")
# allowed_files = os.getenv("ALLOW_FILES", "").split(",")
# app.set_allowed_filenames(allowed_files)
# file_titles = os.getenv("FILE_TITLES", "").split(",")
# app.set_file_titles(file_titles)


def main_process(port: int, allow_files: str, file_titles: str | None = None):
    if isinstance(allow_files, tuple):
        allow_files = ",".join(allow_files)
    if isinstance(file_titles, tuple):
        file_titles = ",".join(file_titles)

    os.environ["ALLOW_FILES"] = allow_files
    os.environ["FILE_TITLES"] = file_titles if file_titles is not None else ""

    app = ColabEasyUI.get_instance("upload")
    allowed_files = os.getenv("ALLOW_FILES", "").split(",")
    app.set_allowed_filenames(allowed_files)
    file_titles_array = os.getenv("FILE_TITLES", "").split(",")
    app.set_file_titles(file_titles_array)

    uvicorn.run(
        # "colab_easy_ui.main:app",
        app,
        host="0.0.0.0",
        port=int(port),
        # reload=True,
        log_level="info",
    )


def main():
    freeze_support()
    fire.Fire(
        {
            "main_process": main_process,
        }
    )


if __name__ == "__main__":
    main()
