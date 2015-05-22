# import string,cgi,time
# from os import curdir, sep
import java_exports
import json
import time
import urllib
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

HOST = 'kibana.topicusonderwijs.nl'
EXTERNAL_PORT = 443
LOCAL_PORT = 8888
BASEDIR = '/ekspor/backend'
BASE_URL = 'https://{host}:{port}{basedir}'.format(host=HOST,port=EXTERNAL_PORT,basedir=BASEDIR)

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            starttime = time.time()
            urlparts = urlparse.urlparse(self.path)
            clz = tuple(c for c in urllib.unquote(urlparts.path).replace('/','.').split('.') if c)
            if clz==('favicon','ico'):
                raise IOError

            query = urlparse.parse_qs(urllib.unquote(urlparts.query))
            view = query.get('view',[None])[0]
            content_type = 'text/html' if view=='html' else 'application/json'
            collectsize = query.get('collectsize',[None])[0]
            to = query.get('to',[None])[0]
            print('clz={clz}'.format(clz=clz))
            print('query={query}'.format(query=query))

            if to is None:
                wholetree = MyHandler.tree
            else:
                filtered = {}
                for k,v in MyHandler.exports_tup.iteritems():
                    fv = set((clz for clz in v if clz.startswith(to)))
                    if fv:
                        filtered[k]=fv
                wholetree = java_exports.construct_annotated_tree(filtered)

#            try:
            if len(clz)>0 and clz[-1].startswith("<"):
                realclz = clz[:-1]
                maxsize = int(clz[-1][1:])
                realclz, subtree = java_exports.lookup(realclz, wholetree)
                subtree = java_exports.filter_smallsize(subtree,maxsize)
            else:
                realclz, subtree = java_exports.lookup(clz, wholetree)

            exports = java_exports.get_leaf_exports(subtree)
            exports_dummydict = {}
            for e in exports:
                exports_dummydict[tuple(e.split('.'))]=['']
            exports_tree = java_exports.construct_annotated_tree(exports_dummydict)

            if collectsize:
                if collectsize[-1]=='%':
                    smallsize = int(subtree['size'] * float(collectsize[:-1])/100)
                else:
                    smallsize = int(collectsize)
                subtree = java_exports.collect_smallsize(subtree,smallsize)
                exports_tree = java_exports.collect_smallsize(exports_tree,smallsize)
            self.send_response(200)
            self.send_header('Content-type',content_type)
            self.send_header('Access-Control-Allow-Origin','*')
            self.end_headers()

            if content_type=='application/json':
                treemap = java_exports.to_treemap(subtree,realclz)
                treemap['exports_tree'] = java_exports.to_treemap(exports_tree)
                self.wfile.write(json.dumps(treemap,indent=2))
            else:
                self.wfile.write(MyHandler.tree_to_html(realclz,subtree))
#            except KeyError:
#                self.send_error(404)
            print('  {:.0f} ms'.format((time.time()-starttime)*1000))

            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    @staticmethod
    def tree_to_html(clz,tree):
        items = ['<li><a href="{docroot}/{clzpath}.{key}?view=html">{key}</a></li>'.format(docroot=BASE_URL,clzpath='.'.join(clz),key='.'.join(k))
                    for k in tree.keys() if type(k) is tuple]
        exports = ['<li>{clz}</li>'.format(clz=clz) for clz in tree.get((),[])]
        attrs = {k:v for k,v in tree.iteritems() if type(k) is str}
        return '''
        <html><body>
        <div>{attr_json}</div>
        <div>Exports:<ul>
        {exports}
        </div></ul>
        <div>Children:<ul>
            {items}
        </ul></div>
        </body>
        </html>
        '''.format(
            items='\n'.join(items),
            attr_json = json.dumps(attrs,indent=2),
            exports = '\n'.join(exports) )





def main():
    try:
        MyHandler.exports_tup = java_exports.read_flat()
        MyHandler.tree = java_exports.construct_annotated_tree(MyHandler.exports_tup)
        server = HTTPServer(('', LOCAL_PORT), MyHandler)
        print 'serving HTTP on port {port}...'.format(port=LOCAL_PORT)
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
