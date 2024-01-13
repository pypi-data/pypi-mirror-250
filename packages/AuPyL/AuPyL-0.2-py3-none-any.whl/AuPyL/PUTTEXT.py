from time import time
from .urlOpen import myURLopen
from .ERR import ConnError
from .CLEAR import CLEAR_LIST


class PutText(object):
    def __init__(
        self,
        X=0,
        Y=0,
        W=100,
        H=100,
        T="None",
        S=10,
        C=(0, 255, 0),
        server_url="http://127.0.0.1:8020/?code=",
        textType=0,
    ):
        self.__type = ["textview", "edittext"]
        self.__url = server_url
        self.__View = {
            "id": f"PutText_{time()}",
            "type": self.__type[textType],
            "color": [255] + list(C),
            "text": T,
            "Width": W,
            "Height": H,
            "size": S,
            "X": X,
            "Y": Y,
            "operation": None,
            "info": "None",
        }
        if textType == 1:
            self.__View["hint"] = ""
        self.__test()
        CLEAR_LIST.append((self.__url, self.__View))

    @property
    def T(self):
        return self.__View["text"]

    @T.setter
    def T(self, a):
        self.__View["text"] = a

    @property
    def C(self):
        return self.__View["color"]

    @C.setter
    def C(self, a):
        self.__View["color"] = 255, *a

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

    @property
    def S(self):
        return self.__View["size"]

    @S.setter
    def S(self, a):
        self.__View["size"] = a

    def show(self):
        self.__View["operation"] = (
            "newly" if self.__View["operation"] is None else "modify"
        )
        myURLopen(url=self.__url, quote_data=self.__View)

    def DEL(self):
        self.__View["operation"] = "delete"
        myURLopen(url=self.__url, quote_data=self.__View)

    def __test(self):
        if isinstance(
            ret := myURLopen(self.__url.split("/?")[0]), ConnectionRefusedError
        ):
            raise ConnError(ret)

    def __del__(self):
        print(self.__View["id"])
        self.DEL()
