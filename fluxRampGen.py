

class fluxRampGenerator:


    def __init__(self,roach_,chanzer_):
        self.roach=roach_
        self.chanzer = chanzer_


    ##
    # aamp from 0.0 to 1.0. Best to keep from 0 to 0.5
    # freq in Hz
    def setRamp(self,aamp, freq):
        f=freq
        perd = 128e6/f
        amp = aamp*65536
        adder = amp/ perd
        dc = 32000 - (amp/2)
        self.roach.write_int('RampGenerator_maxramp',amp*65536.0)
        self.roach.write_int('RampGenerator_rampadder',adder*65536)
        self.roach.write_int('RampGenerator_dcoffset',dc)



    ##
    # true for internal ramp gen. falst for ext ramp gen.
    def setSyncSource(self,syncbit):
    
        self.chanzer.setSyncSource(syncbit)
        
    ##
    # use sync or not in data capure.
    #     
    def setIsSync(self,issync):
        self.chanzer.setIsSync(issync)
       
        
        
        
    ##
    #assume ramp is running, measure ramp pulse freq.
    # turn on chanzer look for sync.
    # set fifo length to correct length for current syn puylse freq. or ramnp freq
    
    def setChannelizerFifoSync(self):
        
        if self.chanzer.b_is_look_sync:

            sync_rate = self.chanzer.getSyncRate()
            if sync_rate<1.0:
                print "ERROR - No Sync signal!!"
                self.chanzer.setReadFifoSize(100)
                self.chanzer.setIsSync(0)
                return
                
            #sync_rate
            self.chanzer.setIsSync(1)
            
            
            seglen = floor(1e6 / sync_rate) - 4
            self.chanzer.setReadFifoSize(seglen)
            print 'Sync/Ramp Freq %f Hz'%sync_rate
            print 'Segment Size %d samples'%seglen
            #seglen
            #self.chanzer.setReadFifoSize(55)
        else:
            print 'Not using sync/fluxramp in data capture'
            self.chanzer.setReadFifoSize(100)

print "Loaded fluxRampGen.py"