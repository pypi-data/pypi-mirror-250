from .urlOpen import myURLopen


def sim_tap(x, y, server_url="http://127.0.0.1:8020/?code="):
    return myURLopen(f"{server_url}0,{x},{y}", ret=True)


def sim_swipe(x1, y1, x2, y2, t=1000, server_url="http://127.0.0.1:8020/?code="):
    return myURLopen(f"{server_url}1,{x1},{y1},{x2},{y2},{t}", ret=True)


def sim_screenshot():
    return myURLopen(f"{server_url}2,", ret=True)


def sim_home(server_url="http://127.0.0.1:8020/?code="):
    return myURLopen(f"{server_url}HOME,", ret=True)


def sim_back(server_url="http://127.0.0.1:8020/?code="):
    return myURLopen(f"{server_url}BACK,", ret=True)


def sim_lockscreen(server_url="http://127.0.0.1:8020/?code="):
    return myURLopen(f"{server_url}Lock,", ret=True)


def OpenApp(pkg, cls, server_url="http://127.0.0.1:8020/?code="):
    return myURLopen(f"{server_url}openapk,{pkg},{cls},", ret=True)
