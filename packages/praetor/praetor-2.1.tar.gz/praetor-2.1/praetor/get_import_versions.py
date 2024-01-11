import subprocess

import praetor_settings

if praetor_settings.dynamic_file_dir != '':
    import sys
    sys.path.append(praetor_settings.dynamic_file_dir)
import python_modules


def get_agent_string():
    versions = []
    procPy = subprocess.Popen(['python','--version'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    pythonVersion = procPy.stderr.read()
    loc = 'Python '
    pyVer = pythonVersion[pythonVersion.find(loc)+len(loc):]
    pyVer = pyVer.strip()
    pyVer = ''.join(e for e in pyVer if e.isalnum() or e == '.' or e == '-')

    reload(python_modules) # Do I need this ???

    for mod in python_modules.modules:
        proc1 = subprocess.Popen(['pip','show',mod],stdout=subprocess.PIPE)
        proc2 = subprocess.Popen(['grep','Version'],stdin=proc1.stdout,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        proc1.stdout.close()

        out, err = proc2.communicate()
        versions.append(out)

    versions = [x.replace('\n','') for x in versions]
    versions = [x[x.find(': ')+2:] for x in versions]

    modString = ["exe:{}='u2p:{}'".format(x,y) for x,y in zip(python_modules.modules,versions)]
    modString.insert(0,"exe:python='u2p:{}'".format(pyVer))

    agentString = ', '.join(modString)

    return agentString
