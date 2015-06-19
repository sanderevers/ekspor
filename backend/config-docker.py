# webserver
HOST = 'kibana.topicusonderwijs.nl'
EXTERNAL_PORT = 443
LOCAL_PORT = 8888
BASEDIR = '/ekspor/backend'
BASE_URL = 'https://{host}:{port}{basedir}'.format(host=HOST,port=EXTERNAL_PORT,basedir=BASEDIR)

# java_exports
EXPORTS_DIR = '/repos/cobra'
IMPORTS = \
    [ { 'path':'/repos/eduarte', 'url':'https://github.com/topicusonderwijs/eduarte/tree/master' }
    , { 'path':'/repos/digdag',  'url':'https://github.com/topicusonderwijs/digdag/tree/master'  }
    , { 'path':'/repos/iridium', 'url':'https://github.com/topicusonderwijs/iridium/tree/master' }
    , { 'path':'/repos/heimdall','url':'https://github.com/topicusonderwijs/heimdall/tree/master'}
    ]
SRC_REGEX = '.*/src/main/java/.*\.java$'
