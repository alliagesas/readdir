# See: https://www.samba.org/samba/docs/current/man-html/smbcacls.1.html
class ACE:
    def __init__(self, acl):
        # Ex: ACL:PINGAT\Corporate_BEA:ALLOWED/OI|CI/0x001000a9
        # Ex: ACL:PINGAT\Domain Admins:ALLOWED/OI|CI|I/FULL
        self.acl = acl
        self.struct = self.acl.split(':')
        # User/Group name
        self.name = self.struct[1]
        struct_split = self.struct[2].split('/')
        # Allowed/Denied
        self.type = struct_split[0]
        # Flags
        self.flags = struct_split[1].split('|')
        # Mask
        self.mask = struct_split[2]

    def specifique(self):
        #print(self.flags)
        return not('I' in self.flags)

    def __str__(self):
        return self.acl