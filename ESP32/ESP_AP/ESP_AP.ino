#include "WiFi.h"
#define LED0 23
#define LED1 22
const char* ssid = "ESP32-1";
const char* password = "123123123";
WiFiServer server(80);

void Connect_WiFi()
{
WiFi.begin(ssid, password);
while(WiFi.status() != WL_CONNECTED)
{
delay(100);
}
}

void setup()
{
Serial.begin(115200);
Serial.print("Setting soft access point mode");
WiFi.softAP(ssid, password);
IPAddress IP = WiFi.softAPIP();
Serial.print("AP IP address: ");
Serial.println(IP);
server.begin();
}
void loop()
{
 WiFiClient client=server.available();

}
