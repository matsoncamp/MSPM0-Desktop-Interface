//#include <cstdint>
#include <stdbool.h>
#include <stdint.h>

uint8_t data[5];

bool _lastresult;

float readTemp(bool force);

float readHum(bool force);

bool read(bool force);

uint32_t expectPulse(bool level);