#!/bin/python

from .device import MBIODevice
from .xmlconfig import XMLConfig


class MBIODeviceEBM(MBIODevice):
    def onInit(self):
        self._vendor='EBM'
        self._model='BASE'
        # must return FAN address
        self._pingRegisterIndex=0xd100

        self.config.set('enablesource', 'bus')
        self.config.set('speedsource', 'bus')
        self.config.set('controlmode', 'speed')
        self.config.set('rpm', 0)
        self.config.set('maxrpm')
        self.config.set('ramp')
        self.config.set('io1type', 'di')
        self.config.set('io2type', 'ai')
        self.config.set('io3type', 'ao')
        self.config.set('watchdogsource')

        self.speed=self.value('speed', unit='%')
        self.rpm=self.value('rpm', unit='t/min')
        self.status=self.value('status', unit=35)
        self.warning=self.value('status', unit=35)
        self.t1=self.value('t1', unit='C')
        self.t2=self.value('t2', unit='C')
        self.t3=self.value('t3', unit='C')
        self.clockwise=self.valueDigital('clockwise')
        self.pow=self.value('pow', 'W')
        self.ene=self.value('ene', 'kWh')

        self._timeoutRefreshSlow=0

    def onLoad(self, xml: XMLConfig):
        item=xml.child('source')
        if item:
            self.config.update('enablesource', item.get('source'))
            if self.config.enablesource=='bus':
                self.enable=self.valueDigital('enable', writable=True)
            else:
                self.enable=self.valueDigital('enable')

        item=xml.child('speed')
        if item:
            self.config.update('speedsource', item.get('source'))
            if self.config.speedsource=='bus':
                self.sp=self.value('sp', unit='%', writable=True, resolution=0.1)

            subitem=item.child('io1')
            if subitem:
                self.config.update('io1type', subitem.get('type'))

            subitem=item.child('io2')
            if subitem:
                self.config.update('io2type', subitem.get('type'))

            subitem=item.child('io3')
            if subitem:
                self.config.update('io3type', subitem.get('type'))

            subitem=item.child('input')
            if subitem:
                self.config.set('x0', 1)
                self.config.set('y0', 0)
                self.config.set('x1', 10)
                self.config.set('y1', 100)
                self.config.update('x0', subitem.getInt('x0', vmin=0, vmax=10))
                self.config.update('x1', subitem.getInt('x1', self.config.x0, vmax=10))
                self.config.update('y0', subitem.getInt('y0', vmin=0, vmax=100))
                self.config.update('y1', subitem.getInt('y1', vmin=self.config.y0, vmax=100))

            subitem=item.child('sensor')
            if subitem:
                self.config.set('sensorsource', 'ai1')
                self.config.set('x0', 1)
                self.config.set('y0', 0)
                self.config.set('x1', 10)
                self.config.set('y1', 100)
                self.config.update('x0', subitem.getInt('x0', vmin=0, vmax=10))
                self.config.update('x1', subitem.getInt('x1', self.config.x0, vmax=10))
                self.config.update('y0', subitem.getInt('y0', vmin=0, vmax=100))
                self.config.update('y1', subitem.getInt('y1', vmin=self.config.y0, vmax=100))
                self.ai1=self.value('ai1', 'V')
                self.ai2=self.value('ai2', 'V')

            subitem=item.child('watchdog')
            if subitem:
                self.config.set('watchdogsource', subitem.get('source'))

            self.config.update('controlmode', item.get('control'))
            self.config.update('rpm', item.getInt('rpm', vmin=0, vmax=64000))
            self.config.update('maxrpm', item.getInt('maxrpm', vmin=0, vmax=self.config.rpm))
            self.config.update('ramp', item.getInt('ramp', vmin=0))

    def poweron(self):
        # paramerter set 0
        self.writeRegistersIfChanged(0xd105, 0)

        # enable source
        data={'bus': 1, 'di1-off': 2, 'di2-off': 3, 'di3-off': 4, 'di1-on': 5, 'di1': 5, 'di2-on': 6, 'di2': 6}
        self.writeRegistersIfChanged(0xd16a, data.get(self.config.sourceenable, 1))

        # speed source
        data={'bus': 1, 'ai1': 0, 'ai2': 2}
        self.writeRegistersIfChanged(0xd101, data.get(self.config.speedsource, 1))

        # control mode
        data={'speed': 0, 'sensor': 1}
        self.writeRegistersIfChanged(0xd106, data.get(self.config.controlmode, 0))

        # start/min/max modulation levels
        self.writeRegistersIfChanged(0xd116, 0)
        self.writeRegistersIfChanged(0xd117, 256)
        self.writeRegistersIfChanged(0xd118, 0)

        # stop enable
        self.writeRegistersIfChanged(0xd112, 1)

        # max speed
        rpm=self.config.rpm
        if rpm>0:
            self.writeRegistersIfChanged(0xd119, rpm)
            self.writeRegistersIfChanged(0xd11a, rpm)

        rpm=self.config.maxrpm
        if rmp==0:
            rpm=self.config.rpm
        self.writeRegistersIfChanged(0xd128, rpm)

        ramp=self.config.ramp
        self.writeRegistersIfChanged(0xd11f, int(float(ramp)/2.5))
        self.writeRegistersIfChanged(0xd120, int(float(ramp)/2.5))

        # input
        if self.config.speedsource != 'bus':
            self.writeRegistersIfChanged(0xd12a, int(self.config.x0/10.0*65536.0))
            self.writeRegistersIfChanged(0xd12c, int(self.config.x1/10.0*65536.0))
            if self.config.controlmode=='speed':
                self.writeRegistersIfChanged(0xd12b, int(self.config.y0/100.0*64000.0))
                self.writeRegistersIfChanged(0xd12d, int(self.config.y1/100.0*64000.0))
            elif self.config.controlmode=='sensor':
                self.writeRegistersIfChanged(0xd12b, int(self.config.y0/100.0*65536.0))
                self.writeRegistersIfChanged(0xd12d, int(self.config.y1/100.0*65536.0))
            elif self.config.controlmode=='openloop':
                self.writeRegistersIfChanged(0xd12b, int(self.config.y0/100.0*65536.0))
                self.writeRegistersIfChanged(0xd12d, int(self.config.y1/100.0*65536.0))

        # limitation control
        self.writeRegistersIfChanged(0xd12f, 0)

        # output speed monitoring 0-10V
        self.writeRegistersIfChanged(0xd130, 1)
        self.writeRegistersIfChanged(0xd140, 0)
        self.writeRegistersIfChanged(0xd141, 0)
        self.writeRegistersIfChanged(0xd142, 64000)
        self.writeRegistersIfChanged(0xd143, 64000)

        # speed source
        data={'bus': 1, 'ai1': 0, 'ai2': 2}
        self.writeRegistersIfChanged(0xd101, data.get(self.config.speedsource, 1))

        if self.config.controlmode=='sensor':
            data={'ai1': 0, 'ai2': 1, 'max': 2, 'min': 3, 'mean': 4}
            self.writeRegistersIfChanged(0xd147, data.get(self.config.sensorsource, 0))

        # shedding
        self.writeRegistersIfChanged(0xd150, 0)

        # IO1
        data={'di': 0, 'ai': 2}
        self.writeRegistersIfChanged(0xd158, data.get(self.config.io1type, 0))

        # IO2
        data={'di': 0, 'ai': 2}
        self.writeRegistersIfChanged(0xd159, data.get(self.config.io1type, 2))

        # IO3
        data={'di': 0, 'di0': 1, 'di!': 1, 'ao': 3}
        self.writeRegistersIfChanged(0xd15a, data.get(self.config.io1type, 3))

        # watchdog
        if self.config.watchdogsource:
            data={'bus': 1, 'ai1': 2, 'ai2': 2}
            self.writeRegistersIfChanged(0xd15c, data.get(self.config.watchdogsource, 0))
            if self.config.watchdogsource=='bus':
                self.writeRegistersIfChanged(0xd15e, int(self.config.getInt('delay', vmin=0)/100.0))
            else:
                self.writeRegistersIfChanged(0xd15f, self.config.getFloat('min', vmin=0)/10.0*65536.0)

            value=self.config.getInt('value', vmin=0, vmax=100)
            if self.config.controlmode=='speed':
                self.writeRegistersIfChanged(0xd15d, int(value/100.0*64000.0))
            else:
                self.writeRegistersIfChanged(0xd15d, int(value/100.0*65536.0))

            # keep rotation direction
            self.writeRegistersIfChanged(0xd15b, 2)
        else:
            self.writeRegistersIfChanged(0xd15c, 0)

        if self.config.controlmode=='sensor':
            # Sensor caracteristics
            encoder=self.encoder()
            encoder.float32(0)
            encoder.float32(100)
            encoder.writeRegistersIfChanged(0xd160)

        return True

    def poweroff(self):
        return True

    def refresh(self):
        r=self.readRegisters(0xd010, 13)
        if r:
            self.speed.updateValue(r[9]/65536.0*100.0)
            self.rpm.updateValue(r[1])
            self.status.updateValue(r[2])
            self.warning.updateValue(r[3])
            self.t1.updateValue(r[5])
            self.t2.updateValue(r[6])
            self.t3.updateValue(r[7])
            self.clockwise.updateValue(r[8])

        if self.isTimeout(self._timeoutRefreshSlow):
            r=self.readRegisters(0xd023, 8)
            if r:
                if self.ai1 is not None:
                    self.ai1.updateValue(r[0]/65536.0*10.0)
                if self.ai2 is not None:
                    self.ai2.updateValue(r[0]/65536.0*10.0)
                self.pow.updateValue(r[4])
                self.ene.updateValue(r[4])
                decoder=self.decoderFromRegisters(r[6:])
                self.ene.updateValue(decoder.dword())
            self._timeoutRefreshSlow=self.timeout(15)

        return 3.0

    def sync(self):
        if self.enable is not None:
            value=self.enable
            if value.isPendingSync():
                self.writeRegisters(0xd00f, value.toReachValue)
                value.clearSync()
        if self.sp is not None:
            value=self.sp
            if value.isPendingSync():
                self.writeRegisters(0xd001, value.toReachValue)
                value.clearSync()


if __name__ == "__main__":
    pass
