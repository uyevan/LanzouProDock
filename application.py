from gevent import pywsgi
from router import app

"""V1"""
from api.v1.allList import getFilesAndDirectories
from api.v1.dowFileById import parseById
from api.v1.dowFileByUrl import parseByUrl
from api.v1.fileList import getFiles
from api.v1.folderList import getDirectory
from api.v1.searchFile import searchFile

"""V2"""
from api.v2.allList import getFilesAndDirectoriesV2
from api.v2.dowFileById import parseByIdV2
from api.v2.dowFileByUrl import parseByUrlV2
from api.v2.fileList import getFilesV2
from api.v2.folderList import getDirectoryV2
from api.v2.searchFile import searchFileV2

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3307)
    server = pywsgi.WSGIServer(('0.0.0.0', 3307), app)
    server.serve_forever()
