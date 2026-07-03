# Projekt implementacji Data Engine v0.2.0

## 1. Cel dokumentu

Ten dokument opisuje projekt implementacji modułu **Data Engine** dla etapu **v0.2.0** projektu TradingLab.

Dokument nie jest jeszcze opisem gotowego kodu. Jest projektem technicznym, który ma poprzedzać implementację.

Zasada pracy:

> Najpierw projektujemy, potem kodujemy.

Implementacja Data Engine v0.2.0 powinna wynikać z tego dokumentu oraz z dokumentów nadrzędnych projektu, w szczególności:

* `README.md`,
* `dokumentacja/architektura/KONSTYTUCJA.md`,
* `dokumentacja/architektura/ARCHITEKTURA.md`,
* `dokumentacja/architektura/DATA_ENGINE.md`,
* `dokumentacja/mapa_drogowa/ROADMAP.md`,
* `dokumentacja/decyzje/ADR-0001-fundamenty-projektu.md`,
* `dokumentacja/decyzje/ADR-0002-narzedzia-testow-i-jakosci-kodu.md`.

## 2. Zakres Data Engine v0.2.0

Data Engine w v0.2.0 odpowiada za pierwszy minimalny cykl życia datasetu danych rynkowych.

Zakres obejmuje:

1. pobranie danych z jednego źródła,
2. zapis surowych danych,
3. normalizację danych do formatu OHLCV,
4. zapis metadanych datasetu,
5. walidację danych,
6. zapis raportu walidacji,
7. wersjonowanie datasetów,
8. odczyt zapisanych elementów datasetu,
9. podstawowe testy automatyczne.

Data Engine nie jest:

* strategią tradingową,
* backtesterem,
* traderem,
* modułem live tradingu,
* rankingiem źródeł danych,
* agentem AI.

Data Engine jest fundamentem danych rynkowych dla przyszłych modułów TradingLab.

## 3. Pierwsze źródło danych

Pierwszym źródłem danych w Data Engine v0.2.0 będzie:

> Polygon/Massive Forex API w planie darmowym.

Pierwszy instrument referencyjny:

> EUR/USD.

Pierwszy typ danych:

> historyczne świece OHLCV.

Pierwszy konektor referencyjny:

> `PolygonForexConnector`.

W v0.2.0 korzystamy z Polygon/Massive Free, ponieważ zapewnia prosty i uporządkowany interfejs API, który dobrze pasuje do pierwszego konektora Data Engine.

Zaakceptowane ograniczenia darmowego planu:

* ograniczony zakres historii,
* brak założenia pracy real-time,
* brak wymogu płatnego planu,
* brak wymogu pełnej historii danych.

Architektura Data Engine nie może zakładać, że Polygon/Massive jest jedynym źródłem prawdy.

W przyszłości możliwe będzie dodanie kolejnych źródeł danych, w szczególności Dukascopy jako darmowego źródła badawczego dla dłuższej historii Forex.

## 4. Dalszy rozwój źródeł danych

W przyszłości Data Engine powinien umożliwiać dodawanie kolejnych providerów danych bez przebudowy fundamentu systemu.

Potencjalne źródła danych na przyszłość:

* Dukascopy,
* Twelve Data,
* Alpha Vantage,
* OANDA,
* inne źródła danych Forex, akcji, indeksów, krypto lub kontraktów.

Dukascopy jest kandydatem na drugie źródło danych, ponieważ może dostarczać bardzo dobre darmowe dane historyczne Forex. Wymaga jednak większej pracy po stronie Data Engine, szczególnie jeśli dane tickowe będą agregowane do świec OHLCV.

W przyszłości możliwe będzie porównywanie wielu źródeł danych oraz ich rankingowanie. Ranking źródła nie musi być globalny. Dla jednej strategii lepsze może być jedno źródło, a dla innej strategii inne.

Data Engine powinien więc umożliwiać ocenę datasetu w kontekście:

* instrumentu,
* interwału,
* okresu historycznego,
* typu strategii,
* jakości danych,
* kompletności danych,
* sposobu agregacji,
* dostępności bid/ask/spread,
* stabilności źródła.

W v0.2.0 ranking źródeł nie jest implementowany. Architektura powinna jednak nie zamykać tej możliwości.

## 5. Format zapisu danych

W v0.2.0 dane są zapisywane w czterech podstawowych elementach:

```text
raw/response.json
normalized/candles.csv
metadata.json
validation_report.json
```

### 5.1. Raw data

Surowe dane są zapisywane jako:

```text
raw/response.json
```

Dla pierwszego źródła, czyli Polygon/Massive, raw data oznaczają możliwie wiernie zapisaną odpowiedź providera.

Raw data są nietykalne. Nie wolno ich nadpisywać ani modyfikować po utworzeniu wersji datasetu.

### 5.2. Normalized data

Znormalizowane świece OHLCV są zapisywane jako:

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

Dane w `candles.csv` mają być czystą tabelą świec. Informacje takie jak provider, dataset_id, symbol, interwał i zakres dat powinny znajdować się w `metadata.json`.

### 5.3. Volume dla Forex

Dla danych Forex pole `volume` może mieć inne znaczenie niż wolumen giełdowy znany z rynku akcji.

W zależności od providera `volume` może oznaczać między innymi:

* wolumen raportowany przez providera,
* tick volume,
* liczbę kwotowań,
* inną metrykę zależną od źródła danych.

Data Engine v0.2.0 zapisuje pole `volume` jako część standardu OHLCV, ale nie interpretuje go jeszcze jako pełnego wolumenu transakcyjnego.

Znaczenie pola `volume` powinno być w przyszłości doprecyzowywane na poziomie providera i metadanych datasetu.

### 5.4. Metadane

Metadane datasetu są zapisywane jako:

```text
metadata.json
```

### 5.5. Raport walidacji

Raport walidacji jest zapisywany jako:

```text
validation_report.json
```

### 5.6. Ścieżka dojścia od `data.csv` do docelowej struktury datasetu

Obecna implementacja Data Engine używa uproszczonego artefaktu:

```text
data.csv
```

Ten plik pełni rolę tymczasowego pliku ze znormalizowanymi świecami OHLCV.

Nie jest to docelowa struktura datasetu v0.2.0.

Model uproszczony został użyty jako etap przejściowy, żeby bezpiecznie domknąć mały, działający pion implementacji:

* modele danych,
* generowanie `dataset_id`,
* budowanie katalogu wersji datasetu,
* zapis i odczyt `metadata.json`,
* zapis i odczyt `validation_report.json`,
* zapis i odczyt OHLCV CSV,
* walidację OHLCV,
* statusy datasetu i statusy walidacji,
* testy automatyczne.

Docelowa struktura datasetu Data Engine v0.2.0 to:

```text
data/datasets/{dataset_id}/{version}/
  raw/
    response.json
  normalized/
    candles.csv
  metadata.json
  validation_report.json
```

Znaczenie artefaktów docelowych:

* `raw/response.json` — możliwie wierny zapis odpowiedzi providera,
* `normalized/candles.csv` — znormalizowane świece OHLCV używane przez system,
* `metadata.json` — opis datasetu, jego źródła, parametrów i statusu życia datasetu,
* `validation_report.json` — wynik technicznej walidacji danych.

Migracja z uproszczonego `data.csv` do docelowej struktury zostanie wykonana mikro-krokami.

Plan migracji:

1. zapisać decyzję architektoniczną w dokumentacji,
2. dodać helpery storage dla `raw/` i `normalized/`,
3. dodać testy nowych helperów storage,
4. przepiąć `create_dataset` na tworzenie katalogów `raw/` i `normalized/`,
5. przepiąć zapis OHLCV z `data.csv` na `normalized/candles.csv`,
6. dodać przejściowy zapis `raw/response.json` dla sample datasetu,
7. przepiąć walidator i sample dataset na `normalized/candles.csv`,
8. wygasić albo usunąć tymczasowy `data.csv`,
9. zaktualizować testy i dokumentację po zakończeniu migracji.

Do czasu zakończenia migracji `data.csv` pozostaje świadomym artefaktem przejściowym, a nie docelowym formatem datasetu.

## 6. Dalszy rozwój formatów zapisu

CSV jest formatem startowym dla v0.2.0. Nie jest docelowym ograniczeniem architektury.

W przyszłości możliwe jest dodanie innych formatów zapisu, w szczególności:

* Parquet,
* Feather,
* SQLite,
* DuckDB,
* innych formatów analitycznych.

Architektura Data Engine nie powinna być trwale związana z CSV.

Dodanie nowego formatu zapisu nie może unieważniać datasetów zapisanych wcześniej jako CSV.

## 7. Struktura katalogów danych

Dane Data Engine są zapisywane lokalnie w katalogu:

```text
data/datasets/
```

Każdy dataset ma osobny katalog:

```text
data/datasets/{dataset_id}/
```

Każda wersja datasetu ma osobny podkatalog:

```text
data/datasets/{dataset_id}/v001/
```

Przykładowa struktura:

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

Prawdziwe dane robocze nie powinny być commitowane do repozytorium.

Do testów automatycznych używane są małe przykładowe datasety zapisane w:

```text
tests/fixtures/data_engine/
```

Przykładowa struktura danych testowych:

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

API key, tokeny i inne sekrety nie mogą być zapisane:

* w kodzie,
* w dokumentacji,
* w datasetach,
* w plikach commitowanych do repozytorium.

W v0.2.0 klucz Polygon/Massive powinien być przekazywany przez konfigurację lokalną albo zmienną środowiskową.

Testy automatyczne nie mogą wymagać prawdziwego API key.

Data Engine powinien być projektowany tak, aby konfiguracja miała pierwszeństwo przed wartościami wpisanymi na sztywno w kodzie.

## 9. Status datasetu a status walidacji

W projekcie rozróżniamy:

1. **status datasetu**,
2. **status walidacji**.

Status datasetu znajduje się w `metadata.json` i opisuje etap życia datasetu.

Status walidacji znajduje się w `validation_report.json` i opisuje wynik sprawdzenia technicznej poprawności danych.

Status datasetu nie zastępuje raportu walidacji.

### 9.1. Statusy datasetu

Status datasetu powinien korzystać ze statusów zdefiniowanych w dokumentacji Data Engine:

```text
RAW
VALIDATED
ACCEPTED
QUARANTINED
REJECTED
DEPRECATED
```

Znaczenie ogólne:

* `RAW` — dataset został utworzony i zawiera dane źródłowe,
* `VALIDATED` — dataset przeszedł proces walidacji,
* `ACCEPTED` — dataset został zaakceptowany do dalszego użycia,
* `QUARANTINED` — dataset wymaga uwagi, ale nie musi być od razu odrzucony,
* `REJECTED` — dataset nie powinien być używany,
* `DEPRECATED` — dataset został zastąpiony albo uznany za przestarzały.

W v0.2.0 pełny workflow akceptacji datasetu może być jeszcze minimalny, ale metadane powinny być zgodne z tym modelem statusów.

### 9.2. Statusy walidacji

Raport walidacji używa osobnych statusów:

```text
not_validated
valid
valid_with_warnings
invalid
```

Znaczenie:

* `not_validated` — raport walidacji został utworzony technicznie, ale właściwa walidacja datasetu nie została jeszcze wykonana,
* `valid` — dane przeszły walidację bez problemów,
* `valid_with_warnings` — dane są technicznie używalne, ale mają ostrzeżenia,
* `invalid` — dane nie powinny być używane dalej bez poprawy albo ponownego utworzenia datasetu.

`not_validated` jest statusem przejściowym potrzebnym w sytuacji, gdy proces budowania datasetu tworzy początkowy `validation_report.json` przed wykonaniem właściwej walidacji.

Nie wolno używać statusu `invalid` jako zamiennika dla stanu „jeszcze nie walidowano”.

Przykład zgodności:

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

Metadane datasetu są zapisywane w pliku:

```text
metadata.json
```

Metadane odpowiadają na pytanie:

> Co to dokładnie za dane i jak można je odtworzyć?

Metadane nie zastępują raportu walidacji.

Minimalna zawartość `metadata.json`:

* wersja schematu metadanych,
* dataset_id,
* wersja datasetu,
* status datasetu,
* typ danych,
* źródło danych,
* konektor,
* instrument,
* interwał,
* zakres dat,
* timezone,
* ścieżki do plików raw, normalized i validation_report,
* data utworzenia datasetu w UTC,
* informacje o wersji datasetu,
* parametry żądania do providera.

Przykładowy format:

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

W sekcji `request` nie wolno zapisywać API key, tokenów ani innych sekretów.

## 11. Dalszy rozwój metadanych

Format `metadata.json` w v0.2.0 jest minimalnym schematem startowym.

W przyszłości metadane mogą zostać rozszerzone między innymi o:

* informacje o licencji i warunkach użycia danych,
* ograniczenia planu dostawcy danych,
* hash plików raw i normalized,
* informacje o pochodzeniu danych i przekształceniach,
* powiązania z wcześniejszymi wersjami datasetu,
* powiązania z datasetami źródłowymi,
* informacje o jakości danych w formie skróconego podsumowania,
* tagi ułatwiające wyszukiwanie datasetów,
* informacje potrzebne do porównywania źródeł danych,
* dokładniejszy opis znaczenia pola `volume`,
* informacje o licencji i dozwolonym użyciu danych.

Każda istotna zmiana struktury `metadata.json` powinna być kontrolowana przez `metadata_schema_version`, tak aby starsze datasety pozostały czytelne.

## 12. Format raportu walidacji

Raport walidacji jest zapisywany jako:

```text
validation_report.json
```

Raport walidacji odpowiada na pytanie:

> Czy dane są technicznie poprawne i jakie mają problemy?

Minimalna zawartość raportu:

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
not_validated
valid
valid_with_warnings
invalid
```

Przykładowy format:

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

## 13. Minimalne reguły walidacji v0.2.0

W v0.2.0 walidacja sprawdza podstawową poprawność techniczną datasetu OHLCV.

Minimalne reguły:

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

Walidacja zgodności interwału i brakujących świec w v0.2.0 ma charakter podstawowy.

Data Engine v0.2.0 nie musi jeszcze implementować pełnego kalendarza rynku Forex, obsługi świąt, DST ani szczegółowych godzin handlu.

Dopuszczalne jest więc, że część wykrytych luk będzie klasyfikowana jako ostrzeżenie, a nie błąd krytyczny.

## 14. Dalszy rozwój raportu walidacji

Format `validation_report.json` w v0.2.0 jest minimalnym schematem startowym.

W przyszłości raport walidacji może zostać rozszerzony między innymi o:

* analizę luk według kalendarza rynku Forex,
* scoring jakości datasetu,
* metryki kompletności danych,
* wykrywanie anomalii cenowych,
* porównywanie datasetów między providerami,
* ocenę zgodności OHLC między źródłami,
* analizę spreadu, jeśli dostępne będą dane bid/ask,
* hash plików użytych w walidacji,
* ocenę przydatności datasetu dla konkretnych typów strategii,
* raporty jakości czytelne dla przyszłych agentów AI.

Każda istotna zmiana struktury `validation_report.json` powinna być kontrolowana przez `validation_schema_version`, tak aby starsze raporty pozostały możliwe do odczytania.

## 15. Sposób generowania dataset_id

`dataset_id` jest czytelnym, deterministycznym identyfikatorem datasetu.

Format:

```text
{provider}_{asset_class}_{symbol}_{data_type}_{price_type}_{interval}_{start}_{end}
```

Przykład:

```text
polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31
```

Zasady:

* `dataset_id` nie zawiera numeru wersji,
* wersja jest zapisywana osobno jako `v001`, `v002`, `v003`,
* wszystko zapisujemy małymi literami,
* nie używamy spacji,
* nie używamy znaków specjalnych typu `/`,
* `EUR/USD` zapisujemy jako `eurusd`,
* daty zapisujemy jako `YYYY-MM-DD`.

Daty w `dataset_id` oznaczają zakres żądany od źródła danych, a nie faktyczny zakres zwróconych danych.

Faktyczny zakres danych jest zapisywany w `validation_report.json`.

Pole `price_type` określa typ ceny albo sposób agregacji.

Przykładowe przyszłe wartości:

* `provider`,
* `bid`,
* `ask`,
* `mid`.

W v0.2.0 dla Polygon/Massive Free używamy:

```text
price_type = provider
```

Oznacza to, że przyjmujemy gotowe bary zwrócone przez providera.

W przyszłości mechanizm `dataset_id` może zostać rozszerzony o fingerprint albo hash parametrów pobrania, jeśli pojawi się potrzeba rozróżniania datasetów o podobnym opisie, ale różnej konfiguracji źródłowej.

## 16. Wersjonowanie datasetów

Każdy dataset posiada:

* `dataset_id`,
* jedną lub więcej wersji.

Wersje są zapisywane jako:

```text
v001
v002
v003
```

Przykład:

```text
data/datasets/{dataset_id}/v001/
data/datasets/{dataset_id}/v002/
data/datasets/{dataset_id}/v003/
```

Pierwsza wersja datasetu ma numer:

```text
v001
```

Kolejne wersje tworzone są przez znalezienie następnego wolnego numeru wersji.

Istniejących wersji nie nadpisujemy.

## 17. Kiedy powstaje nowy dataset

Nowy `dataset_id` powstaje, gdy zmienia się tożsamość datasetu.

Elementy tożsamości datasetu:

* provider,
* asset_class,
* symbol,
* data_type,
* price_type,
* interval,
* requested_start,
* requested_end.

Zmiana interwału z `1d` na `1h` tworzy nowy dataset.

Zmiana zakresu dat tworzy nowy dataset.

Zmiana providera tworzy nowy dataset.

## 18. Kiedy powstaje nowa wersja datasetu

Nowa wersja tego samego datasetu powstaje wtedy, gdy przy tych samych parametrach tożsamości ponownie tworzymy pakiet danych.

Nowa wersja może powstać między innymi przez:

* ponowne pobranie danych,
* zmianę wersji konektora,
* zmianę logiki normalizacji,
* zmianę schematu metadanych,
* zmianę schematu raportu walidacji,
* naprawę błędu w przetwarzaniu,
* ręczne przebudowanie datasetu.

Każda wersja datasetu powinna zawierać w `metadata.json` sekcję `version_info` z numerem wersji, powodem utworzenia wersji oraz opcjonalnym wskazaniem poprzedniej wersji.

Przykład:

```json
{
  "version_info": {
    "version": "v002",
    "created_reason": "refetch_same_parameters",
    "previous_version": "v001"
  }
}
```

Przykładowe wartości `created_reason`:

```text
initial_creation
refetch_same_parameters
connector_change
normalization_change
metadata_schema_change
validation_schema_change
manual_rebuild
```

Po utworzeniu wersji datasetu nie modyfikujemy jej zawartości. Jeśli konieczna jest zmiana danych, metadanych, normalizacji lub raportu walidacji, tworzona jest nowa wersja datasetu.

W v0.2.0 nie tworzymy katalogu `latest`.

Odczyt datasetu powinien wskazywać konkretny:

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

Tworzy nową wersję datasetu na podstawie żądania danych.

Odpowiada za:

* pobranie danych ze źródła,
* zapis raw data,
* normalizację OHLCV,
* zapis `metadata.json`,
* wykonanie walidacji,
* zapis `validation_report.json`.

Logika:

```text
create_dataset(request) -> dataset_reference
```

Request powinien zawierać co najmniej:

* provider,
* asset_class,
* symbol,
* data_type,
* price_type,
* interval,
* requested_start,
* requested_end.

Wynik powinien zawierać co najmniej:

* dataset_id,
* version,
* path,
* dataset_status,
* validation_status.

### 19.2. validate_dataset

Wykonuje walidację istniejącej wersji datasetu i zapisuje `validation_report.json`.

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
* porównywania źródeł,
* rankingu datasetów,
* rankingu providerów,
* obsługi wielu providerów naraz,
* obsługi wielu instrumentów naraz,
* obsługi live tradingu,
* obsługi strategii,
* obsługi backtestingu,
* obsługi agentów AI.

## 21. Dalszy rozwój interfejsu Data Engine

Minimalny interfejs Data Engine w v0.2.0 jest interfejsem startowym.

W przyszłości Data Engine może zostać rozszerzony między innymi o:

* obsługę wielu providerów danych,
* obsługę Dukascopy jako drugiego źródła,
* pobieranie wielu instrumentów,
* pobieranie wielu interwałów,
* aktualizowanie datasetów przez tworzenie nowych wersji,
* pobieranie brakujących zakresów danych,
* łączenie datasetów,
* porównywanie datasetów między źródłami,
* ranking jakości źródeł danych,
* ocenę przydatności datasetu dla konkretnej strategii,
* obsługę formatów innych niż CSV,
* cache danych,
* interfejs CLI,
* interfejs dla przyszłych modułów badawczych,
* interfejs dla przyszłych agentów AI.

Rozszerzenia interfejsu powinny być dodawane stopniowo i dopiero po wcześniejszym zaprojektowaniu.

Publiczny interfejs Data Engine powinien operować na pojęciach domenowych, takich jak:

* dataset,
* dataset_id,
* version,
* provider,
* instrument,
* interval,
* time_range.

Publiczny interfejs nie powinien być projektowany pod szczegóły konkretnego API.

Szczegóły providera powinny być ukryte w konektorach.

## 22. Kompatybilność wsteczna

Rozwój Data Engine powinien zachowywać kompatybilność wsteczną.

Nowe funkcje nie mogą:

* unieważniać istniejących datasetów,
* zmieniać znaczenia wcześniejszych wersji,
* wymuszać modyfikacji danych już zapisanych,
* nadpisywać istniejących wersji datasetów,
* zmieniać znaczenia istniejących operacji publicznego interfejsu.

W szczególności:

* istniejące datasety i ich wersje muszą pozostać możliwe do odczytania,
* stare `metadata.json` i `validation_report.json` muszą pozostać interpretowalne przez wersję schematu,
* dodanie nowego providera nie może zmieniać znaczenia datasetów z wcześniejszych providerów,
* dodanie nowego formatu zapisu nie może unieważniać datasetów zapisanych jako CSV,
* dodanie funkcji typu `get_latest_valid_dataset` nie może zastąpić możliwości jawnego odczytu przez `dataset_id + version`,
* nowe funkcje nie powinny nadpisywać ani modyfikować istniejących wersji datasetów.

Jeżeli w przyszłości konieczna będzie zmiana niekompatybilna wstecznie, musi zostać wcześniej opisana w dokumentacji albo ADR oraz powinna mieć jasną ścieżkę migracji.

## 23. Minimalna struktura modułów w src/tradinglab

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

Odpowiedzialności:

| Plik / katalog                | Odpowiedzialność                                            |
| ----------------------------- | ----------------------------------------------------------- |
| `data_engine/`                | główny moduł Data Engine                                    |
| `engine.py`                   | publiczny interfejs Data Engine                             |
| `models.py`                   | modele requestów, referencji datasetu, metadanych i raportu |
| `dataset_id.py`               | generowanie `dataset_id`                                    |
| `storage.py`                  | zapis i odczyt plików datasetu                              |
| `validation.py`               | walidacja `candles.csv` i tworzenie raportu                 |
| `connectors/base.py`          | bazowy interfejs konektora danych                           |
| `connectors/polygon_forex.py` | pierwszy konektor Polygon/Massive Forex                     |
| `main.py`                     | na razie może pozostać minimalny                            |

W v0.2.0 nie tworzymy jeszcze modułów:

* strategii,
* backtestingu,
* agentów AI,
* rankingu źródeł,
* live tradingu,
* brokerów,
* egzekucji zleceń.

## 24. Zasady stabilnego rozwoju struktury kodu

Struktura Data Engine ma wspierać stabilny rozwój projektu.

Nowe funkcje powinny być dodawane przez rozszerzanie architektury, a nie przez zmianę znaczenia wcześniej działających elementów.

W szczególności:

* dodanie nowego providera nie powinno wymagać przebudowy istniejącego konektora Polygon/Massive,
* dodanie Dukascopy nie powinno zmieniać działania datasetów utworzonych z Polygon/Massive,
* dodanie nowego formatu zapisu, np. Parquet, nie powinno unieważniać CSV,
* dodanie nowych reguł walidacji nie powinno psuć odczytu starszych raportów walidacji,
* dodanie nowych pól w `metadata.json` nie powinno uniemożliwiać odczytu starszych metadanych,
* stare datasety powinny pozostać odczytywalne przez `dataset_id + version`,
* istniejące wersje datasetów nie powinny być modyfikowane ani nadpisywane,
* publiczny interfejs Data Engine powinien być możliwie stabilny.

Data Engine powinien mieć wyraźnie oddzielone:

* publiczny interfejs,
* modele danych,
* konektory providerów,
* zapis i odczyt plików,
* walidację,
* logikę generowania `dataset_id`.

Rozszerzalność nie oznacza tworzenia nadmiarowych modułów na zapas.

W v0.2.0 struktura kodu ma pozostać minimalna. Nowe warstwy, katalogi i abstrakcje dodajemy dopiero wtedy, gdy wynikają z realnych potrzeb projektu.

## 25. Minimalny zakres testów v0.2.0

Testy Data Engine w v0.2.0 mają działać lokalnie i powtarzalnie.

Testy automatyczne nie mogą wymagać:

* prawdziwego API key,
* internetu,
* dostępności zewnętrznego providera,
* limitów API,
* prawdziwego katalogu roboczego `data/datasets/`.

Do testów używane są:

* lokalne dane przykładowe,
* fixtures,
* katalogi tymczasowe tworzone przez pytest.

Minimalny zakres testów obejmuje:

* generowanie `dataset_id`,
* tworzenie struktury katalogów datasetu,
* zapis i odczyt raw data,
* zapis i odczyt normalized candles,
* zapis i odczyt `metadata.json`,
* zapis i odczyt `validation_report.json`,
* walidację poprawnego pliku `candles.csv`,
* walidację błędnego pliku `candles.csv`,
* tworzenie kolejnych wersji `v001`, `v002` bez nadpisywania,
* odczyt datasetu przez jawne wskazanie `dataset_id` i `version`,
* podstawową obsługę błędnych żądań wejściowych.

### 25.1. Pakiety testów dla małych obszarów Data Engine

Testy Data Engine powinny być domykane pakietami dla małych, konkretnych obszarów funkcjonalnych.

Przykładowe obszary:

* generowanie `dataset_id`,
* modele danych,
* zapis i odczyt plików,
* metadane datasetu,
* raport walidacji,
* walidacja OHLCV,
* wersjonowanie datasetów,
* tworzenie sample datasetu,
* publiczny interfejs Data Engine.

Dla każdego obszaru należy najpierw określić przewidywalne scenariusze testowe, a następnie zaimplementować komplet testów dla tego zakresu.

Nie należy uznawać obszaru za zakończony wyłącznie dlatego, że działa jeden poprawny przykład. Obszar jest zakończony dopiero wtedy, gdy posiada testy dla poprawnego przebiegu, błędów, przypadków granicznych oraz liczników, statusów lub raportów, jeśli dany obszar je generuje.

### 25.2. Macierz scenariuszy walidatora OHLCV

Walidator OHLCV jest domykany jako mały, osobny obszar funkcjonalny Data Engine.

Na obecnym etapie walidator odpowiada za sprawdzenie:

* czy plik CSV da się odczytać jako OHLCV,
* czy dataset zawiera co najmniej jeden rekord danych,
* czy wartości `open`, `high`, `low`, `close` i `volume` są logicznie poprawne,
* czy relacje między `open`, `high`, `low` i `close` są spójne,
* czy timestampy są unikalne,
* czy timestampy idą rosnąco,
* czy raport walidacji poprawnie pokazuje status, błędy i liczniki.

Macierz scenariuszy dla walidatora OHLCV:

| ID        | Scenariusz                                                           | Oczekiwany wynik                                                 | Status                      |
| --------- | -------------------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------- |
| OHLCV-001 | Poprawny dataset z dwoma świecami | `valid`, brak błędów, poprawne liczniki | pokryte testem |
| OHLCV-002 | Niepoprawny nagłówek CSV                                             | `invalid`, błąd struktury pliku                                  | pokryte testem              |
| OHLCV-003 | Poprawny nagłówek CSV, ale zero rekordów danych                      | `invalid`, błąd pustego datasetu                                 | pokryte testem              |
| OHLCV-004 | `volume = 0` oraz świeca płaska `open = high = low = close` | `valid` | pokryte testem |
| OHLCV-005 | `open <= 0`                                                          | `invalid`                                                        | pokryte testem              |
| OHLCV-006 | `high <= 0`                                                          | `invalid`                                                        | pokryte testem              |
| OHLCV-007 | `low <= 0`                                                           | `invalid`                                                        | pokryte testem              |
| OHLCV-008 | `close <= 0`                                                         | `invalid`                                                        | pokryte testem              |
| OHLCV-009 | `volume < 0`                                                         | `invalid`                                                        | pokryte testem              |
| OHLCV-010 | `high < low`                                                         | `invalid`                                                        | pokryte testem              |
| OHLCV-011 | `high < open`                                                        | `invalid`                                                        | pokryte testem              |
| OHLCV-012 | `high < close`                                                       | `invalid`                                                        | pokryte testem              |
| OHLCV-013 | `low > open`                                                         | `invalid`                                                        | pokryte testem              |
| OHLCV-014 | `low > close`                                                        | `invalid`                                                        | pokryte testem              |
| OHLCV-015 | Duplikat timestampu                                                  | `invalid`                                                        | pokryte testem              |
| OHLCV-016 | Timestamp mniejszy lub równy timestampowi z poprzedniego wiersza     | `invalid`                                                        | pokryte testem              |
| OHLCV-017 | Jeden plik zawiera rekord poprawny i rekord błędny                   | `invalid`, poprawne `checked_rows`, `valid_rows`, `invalid_rows` | pokryte testem              |
| OHLCV-018 | Jeden rekord zawiera jednocześnie błąd świecy i błąd timestampu      | rekord liczony jako jeden błędny wiersz                          | pokryte testem              |
| OHLCV-019 | Dataset z trzema rekordami, gdzie tylko środkowy ma błędny timestamp | `invalid`, tylko jeden rekord liczony jako błędny                | pokryte testem              |
| OHLCV-020 | Sample dataset generowany skryptem projektu | raport walidacji `valid`, brak błędów; metadata i wynik datasetu `validated` | sprawdzane testem i ręcznie |

Na obecnym etapie walidator OHLCV można uznać za domknięty dla zakresu v0.2.0.

Przyszłe rozszerzenia mogą obejmować osobne reguły dla interwału świec, stref czasowych, luk w danych, sesji rynkowych albo specyficznych wymagań dla różnych klas instrumentów. Nie należą one jednak do obecnego zakresu walidatora OHLCV.

### 25.3. Macierz scenariuszy zapisu i odczytu OHLCV CSV

Warstwa zapisu i odczytu plików OHLCV CSV jest osobnym, małym obszarem funkcjonalnym Data Engine.

Ten obszar odpowiada za:

* definicję oczekiwanego nagłówka OHLCV CSV,
* konwersję `OhlcvBar` do wiersza CSV,
* konwersję wiersza CSV do `OhlcvBar`,
* zapis pustego pliku CSV z samym nagłówkiem,
* zapis pliku CSV z rekordami danych,
* odczyt pliku CSV do obiektów `OhlcvBar`,
* wykrywanie podstawowych błędów struktury pliku,
* przekazywanie błędów wejścia/wyjścia i błędów konwersji danych do warstwy wywołującej,
* zachowanie spójności danych w cyklu zapis → odczyt.

Macierz scenariuszy dla zapisu i odczytu OHLCV CSV:

| ID           | Scenariusz                                                         | Oczekiwany wynik                                                          | Status         |
| ------------ | ------------------------------------------------------------------ | ------------------------------------------------------------------------- | -------------- |
| DATAFILE-001 | Oczekiwany nagłówek OHLCV CSV                                      | Nagłówek zawiera wymagane kolumny w ustalonej kolejności                  | pokryte testem |
| DATAFILE-002 | Konwersja `OhlcvBar` do wiersza CSV                                | Wartości świecy są zapisane jako tekst w oczekiwanym formacie             | pokryte testem |
| DATAFILE-003 | Konwersja wiersza CSV do `OhlcvBar`                                | Tekstowe wartości są poprawnie konwertowane na `datetime` i `Decimal`     | pokryte testem |
| DATAFILE-004 | Wiersz CSV ma błędną liczbę kolumn                                 | Odczyt pojedynczego wiersza kończy się błędem                             | pokryte testem |
| DATAFILE-005 | Zapis pustego OHLCV CSV                                            | Plik zawiera sam nagłówek bez rekordów danych                             | pokryte testem |
| DATAFILE-006 | Zapis OHLCV CSV z rekordami danych                                 | Plik zawiera nagłówek i wszystkie przekazane rekordy                      | pokryte testem |
| DATAFILE-007 | Odczyt OHLCV CSV z nagłówkiem i rekordami                          | Funkcja zwraca listę obiektów `OhlcvBar`                                  | pokryte testem |
| DATAFILE-008 | Odczyt pliku z niepoprawnym nagłówkiem                             | Odczyt kończy się błędem struktury pliku                                  | pokryte testem |
| DATAFILE-009 | Cykl zapis → odczyt dla OHLCV CSV                                  | Odczytane świece są identyczne z zapisanymi świecami                      | pokryte testem |
| DATAFILE-010 | Próba odczytu nieistniejącego pliku                                | Błąd wejścia/wyjścia jest przekazywany do warstwy wywołującej             | pokryte testem |
| DATAFILE-011 | Fizycznie pusty plik bez nagłówka                                  | Odczyt kończy się błędem nagłówka albo błędem struktury pliku             | pokryte testem |
| DATAFILE-012 | Wiersz danych z brakującą kolumną                                  | Odczyt kończy się błędem długości wiersza                                 | pokryte testem |
| DATAFILE-013 | Wiersz danych z dodatkową kolumną                                  | Odczyt kończy się błędem długości wiersza                                 | pokryte testem |
| DATAFILE-014 | Nieparsowalny timestamp                                            | Odczyt kończy się błędem konwersji danych                                 | pokryte testem |
| DATAFILE-015 | Nieparsowalna wartość `open`, `high`, `low`, `close` albo `volume` | Odczyt kończy się błędem konwersji danych                                 | pokryte testem |
| DATAFILE-016 | Zachowanie dokładnych wartości `Decimal` w cyklu zapis → odczyt    | Wartości po odczycie są równe wartościom przed zapisem                    | pokryte testem |

Na obecnym etapie obszar zapisu i odczytu OHLCV CSV można uznać za domknięty dla zakresu v0.2.0.

Przyszłe rozszerzenia mogą obejmować obsługę innych formatów plików, innych separatorów CSV, wymuszonego kodowania, kompresji danych albo dodatkowych formatów timestampów. Nie należą one jednak do obecnego zakresu warstwy zapisu i odczytu OHLCV CSV.

### 25.4. Macierz scenariuszy metadata datasetu

Warstwa metadata datasetu jest osobnym, małym obszarem funkcjonalnym Data Engine.

Ten obszar odpowiada za:

* reprezentację metadata datasetu w modelu `DatasetMetadata`,
* konwersję `DatasetMetadata` do słownika gotowego do zapisu JSON,
* konwersję słownika odczytanego z JSON do `DatasetMetadata`,
* zapis pliku `metadata.json`,
* odczyt pliku `metadata.json`,
* serializację i deserializację pól daty,
* przekazywanie błędów brakujących pól, błędów JSON, błędów wejścia/wyjścia i błędów parsowania dat do warstwy wywołującej,
* normalizację pól tekstowych do `str` zgodnie z obecną logiką,
* zachowanie znaków spoza ASCII przy zapisie JSON,
* zachowanie spójności danych w cyklu zapis → odczyt.

Macierz scenariuszy dla metadata datasetu:

| ID           | Scenariusz                                                       | Oczekiwany wynik                                                       | Status         |
| ------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| METADATA-001 | Konwersja `DatasetMetadata` do słownika                          | Wszystkie pola są zapisane w oczekiwanym formacie                      | pokryte testem |
| METADATA-002 | Konwersja słownika do `DatasetMetadata`                          | Wszystkie pola są poprawnie odtworzone z danych wejściowych            | pokryte testem |
| METADATA-003 | Zapis `metadata.json`                                            | Plik JSON zostaje utworzony i zawiera oczekiwane dane                  | pokryte testem |
| METADATA-004 | Cykl zapis → odczyt przez JSON i `metadata_from_dict`             | Odtworzone metadata są równe metadata wejściowym                       | pokryte testem |
| METADATA-005 | Odczyt `metadata.json` przez `load_metadata`                     | Funkcja zwraca poprawny obiekt `DatasetMetadata`                       | pokryte testem |
| METADATA-006 | Model `DatasetMetadata` opisuje wersję datasetu EUR/USD          | Model przechowuje podstawowe pola datasetu                             | pokryte testem |
| METADATA-007 | Brak wymaganego pola w danych wejściowych                        | Błąd brakującego pola jest przekazywany do warstwy wywołującej         | pokryte testem |
| METADATA-008 | Niepoprawny format daty `requested_start`                        | Odczyt kończy się błędem parsowania daty                               | pokryte testem |
| METADATA-009 | Niepoprawny format daty `requested_end`                          | Odczyt kończy się błędem parsowania daty                               | pokryte testem |
| METADATA-010 | Niepoprawny JSON w pliku `metadata.json`                         | Odczyt kończy się błędem parsowania JSON                               | pokryte testem |
| METADATA-011 | Próba odczytu nieistniejącego pliku `metadata.json`              | Błąd wejścia/wyjścia jest przekazywany do warstwy wywołującej          | pokryte testem |
| METADATA-012 | Wartości tekstowe przekazane jako typy nietekstowe               | Pola tekstowe są normalizowane do `str` zgodnie z obecną logiką        | pokryte testem |
| METADATA-013 | Zapis metadata z polskimi albo niestandardowymi znakami          | Plik JSON zachowuje znaki dzięki zapisowi UTF-8 i `ensure_ascii=False` | pokryte testem |
| METADATA-014 | Zapis metadata kończy plik znakiem nowej linii                   | Plik kończy się pojedynczym znakiem nowej linii                        | pokryte testem |
| METADATA-015 | Próba modyfikacji istniejącego obiektu `DatasetMetadata`         | Obiekt pozostaje niemutowalny                                          | pokryte testem |

Na obecnym etapie obszar metadata datasetu można uznać za domknięty dla zakresu v0.2.0.

Przyszłe rozszerzenia mogą obejmować walidację dozwolonych wartości pól, osobne schematy metadata dla różnych klas aktywów, jawne wersjonowanie schematu metadata, dodatkowe pola techniczne oraz kontrolę zgodności `dataset_id` z zawartością metadata. Nie należą one jednak do obecnego zakresu warstwy metadata datasetu.

### 25.5. Macierz scenariuszy raportu walidacji

Warstwa raportu walidacji jest osobnym, małym obszarem funkcjonalnym Data Engine.

Ten obszar odpowiada za:

* reprezentację raportu walidacji w modelu `ValidationReport`,
* konwersję `ValidationReport` do słownika gotowego do zapisu JSON,
* konwersję słownika odczytanego z JSON do `ValidationReport`,
* zapis pliku `validation_report.json`,
* odczyt pliku `validation_report.json`,
* przekazywanie błędów brakujących pól, błędów JSON, błędów wejścia/wyjścia i błędów konwersji liczników do warstwy wywołującej,
* normalizację pól tekstowych do `str` zgodnie z obecną logiką,
* zachowanie znaków spoza ASCII przy zapisie JSON,
* zachowanie spójności danych w cyklu zapis → odczyt.

Macierz scenariuszy dla raportu walidacji:

| ID | Scenariusz | Oczekiwany wynik | Status |
| ------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| VALIDATION_REPORT-001 | Konwersja `ValidationReport` do słownika | Wszystkie pola są zapisane w oczekiwanym formacie | pokryte testem |
| VALIDATION_REPORT-002 | Konwersja słownika do `ValidationReport` | Wszystkie pola są poprawnie odtworzone z danych wejściowych | pokryte testem |
| VALIDATION_REPORT-003 | Zapis `validation_report.json` | Plik JSON zostaje utworzony i zawiera oczekiwane dane | pokryte testem |
| VALIDATION_REPORT-004 | Cykl zapis → odczyt przez JSON i `validation_report_from_dict` | Odtworzony raport jest równy raportowi wejściowemu | pokryte testem |
| VALIDATION_REPORT-005 | Odczyt `validation_report.json` przez `load_validation_report` | Funkcja zwraca poprawny obiekt `ValidationReport` | pokryte testem |
| VALIDATION_REPORT-006 | Model `ValidationReport` opisuje poprawny dataset | Model przechowuje status, błędy, ostrzeżenia i liczniki | pokryte testem |
| VALIDATION_REPORT-007 | Model `ValidationReport` opisuje niepoprawny dataset | Model przechowuje status `invalid`, błędy, ostrzeżenia i liczniki | pokryte testem |
| VALIDATION_REPORT-008 | Brak wymaganego pola w danych wejściowych | Błąd brakującego pola jest przekazywany do warstwy wywołującej | pokryte testem |
| VALIDATION_REPORT-009 | Niepoprawny JSON w pliku `validation_report.json` | Odczyt kończy się błędem parsowania JSON | pokryte testem |
| VALIDATION_REPORT-010 | Próba odczytu nieistniejącego pliku `validation_report.json` | Błąd wejścia/wyjścia jest przekazywany do warstwy wywołującej | pokryte testem |
| VALIDATION_REPORT-011 | Wartości tekstowe przekazane jako typy nietekstowe | Pola tekstowe oraz elementy `errors` i `warnings` są normalizowane do `str` zgodnie z obecną logiką | pokryte testem |
| VALIDATION_REPORT-012 | Liczniki przekazane jako wartości tekstowe | `checked_rows`, `valid_rows` i `invalid_rows` są konwertowane do `int` | pokryte testem |
| VALIDATION_REPORT-013 | Niepoprawna wartość licznika | Odczyt kończy się błędem konwersji licznika | pokryte testem |
| VALIDATION_REPORT-014 | Zapis raportu z polskimi albo niestandardowymi znakami | Plik JSON zachowuje znaki dzięki zapisowi UTF-8 i `ensure_ascii=False` | pokryte testem |
| VALIDATION_REPORT-015 | Zapis raportu kończy plik znakiem nowej linii | Plik kończy się pojedynczym znakiem nowej linii | pokryte testem |
| VALIDATION_REPORT-016 | Próba modyfikacji istniejącego obiektu `ValidationReport` | Obiekt pozostaje niemutowalny | pokryte testem |

Na obecnym etapie obszar raportu walidacji można uznać za domknięty dla zakresu v0.2.0.

Przyszłe rozszerzenia mogą obejmować pełniejsze wykorzystanie rozdzielonych statusów, dodanie `validation_schema_version`, `validated_at_utc`, szczegółowej sekcji `summary`, listy `checks` oraz bardziej rozbudowanej struktury błędów i ostrzeżeń. Nie należą one jednak do obecnego mikro-kroku domykania istniejącej warstwy zapisu i odczytu raportu walidacji.

### 25.6. Macierz scenariuszy budowania datasetu

Warstwa budowania datasetu jest obszarem spinającym podstawowe artefakty Data Engine.

Ten obszar odpowiada za:

* utworzenie katalogu konkretnej wersji datasetu,
* wygenerowanie deterministycznego `dataset_id` na podstawie `DatasetRequest`,
* zbudowanie ścieżek do `data.csv`, `metadata.json` i `validation_report.json`,
* zapis początkowego pliku `metadata.json`,
* zapis początkowego pliku `validation_report.json`,
* zapis pustego pliku `data.csv` z nagłówkiem OHLCV,
* zwrócenie obiektu `DatasetBuildResult`,
* zabezpieczenie przed nadpisaniem istniejącej wersji datasetu.

Macierz scenariuszy dla budowania datasetu:

| ID | Scenariusz | Oczekiwany wynik | Status |
| ------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| DATASET_BUILDER-001 | Utworzenie datasetu na podstawie poprawnego `DatasetRequest` | Funkcja zwraca `DatasetBuildResult` i tworzy katalog wersji datasetu | pokryte testem |
| DATASET_BUILDER-002 | Zbudowanie ścieżek artefaktów datasetu | Wynik zawiera ścieżki do `data.csv`, `metadata.json` i `validation_report.json` | pokryte testem |
| DATASET_BUILDER-003 | Zapis początkowego `metadata.json` | Plik metadata istnieje i zawiera oczekiwane dane ze statusem `created` | pokryte testem |
| DATASET_BUILDER-004 | Zapis początkowego `validation_report.json` | Plik raportu walidacji istnieje i zawiera status `not_validated` oraz zerowe liczniki | pokryte testem |
| DATASET_BUILDER-005 | Zapis pustego `data.csv` | Plik danych istnieje i zawiera wyłącznie nagłówek OHLCV | pokryte testem |
| DATASET_BUILDER-006 | Utworzenie początkowych artefaktów i katalogów datasetu | Katalog wersji zawiera `data.csv`, `metadata.json`, `validation_report.json`, `raw/` i `normalized/` | pokryte testem |
| DATASET_BUILDER-007 | Próba utworzenia istniejącej wersji datasetu | Funkcja kończy się błędem i nie nadpisuje istniejącego katalogu wersji | pokryte testem |
| DATASET_BUILDER-008 | Utworzenie datasetu w nieistniejącym katalogu bazowym | Funkcja tworzy brakujące katalogi nadrzędne | pokryte testem |
| DATASET_BUILDER-009 | Utworzenie nowej wersji dla istniejącego `dataset_id` | Funkcja tworzy nowy katalog wersji bez naruszania poprzedniej wersji | pokryte testem |
| DATASET_BUILDER-010 | Rozdzielenie początkowych statusów między wynikiem, metadata i raportem walidacji | `DatasetBuildResult` i `metadata.json` mają status `created`, a `validation_report.json` ma status `not_validated` | pokryte testem |
| DATASET_BUILDER-011 | Utworzenie pustych katalogów `raw/` i `normalized/` | Katalogi `raw/` i `normalized/` istnieją i są puste po utworzeniu datasetu | pokryte testem |

Na obecnym etapie obszar budowania datasetu można uznać za domknięty dla zakresu v0.2.0.

Przyszłe rozszerzenia mogą obejmować obsługę częściowo utworzonych datasetów po błędzie zapisu, transakcyjność tworzenia artefaktów, dodatkowe klasy datasetów, walidację parametrów wejściowych oraz osobne strategie nadpisywania lub inkrementacji wersji. Nie należą one jednak do obecnego mikro-kroku domykania istniejącej warstwy budowania datasetu.

### 25.7. Macierz scenariuszy przykładowego datasetu

Warstwa przykładowego datasetu jest małym obszarem demonstracyjnym Data Engine.

Ten obszar odpowiada za:

* zbudowanie deterministycznego `DatasetRequest` dla przykładowych danych OHLCV,
* zbudowanie przykładowych świec OHLCV,
* utworzenie datasetu przez `create_dataset`,
* zapis przykładowych świec do `data.csv`,
* walidację zapisanego pliku OHLCV,
* zapis finalnego `validation_report.json`,
* aktualizację `metadata.json` statusem walidacji,
* zwrócenie `DatasetBuildResult` ze statusem po walidacji,
* opcjonalne usunięcie istniejącej wersji datasetu przy `overwrite=True`.

Macierz scenariuszy dla przykładowego datasetu:

| ID | Scenariusz | Oczekiwany wynik | Status |
| ------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| SAMPLE_DATASET-001 | Utworzenie przykładowego datasetu OHLCV | Katalog wersji zawiera `data.csv`, `metadata.json`, `validation_report.json`, `raw/` i `normalized/` | pokryte testem |
| SAMPLE_DATASET-002 | Zapis znormalizowanych świec OHLCV | Odczyt `normalized/candles.csv` zwraca dokładnie świece z `build_sample_ohlcv_bars` | pokryte testem |
| SAMPLE_DATASET-003 | Zapis metadata i raportu walidacji po walidacji | Metadata i wynik datasetu mają status `validated`, a raport walidacji ma status `valid` | pokryte testem |
| SAMPLE_DATASET-004 | Raport walidacji dla przykładowych świec | Raport ma 2 sprawdzone wiersze, 2 poprawne wiersze, 0 błędnych wierszy oraz brak błędów i ostrzeżeń | pokryte testem |
| SAMPLE_DATASET-005 | Uruchomienie skryptu `scripts/create_sample_dataset.py` | Skrypt kończy się sukcesem, wypisuje ścieżki artefaktów i tworzy katalog `data/datasets` | pokryte testem |
| SAMPLE_DATASET-006 | Deterministyczny `DatasetRequest` przykładowego datasetu | Request ma oczekiwane pola providera, instrumentu, typu danych, interwału i zakresu dat | pokryte testem |
| SAMPLE_DATASET-007 | Deterministyczne przykładowe świece OHLCV | Funkcja zwraca oczekiwane wartości timestampów, cen i wolumenów | pokryte testem |
| SAMPLE_DATASET-008 | Domyślna wersja przykładowego datasetu | Dataset jest tworzony z wersją `v001` | pokryte testem |
| SAMPLE_DATASET-009 | Utworzenie przykładowego datasetu z niestandardową wersją | Dataset, metadata i raport walidacji używają przekazanej wersji, np. `v002` | pokryte testem |
| SAMPLE_DATASET-010 | Próba ponownego utworzenia datasetu bez `overwrite` | Funkcja kończy się błędem istniejącej wersji i nie nadpisuje danych | pokryte testem |
| SAMPLE_DATASET-011 | Ponowne utworzenie datasetu z `overwrite=True` | Istniejąca wersja datasetu zostaje usunięta i odtworzona z poprawnymi artefaktami | pokryte testem |
| SAMPLE_DATASET-012 | Spójność pól metadata z przykładowym requestem | `metadata.json` zachowuje pola z `build_sample_dataset_request` i status po walidacji | pokryte testem |
| SAMPLE_DATASET-013 | Spójność ścieżek i statusów wyniku | `DatasetBuildResult` wskazuje `normalized/candles.csv`, ma status datasetu `validated`, a raport walidacji ma status `valid` | pokryte testem |
| SAMPLE_DATASET-014 | Zapis przejściowego `raw/response.json` | Plik `raw/response.json` istnieje i zawiera wynik `build_sample_raw_response` | pokryte testem |
| SAMPLE_DATASET-015 | Zapis `normalized/candles.csv` w sample dataset | Plik `normalized/candles.csv` istnieje i zawiera przykładowe świece OHLCV | pokryte testem |
| SAMPLE_DATASET-016 | Pozostawienie przejściowego `data.csv` z samym nagłówkiem | Plik `data.csv` nadal istnieje jako artefakt przejściowy i zawiera tylko nagłówek OHLCV | pokryte testem |

Na obecnym etapie obszar przykładowego datasetu można uznać za domknięty dla zakresu v0.2.0.

Przyszłe rozszerzenia mogą obejmować większe sample datasety, różne klasy aktywów, różne interwały, scenariusze celowo niepoprawnych danych demonstracyjnych oraz osobne komendy CLI dla generowania danych przykładowych. Nie należą one jednak do obecnego mikro-kroku domykania istniejącej warstwy przykładowego datasetu.

### 25.8. Macierz scenariuszy identyfikatora datasetu

Warstwa identyfikatora datasetu jest małym, ale krytycznym obszarem Data Engine.

Ten obszar odpowiada za:

* wygenerowanie deterministycznego `dataset_id` na podstawie `DatasetRequest`,
* zachowanie stałej kolejności pól identyfikujących dataset,
* normalizację providera, klasy aktywa, typu danych, typu ceny i interwału,
* normalizację symbolu instrumentu,
* zapis dat żądanego zakresu danych w formacie ISO `YYYY-MM-DD`,
* niedodawanie wersji datasetu do `dataset_id`,
* tworzenie identyfikatora bez spacji i znaków specjalnych niebezpiecznych dla ścieżek plików.

Macierz scenariuszy dla identyfikatora datasetu:

| ID | Scenariusz | Oczekiwany wynik | Status |
| ------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| DATASET_ID-001 | Wygenerowanie `dataset_id` dla standardowego requestu EUR/USD OHLCV 1d | Funkcja zwraca oczekiwany identyfikator `polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31` | pokryte testem |
| DATASET_ID-002 | Normalizacja wariantów symbolu EUR/USD | Różne zapisy symbolu, np. `EUR/USD`, `EUR USD`, `eur-usd`, dają ten sam `dataset_id` | pokryte testem |
| DATASET_ID-003 | Normalizacja typowych pól tekstowych | Spacje i wielkość liter w polach tekstowych nie zmieniają finalnego `dataset_id` | pokryte testem |
| DATASET_ID-004 | Deterministyczność generowania identyfikatora | Dwa wywołania dla tego samego requestu zwracają ten sam wynik | pokryte testem |
| DATASET_ID-005 | Brak spacji i ukośników w `dataset_id` | Wynik nie zawiera spacji ani znaków `/` | pokryte testem |
| DATASET_ID-006 | Normalizacja znaków specjalnych w polach tekstowych innych niż symbol | Znaki specjalne są zamieniane na bezpieczne separatory `_` zgodnie z obecną logiką | pokryte testem |
| DATASET_ID-007 | Usuwanie nadmiarowych separatorów `_` w polach tekstowych | Wielokrotne separatory są redukowane do pojedynczego `_`, a początkowe i końcowe `_` są usuwane | pokryte testem |
| DATASET_ID-008 | Normalizacja symbolu z wieloma znakami specjalnymi | Symbol zachowuje tylko litery i cyfry, np. warianty EUR/USD nadal dają `eurusd` | pokryte testem |
| DATASET_ID-009 | Daty w `dataset_id` pochodzą z `requested_start` i `requested_end` | Identyfikator zawiera daty żądanego zakresu w formacie `YYYY-MM-DD` | pokryte testem |
| DATASET_ID-010 | Zmiana wersji datasetu nie wpływa na `dataset_id` | `dataset_id` nie zawiera `v001`, `v002` ani innego numeru wersji | pokryte testem |
| DATASET_ID-011 | Zmiana pola tożsamości datasetu zmienia `dataset_id` | Zmiana providera, symbolu, typu ceny, interwału albo zakresu dat daje inny identyfikator | pokryte testem |
| DATASET_ID-012 | Wynik pozostaje zgodny ze strukturą katalogów datasetu | `dataset_id` może być bezpiecznie użyty jako element ścieżki `data/datasets/{dataset_id}/{version}` | pokryte testem |

Na obecnym etapie obszar identyfikatora datasetu można uznać za domknięty dla zakresu v0.2.0.

Przyszłe rozszerzenia mogą obejmować walidację pustych pól po normalizacji, obsługę znaków spoza ASCII, jawne ograniczenie długości identyfikatora, dodatkowy fingerprint parametrów źródłowych oraz migrację starszych identyfikatorów, jeśli format `dataset_id` zostanie kiedyś rozszerzony. Nie należą one jednak do obecnego mikro-kroku domykania istniejącej warstwy identyfikatora datasetu.

### 25.9. Macierz scenariuszy ścieżek storage

Warstwa storage jest małym obszarem pomocniczym Data Engine.

W obecnej implementacji v0.2.0 ten obszar odpowiada wyłącznie za budowanie ścieżek do minimalnych artefaktów datasetu:

* katalogu wersji datasetu `data/datasets/{dataset_id}/{version}`,
* pliku danych `data.csv`,
* pliku metadanych `metadata.json`,
* pliku raportu walidacji `validation_report.json`.

Obecna warstwa storage nie tworzy katalogów, nie zapisuje plików, nie odczytuje plików i nie waliduje nazw. Te odpowiedzialności należą do innych warstw albo przyszłych rozszerzeń.

Macierz scenariuszy dla ścieżek storage:

| ID | Scenariusz | Oczekiwany wynik | Status |
| ------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| STORAGE-001 | Zbudowanie ścieżki katalogu wersji datasetu | Funkcja zwraca ścieżkę `{base_data_dir}/datasets/{dataset_id}/{version}` | pokryte testem |
| STORAGE-002 | Zbudowanie ścieżki `metadata.json` | Funkcja zwraca ścieżkę `{dataset_path}/metadata.json` | pokryte testem |
| STORAGE-003 | Zbudowanie ścieżki `validation_report.json` | Funkcja zwraca ścieżkę `{dataset_path}/validation_report.json` | pokryte testem |
| STORAGE-004 | Zbudowanie ścieżki `data.csv` | Funkcja zwraca ścieżkę `{dataset_path}/data.csv` | pokryte testem |
| STORAGE-005 | Helpery storage nie tworzą katalogów ani plików | Samo zbudowanie ścieżek nie powoduje efektów ubocznych w systemie plików | pokryte testem |
| STORAGE-006 | Obsługa niestandardowego katalogu bazowego | Ścieżka wersji datasetu jest budowana względem przekazanego `base_data_dir` | pokryte testem |
| STORAGE-007 | Obsługa niestandardowej wersji datasetu | Ścieżka wersji datasetu zawiera dokładnie przekazany numer wersji, np. `v002` | pokryte testem |
| STORAGE-008 | Spójność nazw artefaktów storage z `DatasetBuildResult` | Nazwy plików storage pozostają zgodne z `data.csv`, `metadata.json` i `validation_report.json` | pokryte testem |
| STORAGE-009 | Obsługa docelowych ścieżek `raw/` i `normalized/` w storage | Warstwa storage udostępnia helpery dla `raw/`, `raw/response.json`, `normalized/` i `normalized/candles.csv` | pokryte testem |

Na obecnym etapie obszar ścieżek storage można uznać za domknięty dla zakresu v0.2.0.

Po mikro-kroku 71B storage udostępnia już helpery dla docelowych ścieżek `raw/`, `raw/response.json`, `normalized/` i `normalized/candles.csv`.

`create_dataset` nadal używa przejściowego `data.csv`.

Przyszłe rozszerzenia obejmą przepięcie buildera i sample datasetu na nową strukturę, formaty inne niż CSV oraz walidację bezpieczeństwa ścieżek.

### 25.10. Macierz scenariuszy statusów Data Engine

Statusy Data Engine są osobnym obszarem, ponieważ w projekcie występują dwa różne pojęcia:

1. status życia datasetu,
2. status wyniku walidacji.

Status życia datasetu jest zapisywany w `metadata.json`.

Status wyniku walidacji jest zapisywany w `validation_report.json`.

`DatasetBuildResult.status` oznacza status życia datasetu, a nie status wyniku walidacji.

Docelowe statusy życia datasetu:

```text
RAW
VALIDATED
ACCEPTED
QUARANTINED
REJECTED
DEPRECATED
```

Docelowe statusy walidacji:

```text
not_validated
valid
valid_with_warnings
invalid
```

Tymczasowe stare statusy implementacyjne:

```text
created
validated
invalid
```

Stare statusy implementacyjne pozostają tylko jako `legacy`, żeby refaktor można było wykonać mikro-krokami bez jednorazowego przepinania buildera, walidatora, modeli i testów.

Nie wolno traktować ich jako docelowego modelu statusów.

Macierz scenariuszy dla statusów Data Engine:

| ID | Scenariusz | Oczekiwany wynik | Status |
| --- | --- | --- | --- |
| STATUS-001 | Kod posiada osobne stałe statusów życia datasetu | Dostępne są stałe `DATASET_LIFECYCLE_STATUS_*` | pokryte testem |
| STATUS-002 | Kod posiada osobne stałe statusów walidacji | Dostępne są stałe `VALIDATION_STATUS_*`, w tym `VALIDATION_STATUS_NOT_VALIDATED` | pokryte testem |
| STATUS-003 | Statusy życia datasetu są unikalne | Lista `DATASET_LIFECYCLE_STATUSES` nie zawiera duplikatów | pokryte testem |
| STATUS-004 | Statusy walidacji są unikalne | Lista `VALIDATION_STATUSES` nie zawiera duplikatów | pokryte testem |
| STATUS-005 | Statusy życia datasetu i statusy walidacji nie mieszają się | Zbiory `DATASET_LIFECYCLE_STATUSES` i `VALIDATION_STATUSES` są rozłączne | pokryte testem |
| STATUS-006 | Stare statusy implementacyjne pozostają tymczasowo dostępne | `created`, `validated`, `invalid` są dostępne jako legacy | pokryte testem |
| STATUS-007 | `metadata.status` używa statusu życia datasetu | `metadata.json` korzysta z `RAW`, `VALIDATED`, `ACCEPTED`, `QUARANTINED`, `REJECTED` albo `DEPRECATED` | do przepięcia |
| STATUS-008 | `validation_report.status` używa statusu walidacji | `validation_report.json` korzysta z `not_validated`, `valid`, `valid_with_warnings` albo `invalid` | pokryte testem |
| STATUS-009 | `DatasetBuildResult.status` oznacza status życia datasetu | Wynik budowania datasetu nie używa statusu walidacji jako statusu datasetu | pokryte testem |
| STATUS-010 | Legacy statusy zostają usunięte albo jawnie utrzymane czasowo | Po przepięciu modeli, walidatora i buildera stare stałe nie są używane jako model docelowy | do domknięcia |

Po mikro-krokach 68 i 69 status raportu walidacji jest już oddzielony od statusu datasetu.

Obszar statusów nie jest jeszcze domknięty, ponieważ `metadata.status` nadal korzysta z tymczasowych statusów legacy, a stare stałe nie zostały jeszcze usunięte.

Za domknięty można go uznać dopiero wtedy, gdy:

1. kod używa rozdzielonych statusów we właściwych miejscach,
2. stare legacy stałe zostaną usunięte albo jawnie oznaczone jako pozostawione czasowo,
3. testy pokrywają osobno statusy datasetu i statusy walidacji,
4. dokumentacja opisuje finalny stan.

## 26. Proponowana struktura testów

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

## 27. Przykładowe testy v0.2.0

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

Po utworzeniu datasetu powinny istnieć:

```text
raw/response.json
normalized/candles.csv
metadata.json
validation_report.json
```

### 27.3. Test metadanych

`metadata.json` powinien zawierać co najmniej:

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

### 27.4. Test walidacji poprawnych świec

Poprawny plik `candles.csv` powinien otrzymać status:

```text
valid
```

albo:

```text
valid_with_warnings
```

### 27.5. Test walidacji błędnych świec

Dla błędnego pliku, na przykład z sytuacją:

```text
high < low
```

raport powinien otrzymać status:

```text
invalid
```

oraz zawierać błąd walidacji.

### 27.6. Test wersjonowania

Tworzenie tego samego datasetu po raz pierwszy powinno utworzyć:

```text
v001
```

Ponowne utworzenie tego samego datasetu powinno utworzyć:

```text
v002
```

Test powinien potwierdzać, że `v001` nadal istnieje i nie została zmodyfikowana.

### 27.7. Test odczytu konkretnej wersji

Data Engine powinien pozwalać na odczyt konkretnej wersji przez:

```text
dataset_id + version
```

bez używania katalogu `latest`.

### 27.8. Test braku sekretów w metadanych

Test powinien potwierdzać, że `metadata.json` nie zawiera API key, tokenów ani innych sekretów.

## 28. Czego nie testujemy w v0.2.0

W v0.2.0 nie testujemy jeszcze:

* prawdziwego API Polygon/Massive,
* Dukascopy,
* porównywania źródeł,
* rankingu jakości datasetów,
* backtestingu,
* strategii,
* agentów AI,
* wielu instrumentów naraz,
* real-time,
* dużych plików danych.

## 29. Dalszy rozwój testów

Zakres testów Data Engine powinien rosnąć razem z funkcjonalnością.

Każda nowa publiczna funkcja, nowy provider, nowy format zapisu, nowa reguła walidacji albo zmiana schematu metadanych powinna otrzymać test automatyczny.

Testy powinny chronić:

* kompatybilność wsteczną,
* odczyt wcześniej utworzonych datasetów,
* brak nadpisywania istniejących wersji,
* stabilność publicznego interfejsu,
* powtarzalność działania Data Engine,
* brak przypadkowego użycia zewnętrznych API w testach offline,
* brak zapisywania sekretów do datasetów.

Funkcjonalność Data Engine uznajemy za gotową dopiero wtedy, gdy przechodzi testy automatyczne.

## 30. ADR dla Data Engine v0.2.0

Decyzje opisane w tym dokumencie mają znaczenie architektoniczne.

Dlatego dla Data Engine v0.2.0 powinien zostać utworzony osobny ADR, na przykład:

```text
dokumentacja/decyzje/ADR-0003-data-engine-v0-2-implementacja.md
```

ADR powinien krótko opisywać najważniejsze decyzje:

* wybór Polygon/Massive Free jako pierwszego źródła danych,
* EUR/USD jako pierwszy instrument referencyjny,
* raw JSON i normalized CSV jako formaty startowe,
* `metadata.json` i `validation_report.json`,
* strukturę `data/datasets/{dataset_id}/v001/`,
* deterministyczny `dataset_id`,
* wersjonowanie bez nadpisywania,
* testy offline,
* zasadę kompatybilności wstecznej.

Pełne szczegóły techniczne pozostają w tym dokumencie implementacyjnym.

## 31. Podsumowanie decyzji v0.2.0

W v0.2.0 Data Engine implementuje mały, stabilny fundament:

* jedno źródło danych,
* jeden instrument referencyjny,
* jeden typ danych,
* prosty format zapisu,
* metadane,
* walidację,
* wersjonowanie,
* testy offline.

Decyzje główne:

```text
Źródło danych: Polygon/Massive Free
Instrument: EUR/USD
Typ danych: historyczne świece OHLCV
Raw data: raw/response.json
Normalized data: normalized/candles.csv
Metadane: metadata.json
Raport walidacji: validation_report.json
Struktura: data/datasets/{dataset_id}/v001/
Testy: offline, fixtures, katalog tymczasowy
```

Data Engine v0.2.0 ma być małym krokiem, ale zaprojektowanym tak, aby w przyszłości możliwy był rozwój bez rozwalania wcześniejszych, działających wersji.
