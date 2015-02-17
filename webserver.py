# import string,cgi,time
# from os import curdir, sep
import java_exports
import json
import time
import urllib
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

HOST = 'localhost'
PORT = 8888
BASE_URL = 'http://{host}:{port}'.format(host=HOST,port=PORT)

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            starttime = time.time()
            urlparts = urlparse.urlparse(self.path)
            clz = tuple(c for c in urllib.unquote(urlparts.path).replace('/','.').split('.') if c)
            query = urlparse.parse_qs(urllib.unquote(urlparts.query))
            view = query.get('view',[None])[0]
            collectsize = query.get('collectsize',[None])[0]
            content_type = 'text/html' if view=='html' else 'application/json'
            print('clz={clz}'.format(clz=clz))
            print('query={query}'.format(query=query))
#            try:
            if len(clz)>0 and clz[-1].startswith("<"):
                realclz = clz[:-1]
                maxsize = int(clz[-1][1:])
                subtree = java_exports.filter_smallsize(java_exports.lookup(realclz, MyHandler.tree),maxsize)
            else:
                realclz = clz
                subtree = java_exports.lookup(realclz, MyHandler.tree)
            if collectsize:
                if collectsize[-1]=='%':
                    smallsize = int(subtree['size'] * float(collectsize[:-1])/100)
                else:
                    smallsize = int(collectsize)
                subtree = java_exports.collect_smallsize(subtree,smallsize)
            exports = java_exports.get_leaf_exports(subtree)
            exports_dummydict = {}
            for e in exports:
                exports_dummydict[tuple(e.split('.'))]=['']
            exports_tree = java_exports.ann_size(java_exports.treeify_simple(exports_dummydict))
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
        MyHandler.tree = java_exports.construct_annotated_tree()
        server = HTTPServer(('', PORT), MyHandler)
        print 'serving HTTP on port {port}...'.format(port=PORT)
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()

if __name__ == '__main__':
    main()
