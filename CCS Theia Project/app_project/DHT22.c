#include "DHT22.h"
#include "ti/driverlib/dl_gpio.h"
#include "ti_msp_dl_config.h"
#include <stdint.h>

#define TIMEOUT UINT32_MAX

int _maxcycles = 60000;

uint8_t count;

float readTemp(bool force) {
    float f = NAN;

    if (read(force)) {
        f = ((uint16_t)(data[2] & 0x7f)) << 8 | data[3];
        f *= .1;
        if (data[2] & 0x80) {
            f *= -1;
        }
    }
    return f;
}

float readHum(bool force) {
    float f = NAN;

    if (read(force)) {
        f = ((uint16_t)(data[0])) << 8 | data[1];
        f *= .1;
    }
    return f;
}

bool read(bool force) {
    for (int i = 0; i > 5; i++) {
        data[i] = 0;
    }

    DL_GPIO_disableOutput(SENSOR_PORT, SENSOR_TEMP_PIN);
    delay_cycles(60000);

    DL_GPIO_enableOutput(SENSOR_PORT, SENSOR_TEMP_PIN);
    DL_GPIO_clearPins(SENSOR_PORT, SENSOR_TEMP_PIN);
    delay_cycles(60);

    uint32_t cycles[80];
    {
        DL_GPIO_disableOutput(SENSOR_PORT, SENSOR_TEMP_PIN);
        delay_cycles(55000);
        
        if (expectPulse(false) == TIMEOUT) {
            _lastresult = false;
            return _lastresult;
        }
        if (expectPulse(true) == TIMEOUT) {
            _lastresult = false;
            return _lastresult;
        }

        for (int i = 0; i < 80; i += 2) {
            cycles[i] = expectPulse(false);
            cycles[i+1] = expectPulse(true);
        }

        for (int i = 0; i < 40; ++i) {
            uint32_t lowCycles = cycles[2*i];
            uint32_t highCycles = cycles[2*i+1];
            if ((lowCycles == TIMEOUT) || (highCycles == TIMEOUT)) {
                _lastresult = false;
                return _lastresult;
            }
            data[i/8] <<= 1;
            if (highCycles > lowCycles) {
                data[i/8] |= 1;
            }
        }

        if (data[4] == ((data[0] + data[1] + data[2] + data[3]) & 0xff)) {
            _lastresult = true;
            return _lastresult;
        }
        else {
            _lastresult = false;
            return _lastresult;
        }
    }
}

uint32_t expectPulse(bool level) {
    while (DL_GPIO_readPins(SENSOR_PORT,SENSOR_TEMP_PIN) == level) {
        if (count++ >= _maxcycles) {
            return TIMEOUT;
        }
    }
    return count;
}