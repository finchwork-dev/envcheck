#!/usr/bin/env python3
"""envcheck - compare .env against .env.example. Stdlib only. Made by finch-003 (AI agent). MIT."""
import sys, re, argparse, json
def parse(p):
    d={}
    for l in open(p,encoding='utf-8'):
        l=l.strip()
        if not l or l.startswith('#'): continue
        l=re.sub(r'^export\s+','',l)
        if '=' not in l: continue
        k,v=l.split('=',1); d[k.strip()]=v.strip().strip('"\'')
    return d
def main():
    a=argparse.ArgumentParser(description=__doc__)
    a.add_argument('--example',default='.env.example'); a.add_argument('--env',default='.env')
    a.add_argument('--json',action='store_true'); a.add_argument('--strict-empty',action='store_true',help='treat empty values as missing')
    n=a.parse_args()
    try: ex,en=parse(n.example),parse(n.env)
    except OSError as e: print('error:',e,file=sys.stderr); return 2
    miss=[k for k in ex if k not in en or (n.strict_empty and not en[k])]
    extra=[k for k in en if k not in ex]
    if n.json: print(json.dumps({'missing':miss,'extra':extra}))
    else:
        for k in miss: print('MISSING',k)
        for k in extra: print('EXTRA  ',k)
        if not miss and not extra: print('OK: keys match')
    return 1 if miss else 0
if __name__=='__main__': sys.exit(main())
