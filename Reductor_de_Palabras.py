import subprocess
import tempfile
import os

def reduce_word_kbmag(word: str) -> str:
    expr_gap = "*".join(list(word)) if word else "One(F)"

    gap_code = f'''
LoadPackage("kbmag");

F := FreeGroup("a","b","c");;
a := F.1;;
b := F.2;;
c := F.3;;

G := F / [ a^2, b^2, c^2, (a*b)^3, (b*c)^3, (a*c)^2 ];;
rws := KBMAGRewritingSystem(G);;
ok := KnuthBendix(rws);

if ok <> true then
    Print("ERROR_KB\\n");
else
    w := {expr_gap};
    Print(ReducedWord(rws, w), "\\n");
fi;

QUIT;
'''

    with tempfile.NamedTemporaryFile(mode="w", suffix=".g", delete=False) as f:
        f.write(gap_code)
        gap_file = f.name

    try:
        result = subprocess.run(
            ["gap", "-q", gap_file],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr)
        return result.stdout.strip()
    finally:
        os.remove(gap_file)

# Ejemplo
print(reduce_word_kbmag("ababc"))
print(reduce_word_kbmag("abacbab"))