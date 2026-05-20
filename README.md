# BPC-IoT Projekt #1 – Meteostanica

## Popis projektu
Autonómny systém na zber meteorologických a diagnostických údajov z odľahlých lokalitách bez existujúcej dátovej infraštruktúry.

### NB-IoT
* **Úloha v projekte:** Zabezpečenie bezdrôtovej LPWAN konektivity v exteriérovom teréne.
* **Typ prevádzky:** Stacionárna stanica odosielajúca malé objemy dát v pravidelných intervaloch.
* **Sieť:** Pripojenie realizované cez prístupový bod (APN) operátora v licencovanom pásme.

### CoAP
* **Úloha v projekte:** Efektívna aplikačná vrstva bežiaca nad transportným protokolom UDP.
* **Implementácia:** Využitie natívneho CoAP stacku modemu Quectel BG77 pomocou AT príkazov (`AT+QCOAP*`).
* **Dátová réžia:** Minimálna spotreba dát vďaka binárnemu formátu správ vhodnému pre IoT.

---

## Hardvér a zapojenie
* **MCU:** Mikrokontrolér s podporou MicroPythonu (Raspberry Pi Pico / STM32).
* **Modem:** Quectel BG77 (NB-IoT konektivita).
* **Senzor:** AHT20 (Digitálny snímač teploty a vlhkosti).
* **RGB LED:** Indikačné diódy NeoPixel pripojené na pin `GP16`.
* **I2C konfigurácia (AHT20):** SDA (`GP14`), SCL (`GP15`), frekvencia `400 kHz`.
* **Adresa senzora:** `0x38` (predvolená).

---

## Štruktúra súborov
* `Main_Meteo_JKKK.py` – Hlavný program: inicializácia periférií, správa napájania modemu, startup sekvencia a periodická slučka merania s konfiguráciou tokenu.
* `BG77.py` – Hardvérový driver pre modem: spracovanie AT príkazov, riadenie relácií a diagnostika siete.
* `ahtx0.py` – Ovládač pre senzor AHT20: inicializácia a vyčítanie hodnôt teploty a vlhkosti cez I2C.

---

## Rýchla konfigurácia
Konfigurácia prístupu sa vykonáva priamo v hlavnom skripte `Main_Meteo_JKKK.py` úpravou premennej:
* **Thingsboard Token:** `token = "VgEuJgBrVmg7NBmWqxl7"`
* **Server IP:** `147.229.148.105` (preddefinovaná v AT príkazoch)
* **CoAP Port:** `5683` (preddefinovaný v AT príkazoch)

---

## Spustenie a tok programu
* **Nahranie súborov:** Skopírujte `BG77.py`, `ahtx0.py` a hlavný skript do pamäte mikrokontroléra.
* **Inicializácia hardvéru:** Po resete sa inicializuje I2C zbernica, senzor AHT20 a nastaví sa indikačná NeoPixel LED.
* **Startup balík (Jednorazovo):** Zariadenie aktivuje PDP kontext (`AT+QIACT=1`), otvorí CoAP reláciu a odošle úvodné diagnostické dáta (RSRP, SINR, CellID a fixné GPS súradnice lokality stožiaru).
* **Periodická slučka (Každých 15 sekúnd):**
  * Vyčítanie reálnej teploty a vlhkosti zo snímača AHT20.
  * Simulácia rýchlosti vetra (generovanie náhodných hodnôt).
  * Aktualizácia sieťových parametrov (RSRP, SINR) z modemu.
  * Odoslanie kompletného telemetrického balíka na Thingsboard.
  * Uzatvorenie CoAP spojenia pre úsporu energie.

---

##  Štruktúra odosielaných údajov (JSON)

### 1. Startup balík
```json
{
  "RSRP": -102,
  "SINR": 12.5,
  "CellID": "2A3F4B",
  "latitude": 49.3695500,
  "longitude": 16.8157000
}
