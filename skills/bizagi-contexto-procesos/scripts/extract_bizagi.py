"""Read-only Bizagi Modeler XPDL extractor; Python standard library."""
import argparse
import collections
import hashlib
import io
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import zipfile

LIMIT = 64 * 1024 * 1024
GRAPHICS = {'NodeGraphicsInfos', 'ConnectorGraphicsInfos'}
ENTITIES = {'Pool', 'Lane', 'WorkflowProcess', 'ActivitySet', 'Activity',
            'Artifact', 'Participant', 'DataObject', 'DataInput', 'DataOutput'}
EDGES = {'Transition': ('From', 'To'), 'MessageFlow': ('Source', 'Target'),
         'Association': ('Source', 'Target')}

def tag(e):
    return e.tag.rsplit('}', 1)[-1]

def tree(e):
    return {'tag': tag(e), 'attributes': dict(e.attrib),
            'text': (e.text or '').strip(),
            'children': [tree(c) for c in e if tag(c) not in GRAPHICS]}

def xml(data):
    probe = data.replace(b'\x00', b'').upper()
    if len(data) > LIMIT or b'<!DOCTYPE' in probe or b'<!ENTITY' in probe:
        raise ValueError('XML excede límites o contiene DTD/entidades')
    return ET.fromstring(data)

def members(data):
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos = z.infolist()
        if sum(i.file_size for i in infos) > LIMIT or len(infos) > 2000:
            raise ValueError('Contenedor excede límites')
        names = [i.filename for i in infos]
        if len(names) != len(set(names)):
            raise ValueError('Nombres duplicados en contenedor')
        return {i.filename: z.read(i) for i in infos if not i.is_dir()}

def diagram(root, source):
    if tag(root) != 'Package' or 'XPDL' not in root.tag.upper():
        raise ValueError(f'No es un Package XPDL compatible: {source}')
    d = {'id': root.get('Id'), 'name': root.get('Name'), 'source': source,
         'entities': [], 'connections': [], 'subprocess_references': [],
         'unresolved_references': [], 'warnings': [], 'semantic': tree(root)}
    def walk(e, parent=None):
        kind = tag(e)
        if kind in ENTITIES:
            d['entities'].append({'id': e.get('Id'), 'name': e.get('Name', ''),
                'kind': kind, 'parent_id': parent, 'attributes': dict(e.attrib),
                'lane_refs': sorted({v for c in e.iter() for k, v in c.attrib.items()
                                     if k in {'LaneId', 'Lane'}}), 'semantic': tree(e)})
            parent = e.get('Id') or parent
        if kind in EDGES:
            a, b = EDGES[kind]
            d['connections'].append({'id': e.get('Id'), 'name': e.get('Name', ''),
                'kind': kind, 'source': e.get(a), 'target': e.get(b),
                'parent_id': parent, 'semantic': tree(e)})
        if kind in {'SubFlow', 'BlockActivity'}:
            d['subprocess_references'].append({'owner_id': parent, 'kind': kind,
                'target': e.get('Id') if kind == 'SubFlow' else e.get('ActivitySetId')})
        for c in e:
            if tag(c) not in GRAPHICS:
                walk(c, parent)
    walk(root)
    ids = [e['id'] for e in d['entities'] if e['id']]
    duplicates = [k for k, n in collections.Counter(ids).items() if n > 1]
    if duplicates:
        d['warnings'].append({'duplicate_ids': duplicates})
    touched = set()
    for edge in d['connections']:
        for endpoint in ('source', 'target'):
            target = edge[endpoint]
            touched.add(target)
            if target not in ids:
                d['unresolved_references'].append({'edge_id': edge['id'],
                    'endpoint': endpoint, 'target': target})
    d['isolated_activities'] = [e['id'] for e in d['entities']
                              if e['kind'] == 'Activity' and e['id'] not in touched]
    known = ENTITIES | set(EDGES) | {'Package', 'SubFlow', 'BlockActivity'}
    d['uninterpreted_tags'] = sorted({tag(e) for e in root.iter()} - known)
    return d

def extract(path, company=None):
    if path.stat().st_size > LIMIT:
        raise ValueError('Archivo excede límite de lectura')
    data = path.read_bytes()
    result = {'schema_version': 1, 'source': str(path.resolve()),
        'sha256': hashlib.sha256(data).hexdigest(), 'company_user_supplied': company,
        'access_mode': 'local_file', 'warnings': [], 'auxiliary': {}, 'diagrams': []}
    files = members(data) if zipfile.is_zipfile(io.BytesIO(data)) else {path.name: data}
    budget = 0
    for name, content in files.items():
        nested = members(content) if name.lower().endswith('.diag') and zipfile.is_zipfile(io.BytesIO(content)) else {None: content}
        budget += sum(len(b) for b in nested.values())
        if budget > LIMIT:
            raise ValueError('Contenido total excede límite')
        for subname, raw in nested.items():
            source = name + '/' + subname if subname else name
            if source.lower().endswith(('.xml', '.xpdl', '.diag')):
                root = xml(raw)
                if tag(root) == 'Package':
                    result['diagrams'].append(diagram(root, source))
                else:
                    result['auxiliary'][source] = tree(root)
            else:
                result['warnings'].append(f'Archivo auxiliar no interpretado: {source}')
    if not result['diagrams']:
        raise ValueError('No se encontró un diagrama XPDL compatible')
    targets = collections.defaultdict(list)
    for d in result['diagrams']:
        targets[d['id']].append(d['id'])
        for e in d['entities']:
            if e['kind'] in {'WorkflowProcess', 'ActivitySet'}:
                targets[e['id']].append(d['id'])
    for d in result['diagrams']:
        for ref in d['subprocess_references']:
            matches = sorted(set(targets.get(ref['target'], []))) if ref['target'] else []
            ref['target_diagrams'] = matches
            ref['status'] = 'resolved' if len(matches) == 1 else 'ambiguous' if matches else 'unresolved'
            if ref['status'] != 'resolved':
                d['unresolved_references'].append(ref.copy())
    return result

def summary(result):
    lines = ['# Contexto de Bizagi', '', f"Fuente: {result['source']}",
             f"SHA-256: {result['sha256']}",
             f"Empresa indicada: {result['company_user_supplied'] or 'No indicada'}",
             'Acceso local; no se verificó conexión directa con Bizagi.', '']
    for d in result['diagrams']:
        counts = collections.Counter(e['kind'] for e in d['entities'])
        lines += [f"## {d['name']} ({d['id']})", f"Origen: {d['source']}",
                  f'Entidades: {dict(counts)}', f"Conexiones: {len(d['connections'])}",
                  f"Referencias sin resolver o ambiguas: {len(d['unresolved_references'])}",
                  f"Actividades aisladas: {len(d['isolated_activities'])}", '']
        for e in d['entities']:
            if e['kind'] in {'Pool', 'Lane', 'Activity'}:
                name = ' '.join(e['name'].split())
                lines.append(f"- {e['kind']}: {name or '(sin nombre)'} [{e['id']}]")
        if d['unresolved_references']:
            lines += ['', 'Referencias por revisar:', json.dumps(d['unresolved_references'], ensure_ascii=False)]
        lines.append('')
    lines += ['## Límites', 'Asignaciones geométricas a lanes y extensiones requieren revisión.',
              'El árbol semántico conserva campos no normalizados; no es validación BPMN completa.',
              'No se añaden inferencias ni propuestas automáticamente.', '', 'Avisos:',
              *[str(w) for w in result['warnings']]]
    return '\n'.join(lines) + '\n'

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source', type=Path)
    p.add_argument('--company')
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    try:
        result = extract(args.source, args.company)
        args.out.mkdir(parents=True, exist_ok=False)
        (args.out / 'context.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        (args.out / 'resumen.md').write_text(summary(result), encoding='utf-8')
        print(json.dumps({'out': str(args.out.resolve()), 'diagrams': len(result['diagrams']),
                          'warnings': result['warnings']}, ensure_ascii=True))
    except (ValueError, OSError, ET.ParseError, zipfile.BadZipFile) as exc:
        p.exit(1, f'Error: {exc}\n')

if __name__ == '__main__':
    main()
