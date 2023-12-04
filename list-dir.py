#!/usr/bin/env/python3
import os, sys, re
from samba.netcmd import ntacl

# https://itconnect.uw.edu/tools-services-support/it-systems-infrastructure/msinf/other-help/understanding-sddl-syntax/


#walk_dir = sys.argv[1]
root_dir = '/shares/corporate/BEA_2'

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(root_dir))

#export_file = os.path.join(os.path.abspath(walk_dir), 'results.txt')
export_file = '/shares/corporate/results.txt'

def sidtoname(sid):
    if sid == 'DA':
        return 'Domain admins'
    elif sid == 'DU':
        return 'Domain users'
    elif sid == 'WD':
        return 'Tout le monde'
    elif sid == 'CO':
        return 'UTILISATEUR CREATEUR'
    elif sid == 'CG':
        return 'GROUPE CREATEUR'
    return os.popen('wbinfo -s %s' % sid).read().replace('\n', '')

class Output:
    def __init__(self, file):
        self.file = file;

    def open(self, mode = 'a'):
        return open(self.file, mode)

    def truncate(self):
        handle = self.open()
        handle.truncate(0)
        handle.close()

    def write(self, string):
        handle = self.open()
        handle.write(string)
        handle.close()

    def writelines(self, lines):
        handle = self.open()
        handle.writelines(lines)
        handle.close()

class ACL:
    def __init__(self, acl):
        self.acl = acl
        self.struct = self.acl.split(';')
        self.sid = self.struct[-1]
        self.name = sidtoname(self.sid)

    def heritage(self):
        return self.struct[1].find('ID') != -1

    def toString(self):
        return ';'.join(self.struct) + ' = ' + self.name

class ACLs:
    def __init__(self, dossier):
        # Lecture des ACL sur le dossier
        self.sddl = os.popen("samba-tool ntacl get \"%s\" --as-sddl" % dossier).readlines()[-1].split(':')
        self.acls = []
        for acl in re.finditer(r'\(([^\(\)]+)\)', self.sddl[3]):
            self.acls.append(ACL(acl.group(1)))

    def droitsSpecifiques(self):
        for acl in self.acls:
            if acl.heritage() == False:
                return True
        # Pas de droits spécifiques et l'héritage est activé
        return False

    def heritage(self):
        return self.sddl[3][0] != 'P'

    def toString(self):
        output = []
        for acl in self.acls:
            output.append(acl.toString())
        return '\n'.join(output)

class Dossier:
    def __init__(self, dossier):
        self.dossier = dossier

        # Lecture des droits
        self.acls = ACLs(self.dossier)

    def toString(self):
        if self.acls.heritage() == False:
            return '\n'.join([self.dossier + ' HERITAGE DESACTIVE', self.acls.toString(), '\n', '\n'])
        elif self.acls.droitsSpecifiques():
            return '\n'.join([self.dossier + ' DROITS SPECIFIQUES', self.acls.toString(), '\n', '\n'])
        return '\n'.join([self.dossier, self.acls.toString(), '\n', '\n'])

# Vidage du fichier de sortie
output = Output(export_file)
output.truncate()

for root, subdirs, files in os.walk(root_dir):
    dossierRoot = Dossier(root)

    for subdir in subdirs:
        pwdSubdir = os.path.join(root, subdir)

        # Lecture des ACL sur le sous-dossier
        sousDossier = Dossier(pwdSubdir)

        if sousDossier.acls.droitsSpecifiques() == True :
            # Des droits spécifiques ont été appliqués au dossier
            output.writelines(sousDossier.toString())