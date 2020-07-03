/*
   Based on Neil Kolban example for IDF: https://github.com/nkolban/esp32-snippets/blob/master/cpp_utils/tests/BLE%20Tests/SampleScan.cpp
   Ported to Arduino ESP32 by Evandro Copercini
*/

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>
#include "WiFi.h"
#include "WebSocketClient.h"

int scanTime = 5; //In seconds
BLEScan* pBLEScan;
const char* ssid = "UTS_709_IoT_2";
const char* password = "uts709iot";
const uint16_t port = 8090;
const char * host = "192.168.2.18";
String dataValue;

WiFiClient client;
WebSocketClient webSocketClient;
class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
//      Serial.printf("Advertised Device: %s \n", advertisedDevice.toString().c_str());
      if(String(advertisedDevice.getAddress().toString().c_str()).equals("24:6f:28:25:f9:92")){
        Serial.print(String(advertisedDevice.toString().c_str()));
        Serial.print(" : ");
        Serial.print(advertisedDevice.getRSSI());
        client.print(String(advertisedDevice.getRSSI()));
      }
    }
    
};

void connectWifi(){
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("...");
  }

  Serial.print("WiFi connected with IP: ");
}

void setup() {
  Serial.begin(115200);
  Serial.println("Scanning...");
  connectWifi();
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);  // less or equal setInterval value
}

void loop() {
  // put your main code here, to run repeatedly:
  if (!client.connected()) {
      Serial.println("Connection to host failed");
      client.connect(host, port);
      
    } else{
      BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
      Serial.println("Scan done!");
      pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory
    }
  delay(1000);
}
