from os import path, listdir

path_xwt_libs = path.abspath(path.dirname(__file__))

libs = {}

if path.exists(path_xwt_libs):
    for lib in listdir(path_xwt_libs):
        _path = path.join(path_xwt_libs, lib)
        if path.isfile(_path):
            if path.splitext(_path)[1] == ".dll":  # 判断文件扩展名是否为“.dll”
                libs[lib] = _path