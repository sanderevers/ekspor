#!/usr/bin/python

import subprocess
import json

EXPORTS_DIR = '/repos/cobra'
IMPORTS_DIRS = ['/repos/eduarte','/repos/digdag','repos/iridium']
SRC_REGEX = '.*/src/main/java/.*\.java$'

def fetch_export_filenames():
    return subprocess.check_output(['find',EXPORTS_DIR,'-regex',SRC_REGEX]).splitlines()

def fetch_import_filenames():
    filenames = []
    for dir in IMPORTS_DIRS:
        filenames.extend(subprocess.check_output(['find',dir,'-regex',SRC_REGEX]).splitlines())
    return filenames

def class_from_filename(filename):
    with_slashes = filename.split('/src/main/java/')[-1]
    without_extension = with_slashes[0:with_slashes.rindex('.'):]
    with_dots = without_extension.replace('/','.')
    return with_dots

# TODO support wildcard imports / implicit package imports
def classes_from_file(text):
    imports = filter(lambda s: s.startswith('import '), text.splitlines())
    classes = [c[len('import '):-1] for c in imports]
    return set(classes)

# a TREE consists of:
# - a set of BRANCHES (which are trees themselves) named by tuples of strings
#   whose (tuple) prefixes do not overlap
# - a LEAF (optional if there are branches) under the empty tuple
# - a dict string -> arbitrary value

def branches(t):
    return dict((k,v) for (k,v) in t.iteritems() if type(k) is tuple and len(k)>0)

NoLeaf = object()
def leaf(t):
    try:
        return t[()]
    except KeyError:
        return NoLeaf

def anns(t):
    return dict((k,v) for (k,v) in t.iteritems() if not type(k) is tuple)

def tree(branches,leaf=NoLeaf,anns={}):
    ret = {}
    assert all(type(k) is tuple and len(k)>0 for k in branches.keys())
    ret.update(branches)
    assert all(not type(k) is tuple for k in anns.keys())
    ret.update(anns)
    if not leaf is NoLeaf:
        ret[()] = leaf
    return ret

def hasleaf(t):
    return () in t

def treeify_simple(flat):
    tree = {}
    for k,v in flat.iteritems():
        if k: # skip empty tuple here
            firstlettermap = tree[k[0]] = tree.get(k[0],{})
            firstlettermap[tuple(k[1:])] = v
    ttree={}
    for k,firstlettermap in tree.iteritems():
        ttree[tuple([k])] = treeify_simple(firstlettermap)
    if () in flat:
        ttree[()] = flat[()]
    return ttree

def ann_size(tree):
    cumsize = 0
    for k,v in tree.iteritems():
        if k==():
            cumsize += len(v)
        elif type(k) is tuple:
            ann_size(v)
            cumsize += v['size']
    tree['size'] = cumsize
    if () in tree:
        tree['$size'] = len(tree[()])
    return tree

def filter_smallsize(t,maxsize):
    newbr = dict((k,v) for (k,v) in branches(t).iteritems() if anns(v)['size']<maxsize)
    newanns = dict(anns(t))
    newanns['size']=sum(anns(v)['size'] for (k,v) in newbr.iteritems())
    return tree(newbr,leaf(t),newanns)


def collect_smallsize(t, minsize):
    branchname = ('<'+str(minsize),)
    newbr = {}
    for k,v in branches(t).iteritems():
        branchsize = anns(v)['size']
        if branchsize < minsize:
            newbr[branchname]=newbr.get(branchname,tree({},leaf=[],anns={'$size':0}))
            newbr[branchname]['$size'] += branchsize
        else:
            newbr[k] = collect_smallsize(v,minsize)
    return tree(newbr,leaf(t),anns(t))


def collapse_minsize(tree, minsize):
    ctree = {}
    for k,v in tree.iteritems():
        if k==():
            ctree[k] = v
        elif type(k) is str:
            ctree[k] = v
        elif v['size']<minsize:
            ctree[k] = {():None, '$size':v['size']}
        else:
            ctree[k] = collapse_minsize(v, minsize)
    return ctree

def concat_paths(t):
    k,v = _concat_paths(t)
    if k==():
        return v
    else:
        return tree({k:v}, leaf(t), anns(t))

def _concat_paths(t):
    br = branches(t)
    if len(br)==1 and not hasleaf(t):
        myk = br.keys()[0]
        brk, brv = _concat_paths(br.values()[0])
        return myk+brk, brv
    else:
        updated_branches = {}
        for k,v in br.iteritems():
            brk,brv = _concat_paths(v)
            updated_branches[k+brk] = brv
        return (),tree(updated_branches, leaf(t), anns(t))

# maakt paden van max 2 lang...
'''
def concat_paths(t):
    def update_branch(k,v):
        branches_v = branches(v)
        if len(branches_v)==1 and not(hasleaf(v)):
            branchname = branches_v.keys()[0]
            subtree = branches_v.values()[0]
            return k+branchname,concat_paths(subtree)
        else:
            return k,concat_paths(v)
    updated_branches = dict(update_branch(k,v) for (k,v) in branches(t).iteritems())
    return tree(updated_branches, leaf(t), anns(t))
'''
'''
def aggregate_paths(t):
    br = branches(t)
    if len(br)==1 and not(hasleaf(t)):
        newbr = {}
        prefix = br.keys()[0]
        subt = br.values()[0]
        for k,v in branches(subt).iteritems():
            newbr[prefix+k] = aggregate_paths(v)
        newanns = {}
        newanns.update(anns(t))
        newanns.update(anns(subt))
        return tree(newbr,leaf(subt),newanns)
    else:
        newbr = {}
        for k,v in br.iteritems():
            newbr[k] = aggregate_paths(v)
        return tree(newbr, leaf(t), anns(t))



def aggregate_paths(tree):
    atree = {}
    if len(tree)==1 and tree.keys()[0] != ():
        prefix = tree.keys()[0]
        for k,v in tree.values()[0].iteritems():
            if k==() or type(k) is str:
                atree[k] = v
            else:
                atree[tuple(list(prefix)+list(k))] = aggregate_paths(v)
    else:
        for k,v in tree.iteritems():
            if k==() or type(k) is str:
                atree[k] = v
            else:
                atree[k] = aggregate_paths(v)
    return atree
'''

def lookup(path, t):
    if len(path)==0:
        return path,t
    br = branches(t)
    for k,v in br.iteritems():
        if k[:1]==path[:1]:
            pathend = path[len(k):]
            pathend,subtree = lookup(pathend, v)
            return k+pathend,subtree
#    for i in range(1,len(path)+1):
#        if path[:i] in br:
#            return lookup(path[i:],br[path[:i]])
    raise KeyError()

def get_leaf_exports(t):
    exports = set()
    if hasleaf(t):
        exports.update(leaf(t))
    for v in branches(t).itervalues():
        exports.update(get_leaf_exports(v))
    return exports

def common_prefix(*strings):
    prefix = strings[0]
    for s in strings[1:]:
#        if not s.startswith(prefix):  # for performance
            prefix = tuple(iter_prefix(prefix,s))
    return prefix


def iter_prefix(s1,s2):
    for c1,c2 in zip(s1,s2):
        if c1==c2:
            yield c1
        else:
            return

def to_treemap(tree,rootpath=()):
#    if len(branches(tree))==1:
#        return _to_treemap(tree,rootpath)[0]
#    else:
        return {'name':'^', 'path':'.'.join(rootpath), 'children':_to_treemap(tree,rootpath)}

def _to_treemap(tree,stack):
    children = []
    for k,v in tree.iteritems():
        if type(k) is str:
            pass
        elif k==():
            children.append({'name':'$', 'size':tree['$size'], 'path':'.'.join(stack)+'$', 'exports':list(v)})
        elif len(branches(v))==0:
            children.append({'name':'.'.join(k), 'size':anns(v)['$size'], 'path':'.'.join(stack+k), 'exports':list(leaf(v))})
        else:
            vchildren = _to_treemap(v,stack+k)
            children.append({'name':'.'.join(k), 'path':'.'.join(stack+k), 'children': vchildren})
    return children

def read_flat():
    import_filenames = fetch_import_filenames()
    imports = {}
    for filename in import_filenames:
        with open(filename) as f:
            clazz = class_from_filename(filename)
            if clazz in imports:
                print 'WARNING: duplicate class in imports: '+clazz
            imports[clazz] = classes_from_file(f.read())

    export_filenames = fetch_export_filenames()
    exports = {}
    for filename in export_filenames:
        clazz = class_from_filename(filename)
        if clazz in exports:
            print 'WARNING: duplicate class in exports: '+clazz
        exports[clazz] = set()

    for clazz, imp_classes in imports.items():
        for imp_class in imp_classes:
            try:
                exports[imp_class].add(clazz)
            except KeyError:
                pass

    exports_tup = {}
    for name,ex in exports.iteritems():
        exports_tup[tuple(name.split('.'))] = ex

    return exports_tup

def construct_annotated_tree(exports_tup):
    tree = treeify_simple(exports_tup)
    ctree = concat_paths(tree)
    atree = ann_size(ctree)
    return atree


def main():
    exports_tup = read_flat()
    atree = construct_annotated_tree(exports_tup)
    ctree = collapse_minsize(atree,atree['size']/40)
    treemap = to_treemap(ctree)

    with open('exports.json','w') as f:
        f.write(json.dumps(treemap,indent=2))

    return atree, ctree
