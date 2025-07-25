# Cold Wallet Pinger

**Cold Wallet Pinger** — Python-утилита для анализа Ethereum-кошельков, которые долгое время не проявляли активности.

---

## Назначение

Позволяет "пинговать" адреса и определять:
- Когда был последний исходящий перевод
- Является ли кошелек **cold** (неактивным)
- Используется для анализа активности китов, multisig-кошельков, старых адресов

---

## Установка

```bash
pip install -r requirements.txt
```

## Использование

```bash
python cold_wallet_pinger.py <ETH_ADDRESS> <ETHERSCAN_API_KEY> [--threshold N]
```

Пример:

```bash
python cold_wallet_pinger.py 0xabc...def YOUR_API_KEY --threshold 90
```

---

## Что делает

- Сканирует последние транзакции по адресу
- Ищет последнюю исходящую транзакцию
- Сравнивает с текущей датой и выдает статус:

```
[✓] Последняя исходящая активность:
    Дата: 2022-10-14
    Прошло дней: 248
    Статус: ❄️ COLD
```

---

## Лицензия

MIT
