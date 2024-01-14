from IPython.display import Javascript
import base64
import portpicker
import asyncio
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import requests
import json


class ColabInternalFetcher:
    tb_port = 0
    javascript = None
    display_javascript = None
    register_callback_func = None

    futures = {}  # type: ignore

    def __init__(self, javascript: Javascript, display_javascript, register_callback_func):
        self.javascript = javascript
        self.display_javascript = display_javascript
        self.register_callback_func = register_callback_func

    def start_tensorboard(self, ipython, tb_logs_dir, logfile=None):
        tb_port = portpicker.pick_unused_port()
        if logfile is not None:
            ipython.system_raw(f"tensorboard --port {tb_port} --logdir {tb_logs_dir} >{logfile} 2>&1 &")
        else:
            ipython.system_raw(f"tensorboard --port {tb_port} --logdir {tb_logs_dir} &")
        self.tb_port = tb_port
        return tb_port

    def generate_internal_fetch_reciever(self, callbacks):
        response_buffers = {}

        def receive_data_from_js(url, callback_key, data, chunk_index, total_chunks):
            # binary_data = base64.b64decode(data)
            # if callback_key in callbacks:
            #   callbacks[callback_key](binary_data)

            if url not in response_buffers:
                response_buffers[url] = [None] * total_chunks
            response_buffers[url][chunk_index] = data

            open("internal_1", "w").write("1")
            # すべてのチャンクが受信されたかチェック
            if all(chunk is not None for chunk in response_buffers[url]):
                open("internal_2", "w").write("2")
                print("ALLDATA RECEIVED")
                base64_data = "".join(response_buffers[url])
                binary_data = base64.b64decode(base64_data)
                del response_buffers[url]
                open("internal_3", "wb").write(binary_data)
                print("binary_data", binary_data)
                if callback_key in callbacks:
                    callbacks[callback_key](binary_data)
                    print("futures", self.futures)
                    self.futures[url].set_result("ffffff")
                    del self.futures[url]
            else:
                print("ALLDATA RECEIVED")

        self.register_callback_func("notebook.receive_data_from_js", receive_data_from_js)

    def generate_internal_fetch_script(self, url, callback_key: str):
        script = f"""
      const internal_fetch = async() =>{{
        console.log("url----","{url}")
        const res = await fetch("{url}")
        console.log("res",res)
        const buf = await res.arrayBuffer()
        console.log("buf",buf)

        const CHUNK_SIZE = 64 * 1024;

        //const base64String = btoa(
        //  String.fromCharCode.apply(null, new Uint8Array(buf))
        //);
        //console.log("base64String",base64String)

        let base64String=\"\"
        for (let i = 0; i < buf.byteLength; i += CHUNK_SIZE) {{
          const chunk = new Uint8Array(buf, i, Math.min(CHUNK_SIZE, buf.byteLength - i));
          base64String += String.fromCharCode.apply(null, chunk);
        }}
        base64String = btoa(base64String); // 生成された文字列をbase64にエンコード
        console.log("base64String", base64String);



        const totalChunks = Math.ceil(base64String.length / CHUNK_SIZE);
        for (let i = 0; i < totalChunks; i++) {{
          const chunk = base64String.slice(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE);
          google.colab.kernel.invokeFunction(
            'notebook.receive_data_from_js', // 関数名
            ["{url}", "{callback_key}", chunk, i, totalChunks],
            {{}}
          );
        }}
      }}
      internal_fetch()


    """
        return script

    def exec_javascript(self, script):
        try:
            open("exec_1.txt", "w").write("1")
            obj = self.javascript(script)
            open("exec_2.txt", "w").write("2")
            self.display_javascript(obj)
            open("exec_3.txt", "w").write("3")
        except Exception as e:
            import traceback

            open("error.txt", "w").write(e)
            open("error1.txt", "w").write(traceback.format_exc())
            print(e)

    # async def get_scalars_tags(self, future):
    # async def get_scalars_tags(self):
    def get_scalars_tags(self):
        url = f"http://localhost:{self.tb_port}/data/plugin/scalars/tags"
        try:
            # GETリクエストを送信
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                open("scalars_tags.txt", "w").write(json.dumps(data))
            else:
                open("scalars_tags_error1.txt", "w").write(f"Request failed with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            # 通信エラーなどの例外を捕捉
            open("scalars_tags_error2.txt", "w").write(f"Request failed with status code {e}")
            print(f"An error occurred: {e}")

        # url = f"http://localhost:{self.port}/data/plugin/scalars/tags"
        # print(url)
        # future = asyncio.Future()
        # self.futures[url] = future
        # script = self.generate_internal_fetch_script(url, "get_scalars_tags_func")

        # # asyncio.get_event_loop().run_until_complete(self.exec_javascript(script))
        # open("test.js", "w").write(script)
        # self.exec_javascript(script)
        # open("test2.js", "w").write(script)

        # data = {
        #     "status": "-----",
        #     "message": "aaaaa",
        #     "description": "easy-file-uploader-py created by wok!",
        # }
        # json_compatible_item_data = jsonable_encoder(data)
        # # return JSONResponse(content=json_compatible_item_data)
        # return script

    def get_scalars_scalars(self, run: str, tag: str):
        url = f"http://localhost:{self.port}/data/plugin/scalars/scalars?run={run}&tag={tag}"
        print(url)
        script = self.generate_internal_fetch_script(url, "get_scalars_scalars_func")
        self.exec_javascript(script)

    def get_images_tags(self):
        url = f"http://localhost:{self.port}/data/plugin/images/tags"
        print(url)
        script = self.generate_internal_fetch_script(url, "get_images_tags_func")
        # self.exec_javascript(script)
        return script

    def get_images_images(self, run: str, tag: str, sample: int):
        url = f"http://localhost:{self.port}/data/plugin/images/images?run={run}&tag={tag}&sample={sample}"
        print(url)
        script = self.generate_internal_fetch_script(url, "get_images_images_func")
        self.exec_javascript(script)

    def get_images_individualImage(self, blob_key):
        url = f"http://localhost:{self.port}/data/plugin/images/individualImage?blob_key={blob_key}"
        print(url)
        script = self.generate_internal_fetch_script(url, "get_images_individualImage_func")
        self.exec_javascript(script)

    def get_audio_tags(self):
        url = f"http://localhost:{self.port}/data/plugin/audio/tags"
        print(url)
        script = self.generate_internal_fetch_script(url, "get_audio_tags_func")
        self.exec_javascript(script)

    def get_audio_audio(self, run: str, tag: str, sample: int):
        url = f"http://localhost:{self.port}/data/plugin/audio/audio?run={run}&tag={tag}&sample={sample}"
        print(url)
        script = self.generate_internal_fetch_script(url, "get_audio_audio_func")
        self.exec_javascript(script)

    def get_audio_individualAudio(self, blob_key):
        url = f"http://localhost:{self.port}/data/plugin/audio/individualAudio?blob_key={blob_key}"
        print(url)
        script = self.generate_internal_fetch_script(url, "get_audio_individualAudio_func")
        self.exec_javascript(script)
