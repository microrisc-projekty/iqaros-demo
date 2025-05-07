# Ukázka sběru dat z technologie IQAROS+

## Připojení k IQRF gateway:
- Pro komunikaci s IQRF gateway je nutné použít MQTT broker - server který propojí gateway a Vaši aplikaci
  - Jedním z vhodných brokerů je [Mosquitto](https://mosquitto.org/)
  - Je možné hostovat vlastní broker lokálně (doporučeno), nebo se připojit k veřejnému brokeru - například [test.mosquitto.org](https://test.mosquitto.org/). Návod pro lokální nastavení Mosquitto brokeru je [zde](./MOSQUITTO.md).
- Pro připojení IQRF gateway k brokeru je třeba nastavit připojení ve webové aplikaci IQAROS+:
  1. Po přihlášení přejděte v levém panelu na Configuration > MQTT Connections
  2. Klikněte na + (Add MQTT connection profile)
  3. Vyplňte následující údaje:
    - Profile name - libovolný název
    - Client ID - stiskněte **Set default**
    - Host - adresa vašeho brokeru (viz první bod návodu)
    - Port - **1883** (8883 v případě že používáte šifrované spojení)
    - Request a Response topic - stiskněte **Set default** (Response topic dále využijete při připojení MQTT klienta)
    - User a Password- váš MQTT uživatel (pokud nepoužíváte MQTT uživatele, nechte obě pole prázdná)
    - ostatní údaje neměňte
  4. Klikněte na Save
  5. Přejděte do záložky Configuration > Data collecting.
  5. Ujistěte se, že váše nově přidané spojení je vybráno v poli *Connection profiles used to send data* .
  6. Dále je v této záložce možné upravit interval zasílání dat (*Data collection period*), pro testovací účely doporučuji nastavit na nejnižší interval - 4 minuty.
  7. Pro testování spojení je také praktické tlačítko *Collect data now* (ikonka prstu v horním panelu). Po jeho stisknutí jsou naměřená data ihned poslána na MQTT broker.

- Pro ověření komunikace je možné použít například program [MQTT Explorer](https://mqtt-explorer.com/).


## Práce s daty:

### Formát dat:
Data budou na MQTT broker přicházet v intervalu nastaveném v IQAROS+. Formát dat je následující:
```
{
  "mType": "iqrfSensorData_ReportAsync",
  "data": {
    "msgId": "async",
    "rsp": {
      "devices": [
        {
          "address": <ADRESA ZAŘÍZENÍ>,
          "rssi": <HODNOTA SIGNÁLU RSSI>,
          "sensors": [
            {
              "type": <TYP SENZORU>,
              "name": <NÁZEV VELIČINY>,
              "unit": <JEDNOTKA>,
              "value": <NAMĚŘENÁ HODNOTA>
            },
            ...
          ]
        },
        ...
      ],
      "reading": <BOOLEAN> // pokud je false, zpráva obsahuje data
    }
  }
}
```
Zpráva obsahuje ještě další data, ale ty nejsou pro základní práci podstatná.

**Pozor:** Důležité je kontrolovat hodnotu atributu *reading* a vyčítat data pouze pokud je hodnota **false**, jinak se může stát, že zpráva nebude obsahovat žádná data.

### Hotové ukázky:
- Po úspěšném připojení k MQTT brokeru je možné začít pracovat s příchozími daty. K dispozici jsou dvě základní ukázky v jazyce Python využívající MQTT klient Paho:
  - `examples/basic.py` - ukázka připojení k brokeru a čtení dat
  - `examples/extended.py` - rozšířená ukázka počítající průměrnou teplotu a vlhkost
- Pro připojení je třeba vyplnit údaje: BROKER_HOST = **IP adresa vašeho MQTT brokera**, RESPONSE_TOPIC = **Response topic z IQAROS+ aplikace**
