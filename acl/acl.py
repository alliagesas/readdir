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
        self.path = path
        # Liste des droits
        self.aces = []
        # Créateur et groupe
        self.command = self.owner = self.group = self.control = None
        #print(path)
        # Lecture des ACLs
        self.acls = self._read_acl(self.path)
        for acl in self.acls:
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
        # print(self.control)
        if self.control != None:
            return not('PD' in self.control)
        else:
            print('Erreur de détection de la chaine CONTROLE pour le dossier ' + self.path + "\nACL lues: " + "\n".join(self.acls) + "Command + " + self.command)
            return False

    # True si des droits spécifiques sont appliqués sur le fichier/dossier
    def specifiques(self):
        for ace in self.aces:
            if ace.specifique():
                return True
        return False

    def __str__(self):
        string = ''
        if self.control != None:
            string = 'CONTROL = ' + '|'.join(self.control)
        if self.aces != None:
            for ace in self.aces:
                string += "\n" + 'ACL = ' + str(ace)
        return string


    def _read_acl(self, path):
        from subprocess import run
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
        self.command = "smbcacls \"//%s/%s\" \"/%s\" %s" % (server, share, share_path, user)
        response = run([self.command], capture_output=True, shell=True)
        #p = Popen(self.command, stdout=PIPE, stderr=PIPE, shell=True)
        #stdout, stderr = p.communicate()
        if len(response.stderr) > 0:
           print('Erreur lors de la commande : ' + self.command + "\n" + response.stderr.decode("utf-8"))
        #print(self.command)
        return response.stdout.decode("utf-8").split('\n')
        # result = os.popen(self.command)
        #print(command)
        #return os.popen(self.command).read().split('\n') or print('Unable to exec ' + command)