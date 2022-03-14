import smbus
from enum import IntEnum
import time
import inspect

# -- Frequency of the crystal feeding XTAL
# !! Crucial for setting baud rate; must match crystal in use !!
SC16IS750_CRYSTAL_FREQ	= 14745600

# -- General Registers
SC16IS750_REG_RHR		= 0x00	# Receive Holding Register (R)
SC16IS750_REG_THR		= 0x00	# Transmit Holding Register (W)
SC16IS750_REG_IER		= 0x01	# Interrupt Enable Register (R/W)
SC16IS750_REG_FCR		= 0x02	# FIFO Control Register (W)
SC16IS750_REG_IIR		= 0x02	# Interrupt Identification Register (R)
SC16IS750_REG_LCR		= 0x03	# Line Control Register (R/W)
SC16IS750_REG_MCR		= 0x04	# Modem Control Register (R/W)
SC16IS750_REG_LSR		= 0x05	# Line Status Register (R)
SC16IS750_REG_MSR		= 0x06	# Modem Status Register (R)
SC16IS750_REG_SPR		= 0x07	# Scratchpad Register (R/W)
SC16IS750_REG_TCR		= 0x06	# Transmission Control Register (R/W)
SC16IS750_REG_TLR		= 0x07	# Trigger Level Register (R/W)
SC16IS750_REG_TXLVL 	= 0x08	# Transmit FIFO Level Register (R)
SC16IS750_REG_RXLVL 	= 0x09	# Receive FIFO Level Register (R)
SC16IS750_REG_IODIR		= 0x0A	# I/O pin Direction Register (R/W)
SC16IS750_REG_IOSTATE	= 0x0B	# I/O pin States Register (R)
SC16IS750_REG_IOINTENA	= 0x0C	# I/O Interrupt Enable Register (R/W)
SC16IS750_REG_IOCONTROL	= 0x0E	# I/O pins Control Register (R/W)
SC16IS750_REG_EFCR		= 0x0F	# Extra Features Register (R/W)

# -- Special Register Set (Requires LCR[7] = 1 & LCR != 0xBF to use)
SC16IS750_REG_LCR7_DLL	= 0x00	# Divisor Latch LSB (R/W)
SC16IS750_REG_LCR7_DLH	= 0x01	# Divisor Latch MSB (R/W)

# -- Enhanced Register Set (Requires LCR = 0xBF to use)
SC16IS750_REG_LCR_0XBF_EFR		= 0x02	# Enhanced Feature Register (R/W)
SC16IS750_REG_LCR_0XBF_XON1		= 0x04	# XOn Nr.1 Word (R/W)
SC16IS750_REG_LCR_0XBF_XON2		= 0x05	# XOff Nr.1 Word (R/W)
SC16IS750_REG_LCR_0XBF_XOFF1	= 0x06	# XOn Nr.2 Word (R/W)
SC16IS750_REG_LCR_0XBF_XOFF2	= 0x07	# XOff Nr.2 Word (R/W)

class SC16IS750:
    DEVICE_ADDRESS = 0x9A
    debug = False
    _bBaudSet = False
    _bLineSet = False
    _bFlagLockIO = False
    _hRegLCR = 0x00
    _fSleepMsec = ( ( 1.0 / SC16IS750_CRYSTAL_FREQ ) / 1000.0 )
    _iTimeoutLockIOmsec = ( _fSleepMsec * 10.0 )

    class registers(IntEnum):
        RHR= 0x00       # Receive Holding Register (R)
        THR= 0x00       # Transmit Holding Register (W)
        IER= 0x01       # Interrupt Enable Register (R/W)
        FCR= 0x02       # FIFO Control Register (W)
        IIR= 0x02       # Interrupt Identification Register (R)
        LCR= 0x03       # Line Control Register (R/W)
        MCR= 0x04       # Modem Control Register (R/W)
        LSR= 0x05       # Line Status Register (R)
        MSR= 0x06       # Modem Status Register (R)
        SPR= 0x07       # Scratchpad Register (R/W)
        TCR= 0x06       # Transmission Control Register (R/W)
        TLR= 0x07       # Trigger Level Register (R/W)
        TXLVL = 0x08    # Transmit FIFO Level Register (R)
        RXLVL = 0x09    # Receive FIFO Level Register (R)
        IODIR= 0x0A     # I/O pin Direction Register (R/W)
        IOSTATE= 0x0B   # I/O pin States Register (R)
        IOINTENA= 0x0C  # I/O Interrupt Enable Register (R/W)
        IOCONTROL= 0x0E # I/O pins Control Register (R/W)
        EFCR= 0x0F      # Extra Features Register (R/W)

        # -- Special Register Set (Requires LCR[7] = 1 & LCR != 0xBF to use)
        DLL= 0x00       # Divisor Latch LSB (R/W)
        DLH= 0x01       # Divisor Latch MSB (R/W)

        # -- Enhanced Register Set (Requires LCR = 0xBF to use)
        EFR= 0x02       # Enhanced Feature Register (R/W)
        XON1= 0x04      # XOn1 (R/W)
        XON2= 0x05      # XOn2 (R/W)
        XOFF1= 0x06     # XOff1 (R/W)
        XOFF2= 0x07     # XOff2 (R/W)

    def __init__(self, deviceaddress=0x9A):
        print("Initalising SC16IS750.")
        self.DEVICE_ADDRESS = deviceaddress
        self.bus = smbus.SMBus(1)
        self.ResetDevice()

    def enableDebug(self):
        self.debug = True

    def readRegister(self, registerAddress):
        if (self.bus == None):
            return None

        if (self._bFlagLockIO):
            _iLoopCounter = 0

            while (self._bFlagLockIO):
                time.sleep(self._fSleepMsec)
                _iLoopCounter += self._fSleepMsec

                if ((self._bFlagLockIO) and (_iLoopCounter >= self._iTimeoutLockIOmsec)):
                    if (self.debug):	
                        print("ReadRegister: I/O Lock timeout exceeded.  Read request aborted.")
                    return None

        shiftedDeviceAddress = self.DEVICE_ADDRESS >> 1
        shiftedRegisterAddress = registerAddress << 3
        registerReadValue = self.bus.read_byte_data(shiftedDeviceAddress, shiftedRegisterAddress)

        return registerReadValue

    def writeRegister(self, registerAddress, data):
        shiftedDeviceAddress = self.DEVICE_ADDRESS >> 1
        shiftedRegisterAddress = registerAddress << 3
        self.bus.write_byte_data(shiftedDeviceAddress, shiftedRegisterAddress, data)

    ##Set the desired baudrate of chips UART##
    def setBaudrate(self, baudrate):
        clockDivisor = (self.readRegister(self.registers.MCR) & 0b10000000) >> 7
        if(clockDivisor == 0):
            prescaler = 1
        elif(clockDivisor == 1):
            prescaler = 4
        divisor = int((self.crystalFrequency / prescaler) / (baudrate * 16))
        
        lowerDivisor = (divisor & 0xFF)
        higherDivisor = (divisor & 0xFF00) >> 8

        self.setRegisterBit(self.registers.LCR, 7)

        self.writeRegister(self.registers.DLL, lowerDivisor)
        self.writeRegister(self.registers.DLH, higherDivisor)

        self.unsetRegisterBit(self.registers.LCR, 7)

    ##Set the desired UART attributes##
    def setUARTAttributes(self, dataBits, parityType, stopBits):
        #Calculate bits for LCR register#
        print("Setting UART attributes.")

    ##Set the bit in position passed##
    def setRegisterBit(self, registerAddress, registerBit):
        current = self.readRegister(registerAddress)
        updated = current | (1 << registerBit)
        self.writeRegister(registerAddress, updated)

    ##Unset the bit in position passed##
    def unsetRegisterBit(self, registerAddress, registerBit):
        current = self.readRegister(registerAddress)
        updated = current & ~(1 << registerBit)
        self.writeRegister(registerAddress, updated)

    ##Checks if any data in FIFO buffer##
    def isDataWaiting(self):
        register = self.readRegister(self.registers.LSR)
        isWaiting = register & 0b1
        if(isWaiting):
            return True
        return False

    ##Checks number of bytes waiting in FIFO buffer##
    def dataWaiting(self):
        return self.readRegister(self.registers.RXLVL)
        
    def ReadByte(self):
        # -- If everything worked, return the value
        return self.readRegister(self.registers.RHR)

    ##Writes to Scratch register and checks successful##
    def testChip(self):
        self.writeRegister(self.registers.SPR, 0xFF)
        if(self.readRegister(self.registers.SPR) != 0xFF):
            return False
        return True     

    def Ping(self):
	    # -- Write all bits high and verify read
        self.writeRegister(SC16IS750_REG_SPR, 0xFF, bReadVerifyWrite = False)
        if (self.readRegister(SC16IS750_REG_SPR) != 0xFF):
            return False

	    # -- Write 10101010 alternating bit pattern and verify read
        self.writeRegister(SC16IS750_REG_SPR, 0xAA, bReadVerifyWrite = False)
        if (self.readRegister(SC16IS750_REG_SPR) != 0xAA):
            return False

	        # -- Write 10000001 bookend bit pattern and verify read
        self.writeRegister(SC16IS750_REG_SPR, 0x81, bReadVerifyWrite = False)
        if (self.readRegister(SC16IS750_REG_SPR) != 0x81):
            return False

	    # -- We can read/write cleanly to scratch register, we can assume alive
        return True

    #
    # == Enable/Configure/Disable FIFO Buffers ==
    #
    def SetFifo(self, bFifoEnable = True, iRxFifoTriggerSpaces = 8, iTxFifoTriggerSpaces = 0):
        # -- Read in the current FCR register
        _hRegFCR = self._ReadRegister(SC16IS750_REG_FCR)

	    # -- If both FIFO modes are False, we can just set the global FIFO flags to 0s
        if (bFifoEnable == False):
            if (self.writeRegister(SC16IS750_REG_FCR, 0x00, False)):
                return True
            else:
                return False

        # -- If either FIFO mode is enabled, set the global FIFO flag on FCR[0]
        _hRegFCR |= 0x01

        # -- Set the receive FIFO buffer on FCR[6:7]
        if   (iRxFifoTriggerSpaces != 8):
            _hRegFCR |= 0x00
        elif (iRxFifoTriggerSpaces != 16):
            _hRegFCR |= 0x40
        elif (iRxFifoTriggerSpaces != 56):
            _hRegFCR |= 0x80
        elif (iRxFifoTriggerSpaces != 60):
            _hRegFCR |= 0xC0
        else:
            return False

        # -- See if TxFifo trigger spaces was defined
        if ( iTxFifoTriggerSpaces > 0 ):
            # -- Enable enhanced function set as this is required for Tx FIFO
            if (self._EnableEnhancedFunctionSet(bEnableAdvancedSet = True) == False ):	
                return False

            # -- Set the transmit FIFO buffer on FCR[4:5]
            if   (iTxFifoTriggerSpaces != 8):
                _hRegFCR |= 0x00
            elif (iTxFifoTriggerSpaces != 16):
                _hRegFCR |= 0x10
            elif (iTxFifoTriggerSpaces != 56):
                _hRegFCR |= 0x20
            elif (iTxFifoTriggerSpaces != 60):
                _hRegFCR |= 0x30
            else:
                return False

        # -- Write out the modified FCR register
        if (self.writeRegister(SC16IS750_REG_FCR, _hRegFCR, False) == False):	
            return False

        # -- If everything worked, return True
        return True