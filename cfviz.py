#!/usr/bin/env python

import json
from numbers import Number
import sys
from compiler.ast import flatten

def main():
    if sys.argv[1:2] != []:
        with open(sys.argv[1]) as h:
            template = json.load(h)
    else:
        template = json.load(sys.stdin)

    (graph, edges) = extract_graph(template['Description'], template['Resources'])
    graph['edges'].extend(edges)
    handle_terminals(template, graph, 'Parameters', 'source')
    handle_terminals(template, graph, 'Outputs', 'sink')

    render(graph)

def handle_terminals(template, graph, name, rank):
    if name in template:
        (subgraph, edges) = extract_graph(name, template[name])
        subgraph['rank'] = rank
        subgraph['style'] = 'filled,rounded'
        graph['subgraphs'].append(subgraph)
        graph['edges'].extend(edges)

def extract_graph(name, elem):
    graph = {'name': name, 'nodes': [], 'edges': [], 'subgraphs': []}
    edges = []
    for item, details in elem.iteritems():
        graph['nodes'].append({'name': item})
        edges.extend(flatten(find_refs(item, details)))
    return (graph, edges)

def find_refs(context, elem):
    if isinstance(elem, dict):
        refs = []
        for k, v in elem.iteritems():
            if unicode(k) == unicode('Ref'):
                assert isinstance(v, basestring), 'Expected a string: %s' % v
                refs.append({'from': v, 'to': context})
            elif unicode(k) == unicode('Fn::GetAtt'):
                assert isinstance(v, list), 'Expected a list: %s' % v
                refs.append({'from': v[0], 'to': context})
            else:
                refs.extend(find_refs(context, v))
        return refs
    elif isinstance(elem, list):
        return map(lambda e: find_refs(context, e), elem)
    elif isinstance(elem, basestring):
        return []
    elif isinstance(elem, bool):
        return []
    elif isinstance(elem, Number):
        return []
    else:
        raise AssertionError('Unexpected type: %s' % elem)

def render(graph, subgraph=False):
    print '%s "%s" {' % ('subgraph' if subgraph else 'digraph', graph['name'])
    print 'labeljust=l;'
    print 'node [shape=box];'
    if 'style' in graph:
        print 'node [style="%s"]' % graph['style']
    if 'rank' in graph:
        print 'rank=%s' % graph['rank']
    for n in graph['nodes']:
        print '"%s"' % n['name']
    for s in graph['subgraphs']:
        render(s, True)
    for e in graph['edges']:
        print '"%s" -> "%s";' % (e['from'], e['to'])
    print '}'

def debug(*s):
    print >>sys.stderr, s

if __name__ == '__main__':
    main()
