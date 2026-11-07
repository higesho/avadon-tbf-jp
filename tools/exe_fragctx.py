"""Describe how Avadon.exe assembles messages from string fragments (for the translators).

usage:
    python -I exe_fragctx.py Avadon.exe EXE_STRINGS_TSV OUT_JSON

The message helpers 0x46ddb0 / 0x46de30 print
    [ebp+8] + ecx + edx + esi + (bx >= 0 ? number(bx) : "") + [ebp+0xc]
(sprintf "%s%s%s%s%d%s"). For every call, the values loaded into those registers and
pushed as the two stack arguments in the preceding instructions are resolved to string
literals where possible, giving e.g.  "You get " + <x> + " coins."
For other calls (sprintf etc.) the string literals pushed before the call are listed.
Writes {va: ["description", ...]} for every string va in the tsv that takes part.
"""
import json
import re
import sys

import capstone
import pefile

sys.stdout.reconfigure(encoding='utf-8')
CONCAT = {0x46ddb0: 'message', 0x46de30: 'message'}
REGS32 = {'ecx', 'edx', 'esi', 'ebx', 'eax', 'edi'}


def main(argv):
    exe, tsv, out = argv
    rows = [l.split('\t') for l in open(tsv, encoding='utf-8').read().split('\n')[1:] if l.strip()]
    strings = {int(r[0], 16): r[3] for r in rows}
    pe = pefile.PE(exe, fast_load=True)
    base = pe.OPTIONAL_HEADER.ImageBase
    img = pe.get_memory_mapped_image()
    text = [s for s in pe.sections if s.Name.startswith(b'.text')][0]
    t0 = base + text.VirtualAddress
    code = img[text.VirtualAddress:text.VirtualAddress + text.Misc_VirtualSize]
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    md.detail = True
    insns, off = [], 0
    while off < len(code):
        got = False
        for ins in md.disasm(code[off:off + 32], t0 + off, 1):
            insns.append(ins)
            off += ins.size
            got = True
        if not got:
            off += 1

    def lit(v):
        if v in strings:
            return "'%s'" % strings[v]
        if v is not None and 0x5a5d80 <= v < 0x5b06f8:  # format strings and other game texts not in the tsv
            o = v - base
            b = img[o:img.find(b'\0', o, o + 200)]
            if b and all(32 <= c < 127 for c in b):
                return "'%s'" % b.decode('ascii')
            if not b:
                return "''"
        return None

    ctx = {}

    def add(va, desc):
        lst = ctx.setdefault('0x%06x' % va, [])
        if desc not in lst and len(lst) < 6:
            lst.append(desc)

    for i, ins in enumerate(insns):
        if ins.mnemonic != 'call' or ins.operands[0].type != capstone.x86.X86_OP_IMM:
            continue
        tgt = ins.operands[0].imm & 0xffffffff
        regs, pushes, used = {}, [], []
        for j in range(i - 1, max(i - 30, 0), -1):
            c = insns[j]
            if c.mnemonic in ('call', 'ret', 'jmp') or c.mnemonic.startswith('j'):
                break
            ops = c.operands
            if c.mnemonic == 'push':
                v = ops[0].imm & 0xffffffff if ops[0].type == capstone.x86.X86_OP_IMM else None
                pushes.append(lit(v) if v is not None and lit(v) else '<%s>' % c.op_str)
                if v in strings:
                    used.append(v)
            elif c.mnemonic == 'mov' and len(ops) == 2 and ops[0].type == capstone.x86.X86_OP_REG:
                r = c.reg_name(ops[0].reg)
                if r in REGS32 and r not in regs:
                    v = ops[1].imm & 0xffffffff if ops[1].type == capstone.x86.X86_OP_IMM else None
                    regs[r] = lit(v) if v is not None and lit(v) else '<%s>' % c.op_str.split(', ', 1)[1]
                    if v in strings:
                        used.append(v)
            elif c.mnemonic == 'lea' and len(ops) == 2 and ops[0].type == capstone.x86.X86_OP_REG:
                r = c.reg_name(ops[0].reg)
                if r not in regs:
                    regs[r] = '<buffer>'
        if not used:
            continue
        if tgt in CONCAT:
            a8 = pushes[0] if len(pushes) > 0 else '<?>'
            ac = pushes[1] if len(pushes) > 1 else '<?>'
            parts = [a8, regs.get('ecx', '<?>'), regs.get('edx', '<?>'), regs.get('esi', '<?>')]
            num = regs.get('ebx')
            if num is None or not num.startswith('<0xffff'):
                parts.append('<number>')
            parts.append(ac)
            parts = [p for p in parts if p not in ("''",)]
            desc = 'message: ' + ' + '.join(parts)
        else:
            desc = 'call %06x(%s)%s' % (tgt, ', '.join(reversed(pushes)),
                                         ''.join(' %s=%s' % (r, v) for r, v in sorted(regs.items()) if v.startswith("'")))
        for v in used:
            add(v, desc)
    json.dump(ctx, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
    print(len(ctx), 'strings with context')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
