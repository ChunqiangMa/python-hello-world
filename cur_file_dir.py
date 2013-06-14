# 获取当前文件所在文件夹路径.
#
# 通过sys.path[0]判断并返回当前文件所在文件夹路径.
def cur_file_dir():
    path = sys.path[0]
    if os.path.isdir(path):
        return path
    if os.path.isfile(path):
        return os.path.dirname(path)
