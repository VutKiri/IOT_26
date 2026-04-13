# Project Meteostation
____________________________________________________________________________________________________
IOT PROJECT 2026
____________________________________________________________________________________________________
## Zadanie:
Naprogramujte a zprovozněte bezdrátovou meteostanici pro měření povětrnostních
podmínek jako je teplota a vlhkost.
Předpokládejte:
### • Nasazení meteostanice na starém meteorologickém stožáru, nejméně ve výšce 10 m nad zemí.
### • Lokalita stožáru v oblastech bez přístupu ke konvenčním metodám připojení (les, odlehlé budovy, pole).
### • Stožár je vybaven silnoproudým rozvodem, avšak datové rozvody nejsou přítomny.
____________________________________________________________________________________________________
Meteostanice bude odesílat v definovaných intervalech hodnoty o daných veličinách
(teplota, vlhkost, rychlost větru) na vzdálený server, stejně jako údaje a parametry relevantní
pro daný rádiový kanál zvolené technologie.
• WiFi – RSSI
• LoRa – DR – Spreading Factor
• NB-IoT / LTE Cat-M – RSRP, SINR
• V případě volby jiné technologie jiné relevantní parametry

Při prvním připojení (startup) meteostanice budou, společně s údaji o veličinách a rádiovém
kanálu, odeslány i údaje GPS o fixní poloze zařízení a informace o zařízení (smyšlené Device
ID, smyšlená verze firmwaru, smyšlený název výrobce - vaše VUTID) a jeho konektivitě:
• WiFi – „WiFi“, SSID, Číslo zvoleného kanálu.
• LoRa – „LoRa“, EUI, Adres zařízení.
• NB-IoT /LTE Cat-M – „NB-IoT“/„LTE Cat-M/eMTC“, CellID, Tracking Area Code (TAC), LTE pásmo (Band), EARFCN.
• V případě volby jiné technologie jiné relevantní položky jako například název technologie, frekvence, označení Gatewaye, ID zařízení atd.
____________________________________________________________________________________________________
Zaslaná data budou zobrazena na platformě Thingsboard. (Uvažujte vhodnost využití pro
danou technologii. V případě nutnosti konzultujte vyučujícího.)
Pro danou aplikaci, vhodně zvolte anténu pro dané zařízení.
Všechny ostatní parametry/postupy zvolte dle Vašeho uvážení a následně uveďte zdůvodnění
Vaší volby do popisu technického řešení.
