# ADR-0002 — Narzędzia testów i jakości kodu

## Status

Zaakceptowana

## Data

2026-06-27

## Kontekst

TradingLab ma być projektem rozwijanym przez wiele lat.
Od początku projektu przyjęto zasadę, że kod powinien być testowalny, czytelny i możliwy do utrzymania.

Przed rozpoczęciem implementacji modułów biznesowych należy przygotować podstawowe narzędzia wspierające jakość kodu.

## Decyzja

Projekt TradingLab będzie używał następujących narzędzi developerskich:

* `pytest` — do uruchamiania testów,
* `ruff` — do analizy jakości kodu oraz formatowania.

Narzędzia zostały dodane jako zależności developerskie projektu przy użyciu `uv`.

## Uzasadnienie

### pytest

`pytest` jest standardowym i szeroko stosowanym narzędziem do testowania projektów Python.

Umożliwia:

* pisanie prostych testów jednostkowych,
* testowanie modułów niezależnie od reszty systemu,
* automatyczne sprawdzanie poprawności działania kodu,
* rozwój projektu bez ciągłego ręcznego testowania.

### ruff

`ruff` pozwala sprawdzać jakość kodu i formatować go w spójny sposób.

Umożliwia:

* wykrywanie prostych błędów,
* utrzymanie jednolitego stylu kodu,
* ograniczenie bałaganu w projekcie,
* szybką analizę kodu bez wielu osobnych narzędzi.

## Konsekwencje

Każdy istotny moduł TradingLab powinien docelowo posiadać testy.

Kod powinien przechodzić podstawowe sprawdzenie jakości przed zapisaniem większych zmian.

Dodanie tych narzędzi przed rozpoczęciem prac nad Data Engine pozwala budować projekt na stabilnym fundamencie technicznym.
