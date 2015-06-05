# config file for local usage.
# in docker container, this is replaced by config-docker.py

# webserver
HOST = 'localhost'
EXTERNAL_PORT = 8888
LOCAL_PORT = 8888
BASEDIR = ''
BASE_URL = 'http://{host}:{port}{basedir}'.format(host=HOST,port=EXTERNAL_PORT,basedir=BASEDIR)

# java_exports
EXPORTS_DIR = '/Users/sandr/work/cobra'
IMPORTS_DIRS = ['/Users/sandr/work/eduarte','/Users/sandr/work/digdag','/Users/sandr/work/iridium']
SRC_REGEX = '.*/src/main/java/.*\.java$'
