# Lokální nastavení MQTT brokeru Mosquitto
1) Instalace Mosquitto podle oficiálního [návodu](https://mosquitto.org/download/) (anglicky).
2) Konfigurační soubor mosquitto.conf:
Vytvořte soubor s názvem mosquitto.conf a vložte do něj následující obsah:
    ```
    listener 1883
    protocol mqtt
    allow_anonymous true
    ```
3) Nyní můžete spustit Mosquitto z příkazové řádky pomocí příkazu:
    ```
    mosquitto -c ./mosquitto.conf
    ```
    Pozor: je třeba být ve stejném adresáři jako je soubor mosquitto.conf.


4) Pokud nejsou vypsány žádné chyby, broker běží a je možné se k němu připojit (při správném nastavení není žádný výpis a příkaz není automaticky ukončen). Pokud chcete broker zastavit, zavřete okno příkazové řádky, nebo zadejte Ctrl+C. Pro připojení je možné využít ip adresu počítače (např.: mqtt://192.168.1.2:1883) a vhodný program (např. [MQTT explorer](https://mqtt-explorer.com/) nebo libovolný MQTT klient).

5) Je možné dále nastavit pro broker uživatele a heslo, více info v [oficiálním návodu](https://mosquitto.org/documentation/authentication-methods/).
