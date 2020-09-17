#include "WiFi.h"
//const char* ssid = "DH iMac";
//const char* password = "12345678";
const char* ssid = "UTS_709_IoT_2";
const char* password = "uts709iot";
//const char* ssid = "Le Duc Thanh";
//const char* password = "01213601997";
//const char* ssid = "Finita CAFE";
//const char* password = "chanhdaxay";

const uint16_t port = 8090;
const char * host = "192.168.2.13";
String dataValue;

WiFiClient client;
//WebSocketClient webSocketClient;

void setup()
{
    Serial.begin(115200);
    // Set WiFi to station mode and disconnect from an AP if it was previously connected
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.println("...");
    }
 
    Serial.print("WiFi connected with IP: ");
    Serial.println(WiFi.localIP());

    Serial.println("Setup done");
    
    client.connect(host, port);
    if (!client.connected()) {
 
        Serial.println("Connection to host failed");
    } else {
        Serial.println("Connected to server successful!");
    }
    
 
    
}

void loop()
{
    if (!client.connected()) {
      Serial.println("Connection to host failed");
      client.connect(host, port);
      
    } else{
      Serial.println("scan start");
      int n = WiFi.scanNetworks();
      Serial.println("scan done");
      if (n == 0) {
          Serial.println("no networks found");
      } else {
          Serial.print(n);
          Serial.println(" networks found");
          for (int i = 0; i < n; ++i) {
               if (WiFi.SSID(i).equals("ESP32-1") ||  
                      WiFi.SSID(i).equals("ESP32-3") || 
                      WiFi.SSID(i).equals("ESP32-4") || 
                      WiFi.SSID(i).equals("ESP32-5")  
//                      WiFi.SSID(i).equals("Chuckylee") 
                      ) {
                Serial.print(WiFi.SSID(i));
                Serial.print(" (");
                Serial.print(WiFi.RSSI(i));
                Serial.print(" )");
//                dataValue += String(WiFi.SSID(i));
//                dataValue += String(" ");
                dataValue += String(WiFi.RSSI(i));
                dataValue += String(" ");
              }
        }
        client.print(dataValue);
    dataValue ="";
    Serial.println("");
    }
    Serial.println("");
    }
    
    

    // Wait a bit before scanning again
    delay(2000);
}
