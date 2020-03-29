#!/usr/bin/env python

import sys
import json
import yaml
import datetime
import collections
from numbers import Number


def flatten(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, dict):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


def main():
    template = open_cfn(sys.argv)

    (graph, edges) = extract_graph(template.get('Description', ''), template['Resources'])
    graph['edges'].extend(edges)
    handle_terminals(template, graph, 'Parameters', 'source')
    handle_terminals(template, graph, 'Outputs', 'sink')
    graph['subgraphs'].append(handle_psuedo_params(graph['edges']))

    render(graph)


def open_cfn(argv):
    if argv[1:2] != []:
        input_filename = argv[1]
        with open(input_filename) as h:
            if any(extension in input_filename for extension in ['.yml', '.yaml']):
                text = h.read()
                # the !syntax doesn't parse in python's yaml library, and we're not reading to that depth
                cfn_intrinsic_functions = ['!GetAtt', '!Ref', '!Sub']
                for f in cfn_intrinsic_functions:
                    text = text.replace(f,' ')
                template = yaml.load(text)
            else:
                template = json.load(h)
    else:
        template = json.load(sys.stdin)
    return template


def handle_terminals(template, graph, name, rank):
    if name in template:
        (subgraph, edges) = extract_graph(name, template[name])
        subgraph['rank'] = rank
        subgraph['style'] = 'filled,rounded'
        graph['subgraphs'].append(subgraph)
        graph['edges'].extend(edges)


def handle_psuedo_params(edges):
    graph = {'name': 'Psuedo Parameters', 'nodes': [], 'edges': [], 'subgraphs': []}
    graph['shape'] = 'ellipse'
    params = set()
    for e in edges:
        if e['from'].startswith(u'AWS::'):
            params.add(e['from'])
    graph['nodes'].extend({'name': n} for n in params)
    return graph


def extract_graph(name, elem):
    graph = {'name': name, 'nodes': [], 'edges': [], 'subgraphs': []}
    edges = []
    for item, details in elem.items():
        graph['nodes'].append({'name': item})
        edges.extend(flatten(find_refs(item, details)))
    return (graph, edges)


def find_refs(context, elem):
    if isinstance(elem, dict):
        refs = []
        for k, v in elem.items():
            if k == 'Ref':
                assert isinstance(v, str), 'Expected a string: %s' % v
                refs.append({'from': v, 'to': context})
            elif k == 'Fn::GetAtt':
                assert isinstance(v, list), 'Expected a list: %s' % v
                refs.append({'from': v[0], 'to': context})
            else:
                refs.extend(find_refs(context, v))
        return refs
    elif isinstance(elem, list):
        return map(lambda e: find_refs(context, e), elem)
    elif isinstance(elem, str):
        return []
    elif isinstance(elem, bool):
        return []
    elif isinstance(elem, Number):
        return []
    elif isinstance(elem, datetime.date):
        return []
    else:
        raise AssertionError('Unexpected type: %s' % elem)


def render(graph, subgraph=False):
    print('%s "%s" {' % ('subgraph' if subgraph else 'digraph', graph['name']))
    print('labeljust=l;')
    print('node [shape={}];'.format(graph.get('shape', 'box')))
    if 'style' in graph:
        print('node [style="%s"]' % graph['style'])
    if 'rank' in graph:
        print('rank=%s' % graph['rank'])
    for n in graph['nodes']:
        print('"%s"' % n['name'])
    for s in graph['subgraphs']:
        render(s, True)
    for e in graph['edges']:
        print('"%s" -> "%s";' % (e['from'], e['to']))
    print('}')


def debug(*s):
    print(sys.stderr, s)


if __name__ == '__main__':
    main()
