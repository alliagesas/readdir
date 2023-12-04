# Exemple:
# REVISION:1
# CONTROL:SR|PD|SI|DI|DP
# OWNER:PINGAT\Administrator
# GROUP:PINGAT\Domain Admins
# ACL:PINGAT\Domain Admins:ALLOWED/OI|CI/FULL
# ACL:PINGAT\Marseille_BE_Production:ALLOWED/OI|CI/FULL

import os
from .ace import ACE

class ACL:
    def __init__(self, path):
        # Liste des droits
        self.aces = []
        # Créateur et groupe
        self.owner = self.group = self.control = None
        #print(path)
        # Lecture des ACLs
        acls = self._read_acl(path)
        for acl in acls:
            acl_split = acl.split(':')
            if acl_split[0] == 'OWNER':
                # OWNER
                self.owner = acl_split[1]

            elif acl_split[0] == 'GROUP':
                # GROUP
                self.group = acl_split[1]

            if acl_split[0] == 'CONTROL':
                # CONTROL line
                #print('CONTROL = ' + acl_split[1])
                self.control = acl_split[1].split('|')

            elif acl_split[0] == 'ACL':
                # ACE line
                #print('ACL = ' + acl)
                self.aces.append(ACE(acl))

    # True si l'héritage des droits est activé
    def heritage(self):
        #print(self.control)
        return not('PD' in self.control)

    # True si des droits spécifiques sont appliqués sur le fichier/dossier
    def specifiques(self):
        for ace in self.aces:
            if ace.specifique():
                return True
        return False

    def __str__(self):
        string = 'CONTROL = ' + '|'.join(self.control)
        for ace in self.aces:
            string += "\n" + 'ACL = ' + str(ace)
        return string


    def _read_acl(self, path):
        from readdir import args
        path = path.replace('\\', '/')
        path_split = [e for e in path.split('/') if e]
        server = path_split[0]
        share = path_split[1]
        share_path = "/".join(path_split[2:]) if len(path_split) > 2 else ''
        user = ''
        if len(args.username) > 0:
            user += ' -U'
            if len(args.domain) > 0:
                user += args.domain + '\\\\' + args.username
            else:
                user += args.username
            if len(args.password) > 0:
                user += '%' + args.password
        command = "smbcacls \"//%s/%s\" \"/%s\" %s" % (server, share, share_path, user)
        #print(command)
        return os.popen(command).read().split('\n') or exit('Unable to exec ' + command)