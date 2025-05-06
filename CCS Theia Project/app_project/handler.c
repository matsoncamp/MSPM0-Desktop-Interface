#include "handler.h"
//#include "DHT22.h"
#include "ti/driverlib/dl_gpio.h"
#include "ti/driverlib/dl_uart_main.h"
#include "ti_msp_dl_config.h"

void gpio_handler(uint8_t color) {
    switch (color) {
        case 'R':
            DL_GPIO_togglePins(LEDS_PORT, LEDS_RED_PIN);
            DL_UART_Main_transmitData(BLE_INST, 57);
            break;
        case 'G':
            DL_GPIO_togglePins(LEDS_PORT, LEDS_GREEN_PIN);
                break;
        case 'B':
            DL_GPIO_togglePins(LEDS_PORT, LEDS_BLUE_PIN);
            break;
        case 'M':
            DL_GPIO_togglePins(MONO_PORT, MONO_LIGHT_PIN);
            break;
    }
}

void temp() {
    
}

void humidity() {
    
}

void message_handler(uint8_t message, char mode) {
    if (mode == 'g') {
        if (message == 'G' | message == 'R' | message == 'B' | message == 'M') {
            gpio_handler(message);
        }
        else if (message == 'T') {
            temp();
        }
        else if (message == 'H') {
            humidity();
        }
    }
}