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

"""V3"""
from api.v3.getFiles import iGetFiles
from api.v3.getFolderId import iGetFolderId
from api.v3.searchFile import iSearchFile
from api.v3.dowFile import iParse
from api.v3.dowFile import iParse301

"""index"""
from api.index import indexA
from api.index import indexB
from api.index import indexC
from api.index import indexD
from api.index import indexE
from api.index import indexF
from api.index import index404
from api.index import page_not_found

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=3307)
    server = pywsgi.WSGIServer(('0.0.0.0', 3307), app)
    print("Server started")
    server.serve_forever()