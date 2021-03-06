//battery meter code for uno arduino
int 
int interval = 1; //sample time interval (1000 (ms) = 1 second)
float bat_high = 13.10;
float bat_low = 11.40;
int samples = 100; //number of samples taken
int analog_read = 0; 
int pin_to_read = 1; 
int reading_sum_total = 0;
int reading_sum_avg = 0;
float volt = 0;

void setup()
{
  Serial.begin(9600);
}
void loop()
{
	for(int i = 0; i < samples ; i++)
  	{
		analog_read = analogRead(pin_to_read);
		reading_sum_total += analog_read;
		delay(10);
    }
	reading_sum_avg = reading_sum_total / samples;
	volt = (reading_sum_avg - bat_low) / (bat_high - bat_low);
	Serial.print("Voltage: ");
	Serial.println (volt);
	delay(interval);
}


