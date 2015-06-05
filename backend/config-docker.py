# webserver
HOST = 'kibana.topicusonderwijs.nl'
EXTERNAL_PORT = 443
LOCAL_PORT = 8888
BASEDIR = '/ekspor/backend'
BASE_URL = 'https://{host}:{port}{basedir}'.format(host=HOST,port=EXTERNAL_PORT,basedir=BASEDIR)

# java_exports
EXPORTS_DIR = '/repos/cobra'
IMPORTS_DIRS = ['/repos/eduarte','/repos/digdag','repos/iridium']
SRC_REGEX = '.*/src/main/java/.*\.java$'
