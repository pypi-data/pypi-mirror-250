from multiprocessing import Process, Queue, Event
from time import time, sleep
from .urlOpen import myURLopen
from .ERR import ConnError, PermissionsError
from ._import_module import *


class Screen(Process):
    def __init__(self, server_url="http://127.0.0.1:8020/?code="):
        super().__init__()
        self.__min_x = 0
        self.__max_x = 1088
        self.__min_y = 0
        self.__max_y = 2333
        self.__url = f"{server_url}cupter"
        self.__Q = Queue(1)
        self.__isStart = Event()
        self.__isRun = Event()
        self.__get = Event()
        self.__bk = Event()
        self.daemon = True
        self.__test()
        self.start()
        self.__img_init()

    def __test(self):
        if isinstance(ret := myURLopen(self.__url), ConnectionRefusedError):
            raise ConnError(ret)
        ret = myURLopen(self.__url, ret=True)
        print(len(ret))
        if len(ret) <= 40:
            raise PermissionsError

    def __set_xy(self, a, b, c):
        for i in a:
            if i == 0:
                b += c
            elif i == 255:
                break
        return b

    def __img_init(self):
        img = self.get()
        y, x = img.shape[:2]
        x_line = img[:, :, 3][y // 2 : y // 2 + 1, :][0].tolist()
        y_line = img[:, :, 3][:, x // 2 : x // 2 + 1].reshape(1, -1)[0].tolist()
        self.__min_x = self.__set_xy(x_line, self.__min_x, 1)
        self.__max_x = self.__set_xy(x_line[::-1], self.__max_x, -1)
        self.__min_y = self.__set_xy(y_line, self.__min_y, 1)
        self.__max_y = self.__set_xy(y_line[::-1], self.__max_y, -1)

    def __while_run(self):
        T1 = time()
        while not self.__bk.is_set():
            T2 = time() - T1
            if T2 > 15:
                sleep(1)
            elif T2 > 300:
                sleep(5)
            ret = myURLopen(self.__url, ret=True)
            if not ret:
                continue
            if self.__get.is_set():
                img = cv.imdecode(np.frombuffer(ret, np.uint8), cv.IMREAD_UNCHANGED)
                if img is None:
                    continue
                self.__Q.put(img)
                self.__get.clear()
                T1 = time()

    def run(self):
        if self.__isRun.is_set():
            assert False, f"module '{__class__.__name__}' has no attribute 'run'"
        self.__isRun.set()
        self.__while_run()

    def get(self, func=None, *args, **kwargs):
        self.__get.set()
        img = self.__Q.get()[self.__min_y : self.__max_y, self.__min_x : self.__max_x]
        return img if func is None else func(img, *args, **kwargs)

    def DEL(self):
        self.__bk.set()

    def start(self):
        if self.__isStart.is_set():
            assert False, f"module '{__class__.__name__}' has no attribute 'start'"
        self.__isStart.set()
        super().start()

    def join(self):
        super().join(0.1)
        if self.is_alive():
            assert False, f"module '{__class__.__name__}' has no attribute 'join'"

    def terminate(self):
        assert False, f"module '{__class__.__name__}' has no attribute 'terminate'"
