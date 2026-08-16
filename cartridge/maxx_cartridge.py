#!/usr/bin/env python3
"""MAXX Cartridge reference CLI: portable, offline-first, stdlib only."""
from __future__ import annotations
import argparse, hashlib, json, os, platform, shutil, sys, time
from pathlib import Path

VERSION="0.1.0"
REQUIRED=["00_SYSTEM","01_IDENTITY","02_MEMORY","03_SKILLS","04_WORK","05_PROJECTS","06_USER_DATA","07_MODELS","08_SYNC/incoming","08_SYNC/outgoing","08_SYNC/conflicts","08_SYNC/journal","09_HOSTS","99_RECOVERY/snapshots"]

def ts(): return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
def atomic(path,text):
    path.parent.mkdir(parents=True,exist_ok=True); tmp=path.with_suffix(path.suffix+".tmp"); tmp.write_text(text,encoding="utf-8"); os.replace(tmp,path)
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()
def host():
    android=bool(os.environ.get("ANDROID_ROOT") or os.environ.get("TERMUX_VERSION"))
    return {"os":"android" if android else platform.system().lower(),"machine":platform.machine().lower(),"python":platform.python_version(),"termux":bool(os.environ.get("TERMUX_VERSION"))}
def init(root,agent,medium):
    root.mkdir(parents=True,exist_ok=True)
    for d in REQUIRED:(root/d).mkdir(parents=True,exist_ok=True)
    m={"schema":"maxx-cartridge","version":VERSION,"agent":agent,"medium":medium,"created_at":ts(),"source_of_truth":"cartridge","sync":{"mode":"offline-first","conflict_policy":"never-overwrite-silently"}}
    atomic(root/"cartridge.json",json.dumps(m,indent=2)+"\n")
    atomic(root/"CONTEXT.md",f"# {agent} Cartridge\n\nRead `cartridge.json`, then `00_SYSTEM/CONTEXT.md`. Load only task-relevant context.\n")
    atomic(root/"STATUS.md",f"# Status\n\n- agent: {agent}\n- state: initialized\n- last_updated: {ts()}\n")
    atomic(root/"00_SYSTEM/CONTEXT.md","# System Router\n\nIdentity `../01_IDENTITY/`; memory `../02_MEMORY/`; skills `../03_SKILLS/`; work `../04_WORK/`; projects `../05_PROJECTS/`; user data `../06_USER_DATA/`; models `../07_MODELS/`; sync `../08_SYNC/`; hosts `../09_HOSTS/`; recovery `../99_RECOVERY/`.\n")
    atomic(root/"01_IDENTITY/IDENTITY.md",f"# Agent Identity\n\nname: {agent}\nrole: portable offline-first agent\n")
    for d in ["02_MEMORY","03_SKILLS","04_WORK","05_PROJECTS","06_USER_DATA","07_MODELS","08_SYNC","09_HOSTS","99_RECOVERY"]:
        p=root/d/"CONTEXT.md"
        if not p.exists(): atomic(p,f"# {d} Context\n\nKeep this router small; load child records only when relevant.\n")
    return m
def validate(root):
    e=[]; mp=root/"cartridge.json"
    if not mp.exists():e.append("missing cartridge.json")
    else:
        try:
            if json.loads(mp.read_text()).get("schema")!="maxx-cartridge":e.append("invalid schema")
        except Exception as x:e.append(f"invalid manifest: {x}")
    for d in REQUIRED:
        if not (root/d).is_dir():e.append(f"missing directory: {d}")
    for f in ["CONTEXT.md","STATUS.md","00_SYSTEM/CONTEXT.md","01_IDENTITY/IDENTITY.md"]:
        if not (root/f).is_file():e.append(f"missing file: {f}")
    return not e,e
def manifest(root):
    files=[]
    for p in root.rglob("*"):
        if not p.is_file():continue
        rel=str(p.relative_to(root)).replace(os.sep,"/")
        if rel.startswith("08_SYNC/journal/") or rel.startswith("99_RECOVERY/snapshots/"):continue
        files.append({"path":rel,"size":p.stat().st_size,"sha256":sha(p)})
    files.sort(key=lambda x:x["path"]); canonical=json.dumps(files,sort_keys=True,separators=(",",":")).encode()
    return {"created_at":ts(),"files":files,"tree_sha256":hashlib.sha256(canonical).hexdigest()}
def snapshot(root):
    data=manifest(root); out=root/"99_RECOVERY/snapshots"/f"manifest-{time.strftime('%Y%m%d-%H%M%S',time.gmtime())}.json"; atomic(out,json.dumps(data,indent=2)+"\n"); return out
def journal(root,op,path,details=None):
    p=root/"08_SYNC/journal/events.jsonl"; p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("a",encoding="utf-8") as f:f.write(json.dumps({"ts":ts(),"op":op,"path":path,"details":details or {}},sort_keys=True)+"\n")
    return p
def import_tree(root,source,label):
    if not source.is_dir():raise ValueError("source must be a directory")
    dst=root/"06_USER_DATA/Imports"/label
    if dst.exists():raise FileExistsError(f"import destination exists: {dst}")
    dst.parent.mkdir(parents=True,exist_ok=True); shutil.copytree(source,dst,copy_function=shutil.copy2)
    files=[p for p in dst.rglob("*") if p.is_file()]; size=sum(p.stat().st_size for p in files); journal(root,"import",str(dst.relative_to(root)),{"files":len(files),"bytes":size}); return {"destination":str(dst),"files":len(files),"bytes":size}
def sync_plan(root,previous=None):
    cur=manifest(root); old={}
    if previous: old={x["path"]:x for x in json.loads(previous.read_text()).get("files",[])}
    new={x["path"]:x for x in cur["files"]}; changed=[p for p in new if p not in old or new[p]["sha256"]!=old[p].get("sha256")]; deleted=[p for p in old if p not in new]
    return {"tree_sha256":cur["tree_sha256"],"changed":sorted(changed),"deleted":sorted(deleted)}
def main(argv=None):
    p=argparse.ArgumentParser(prog="maxx-cartridge"); p.add_argument("--root",default="."); s=p.add_subparsers(dest="cmd",required=True)
    a=s.add_parser("init"); a.add_argument("--agent",default="Agent Max"); a.add_argument("--medium",choices=["usb","microsd","folder"],default="folder")
    for n in ["status","validate","snapshot"]:s.add_parser(n)
    a=s.add_parser("import"); a.add_argument("source"); a.add_argument("--label",required=True)
    a=s.add_parser("journal"); a.add_argument("op"); a.add_argument("path")
    a=s.add_parser("sync-plan"); a.add_argument("--previous")
    a=p.parse_args(argv); root=Path(a.root).expanduser().resolve()
    try:
        if a.cmd=="init":print(json.dumps(init(root,a.agent,a.medium),indent=2));return 0
        if a.cmd in ("status","validate"):
            ok,e=validate(root); out={"ok":ok,"errors":e};
            if a.cmd=="status":out.update({"root":str(root),"host":host(),"manifest":json.loads((root/"cartridge.json").read_text()) if ok else None})
            print(json.dumps(out,indent=2));return 0 if ok else 2
        if a.cmd=="snapshot":print(snapshot(root));return 0
        if a.cmd=="import":print(json.dumps(import_tree(root,Path(a.source).expanduser().resolve(),a.label),indent=2));return 0
        if a.cmd=="journal":print(journal(root,a.op,a.path));return 0
        if a.cmd=="sync-plan":print(json.dumps(sync_plan(root,Path(a.previous).expanduser().resolve() if a.previous else None),indent=2));return 0
    except (OSError,ValueError,json.JSONDecodeError) as x:print(f"error: {x}",file=sys.stderr);return 1
    return 1
if __name__=="__main__":raise SystemExit(main())
