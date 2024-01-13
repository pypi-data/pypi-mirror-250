from time import time
from threading import Timer
from base64 import b64encode
from .urlOpen import myURLopen
from .ERR import ConnError
from ._import_module import *
from .CLEAR import CLEAR_LIST


class ShowImg(object):
    def __init__(
        self, X=0, Y=0, W=500, H=500, server_url="http://127.0.0.1:8020/?code="
    ):
        self.__OTime = False
        self.__url = server_url.split("/?")[0]
        self.__View = {
            "id": f"ImgShow_{time()}",
            "type": "imgview",
            "Width": W,
            "Height": H,
            "X": X,
            "Y": Y,
            "operation": "newly",
            "info": "None",
        }
        self.__test()
        CLEAR_LIST.append((self.__url, self.__View))

    @property
    def W(self):
        return self.__View["Width"]

    @W.setter
    def W(self, a):
        self.__View["Width"] = a

    @property
    def H(self):
        return self.__View["Height"]

    @H.setter
    def H(self, a):
        self.__View["Height"] = a

    @property
    def X(self):
        return self.__View["X"]

    @X.setter
    def X(self, a):
        self.__View["X"] = a

    @property
    def Y(self):
        return self.__View["Y"]

    @Y.setter
    def Y(self, a):
        self.__View["Y"] = a

    def show(self, img=None, OutTime=None):
        if self.__OTime:
            self.__View["operation"] = "newly"
            self.__OTime = False
        else:
            self.__View["operation"] = (
                "newly" if "Base64" not in self.__View else "modify"
            )
        self.__setImg(img)
        myURLopen(url=self.__url, data=self.__View)
        if OutTime is not None:
            Timer(OutTime, self.__outtime).start()

    def DEL(self):
        self.__View["operation"] = "delete"
        myURLopen(url=self.__url, data=self.__View)

    def __setImg(self, img):
        if isinstance(img, np.ndarray):
            bin = cv.imencode(".png", img)[1]
        if isinstance(img, str):
            with open(img, "rb") as f:
                bin = f.read()
        elif img is None:
            return
        self.__View["Base64"] = b64encode(bin).decode("utf-8")

    def __outtime(self):
        self.__OTime = True
        self.DEL()

    def __test(self):
        if isinstance(ret := myURLopen(self.__url), ConnectionRefusedError):
            raise ConnError(ret)

    def __del__(self):
        print(self.__View["id"])
        self.DEL()
