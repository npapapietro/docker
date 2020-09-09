import os
import subprocess
import sys

_PYTHON_VERSIONS_ = ["3.6", "3.7", "3.8"]

_TAGS = [
    ("Dockerfile", "basecuda"),
    ("Dockerfile.cuda", "cuda"),
    ("Dockerfile.nightly", "rustnightly"),
    ("Dockerfile.stable", "rust"),
    ("Dockerfile.cuda.stable", "cudarust")
]

cwd = os.path.abspath(os.path.dirname(__file__))

for py in _PYTHON_VERSIONS_:
    dirname = os.path.join(cwd, f"Python{py}")
    for dockerimage, tag in _TAGS:
        tag = "npapapietro/pythonbundles:py" + py.replace('.','') + tag
        
        dockerfile = os.path.join(dirname, dockerimage)
        if not os.path.isfile(dockerfile):
            continue
        
        cmd = [
            "docker", "build",
            "-t", tag,
            "-f", dockerfile,
            "."
        ]
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, b''):
            sys.stdout.write(line.decode('utf-8'))
        p.wait()
        
        cmd = [
            "docker", "push", tag
        ]
        p = subprocess.Popen(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        for line in iter(p.stdout.readline, b''):
            sys.stdout.write(line.decode('utf-8'))
        p.wait()
        print("\n")
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("Finished with", tag)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("\n")
