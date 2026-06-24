#define RESET_WATCHDOG1 9

void ResetWatchdog1()
{
     pinMode(RESET_WATCHDOG1, OUTPUT);
     delay(200);
     pinMode(RESET_WATCHDOG1, INPUT);
     Serial.println("Watchdog1 Reset");
}
http://store.switchdoc.com/switchdoc-labs-dual-watchdog-timer-board-for-arduino-raspberry-pi/
NAME                PIN      I/O   DESCRIPTION
DOG1_TRIGGER        JP2 / 1   I    Resets WatchDog 1.Should be held in high-impedance and then taken to ground to “pat the dog”.
DOG2_TRIGGER        JP2 / 2   I    Resets WatchDog 2. Should be held in high-impedance and then taken to ground to “pat the dog”.
DOG1_ARDUINORESET   JP3 / 1   O    When WatchDog 1 triggers, this pin is pulled to GND for ~300ms. Otherwise high-impedance.
DOG1_PULSEHIGH      JP3 / 2   O    Active Low Output. Pulses High for ~300msec when the WatchDog is triggered.
DOG2_ARDUINORESET   JP5 / 1   O    When WatchDog 1 triggers, this pin is pulled to GND for ~300ms. Otherwise high-impedance.
DOG2_PULSEHIGH      JP5 / 2   O    Active Low Output. Pulses High for ~300msec when the WatchDog is 


#define RESET_WATCHDOG1 9

void ResetWatchdog1()
{
     pinMode(RESET_WATCHDOG1, OUTPUT);
     delay(20000);
     pinMode(RESET_WATCHDOG1, INPUT);
     Serial.println("Watchdog1 Reset");
}

void setup() {
  // initialize serial communications at 9600 bps:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  ResetWatchdog1();
}

