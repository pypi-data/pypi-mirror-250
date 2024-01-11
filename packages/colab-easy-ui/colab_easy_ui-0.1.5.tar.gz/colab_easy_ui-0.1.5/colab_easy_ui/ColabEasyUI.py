import os
from typing import Callable
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException
from fastapi import Request
from fastapi import Response
from fastapi.routing import APIRoute
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles

from colab_easy_ui.upload import EasyFileUploaderInternal
import uvicorn
import threading


class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except RequestValidationError as exc:  # type: ignore
                print("Exception", request.url, str(exc))
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_route_handler


class ColabEasyUI(FastAPI):
    _instance = None

    @classmethod
    def get_instance(
        cls,
        upload_dir: str,
    ):
        if cls._instance is None:
            app_fastapi = ColabEasyUI(upload_dir)

            app_fastapi.mount(
                "/front",
                StaticFiles(directory=f"{os.path.dirname(__file__)}/front/dist", html=True),
                name="static",
            )

            cls._instance = app_fastapi
            return cls._instance

        return cls._instance

    def __init__(self, upload_dir: str):
        super().__init__()
        self.router.route_class = ValidationErrorLoggingRoute
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.fileUploader = EasyFileUploaderInternal(upload_dir)
        self.include_router(self.fileUploader.router)

    def _run_server(self, port: int):
        uvicorn.run(self, host="127.0.0.1", port=port, log_level="info")

    def start(self, port):
        server_thread = threading.Thread(target=self._run_server, args=(port,))
        server_thread.start()

    def main_process(self, port: int, allow_files: str, file_titles: str | None = None):
        app = ColabEasyUI.get_instance("upload")
        allowed_files = os.getenv("ALLOW_FILES", "").split(",")
        app.set_allowed_filenames(allowed_files)
        file_titles_array = os.getenv("FILE_TITLES", "").split(",")
        app.set_file_titles(file_titles_array)
        uvicorn.run(self, host="127.0.0.1", port=port, log_level="info")
        # uvicorn.run(app, host="127.0.0.1", port=int(port), log_level="info")

    def set_allowed_filenames(self, filenames: list[str]):
        self.fileUploader.allowed_filenames = filenames

    def set_file_titles(self, file_titles: list[str]):
        self.fileUploader.file_titles = file_titles
