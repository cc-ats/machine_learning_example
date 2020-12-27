class QChemInpFile(object):
    def __init__(self, arrays=[]):
        self.list_of_arrays=[]
        self.list_of_content=[]
        self.runinfo=_rundata()
        self.__jtype="undef"
        for k in arrays:
            self.add(k)

    def add(self,new_array):
        ''' Adds an array to your inputfile object.'''
        if type(new_array) == type(rem_array()):
            self.rem = new_array
            if "rem" in self.list_of_content:
                index = self.list_of_content.index("rem")
                self.list_of_arrays[index]=new_array
            else:
                self.list_of_content.append("rem")
                self.list_of_arrays.append(new_array)
            self._jtype = new_array.jobtype() #rem variable "jobtype" defines type

        elif type(new_array) == type(mol_array()):
            self.molecule = new_array
            if "molecule" in self.list_of_content:
                index = self.list_of_content.index("molecule")
                self.list_of_arrays[index]=new_array
            else:
                self.list_of_content.append("molecule")
                self.list_of_arrays.append(new_array)

        elif type(new_array) == type(comment_array()):
            self.list_of_content.append("comment")
            self.list_of_arrays.append(new_array)

        elif type(new_array) == type(basis_array()):
            self.basis = new_array
            if "basis" in self.list_of_content:
                index = self.list_of_content.index("basis")
                self.list_of_arrays[index]=new_array
            else:
                self.list_of_content.append("basis")
                self.list_of_arrays.append(new_array)

        elif type(new_array) == type(ecp_array()):
            self.ecp = new_array
            if "ecp" in self.list_of_content:
                index = self.list_of_content.index("ecp")
                self.list_of_arrays[index]=new_array
            else:
                self.list_of_content.append("ecp")
                self.list_of_arrays.append(new_array)

        elif type(new_array) == type(_unsupported_array()):
            self.list_of_content.append(str(new_array.type))
            self.list_of_arrays.append(new_array)

        #poor man's typecasting because these feel equivalent to users
        elif (type(new_array) == cartesian  or type(new_array)== zmat or type(new_array) == tinker):
            self.add(mol_array(new_array))

        else:
            print("Array type unknown.")

    def remove(self,position=0): #if not specified delete last
        ''' Removes an array from your inputfile object. If no other specified the last is removed.'''
        del self.list_of_content[position-1]
        del self.list_of_arrays[position-1]

    def __str__(self):
        ret_str = ""
        for k in self.list_of_arrays:
            ret_str += k.__str__() + "\n"
        return ret_str

    def write(self,filename):
        f = open(filename,'w')
        str_ret = self.__str__()
        print(str_ret, file=f)
        f.close()

    def info(self):
        '''A quick overview of your inputfile.''' # Health check could be put here
        if "rem" and "molecule" in self.list_of_content:
            status = "valid"
        else:
            status = "invalid"

        print("Type: inputfile")
        print("Status: " + status)

    def run(self,name='',loc53='',qchem='',nt=1,np=1,timestamp=False):
        '''Makes Q-Chem process the given batch inputfile object. Optional parameters are

        name  ...... filename (without file extension, will be \".in\" and \".out\" by default)
        loc53 ...... 53.0 file location
        nt ......... number of threads
        np ......... number of processors.
        timestamp... adds a timestamp to input and output if set True.

        If nothing specified, pyQChem will fall back on information in the corresponding runinfo object.'''

        running_scripts._run(self,name,loc53,qchem,nt,np,timestamp)

    def __add__(self,other):
        #autoadd subarrays - works
        import copy
        new=copy.deepcopy(self)
        new.add(other)
        return new