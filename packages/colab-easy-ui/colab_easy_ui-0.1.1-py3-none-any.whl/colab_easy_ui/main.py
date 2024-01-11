import fire
import uvicorn
import os
from multiprocessing import freeze_support

from colab_easy_ui.ColabEasyUI import ColabEasyUI

import threading
import uvicorn
from colab_easy_ui.ColabEasyUI import ColabEasyUI
import os


def main_process(port: int, allow_files: str, file_titles: str | None = None):
    app = ColabEasyUI.get_instance("upload")
    allowed_files = os.getenv("ALLOW_FILES", "").split(",")
    app.set_allowed_filenames(allowed_files)
    file_titles_array = os.getenv("FILE_TITLES", "").split(",")
    app.set_file_titles(file_titles_array)
    uvicorn.run(app, host="127.0.0.1", port=int(port), log_level="info")

    # # Uvicornをバックグラウンドスレッドで実行
    # server_thread = threading.Thread(target=run_server)
    # server_thread.start()


def main():
    freeze_support()
    fire.Fire(
        {
            "main_process": main_process,
        }
    )


if __name__ == "__main__":
    main()
