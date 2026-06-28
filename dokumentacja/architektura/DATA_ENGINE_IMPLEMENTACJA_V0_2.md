# Projekt implementacji Data Engine v0.2.0

## 1. Cel dokumentu

Ten dokument opisuje projekt implementacji moduĹ‚u **Data Engine** dla etapu **v0.2.0** projektu TradingLab.

Dokument nie jest jeszcze opisem gotowego kodu. Jest projektem technicznym, ktĂłry ma poprzedzaÄ‡ implementacjÄ™.

Zasada pracy:

> Najpierw projektujemy, potem kodujemy.

Implementacja Data Engine v0.2.0 powinna wynikaÄ‡ z tego dokumentu oraz z dokumentĂłw nadrzÄ™dnych projektu, w szczegĂłlnoĹ›ci:

* `README.md`,
* `dokumentacja/architektura/KONSTYTUCJA.md`,
* `dokumentacja/architektura/ARCHITEKTURA.md`,
* `dokumentacja/architektura/DATA_ENGINE.md`,
* `dokumentacja/mapa_drogowa/ROADMAP.md`,
* `dokumentacja/decyzje/ADR-0001-fundamenty-projektu.md`,
* `dokumentacja/decyzje/ADR-0002-narzedzia-testow-i-jakosci-kodu.md`.

## 2. Zakres Data Engine v0.2.0

Data Engine w v0.2.0 odpowiada za pierwszy minimalny cykl ĹĽycia datasetu danych rynkowych.

Zakres obejmuje:

1. pobranie danych z jednego ĹşrĂłdĹ‚a,
2. zapis surowych danych,
3. normalizacjÄ™ danych do formatu OHLCV,
4. zapis metadanych datasetu,
5. walidacjÄ™ danych,
6. zapis raportu walidacji,
7. wersjonowanie datasetĂłw,
8. odczyt zapisanych elementĂłw datasetu,
9. podstawowe testy automatyczne.

Data Engine nie jest:

* strategiÄ… tradingowÄ…,
* backtesterem,
* traderem,
* moduĹ‚em live tradingu,
* rankingiem ĹşrĂłdeĹ‚ danych,
* agentem AI.

Data Engine jest fundamentem danych rynkowych dla przyszĹ‚ych moduĹ‚Ăłw TradingLab.

## 3. Pierwsze ĹşrĂłdĹ‚o danych

Pierwszym ĹşrĂłdĹ‚em danych w Data Engine v0.2.0 bÄ™dzie:

> Polygon/Massive Forex API w planie darmowym.

Pierwszy instrument referencyjny:

> EUR/USD.

Pierwszy typ danych:

> historyczne Ĺ›wiece OHLCV.

Pierwszy konektor referencyjny:

> `PolygonForexConnector`.

W v0.2.0 korzystamy z Polygon/Massive Free, poniewaĹĽ zapewnia prosty i uporzÄ…dkowany interfejs API, ktĂłry dobrze pasuje do pierwszego konektora Data Engine.

Zaakceptowane ograniczenia darmowego planu:

* ograniczony zakres historii,
* brak zaĹ‚oĹĽenia pracy real-time,
* brak wymogu pĹ‚atnego planu,
* brak wymogu peĹ‚nej historii danych.

Architektura Data Engine nie moĹĽe zakĹ‚adaÄ‡, ĹĽe Polygon/Massive jest jedynym ĹşrĂłdĹ‚em prawdy.

W przyszĹ‚oĹ›ci moĹĽliwe bÄ™dzie dodanie kolejnych ĹşrĂłdeĹ‚ danych, w szczegĂłlnoĹ›ci Dukascopy jako darmowego ĹşrĂłdĹ‚a badawczego dla dĹ‚uĹĽszej historii Forex.

## 4. Dalszy rozwĂłj ĹşrĂłdeĹ‚ danych

W przyszĹ‚oĹ›ci Data Engine powinien umoĹĽliwiaÄ‡ dodawanie kolejnych providerĂłw danych bez przebudowy fundamentu systemu.

Potencjalne ĹşrĂłdĹ‚a danych na przyszĹ‚oĹ›Ä‡:

* Dukascopy,
* Twelve Data,
* Alpha Vantage,
* OANDA,
* inne ĹşrĂłdĹ‚a danych Forex, akcji, indeksĂłw, krypto lub kontraktĂłw.

Dukascopy jest kandydatem na drugie ĹşrĂłdĹ‚o danych, poniewaĹĽ moĹĽe dostarczaÄ‡ bardzo dobre darmowe dane historyczne Forex. Wymaga jednak wiÄ™kszej pracy po stronie Data Engine, szczegĂłlnie jeĹ›li dane tickowe bÄ™dÄ… agregowane do Ĺ›wiec OHLCV.

W przyszĹ‚oĹ›ci moĹĽliwe bÄ™dzie porĂłwnywanie wielu ĹşrĂłdeĹ‚ danych oraz ich rankingowanie. Ranking ĹşrĂłdĹ‚a nie musi byÄ‡ globalny. Dla jednej strategii lepsze moĹĽe byÄ‡ jedno ĹşrĂłdĹ‚o, a dla innej strategii inne.

Data Engine powinien wiÄ™c umoĹĽliwiaÄ‡ ocenÄ™ datasetu w kontekĹ›cie:

* instrumentu,
* interwaĹ‚u,
* okresu historycznego,
* typu strategii,
* jakoĹ›ci danych,
* kompletnoĹ›ci danych,
* sposobu agregacji,
* dostÄ™pnoĹ›ci bid/ask/spread,
* stabilnoĹ›ci ĹşrĂłdĹ‚a.

W v0.2.0 ranking ĹşrĂłdeĹ‚ nie jest implementowany. Architektura powinna jednak nie zamykaÄ‡ tej moĹĽliwoĹ›ci.

## 5. Format zapisu danych

W v0.2.0 dane sÄ… zapisywane w czterech podstawowych elementach:

```text
raw/response.json
normalized/candles.csv
metadata.json
validation_report.json
```

### 5.1. Raw data

Surowe dane sÄ… zapisywane jako:

```text
raw/response.json
```

Dla pierwszego ĹşrĂłdĹ‚a, czyli Polygon/Massive, raw data oznaczajÄ… moĹĽliwie wiernie zapisanÄ… odpowiedĹş providera.

Raw data sÄ… nietykalne. Nie wolno ich nadpisywaÄ‡ ani modyfikowaÄ‡ po utworzeniu wersji datasetu.

### 5.2. Normalized data

Znormalizowane Ĺ›wiece OHLCV sÄ… zapisywane jako:

```text
normalized/candles.csv
```

Minimalny format `candles.csv`:

```csv
timestamp_utc,open,high,low,close,volume
2024-01-02T00:00:00Z,1.1034,1.1048,1.0921,1.0945,12345
```

Kolumny:

* `timestamp_utc`,
* `open`,
* `high`,
* `low`,
* `close`,
* `volume`.

Dane w `candles.csv` majÄ… byÄ‡ czystÄ… tabelÄ… Ĺ›wiec. Informacje takie jak provider, dataset_id, symbol, interwaĹ‚ i zakres dat powinny znajdowaÄ‡ siÄ™ w `metadata.json`.

### 5.3. Volume dla Forex

Dla danych Forex pole `volume` moĹĽe mieÄ‡ inne znaczenie niĹĽ wolumen gieĹ‚dowy znany z rynku akcji.

W zaleĹĽnoĹ›ci od providera `volume` moĹĽe oznaczaÄ‡ miÄ™dzy innymi:

* wolumen raportowany przez providera,
* tick volume,
* liczbÄ™ kwotowaĹ„,
* innÄ… metrykÄ™ zaleĹĽnÄ… od ĹşrĂłdĹ‚a danych.

Data Engine v0.2.0 zapisuje pole `volume` jako czÄ™Ĺ›Ä‡ standardu OHLCV, ale nie interpretuje go jeszcze jako peĹ‚nego wolumenu transakcyjnego.

Znaczenie pola `volume` powinno byÄ‡ w przyszĹ‚oĹ›ci doprecyzowywane na poziomie providera i metadanych datasetu.

### 5.4. Metadane

Metadane datasetu sÄ… zapisywane jako:

```text
metadata.json
```

### 5.5. Raport walidacji

Raport walidacji jest zapisywany jako:

```text
validation_report.json
```

## 6. Dalszy rozwĂłj formatĂłw zapisu

CSV jest formatem startowym dla v0.2.0. Nie jest docelowym ograniczeniem architektury.

W przyszĹ‚oĹ›ci moĹĽliwe jest dodanie innych formatĂłw zapisu, w szczegĂłlnoĹ›ci:

* Parquet,
* Feather,
* SQLite,
* DuckDB,
* innych formatĂłw analitycznych.

Architektura Data Engine nie powinna byÄ‡ trwale zwiÄ…zana z CSV.

Dodanie nowego formatu zapisu nie moĹĽe uniewaĹĽniaÄ‡ datasetĂłw zapisanych wczeĹ›niej jako CSV.

## 7. Struktura katalogĂłw danych

Dane Data Engine sÄ… zapisywane lokalnie w katalogu:

```text
data/datasets/
```

KaĹĽdy dataset ma osobny katalog:

```text
data/datasets/{dataset_id}/
```

KaĹĽda wersja datasetu ma osobny podkatalog:

```text
data/datasets/{dataset_id}/v001/
```

PrzykĹ‚adowa struktura:

```text
data/
  datasets/
    polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31/
      v001/
        raw/
          response.json
        normalized/
          candles.csv
        metadata.json
        validation_report.json
```

Prawdziwe dane robocze nie powinny byÄ‡ commitowane do repozytorium.

Do testĂłw automatycznych uĹĽywane sÄ… maĹ‚e przykĹ‚adowe datasety zapisane w:

```text
tests/fixtures/data_engine/
```

PrzykĹ‚adowa struktura danych testowych:

```text
tests/
  fixtures/
    data_engine/
      polygon_forex_eurusd_1d_sample/
        raw/
          response.json
        normalized/
          candles.csv
        metadata.json
        validation_report.json
```

## 8. Sekrety i konfiguracja

API key, tokeny i inne sekrety nie mogÄ… byÄ‡ zapisane:

* w kodzie,
* w dokumentacji,
* w datasetach,
* w plikach commitowanych do repozytorium.

W v0.2.0 klucz Polygon/Massive powinien byÄ‡ przekazywany przez konfiguracjÄ™ lokalnÄ… albo zmiennÄ… Ĺ›rodowiskowÄ….

Testy automatyczne nie mogÄ… wymagaÄ‡ prawdziwego API key.

Data Engine powinien byÄ‡ projektowany tak, aby konfiguracja miaĹ‚a pierwszeĹ„stwo przed wartoĹ›ciami wpisanymi na sztywno w kodzie.

## 9. Status datasetu a status walidacji

W projekcie rozrĂłĹĽniamy:

1. **status datasetu**,
2. **status walidacji**.

Status datasetu znajduje siÄ™ w `metadata.json` i opisuje etap ĹĽycia datasetu.

Status walidacji znajduje siÄ™ w `validation_report.json` i opisuje wynik sprawdzenia technicznej poprawnoĹ›ci danych.

Status datasetu nie zastÄ™puje raportu walidacji.

### 9.1. Statusy datasetu

Status datasetu powinien korzystaÄ‡ ze statusĂłw zdefiniowanych w dokumentacji Data Engine:

```text
RAW
VALIDATED
ACCEPTED
QUARANTINED
REJECTED
DEPRECATED
```

Znaczenie ogĂłlne:

* `RAW` â€” dataset zostaĹ‚ utworzony i zawiera dane ĹşrĂłdĹ‚owe,
* `VALIDATED` â€” dataset przeszedĹ‚ proces walidacji,
* `ACCEPTED` â€” dataset zostaĹ‚ zaakceptowany do dalszego uĹĽycia,
* `QUARANTINED` â€” dataset wymaga uwagi, ale nie musi byÄ‡ od razu odrzucony,
* `REJECTED` â€” dataset nie powinien byÄ‡ uĹĽywany,
* `DEPRECATED` â€” dataset zostaĹ‚ zastÄ…piony albo uznany za przestarzaĹ‚y.

W v0.2.0 peĹ‚ny workflow akceptacji datasetu moĹĽe byÄ‡ jeszcze minimalny, ale metadane powinny byÄ‡ zgodne z tym modelem statusĂłw.

### 9.2. Statusy walidacji

Raport walidacji uĹĽywa osobnych statusĂłw:

```text
valid
valid_with_warnings
invalid
```

Znaczenie:

* `valid` â€” dane przeszĹ‚y walidacjÄ™ bez problemĂłw,
* `valid_with_warnings` â€” dane sÄ… technicznie uĹĽywalne, ale majÄ… ostrzeĹĽenia,
* `invalid` â€” dane nie powinny byÄ‡ uĹĽywane dalej bez poprawy albo ponownego utworzenia datasetu.

PrzykĹ‚ad zgodnoĹ›ci:

```json
{
  "dataset": {
    "status": "VALIDATED"
  }
}
```

oraz:

```json
{
  "status": "valid_with_warnings"
}
```

## 10. Format metadanych datasetu

Metadane datasetu sÄ… zapisywane w pliku:

```text
metadata.json
```

Metadane odpowiadajÄ… na pytanie:

> Co to dokĹ‚adnie za dane i jak moĹĽna je odtworzyÄ‡?

Metadane nie zastÄ™pujÄ… raportu walidacji.

Minimalna zawartoĹ›Ä‡ `metadata.json`:

* wersja schematu metadanych,
* dataset_id,
* wersja datasetu,
* status datasetu,
* typ danych,
* ĹşrĂłdĹ‚o danych,
* konektor,
* instrument,
* interwaĹ‚,
* zakres dat,
* timezone,
* Ĺ›cieĹĽki do plikĂłw raw, normalized i validation_report,
* data utworzenia datasetu w UTC,
* informacje o wersji datasetu,
* parametry ĹĽÄ…dania do providera.

PrzykĹ‚adowy format:

```json
{
  "metadata_schema_version": "1.0",
  "dataset": {
    "dataset_id": "polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31",
    "version": "v001",
    "status": "RAW",
    "data_type": "ohlcv_candles"
  },
  "version_info": {
    "version": "v001",
    "created_reason": "initial_creation",
    "previous_version": null
  },
  "source": {
    "provider": "polygon_massive",
    "connector": "polygon_forex",
    "connector_version": "0.1.0",
    "access_plan": "free",
    "endpoint_type": "forex_aggregates"
  },
  "instrument": {
    "asset_class": "forex",
    "symbol": "EURUSD",
    "base_currency": "EUR",
    "quote_currency": "USD"
  },
  "time_range": {
    "requested_start": "2024-01-01",
    "requested_end": "2024-12-31",
    "timezone": "UTC",
    "interval": "1d"
  },
  "request": {
    "endpoint": "forex_aggregates",
    "parameters": {
      "symbol": "EURUSD",
      "multiplier": 1,
      "timespan": "day",
      "from": "2024-01-01",
      "to": "2024-12-31",
      "sort": "asc"
    }
  },
  "data_format": {
    "raw": {
      "format": "json",
      "path": "raw/response.json"
    },
    "normalized": {
      "format": "csv",
      "path": "normalized/candles.csv"
    },
    "validation_report": {
      "format": "json",
      "path": "validation_report.json"
    }
  },
  "created_at_utc": "2026-06-28T09:30:00Z",
  "notes": ""
}
```

W sekcji `request` nie wolno zapisywaÄ‡ API key, tokenĂłw ani innych sekretĂłw.

## 11. Dalszy rozwĂłj metadanych

Format `metadata.json` w v0.2.0 jest minimalnym schematem startowym.

W przyszĹ‚oĹ›ci metadane mogÄ… zostaÄ‡ rozszerzone miÄ™dzy innymi o:

* informacje o licencji i warunkach uĹĽycia danych,
* ograniczenia planu dostawcy danych,
* hash plikĂłw raw i normalized,
* informacje o pochodzeniu danych i przeksztaĹ‚ceniach,
* powiÄ…zania z wczeĹ›niejszymi wersjami datasetu,
* powiÄ…zania z datasetami ĹşrĂłdĹ‚owymi,
* informacje o jakoĹ›ci danych w formie skrĂłconego podsumowania,
* tagi uĹ‚atwiajÄ…ce wyszukiwanie datasetĂłw,
* informacje potrzebne do porĂłwnywania ĹşrĂłdeĹ‚ danych,
* dokĹ‚adniejszy opis znaczenia pola `volume`,
* informacje o licencji i dozwolonym uĹĽyciu danych.

KaĹĽda istotna zmiana struktury `metadata.json` powinna byÄ‡ kontrolowana przez `metadata_schema_version`, tak aby starsze datasety pozostaĹ‚y czytelne.

## 12. Format raportu walidacji

Raport walidacji jest zapisywany jako:

```text
validation_report.json
```

Raport walidacji odpowiada na pytanie:

> Czy dane sÄ… technicznie poprawne i jakie majÄ… problemy?

Minimalna zawartoĹ›Ä‡ raportu:

* `validation_schema_version`,
* `dataset_id`,
* `version`,
* status walidacji,
* `validated_at_utc`,
* `summary`,
* `checks`,
* `errors`,
* `warnings`.

Minimalne statusy walidacji:

```text
valid
valid_with_warnings
invalid
```

PrzykĹ‚adowy format:

```json
{
  "validation_schema_version": "1.0",
  "dataset_id": "polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31",
  "version": "v001",
  "status": "valid_with_warnings",
  "validated_at_utc": "2026-06-28T09:45:00Z",
  "summary": {
    "row_count": 260,
    "actual_start": "2024-01-01T00:00:00Z",
    "actual_end": "2024-12-31T00:00:00Z",
    "errors_count": 0,
    "warnings_count": 1
  },
  "checks": [
    {
      "check_id": "V001",
      "name": "normalized file exists",
      "severity": "error",
      "status": "passed"
    },
    {
      "check_id": "V002",
      "name": "required columns exist",
      "severity": "error",
      "status": "passed"
    }
  ],
  "errors": [],
  "warnings": [
    {
      "code": "W001",
      "message": "Dataset contains gaps. Gap analysis is basic in v0.2.0 and does not use a full Forex market calendar."
    }
  ]
}
```

## 13. Minimalne reguĹ‚y walidacji v0.2.0

W v0.2.0 walidacja sprawdza podstawowÄ… poprawnoĹ›Ä‡ technicznÄ… datasetu OHLCV.

Minimalne reguĹ‚y:

```text
V001 - normalized file exists
V002 - required columns exist
V003 - dataset is not empty
V004 - timestamps are parseable
V005 - timestamps are sorted ascending
V006 - timestamps are unique
V007 - OHLC values are numeric
V008 - OHLC values are not missing
V009 - OHLC prices are non-negative
V010 - OHLC logic is correct
V011 - volume is numeric and non-negative
V012 - actual data range can be determined
V013 - actual data range is compatible with requested range
V014 - timestamps are compatible with declared interval
V015 - basic missing candle detection
```

Walidacja OHLC oznacza co najmniej:

* `high >= open`,
* `high >= close`,
* `high >= low`,
* `low <= open`,
* `low <= close`,
* `low <= high`.

Walidacja zgodnoĹ›ci interwaĹ‚u i brakujÄ…cych Ĺ›wiec w v0.2.0 ma charakter podstawowy.

Data Engine v0.2.0 nie musi jeszcze implementowaÄ‡ peĹ‚nego kalendarza rynku Forex, obsĹ‚ugi Ĺ›wiÄ…t, DST ani szczegĂłĹ‚owych godzin handlu.

Dopuszczalne jest wiÄ™c, ĹĽe czÄ™Ĺ›Ä‡ wykrytych luk bÄ™dzie klasyfikowana jako ostrzeĹĽenie, a nie bĹ‚Ä…d krytyczny.

## 14. Dalszy rozwĂłj raportu walidacji

Format `validation_report.json` w v0.2.0 jest minimalnym schematem startowym.

W przyszĹ‚oĹ›ci raport walidacji moĹĽe zostaÄ‡ rozszerzony miÄ™dzy innymi o:

* analizÄ™ luk wedĹ‚ug kalendarza rynku Forex,
* scoring jakoĹ›ci datasetu,
* metryki kompletnoĹ›ci danych,
* wykrywanie anomalii cenowych,
* porĂłwnywanie datasetĂłw miÄ™dzy providerami,
* ocenÄ™ zgodnoĹ›ci OHLC miÄ™dzy ĹşrĂłdĹ‚ami,
* analizÄ™ spreadu, jeĹ›li dostÄ™pne bÄ™dÄ… dane bid/ask,
* hash plikĂłw uĹĽytych w walidacji,
* ocenÄ™ przydatnoĹ›ci datasetu dla konkretnych typĂłw strategii,
* raporty jakoĹ›ci czytelne dla przyszĹ‚ych agentĂłw AI.

KaĹĽda istotna zmiana struktury `validation_report.json` powinna byÄ‡ kontrolowana przez `validation_schema_version`, tak aby starsze raporty pozostaĹ‚y moĹĽliwe do odczytania.

## 15. SposĂłb generowania dataset_id

`dataset_id` jest czytelnym, deterministycznym identyfikatorem datasetu.

Format:

```text
{provider}_{asset_class}_{symbol}_{data_type}_{price_type}_{interval}_{start}_{end}
```

PrzykĹ‚ad:

```text
polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31
```

Zasady:

* `dataset_id` nie zawiera numeru wersji,
* wersja jest zapisywana osobno jako `v001`, `v002`, `v003`,
* wszystko zapisujemy maĹ‚ymi literami,
* nie uĹĽywamy spacji,
* nie uĹĽywamy znakĂłw specjalnych typu `/`,
* `EUR/USD` zapisujemy jako `eurusd`,
* daty zapisujemy jako `YYYY-MM-DD`.

Daty w `dataset_id` oznaczajÄ… zakres ĹĽÄ…dany od ĹşrĂłdĹ‚a danych, a nie faktyczny zakres zwrĂłconych danych.

Faktyczny zakres danych jest zapisywany w `validation_report.json`.

Pole `price_type` okreĹ›la typ ceny albo sposĂłb agregacji.

PrzykĹ‚adowe przyszĹ‚e wartoĹ›ci:

* `provider`,
* `bid`,
* `ask`,
* `mid`.

W v0.2.0 dla Polygon/Massive Free uĹĽywamy:

```text
price_type = provider
```

Oznacza to, ĹĽe przyjmujemy gotowe bary zwrĂłcone przez providera.

W przyszĹ‚oĹ›ci mechanizm `dataset_id` moĹĽe zostaÄ‡ rozszerzony o fingerprint albo hash parametrĂłw pobrania, jeĹ›li pojawi siÄ™ potrzeba rozrĂłĹĽniania datasetĂłw o podobnym opisie, ale rĂłĹĽnej konfiguracji ĹşrĂłdĹ‚owej.

## 16. Wersjonowanie datasetĂłw

KaĹĽdy dataset posiada:

* `dataset_id`,
* jednÄ… lub wiÄ™cej wersji.

Wersje sÄ… zapisywane jako:

```text
v001
v002
v003
```

PrzykĹ‚ad:

```text
data/datasets/{dataset_id}/v001/
data/datasets/{dataset_id}/v002/
data/datasets/{dataset_id}/v003/
```

Pierwsza wersja datasetu ma numer:

```text
v001
```

Kolejne wersje tworzone sÄ… przez znalezienie nastÄ™pnego wolnego numeru wersji.

IstniejÄ…cych wersji nie nadpisujemy.

## 17. Kiedy powstaje nowy dataset

Nowy `dataset_id` powstaje, gdy zmienia siÄ™ toĹĽsamoĹ›Ä‡ datasetu.

Elementy toĹĽsamoĹ›ci datasetu:

* provider,
* asset_class,
* symbol,
* data_type,
* price_type,
* interval,
* requested_start,
* requested_end.

Zmiana interwaĹ‚u z `1d` na `1h` tworzy nowy dataset.

Zmiana zakresu dat tworzy nowy dataset.

Zmiana providera tworzy nowy dataset.

## 18. Kiedy powstaje nowa wersja datasetu

Nowa wersja tego samego datasetu powstaje wtedy, gdy przy tych samych parametrach toĹĽsamoĹ›ci ponownie tworzymy pakiet danych.

Nowa wersja moĹĽe powstaÄ‡ miÄ™dzy innymi przez:

* ponowne pobranie danych,
* zmianÄ™ wersji konektora,
* zmianÄ™ logiki normalizacji,
* zmianÄ™ schematu metadanych,
* zmianÄ™ schematu raportu walidacji,
* naprawÄ™ bĹ‚Ä™du w przetwarzaniu,
* rÄ™czne przebudowanie datasetu.

KaĹĽda wersja datasetu powinna zawieraÄ‡ w `metadata.json` sekcjÄ™ `version_info` z numerem wersji, powodem utworzenia wersji oraz opcjonalnym wskazaniem poprzedniej wersji.

PrzykĹ‚ad:

```json
{
  "version_info": {
    "version": "v002",
    "created_reason": "refetch_same_parameters",
    "previous_version": "v001"
  }
}
```

PrzykĹ‚adowe wartoĹ›ci `created_reason`:

```text
initial_creation
refetch_same_parameters
connector_change
normalization_change
metadata_schema_change
validation_schema_change
manual_rebuild
```

Po utworzeniu wersji datasetu nie modyfikujemy jej zawartoĹ›ci. JeĹ›li konieczna jest zmiana danych, metadanych, normalizacji lub raportu walidacji, tworzona jest nowa wersja datasetu.

W v0.2.0 nie tworzymy katalogu `latest`.

Odczyt datasetu powinien wskazywaÄ‡ konkretny:

```text
dataset_id + version
```

## 19. Minimalny interfejs Data Engine

Minimalny publiczny interfejs Data Engine w v0.2.0 obejmuje:

1. `create_dataset`,
2. `validate_dataset`,
3. `load_metadata`,
4. `load_validation_report`,
5. `load_normalized_candles`.

### 19.1. create_dataset

Tworzy nowÄ… wersjÄ™ datasetu na podstawie ĹĽÄ…dania danych.

Odpowiada za:

* pobranie danych ze ĹşrĂłdĹ‚a,
* zapis raw data,
* normalizacjÄ™ OHLCV,
* zapis `metadata.json`,
* wykonanie walidacji,
* zapis `validation_report.json`.

Logika:

```text
create_dataset(request) -> dataset_reference
```

Request powinien zawieraÄ‡ co najmniej:

* provider,
* asset_class,
* symbol,
* data_type,
* price_type,
* interval,
* requested_start,
* requested_end.

Wynik powinien zawieraÄ‡ co najmniej:

* dataset_id,
* version,
* path,
* dataset_status,
* validation_status.

### 19.2. validate_dataset

Wykonuje walidacjÄ™ istniejÄ…cej wersji datasetu i zapisuje `validation_report.json`.

### 19.3. load_metadata

Wczytuje `metadata.json` dla wskazanego `dataset_id` i wersji.

### 19.4. load_validation_report

Wczytuje `validation_report.json` dla wskazanego `dataset_id` i wersji.

### 19.5. load_normalized_candles

Wczytuje `normalized/candles.csv` dla wskazanego `dataset_id` i wersji.

## 20. Czego nie ma w interfejsie v0.2.0

W v0.2.0 Data Engine nie posiada jeszcze funkcji:

* `update_dataset`,
* `overwrite_dataset`,
* `get_latest_valid_dataset`,
* porĂłwnywania ĹşrĂłdeĹ‚,
* rankingu datasetĂłw,
* rankingu providerĂłw,
* obsĹ‚ugi wielu providerĂłw naraz,
* obsĹ‚ugi wielu instrumentĂłw naraz,
* obsĹ‚ugi live tradingu,
* obsĹ‚ugi strategii,
* obsĹ‚ugi backtestingu,
* obsĹ‚ugi agentĂłw AI.

## 21. Dalszy rozwĂłj interfejsu Data Engine

Minimalny interfejs Data Engine w v0.2.0 jest interfejsem startowym.

W przyszĹ‚oĹ›ci Data Engine moĹĽe zostaÄ‡ rozszerzony miÄ™dzy innymi o:

* obsĹ‚ugÄ™ wielu providerĂłw danych,
* obsĹ‚ugÄ™ Dukascopy jako drugiego ĹşrĂłdĹ‚a,
* pobieranie wielu instrumentĂłw,
* pobieranie wielu interwaĹ‚Ăłw,
* aktualizowanie datasetĂłw przez tworzenie nowych wersji,
* pobieranie brakujÄ…cych zakresĂłw danych,
* Ĺ‚Ä…czenie datasetĂłw,
* porĂłwnywanie datasetĂłw miÄ™dzy ĹşrĂłdĹ‚ami,
* ranking jakoĹ›ci ĹşrĂłdeĹ‚ danych,
* ocenÄ™ przydatnoĹ›ci datasetu dla konkretnej strategii,
* obsĹ‚ugÄ™ formatĂłw innych niĹĽ CSV,
* cache danych,
* interfejs CLI,
* interfejs dla przyszĹ‚ych moduĹ‚Ăłw badawczych,
* interfejs dla przyszĹ‚ych agentĂłw AI.

Rozszerzenia interfejsu powinny byÄ‡ dodawane stopniowo i dopiero po wczeĹ›niejszym zaprojektowaniu.

Publiczny interfejs Data Engine powinien operowaÄ‡ na pojÄ™ciach domenowych, takich jak:

* dataset,
* dataset_id,
* version,
* provider,
* instrument,
* interval,
* time_range.

Publiczny interfejs nie powinien byÄ‡ projektowany pod szczegĂłĹ‚y konkretnego API.

SzczegĂłĹ‚y providera powinny byÄ‡ ukryte w konektorach.

## 22. KompatybilnoĹ›Ä‡ wsteczna

RozwĂłj Data Engine powinien zachowywaÄ‡ kompatybilnoĹ›Ä‡ wstecznÄ….

Nowe funkcje nie mogÄ…:

* uniewaĹĽniaÄ‡ istniejÄ…cych datasetĂłw,
* zmieniaÄ‡ znaczenia wczeĹ›niejszych wersji,
* wymuszaÄ‡ modyfikacji danych juĹĽ zapisanych,
* nadpisywaÄ‡ istniejÄ…cych wersji datasetĂłw,
* zmieniaÄ‡ znaczenia istniejÄ…cych operacji publicznego interfejsu.

W szczegĂłlnoĹ›ci:

* istniejÄ…ce datasety i ich wersje muszÄ… pozostaÄ‡ moĹĽliwe do odczytania,
* stare `metadata.json` i `validation_report.json` muszÄ… pozostaÄ‡ interpretowalne przez wersjÄ™ schematu,
* dodanie nowego providera nie moĹĽe zmieniaÄ‡ znaczenia datasetĂłw z wczeĹ›niejszych providerĂłw,
* dodanie nowego formatu zapisu nie moĹĽe uniewaĹĽniaÄ‡ datasetĂłw zapisanych jako CSV,
* dodanie funkcji typu `get_latest_valid_dataset` nie moĹĽe zastÄ…piÄ‡ moĹĽliwoĹ›ci jawnego odczytu przez `dataset_id + version`,
* nowe funkcje nie powinny nadpisywaÄ‡ ani modyfikowaÄ‡ istniejÄ…cych wersji datasetĂłw.

JeĹĽeli w przyszĹ‚oĹ›ci konieczna bÄ™dzie zmiana niekompatybilna wstecznie, musi zostaÄ‡ wczeĹ›niej opisana w dokumentacji albo ADR oraz powinna mieÄ‡ jasnÄ… Ĺ›cieĹĽkÄ™ migracji.

## 23. Minimalna struktura moduĹ‚Ăłw w src/tradinglab

Minimalna struktura kodu Data Engine:

```text
src/
  tradinglab/
    __init__.py
    main.py

    data_engine/
      __init__.py
      engine.py
      models.py
      dataset_id.py
      storage.py
      validation.py

      connectors/
        __init__.py
        base.py
        polygon_forex.py
```

OdpowiedzialnoĹ›ci:

| Plik / katalog                | OdpowiedzialnoĹ›Ä‡                                            |
| ----------------------------- | ----------------------------------------------------------- |
| `data_engine/`                | gĹ‚Ăłwny moduĹ‚ Data Engine                                    |
| `engine.py`                   | publiczny interfejs Data Engine                             |
| `models.py`                   | modele requestĂłw, referencji datasetu, metadanych i raportu |
| `dataset_id.py`               | generowanie `dataset_id`                                    |
| `storage.py`                  | zapis i odczyt plikĂłw datasetu                              |
| `validation.py`               | walidacja `candles.csv` i tworzenie raportu                 |
| `connectors/base.py`          | bazowy interfejs konektora danych                           |
| `connectors/polygon_forex.py` | pierwszy konektor Polygon/Massive Forex                     |
| `main.py`                     | na razie moĹĽe pozostaÄ‡ minimalny                            |

W v0.2.0 nie tworzymy jeszcze moduĹ‚Ăłw:

* strategii,
* backtestingu,
* agentĂłw AI,
* rankingu ĹşrĂłdeĹ‚,
* live tradingu,
* brokerĂłw,
* egzekucji zleceĹ„.

## 24. Zasady stabilnego rozwoju struktury kodu

Struktura Data Engine ma wspieraÄ‡ stabilny rozwĂłj projektu.

Nowe funkcje powinny byÄ‡ dodawane przez rozszerzanie architektury, a nie przez zmianÄ™ znaczenia wczeĹ›niej dziaĹ‚ajÄ…cych elementĂłw.

W szczegĂłlnoĹ›ci:

* dodanie nowego providera nie powinno wymagaÄ‡ przebudowy istniejÄ…cego konektora Polygon/Massive,
* dodanie Dukascopy nie powinno zmieniaÄ‡ dziaĹ‚ania datasetĂłw utworzonych z Polygon/Massive,
* dodanie nowego formatu zapisu, np. Parquet, nie powinno uniewaĹĽniaÄ‡ CSV,
* dodanie nowych reguĹ‚ walidacji nie powinno psuÄ‡ odczytu starszych raportĂłw walidacji,
* dodanie nowych pĂłl w `metadata.json` nie powinno uniemoĹĽliwiaÄ‡ odczytu starszych metadanych,
* stare datasety powinny pozostaÄ‡ odczytywalne przez `dataset_id + version`,
* istniejÄ…ce wersje datasetĂłw nie powinny byÄ‡ modyfikowane ani nadpisywane,
* publiczny interfejs Data Engine powinien byÄ‡ moĹĽliwie stabilny.

Data Engine powinien mieÄ‡ wyraĹşnie oddzielone:

* publiczny interfejs,
* modele danych,
* konektory providerĂłw,
* zapis i odczyt plikĂłw,
* walidacjÄ™,
* logikÄ™ generowania `dataset_id`.

RozszerzalnoĹ›Ä‡ nie oznacza tworzenia nadmiarowych moduĹ‚Ăłw na zapas.

W v0.2.0 struktura kodu ma pozostaÄ‡ minimalna. Nowe warstwy, katalogi i abstrakcje dodajemy dopiero wtedy, gdy wynikajÄ… z realnych potrzeb projektu.

## 25. Minimalny zakres testĂłw v0.2.0

Testy Data Engine w v0.2.0 majÄ… dziaĹ‚aÄ‡ lokalnie i powtarzalnie.

Testy automatyczne nie mogÄ… wymagaÄ‡:

* prawdziwego API key,
* internetu,
* dostÄ™pnoĹ›ci zewnÄ™trznego providera,
* limitĂłw API,
* prawdziwego katalogu roboczego `data/datasets/`.

Do testĂłw uĹĽywane sÄ…:

* lokalne dane przykĹ‚adowe,
* fixtures,
* katalogi tymczasowe tworzone przez pytest.

Minimalny zakres testĂłw obejmuje:

* generowanie `dataset_id`,
* tworzenie struktury katalogĂłw datasetu,
* zapis i odczyt raw data,
* zapis i odczyt normalized candles,
* zapis i odczyt `metadata.json`,
* zapis i odczyt `validation_report.json`,
* walidacjÄ™ poprawnego pliku `candles.csv`,
* walidacjÄ™ bĹ‚Ä™dnego pliku `candles.csv`,
* tworzenie kolejnych wersji `v001`, `v002` bez nadpisywania,
* odczyt datasetu przez jawne wskazanie `dataset_id` i `version`,
* podstawowÄ… obsĹ‚ugÄ™ bĹ‚Ä™dnych ĹĽÄ…daĹ„ wejĹ›ciowych.

## 26. Proponowana struktura testĂłw

```text
tests/
  test_smoke.py

  data_engine/
    test_dataset_id.py
    test_storage.py
    test_validation.py
    test_engine.py

  fixtures/
    data_engine/
      polygon_forex_eurusd_1d_sample/
        raw/
          response.json
        normalized/
          candles.csv
        metadata.json
        validation_report.json
```

## 27. PrzykĹ‚adowe testy v0.2.0

### 27.1. Test generowania dataset_id

Dla danych:

```text
provider = polygon_massive
asset_class = forex
symbol = EURUSD
data_type = ohlcv
price_type = provider
interval = 1d
requested_start = 2024-01-01
requested_end = 2024-12-31
```

oczekiwany `dataset_id`:

```text
polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31
```

### 27.2. Test zapisu struktury datasetu

Po utworzeniu datasetu powinny istnieÄ‡:

```text
raw/response.json
normalized/candles.csv
metadata.json
validation_report.json
```

### 27.3. Test metadanych

`metadata.json` powinien zawieraÄ‡ co najmniej:

```text
metadata_schema_version
dataset.dataset_id
dataset.version
dataset.status
dataset.data_type
source.provider
source.connector
instrument.symbol
time_range.requested_start
time_range.requested_end
time_range.interval
request.endpoint
request.parameters
created_at_utc
data_format
version_info
```

### 27.4. Test walidacji poprawnych Ĺ›wiec

Poprawny plik `candles.csv` powinien otrzymaÄ‡ status:

```text
valid
```

albo:

```text
valid_with_warnings
```

### 27.5. Test walidacji bĹ‚Ä™dnych Ĺ›wiec

Dla bĹ‚Ä™dnego pliku, na przykĹ‚ad z sytuacjÄ…:

```text
high < low
```

raport powinien otrzymaÄ‡ status:

```text
invalid
```

oraz zawieraÄ‡ bĹ‚Ä…d walidacji.

### 27.6. Test wersjonowania

Tworzenie tego samego datasetu po raz pierwszy powinno utworzyÄ‡:

```text
v001
```

Ponowne utworzenie tego samego datasetu powinno utworzyÄ‡:

```text
v002
```

Test powinien potwierdzaÄ‡, ĹĽe `v001` nadal istnieje i nie zostaĹ‚a zmodyfikowana.

### 27.7. Test odczytu konkretnej wersji

Data Engine powinien pozwalaÄ‡ na odczyt konkretnej wersji przez:

```text
dataset_id + version
```

bez uĹĽywania katalogu `latest`.

### 27.8. Test braku sekretĂłw w metadanych

Test powinien potwierdzaÄ‡, ĹĽe `metadata.json` nie zawiera API key, tokenĂłw ani innych sekretĂłw.

## 28. Czego nie testujemy w v0.2.0

W v0.2.0 nie testujemy jeszcze:

* prawdziwego API Polygon/Massive,
* Dukascopy,
* porĂłwnywania ĹşrĂłdeĹ‚,
* rankingu jakoĹ›ci datasetĂłw,
* backtestingu,
* strategii,
* agentĂłw AI,
* wielu instrumentĂłw naraz,
* real-time,
* duĹĽych plikĂłw danych.

## 29. Dalszy rozwĂłj testĂłw

Zakres testĂłw Data Engine powinien rosnÄ…Ä‡ razem z funkcjonalnoĹ›ciÄ….

KaĹĽda nowa publiczna funkcja, nowy provider, nowy format zapisu, nowa reguĹ‚a walidacji albo zmiana schematu metadanych powinna otrzymaÄ‡ test automatyczny.

Testy powinny chroniÄ‡:

* kompatybilnoĹ›Ä‡ wstecznÄ…,
* odczyt wczeĹ›niej utworzonych datasetĂłw,
* brak nadpisywania istniejÄ…cych wersji,
* stabilnoĹ›Ä‡ publicznego interfejsu,
* powtarzalnoĹ›Ä‡ dziaĹ‚ania Data Engine,
* brak przypadkowego uĹĽycia zewnÄ™trznych API w testach offline,
* brak zapisywania sekretĂłw do datasetĂłw.

FunkcjonalnoĹ›Ä‡ Data Engine uznajemy za gotowÄ… dopiero wtedy, gdy przechodzi testy automatyczne.

## 30. ADR dla Data Engine v0.2.0

Decyzje opisane w tym dokumencie majÄ… znaczenie architektoniczne.

Dlatego dla Data Engine v0.2.0 powinien zostaÄ‡ utworzony osobny ADR, na przykĹ‚ad:

```text
dokumentacja/decyzje/ADR-0003-data-engine-v0-2-implementacja.md
```

ADR powinien krĂłtko opisywaÄ‡ najwaĹĽniejsze decyzje:

* wybĂłr Polygon/Massive Free jako pierwszego ĹşrĂłdĹ‚a danych,
* EUR/USD jako pierwszy instrument referencyjny,
* raw JSON i normalized CSV jako formaty startowe,
* `metadata.json` i `validation_report.json`,
* strukturÄ™ `data/datasets/{dataset_id}/v001/`,
* deterministyczny `dataset_id`,
* wersjonowanie bez nadpisywania,
* testy offline,
* zasadÄ™ kompatybilnoĹ›ci wstecznej.

PeĹ‚ne szczegĂłĹ‚y techniczne pozostajÄ… w tym dokumencie implementacyjnym.

## 31. Podsumowanie decyzji v0.2.0

W v0.2.0 Data Engine implementuje maĹ‚y, stabilny fundament:

* jedno ĹşrĂłdĹ‚o danych,
* jeden instrument referencyjny,
* jeden typ danych,
* prosty format zapisu,
* metadane,
* walidacjÄ™,
* wersjonowanie,
* testy offline.

Decyzje gĹ‚Ăłwne:

```text
ĹąrĂłdĹ‚o danych: Polygon/Massive Free
Instrument: EUR/USD
Typ danych: historyczne Ĺ›wiece OHLCV
Raw data: raw/response.json
Normalized data: normalized/candles.csv
Metadane: metadata.json
Raport walidacji: validation_report.json
Struktura: data/datasets/{dataset_id}/v001/
Testy: offline, fixtures, katalog tymczasowy
```

Data Engine v0.2.0 ma byÄ‡ maĹ‚ym krokiem, ale zaprojektowanym tak, aby w przyszĹ‚oĹ›ci moĹĽliwy byĹ‚ rozwĂłj bez rozwalania wczeĹ›niejszych, dziaĹ‚ajÄ…cych wersji.
