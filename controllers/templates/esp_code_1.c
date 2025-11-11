#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#define sensorPin 4  
#define relePin1 5  
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

float totalLitros = 0.0;
float metaLitros = 0.0;

bool cicloDoDiaConcluido = false;
bool releAtivo = false;
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

    int httpResponseCode = http.POST(jsonPayload);
    if (httpResponseCode == 200)
      Serial.println("✅ Válvula desligada com sucesso.");
    else
      Serial.println("❌ Erro ao desligar válvula: " + String(httpResponseCode));
    http.end();
  } else Serial.println("⚠️ WiFi desconectado!");
}

int mudarFaseVegetal(int botao) {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String serverUrl = BASE_URL + "controllers/api/update/vegetablephase/";
    http.begin(serverUrl);
    http.addHeader("Content-Type", "application/json");

    String jsonPayload = "{";
    jsonPayload += "\"controllerId\": " + String(CONTROLLER_ID) + ",";
    jsonPayload += "\"valveId\": 1,";
    jsonPayload += "\"securityCode\": \"" + String(SECURITY_CODE) + "\",";
    jsonPayload += "\"controllerUuid\": \"" + String(CONTROLLER_UUID) + "\",";
    jsonPayload += "\"phaseVegetable\": " + String(botao);
    jsonPayload += "}";

    int httpResponseCode = http.POST(jsonPayload);
    http.end();
    return httpResponseCode;
  }
  return -1;
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

    int httpResponseCode = http.POST(jsonPayload);
    http.end();
    return httpResponseCode;
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

  if (releAtivo) {
    lcd.setCursor(0, 0);
    lcd.print("Fluxo Monitorado");
    lcd.setCursor(0, 1);
    lcd.print("V1:");
    lcd.print(totalLitros, 1);
    lcd.print("TP:");
    lcd.print(totalPulses);
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
  digitalWrite(relePin1, HIGH);

  pinMode(BOTAO1, INPUT_PULLUP);
  pinMode(BOTAO2, INPUT_PULLUP);
  pinMode(BOTAO3, INPUT_PULLUP);
  pinMode(BOTAO4, INPUT_PULLUP);
  pinMode(BOTAO5, INPUT_PULLUP);
  pinMode(BOTAO_LCD, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(sensorPin), increase, RISING);
  attachInterrupt(digitalPinToInterrupt(BOTAO1), isrBotao1, FALLING);
  attachInterrupt(digitalPinToInterrupt(BOTAO2), isrBotao2, FALLING);
  attachInterrupt(digitalPinToInterrupt(BOTAO3), isrBotao3, FALLING);
  attachInterrupt(digitalPinToInterrupt(BOTAO4), isrBotao4, FALLING);
  attachInterrupt(digitalPinToInterrupt(BOTAO5), isrBotao5, FALLING);
  attachInterrupt(digitalPinToInterrupt(BOTAO_LCD), isrBotaoLCD, FALLING);

  Serial.begin(115200);
  Wire.begin(SDA_PIN, SCL_PIN);
  lcd.begin(16, 2);
  lcd.backlight();
  lcd.print("AcquaCallidus");
  lcd.setCursor(0, 1);
  lcd.print("Iniciando...");
  delay(2000);
  lcd.clear();

  WiFi.begin(ssid, password);
  lcd.print("Conectando WiFi");

  unsigned long startAttemptTime = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    if (millis() - startAttemptTime > 15000) {
      lcd.clear();
      lcd.print("ERRO WiFi!");
      delay(60000);
      ESP.restart();
    }
  }

  lcd.clear();
  lcd.print("WiFi Conectado");
  lcd.setCursor(0, 1);
  lcd.print(WiFi.localIP());
  delay(2000);
  lcd.clear();

  lcd.print("Conectando Serv.");
  if (conectarServidor() <= 0) {
    lcd.clear();
    lcd.print("ERRO Servidor!");
    delay(60000);
    ESP.restart();
  }

  delay(2000);
  exibirTela();
}

void loop() {
  static unsigned long lastTime = 0;
  unsigned long currentTime = millis();

  if (currentTime - lastTime >= 1000) {
    float litros = pulse / fatorCalibracao;
    if (releAtivo) totalLitros += litros;
    Serial.printf("Pulsos: %ld | Fluxo: %.2f L/s | Total: %.2f L\n", pulse, litros, totalLitros);
    exibirTela();
    pulse = 0;
    lastTime = currentTime;
  }

  if ((millis() >= proximaIrrigacao) || ultimoDia == 0) {
    ultimoDia = millis();
    cicloDoDiaConcluido = false;
    totalLitros = 0;
    metaLitros = getLitrosPorValvula(valve_ids[0]);
    releAtivo = true;
    digitalWrite(relePin1, LOW);
    proximaIrrigacao = ultimoDia + intervaloIrrigacao;
    lcd.clear();
    lcd.print("Fluxo Monitorado");
    Serial.println("Novo ciclo iniciado.");
  }

  if (!cicloDoDiaConcluido && releAtivo && totalLitros >= metaLitros) {
    digitalWrite(relePin1, HIGH);
    releAtivo = false;
    cicloDoDiaConcluido = true;
    desligarValvulaNoServidor(valve_ids[0], totalLitros);
    totalLitros = 0;
    proximaIrrigacao = millis() + intervaloIrrigacao;
    lcd.clear();
    lcd.print("Irrig. concluida");
    delay(60000);
  }

  if (botao1Pressionado) { botao1Pressionado = false; mudarFaseVegetal(1); }
  else if (botao2Pressionado) { botao2Pressionado = false; mudarFaseVegetal(2); }
  else if (botao3Pressionado) { botao3Pressionado = false; mudarFaseVegetal(3); }
  else if (botao4Pressionado) { botao4Pressionado = false; mudarFaseVegetal(4); }
  else if (botao5Pressionado) { botao5Pressionado = false; mudarFaseVegetal(5); }
  else if (botaoLCDPressionado) {
    lcdLigado = !lcdLigado;
    botaoLCDPressionado = false;
    exibirTela();
  }
}
