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
IMPORTS = \
    [ { 'path':'/Users/sandr/work/eduarte', 'url':'https://github.com/topicusonderwijs/eduarte/tree/master' }
    , { 'path':'/Users/sandr/work/digdag',  'url':'https://github.com/topicusonderwijs/digdag/tree/master'  }
    , { 'path':'/Users/sandr/work/iridium', 'url':'https://github.com/topicusonderwijs/iridium/tree/master' }
    , { 'path':'/Users/sandr/work/heimdall', 'url':'https://github.com/topicusonderwijs/heimdall/tree/master' }
    ]
SRC_REGEX = '.*/src/main/java/.*\.java$'
