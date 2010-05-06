from VerilogSim import VerilogSim

class IcarusVerilog(VerilogSim):
    """
    Defaults:
        TIMESCALE   : 1ns / 10ps
        OUTFILE     : sim
        DUMPFILE    : dump.vcd
        WARN        : all
    """
    def __init__(self, cfg):
        VerilogSim.__init__(self, cfg)
        self.cfg = cfg
        self.compCmd = ['iverilog']
        self.simCmd = ['./sim']
        self.plusargs = None
#        self.flags = {}

        ## Default flags specific to Icarus Verilog
        ## and any required list comprehension commands
        self['warn'] = ['-Wall']
        self['outfile'] = ['-osim']
        ## List comprehension functions for specific flags
        self.flag_cmds['warn'] = lambda x: self._prepend('-W', x)
        self.flag_cmds['outfile'] = lambda x: self._prepend('-o', x)

        ## Run the populate method to do the cfg conversion
        self.populate()

        self.buildCompCmd()
        self.buildSimCmd()
        self.cmds = [self.compCmd, self.simCmd]

    def buildCompCmd(self):
        self.compCmd =  ['iverilog'] +  \
                        self['warn'] +  \
                        self['outfile'] + \
                        self['defines'] + \
                        self['rtl_inc_dirs'] + \
                        self['test_inc_dirs'] + \
                        self['rtl_files'] + \
                        self['test_files'] + \
                        self['plusargs']

    def buildSimCmd(self):
        self.simCmd = self.cfg['outfile']
#        print "IcarusVerilog Simulation"
#        for i,f in self.sim_flags:
#            if(i in self.data and not None):
#                if(f is not None):
#                    flag = f(self[i])
#                    self.simCmd += flag

#        self.simCmd = [self.outfile, self.plusargs]

        ## Remove all None items from the list
#        for i in range(self.compCmd.count(None)): 
#            self.compCmd.remove(None)
#        for i in range(self.simCmd.count(None)): 
#            self.simCmd.remove(None)
                    
#                    '-W%s' % self.warn,
#                    '-o%s' % self.outfile,
#                   ] #\
                    #+ self.prepend('-D', self.defines) \
                    #+ self.prepend('-I' + rel_proj_root + "/", inc_dirs) \
                    #+ self.prepend(rel_proj_root + "/", src_files)

