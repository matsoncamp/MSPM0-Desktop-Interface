# MSPM0-Desktop-Interface
This project creates a desktop interface using the Python libraries tkinter and bleak to control an MSPM0 microcontroller through an external BLE device. The program for the application is **app.py**, however it has also been created into a .exe file called **MSPM0 App**.
Currently, the application is capable of toggling LEDs on the MSPM0. If there is time for future work, I2C and SPI functionality will be added.\
The current version of the app includes a row of buttons for a DHT22 temperature and humidity sensor. However, these buttons currently have no functionality as conversion of the DHT Arduino library to C was troublesome.\
If you create edits to the app.py file, and want to update the .exe file, use pyinstaller in the command line. To install pyinstaller, use:
```sh
pip install pyinstaller
```
To recompile the .exe, use the following command:
```sh
pyinstaller app.py --onefile --distpath "path/to/file" --name "MSPM0 App" --noconsole
```
