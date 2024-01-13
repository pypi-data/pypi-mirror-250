import sys


def hook_err(exc_type, exc_value, traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        from .CLEAR import CLEAR_LIST
        from .urlOpen import myURLopen

        for u, i in CLEAR_LIST:
            if "PutText_" in i["id"] or "Button_" in i["id"]:
                i["operation"] = "delete"
                print(f'\n[url]{u}\t[id]{i["id"]}')
                myURLopen(url=u, quote_data=i)
            elif "ImgShow_" in i["id"]:
                i["operation"] = "delete"
                i["Base64"] = "None"
                print(f'\n[url]{u}\t[id]{i["id"]}')
                myURLopen(url=u, data=i)
        print("\nKeyboardInterrupt\n")
    elif issubclass(exc_type, AssertionError):
        from traceback import format_exception

        formatted_exc = format_exception(exc_type, exc_value, traceback)
        err = ""
        for i in formatted_exc:
            if "assert" in i:
                print(err)
                print(f"AssertionError : {exc_value}")
                return
            else:
                err += i
    else:
        sys.__excepthook__(exc_type, exc_value, traceback)


sys.excepthook = hook_err
