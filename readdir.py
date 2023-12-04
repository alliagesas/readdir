#!/bin/env python3

# https://itconnect.uw.edu/tools-services-support/it-systems-infrastructure/msinf/other-help/understanding-sddl-syntax/
# https://github.com/An0ther0ne/SSDL_Utils
# https://gist.github.com/jborean93/a3cb93fa6237012ebf587e1fbe8fc903
# https://www.samba.org/samba/docs/current/man-html/smbcacls.1.html

# Requirements
# apt install python3-pip -y
# python3 -m pip install smbprotocol

from fs.listdir import smb_listdir
import argparse
import output

parser = argparse.ArgumentParser(description='Rercherche des dossiers aux droits spécifiques')
parser.add_argument('partage', type=str, help='Chemin UNC du dossier ou partage à analyser')
parser.add_argument('-d', '--domain', dest='domain', default='PINGAT', help='Nom du domaine AD')
parser.add_argument('-u', '--username', dest='username', default='administrator', help='Nom d\'utilisateur')
parser.add_argument('-p', '--password', dest='password', default='', help='Mot de passe')
parser.add_argument('-r', '--recurse', dest='recurse', action='store_true', help='Récursif, parcourir les dossiers ET les sous-dossiers.')
parser.add_argument('-o', '--output', dest='output', default='output.txt', help='Chemin vers le fichier de sortie (TXT)')
args = parser.parse_args()

# Vidage du fichier de sortie
output = output.Output(args.output)
output.truncate()

def main():
    print('Parcours du dossier : ' + args.partage)
    smb_listdir(args.partage, recurse=args.recurse)

if __name__ == '__main__':
    main()
