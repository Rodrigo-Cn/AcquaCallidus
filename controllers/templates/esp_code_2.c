#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define sensorPin 4  
#define relePin1 5  
#define relePin2 18  
#define SDA_PIN 21  
#define SCL_PIN 22  

#define BOTAO1 32
#define BOTAO2 33
#define BOTAO3 25
#define BOTAO4 26
#define BOTAO5 27
#define BOTAO_LCD 14  

const char* ssid = "{ssid}";
const char* password = "{password}";
const String BASE_URL = "{baseUrl}";
const int CONTROLLER_ID = {controllerId};
const char* SECURITY_CODE = "{securityCode}";
const char* CONTROLLER_UUID = "{controllerUuid}";

int valve_ids[] = { {valveIds} };

LiquidCrystal_I2C lcd(0x27, 16, 2);

volatile long pulse = 0;
long totalPulses = 0;
float fatorCalibracao = 7.5;

float totalLitrosV1 = 0.0;
float totalLitrosV2 = 0.0;
float metaV1 = 0.0;
float metaV2 = 0.0;

bool cicloDoDiaConcluido = false;
bool rele1Ativo = false;
bool rele2Ativo = false;

unsigned long ultimoDia = 0;
unsigned long intervaloIrrigacao = 86340000; 
unsigned long proximaIrrigacao = 0;

int telaAtual = 0;
bool lcdLigado = true;

volatile bool botao1Pressionado = false;
volatile bool botao2Pressionado = false;
volatile bool botao3Pressionado = false;
volatile bool botao4Pressionado = false;
volatile bool botao5Pressionado = false;
volatile bool botaoLCDPressionado = false;

volatile unsigned long lastInterruptTime4 = 0;

void IRAM_ATTR increase() { pulse++; totalPulses++; }
void IRAM_ATTR isrBotao1() { botao1Pressionado = true; }
void IRAM_ATTR isrBotao2() { botao2Pressionado = true; }
void IRAM_ATTR isrBotao3() { botao3Pressionado = true; }
void IRAM_ATTR isrBotao4() {
  unsigned long currentTime = millis();
  if (currentTime - lastInterruptTime4 > 200) botao4Pressionado = true;
  lastInterruptTime4 = currentTime;
}
void IRAM_ATTR isrBotao5() { botao5Pressionado = true; }
void IRAM_ATTR isrBotaoLCD() { botaoLCDPressionado = true; }

float getLitrosPorValvula(int valveId) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = BASE_URL + "controllers/api/valve/on/";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    String ipLocal = WiFi.localIP().toString();

    String jsonPayload = "{";
    jsonPayload += "\"controllerId\": " + String(CONTROLLER_ID) + ",";
    jsonPayload += "\"valveId\": " + String(valveId) + ",";
    jsonPayload += "\"securityCode\": \"" + String(SECURITY_CODE) + "\",";
    jsonPayload += "\"controllerUuid\": \"" + String(CONTROLLER_UUID) + "\",";
    jsonPayload += "\"ipAdress\": \"" + ipLocal + "\"";
    jsonPayload += "}";

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode == 200) {
      String payload = http.getString();
      StaticJsonDocument<256> doc;
      if (!deserializeJson(doc, payload)) {
        float meta = doc["total_liters"];
        http.end();
        return meta;
      }
    }
    http.end();
  }
  return 0.0;
}

void desligarValvulaNoServidor(int valveId, float litrosIrrigados) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String url = BASE_URL + "controllers/api/valve/off/";
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    String ipLocal = WiFi.localIP().toString();

    String jsonPayload = "{";
    jsonPayload += "\"controllerId\": " + String(CONTROLLER_ID) + ",";
    jsonPayload += "\"valveId\": " + String(valveId) + ",";
    jsonPayload += "\"securityCode\": \"" + String(SECURITY_CODE) + "\",";
    jsonPayload += "\"controllerUuid\": \"" + String(CONTROLLER_UUID) + "\",";
    jsonPayload += "\"ipAdress\": \"" + ipLocal + "\",";
    jsonPayload += "\"irrigatedLiters\": " + String(litrosIrrigados);
    jsonPayload += "}";

    http.POST(jsonPayload);
    http.end();
  }
}

int conectarServidor() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(BASE_URL + "controllers/api/connect/");
    http.addHeader("Content-Type", "application/json");

    String ipLocal = WiFi.localIP().toString();
    int signalStrength = WiFi.RSSI();

    String jsonPayload = "{";
    jsonPayload += "\"controllerId\": " + String(CONTROLLER_ID) + ",";
    jsonPayload += "\"securityCode\": \"" + String(SECURITY_CODE) + "\",";
    jsonPayload += "\"controllerUuid\": \"" + String(CONTROLLER_UUID) + "\",";
    jsonPayload += "\"ipAddress\": \"" + ipLocal + "\",";
    jsonPayload += "\"signalStrength\": " + String(signalStrength);
    jsonPayload += "}";

    int code = http.POST(jsonPayload);
    http.end();
    return code;
  }
  return -1;
}

void exibirTela() {
  if (!lcdLigado) {
    lcd.clear();
    lcd.noBacklight();
    return;
  }

  lcd.backlight();
  lcd.clear();

  if (rele1Ativo || rele2Ativo) {
    lcd.setCursor(0, 0);
    lcd.print("Fluxo Monitorado");
    lcd.setCursor(0, 1);
    lcd.print("V1:");
    lcd.print(totalLitrosV1, 1);
    lcd.print(" V2:");
    lcd.print(totalLitrosV2, 1);
  } else if (cicloDoDiaConcluido) {
    unsigned long agora = millis();
    unsigned long tempoRestante = (proximaIrrigacao > agora) ? (proximaIrrigacao - agora) / 1000 : 0;
    unsigned int horas = tempoRestante / 3600;
    unsigned int minutos = (tempoRestante % 3600) / 60;
    unsigned int segundos = tempoRestante % 60;

    lcd.setCursor(0, 0);
    lcd.print("Prox ciclo em:");
    lcd.setCursor(0, 1);
    char buffer[17];
    snprintf(buffer, sizeof(buffer), "%02u:%02u:%02u hrs", horas, minutos, segundos);
    lcd.print(buffer);
  } else {
    lcd.setCursor(0, 0);
    lcd.print("Aguardando ciclo");
    lcd.setCursor(0, 1);
    lcd.print("...");
  }
}

void setup() {
  pinMode(sensorPin, INPUT_PULLUP);
  pinMode(relePin1, OUTPUT);
  pinMode(relePin2, OUTPUT);
  digitalWrite(relePin1, HIGH);
  digitalWrite(relePin2, HIGH);

  pinMode(BOTAO1, INPUT_PULLUP);
  pinMode(BOTAO2, INPUT_PULLUP);
  pinMode(BOTAO3, INPUT_PULLUP);
  pinMode(BOTAO4, INPUT_PULLUP);
  pinMode(BOTAO5, INPUT_PULLUP);
  pinMode(BOTAO_LCD, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(sensorPin), increase, RISING);
  attachInterrupt(digitalPinToInterrupt(BOTAO_LCD), isrBotaoLCD, FALLING);

  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);
  lcd.begin(16, 2);
  lcd.backlight();
  lcd.print("AcquaCallidus");
  delay(2000);
  lcd.clear();

  WiFi.begin(ssid, password);
  lcd.print("Conectando WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  lcd.clear();
  lcd.print("WiFi conectado!");
  delay(1000);
  conectarServidor();
  exibirTela();
}

void loop() {
  static unsigned long lastTime = 0;
  unsigned long currentTime = millis();

  if (currentTime - lastTime >= 1000) {
    float litros = pulse / fatorCalibracao;

    if (rele1Ativo) totalLitrosV1 += litros;
    if (rele2Ativo) totalLitrosV2 += litros;

    pulse = 0;
    lastTime = currentTime;
    exibirTela();
  }

  if ((millis() >= proximaIrrigacao) || ultimoDia == 0) {
    ultimoDia = millis();
    cicloDoDiaConcluido = false;
    totalLitrosV1 = 0;
    totalLitrosV2 = 0;
    metaV1 = getLitrosPorValvula(valve_ids[0]);
    rele1Ativo = true;
    rele2Ativo = false;
    digitalWrite(relePin1, LOW);
    proximaIrrigacao = ultimoDia + intervaloIrrigacao;
  }

  if (rele1Ativo && totalLitrosV1 >= metaV1) {
    digitalWrite(relePin1, HIGH);
    rele1Ativo = false;
    desligarValvulaNoServidor(valve_ids[0], totalLitrosV1);

    metaV2 = getLitrosPorValvula(valve_ids[1]);
    rele2Ativo = true;
    digitalWrite(relePin2, LOW);
    delay(2000);
  }

  if (rele2Ativo && totalLitrosV2 >= metaV2) {
    digitalWrite(relePin2, HIGH);
    rele2Ativo = false;
    cicloDoDiaConcluido = true;
    desligarValvulaNoServidor(valve_ids[1], totalLitrosV2);
    totalLitrosV1 = totalLitrosV2 = 0;
    proximaIrrigacao = millis() + intervaloIrrigacao;
    lcd.clear();
    lcd.print("Irrig. concluida");
    delay(60000);
  }

  if (botaoLCDPressionado) {
    lcdLigado = !lcdLigado;
    botaoLCDPressionado = false;
    exibirTela();
  }
}
