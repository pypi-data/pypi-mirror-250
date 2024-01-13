# global ONE_LETTER
# global TWO_LETTER
# global FULL_NAME
import sys
from apalib.Data import data as data
global FLAGS
FLAGS = {}


class DNA:
    def __init__(self, seqNum=None, atoms=None, resName=None, set_name=True, chainID=None):
        # self.seqNum = number
        # self.atoms = atoms
        # self.resName = name
        self.SetResName(resName, set_name)
        self.SetSeqNum(seqNum)
        self.SetAtoms(atoms)
        self.SetChainID(chainID)

    def DeepCopy(self):
        return DNA(seqNum=self.seqNum,
                   atoms=self.atoms,
                   resName=self.resName,
                   set_name=True)

    def AddAttribute(self, attr, var):
        self.__dict__[attr] = var

    def SetSeqNum(self, num):
        self.seqNum = num

    def SetAtoms(self, atoms):
        self.atoms = atoms
        # self.CalculateCentroid(atoms)

    def GetAtoms(self):
        return self.atoms

    def CalculateCentroid(self):
        if 'atoms' not in self.__dict__:
            self.centroid = None
            return
        # TODO Deal with non-1 occupancy
        residue = data.Map('DNA Nucleotides', self.resName)
        if residue in data.GetJson()['DNA Nucleotides'].keys():
            # If residue is not specified
            x_coord = 0
            y_coord = 0
            z_coord = 0
            num_atoms = 0
            for atom in [atom for atom in self.atoms if
                         atom.name in data.GetJson()['DNA Nucleotides'][residue]['Centroid']]:
                if atom.element == 'H':
                    continue
                x_coord += atom.GetCoordinates()[0]
                y_coord += atom.GetCoordinates()[1]
                z_coord += atom.GetCoordinates()[2]
                num_atoms += 1
            self.centroid = list()
            try:
                self.centroid.append(x_coord / num_atoms)
                self.centroid.append(y_coord / num_atoms)
                self.centroid.append(z_coord / num_atoms)
            except ZeroDivisionError:
                self.centroid.clear()
                beta = [atom for atom in self.atoms if atom.name == 'CB']
                alpha = [atom for atom in self.atoms if atom.name == 'CA']
                if len(beta) != 0:
                    self.centroid.append(beta[0].coordinates[0])
                    self.centroid.append(beta[0].coordinates[1])
                    self.centroid.append(beta[0].coordinates[2])
                    self.RaiseFlag('B_CENTROID')
                elif len(alpha) != 0:
                    self.centroid.append(alpha[0].coordinates[0])
                    self.centroid.append(alpha[0].coordinates[1])
                    self.centroid.append(alpha[0].coordinates[2])
                    self.RaiseFlag('A_CENTROID')
                else:
                    self.centroid = None
                    self.vector = None
                    self.RaiseFlag('BAD_CENTROID')
                    return
            # After all that, set the centroidal vector
            self.vector = [self.centroid[0] - self.GetCA().GetCoordinates()[0],
                           self.centroid[1] - self.GetCA().GetCoordinates()[1],
                           self.centroid[2] - self.GetCA().GetCoordinates()[2]]

        elif len(self.resName) == 4 and self.resName[1:] in data.GetJson()['Amino Acids'][residue]['Centroid']:
            sys.stderr.write("ROTAMER!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        else:
            sys.exit("UNKNOWN DNA RESIDUE YO. DO SOMETHING ABOUT THIS!!!!!")

    def GetCA(self):
        if self.atoms is None:
            return None
        for atom in self.atoms:
            if 'C1' in atom.GetName():
                return atom
        return None

    def InsertAtom(self, atom):
        if self.atoms is None:
            self.atoms = list()
        self.atoms.append(atom)

    def SetResName(self, name, set_name):
        if not set_name:
            self.resName = name
            self.RaiseFlag('NO_NAME_CHECK')
            return
        else:
            self.CheckFlag('NO_NAME_CHECK')
        if data.ValidateDNA(name):
            self.resName = data.SetDNAName(name)
        # elif name in self.FULL_NAME:
        #     self.resName = self.FULL_NAME[name]
        # elif name in self.ONE_LETTER:
        #     self.resName = 'D' + name
        else:
            self.resName = None
            self.RaiseFlag('BAD_NAME')
            return
        self.CheckFlag('BAD_NAME')
        return

    def GetResName(self):
        return self.resName

    def SetChainID(self, c):
        self.chainID = c

    def WriteForPDB(self):
        retstr = ""
        for atom in self.atoms:
            retstr += atom.WritePDB(intro="ATOM  ")
        return retstr


    @staticmethod
    def CheckFlag(f):
        global FLAGS
        if f in FLAGS:
            return FLAGS[f]
        return False

    @staticmethod
    def RaiseFlag(flag):
        global FLAGS
        FLAGS[flag] = True

    @staticmethod
    def ClearFlag(flag):
        global FLAGS
        FLAGS[flag] = False

    def __lt__(self, other):
        return self.seqNum < other.number

    def __repr__(self):
        return f"RESIDUE: {self.resName}, NUMBER: {self.seqNum}"

    def __str__(self):
        return f"{self.resName} {self.seqNum}"


global ONE_LETTER
ONE_LETTER = {
    'A': 'ADENINE',
    'C': 'CYTOSINE',
    'G': 'GUANINE',
    'T': 'THYMINE',
    'U': 'URACIL',
    'I': 'INOSINE'
}
global TWO_LETTER
TWO_LETTER = {
    'DA': 'ADENINE',
    'DC': 'CYTOSINE',
    'DG': 'GUANINE',
    'DT': 'THYMINE',
    'DU': 'URACIL',
    'DI': 'INOSINE'
}
global FULL_NAME
FULL_NAME = {
    'ADENINE': 'DA',
    'CYTOSINE': 'DC',
    'GUANINE': 'DG',
    'THYMINE': 'DT',
    'URACIL': 'DU',
    'INOSINE': 'DI'
}
