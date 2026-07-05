# ADR-0003: Decyzje implementacyjne Data Engine v0.2.0

## Status

Zaakceptowana

## Kontekst

Projekt TradingLab zakończył etap **v0.1.0 — Fundamenty projektu** i przechodzi do etapu **v0.2.0 — Data Engine**.

Data Engine ma być fundamentem danych rynkowych dla przyszłych modułów systemu. Nie jest strategią, backtesterem, traderem ani modułem live tradingu.

Dla etapu v0.2.0 przygotowano dokument implementacyjny:

* `dokumentacja/architektura/DATA_ENGINE_IMPLEMENTACJA_V0_2.md`

Dokument ten opisuje szczegółowy projekt implementacji pierwszej wersji Data Engine.

Ponieważ decyzje dotyczące źródła danych, formatów zapisu, struktury datasetów, wersjonowania, identyfikatorów, walidacji i testów mają znaczenie architektoniczne, powinny zostać zapisane jako ADR.

Ten ADR opisuje decyzje architektoniczne przyjęte dla Data Engine v0.2.0. Nie oznacza to, że wszystkie opisane elementy są już zaimplementowane w kodzie. Część decyzji jest wdrażana stopniowo mikro-krokami.

Aktualny stan implementacji należy weryfikować z dokumentem implementacyjnym, testami i kodem.

## Decyzja

Dla Data Engine v0.2.0 przyjmujemy następujące decyzje.

### 1. Pierwsze źródło danych

Pierwszym docelowym źródłem danych będzie:

> Polygon/Massive Forex API w planie darmowym.

Pierwszym instrumentem referencyjnym będzie:

> EUR/USD.

Pierwszym typem danych będą:

> historyczne świece OHLCV.

Pierwszym docelowym konektorem referencyjnym będzie:

> `PolygonForexConnector`.

Stan implementacji:

* konektor `PolygonForexConnector` nie jest jeszcze zaimplementowany,
* pobieranie danych z API providera nie jest jeszcze zaimplementowane,
* obecny kod posiada fundament lokalnego Data Engine, sample dataset oraz walidację lokalnych danych OHLCV.

Uzasadnienie:

* Polygon/Massive zapewnia uporządkowany interfejs API,
* dobrze pasuje do pierwszego konektora Data Engine,
* pozwala skupić się na cyklu życia datasetu zamiast na złożonym pobieraniu danych,
* plan darmowy wystarcza do pierwszego etapu prac.

Architektura Data Engine nie może jednak zakładać, że Polygon/Massive jest jedynym źródłem prawdy. W przyszłości możliwe będzie dodanie kolejnych źródeł danych, w szczególności Dukascopy jako darmowego źródła badawczego dla dłuższej historii Forex.

### 2. Format zapisu danych

W v0.2.0 dataset składa się z następujących elementów:

```text
raw/response.json
normalized/candles.csv
metadata.json
validation_report.json
```

Raw data są zapisywane jako JSON, ponieważ pierwsze źródło danych ma zwracać odpowiedź API w formacie możliwym do zapisania jako JSON.

Znormalizowane dane OHLCV są zapisywane jako CSV, ponieważ CSV jest prosty, czytelny, łatwy do testowania i nie wymaga dodatkowych zależności.

Stan implementacji:

* `metadata.json` jest zaimplementowany,
* `validation_report.json` jest zaimplementowany,
* `normalized/candles.csv` jest zaimplementowany,
* `raw/response.json` jest obecnie używany w sample dataset jako przykładowy artefakt surowej odpowiedzi,
* prawdziwa odpowiedź API providera nie jest jeszcze pobierana.

CSV jest formatem startowym, a nie docelowym ograniczeniem architektury. W przyszłości możliwe jest dodanie innych formatów, na przykład Parquet, bez unieważniania datasetów zapisanych wcześniej jako CSV.

### 3. Struktura katalogów datasetów

Dane Data Engine są zapisywane lokalnie w strukturze:

```text
data/datasets/{dataset_id}/{version}/
```

Przykład:

```text
data/datasets/polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31/v001/
```

Każda wersja datasetu zawiera własne:

```text
raw/response.json
normalized/candles.csv
metadata.json
validation_report.json
```

Prawdziwe dane robocze nie powinny być commitowane do repozytorium.

Do testów automatycznych używane są małe przykładowe dane, fixtures albo katalogi tymczasowe tworzone przez pytest.

### 4. Identyfikator datasetu

`dataset_id` jest czytelnym, deterministycznym identyfikatorem datasetu.

Format:

```text
{provider}_{asset_class}_{symbol}_{data_type}_{price_type}_{interval}_{start}_{end}
```

Przykład:

```text
polygon_massive_forex_eurusd_ohlcv_provider_1d_2024-01-01_2024-12-31
```

`dataset_id` nie zawiera numeru wersji.

Daty w `dataset_id` oznaczają zakres żądany od źródła danych, a nie faktyczny zakres zwróconych danych.

W przyszłości mechanizm `dataset_id` może zostać rozszerzony o fingerprint albo hash parametrów pobrania, jeśli pojawi się potrzeba rozróżniania datasetów o podobnym opisie, ale różnej konfiguracji źródłowej.

### 5. Wersjonowanie datasetów

Każdy dataset posiada wersje zapisywane jako:

```text
v001
v002
v003
```

Pierwsza wersja datasetu ma numer:

```text
v001
```

Istniejących wersji nie nadpisujemy.

Jeśli ten sam dataset jest tworzony ponownie, powstaje kolejna wersja.

Po utworzeniu wersji datasetu nie modyfikujemy jej zawartości. Jeśli konieczna jest zmiana danych, metadanych, normalizacji lub raportu walidacji, tworzona jest nowa wersja datasetu.

W v0.2.0 nie tworzymy katalogu `latest`.

Odczyt datasetu powinien wskazywać jawnie:

```text
dataset_id + version
```

### 6. Status datasetu i status walidacji

Rozróżniamy:

1. status życia datasetu,
2. status wyniku walidacji.

Status życia datasetu znajduje się w `metadata.json`.

Docelowe statusy życia datasetu:

```text
RAW
VALIDATED
ACCEPTED
QUARANTINED
REJECTED
DEPRECATED
```

Status wyniku walidacji znajduje się w `validation_report.json`.

Statusy wyniku walidacji:

```text
not_validated
valid
valid_with_warnings
invalid
```

Status datasetu nie zastępuje raportu walidacji.

Stan implementacji:

* `create_dataset` nadaje datasetowi status życia `RAW`,
* sample dataset korzysta z publicznego `validate_dataset` i po udanej walidacji otrzymuje status życia `VALIDATED`,
* początkowy raport walidacji używa statusu `not_validated`,
* walidator OHLCV używa statusów walidacji, między innymi `valid` i `invalid`,
* legacy statusy `created`, `validated` i `invalid` nie są już statusami życia datasetu.

### 7. Metadane datasetu

Metadane datasetu są zapisywane w pliku:

```text
metadata.json
```

Metadane mają umożliwiać identyfikację i odtworzenie datasetu.

Docelowo metadane mogą zawierać między innymi:

* wersję schematu metadanych,
* `dataset_id`,
* wersję datasetu,
* status życia datasetu,
* typ danych,
* źródło danych,
* konektor,
* instrument,
* interwał,
* zakres dat,
* timezone,
* ścieżki do plików datasetu,
* datę utworzenia datasetu w UTC,
* informacje o wersji datasetu,
* parametry żądania do providera.

API key, tokeny i inne sekrety nie mogą być zapisywane w metadanych.

Stan implementacji:

Obecny model `DatasetMetadata` jest prostszy i zawiera:

```text
dataset_id
version
provider
asset_class
symbol
data_type
price_type
interval
requested_start
requested_end
status
```

Pełniejszy schemat metadanych jest decyzją docelową, ale nie jest jeszcze w całości zaimplementowany.

### 8. Raport walidacji

Raport walidacji jest zapisywany w pliku:

```text
validation_report.json
```

Docelowo raport walidacji może zawierać:

* wersję schematu raportu,
* `dataset_id`,
* wersję datasetu,
* status walidacji,
* datę walidacji w UTC,
* podsumowanie,
* listę wykonanych reguł walidacyjnych,
* błędy,
* ostrzeżenia.

Stan implementacji:

Obecny model `ValidationReport` jest prostszy i zawiera:

```text
dataset_id
version
status
errors
warnings
checked_rows
valid_rows
invalid_rows
```

W v0.2.0 obecna walidacja obejmuje podstawową poprawność techniczną danych OHLCV, między innymi:

* istnienie pliku znormalizowanego,
* wymagane kolumny,
* niepusty dataset,
* poprawność timestampów,
* sortowanie timestampów,
* unikalność timestampów,
* numeryczność wartości OHLC,
* brak pustych wartości OHLC,
* brak ujemnych cen,
* logiczną poprawność OHLC,
* numeryczność i nieujemność `volume`.

Pełny kalendarz rynku Forex, święta, DST i szczegółowe godziny handlu nie są wymagane w v0.2.0.

### 9. Sekrety i konfiguracja

API key, tokeny i inne sekrety nie mogą być zapisane:

* w kodzie,
* w dokumentacji,
* w datasetach,
* w plikach commitowanych do repozytorium.

W v0.2.0 klucz Polygon/Massive powinien być przekazywany przez konfigurację lokalną albo zmienną środowiskową.

Stan implementacji:

* projekt nie posiada jeszcze prawdziwego konektora providera,
* testy automatyczne nie wymagają prawdziwego API key,
* sposób konfiguracji sekretów zostanie doprecyzowany przy implementacji pierwszego konektora providera.

### 10. Minimalny interfejs Data Engine

Docelowy minimalny publiczny interfejs Data Engine v0.2.0 obejmuje:

```text
create_dataset
validate_dataset
load_dataset
load_metadata
load_validation_report
load_normalized_candles
```

Stan implementacji:

Obecny eksportowany interfejs obejmuje przede wszystkim:

```text
create_dataset
generate_dataset_id
validate_dataset
load_dataset
load_metadata
load_validation_report
load_normalized_candles
modele danych Data Engine
```

Funkcje publicznego interfejsu:

```text
validate_dataset
load_dataset
load_metadata
load_validation_report
load_normalized_candles
```

są zaimplementowane jako publiczny, domenowy interfejs Data Engine.

Publiczny interfejs działa przez:

```text
base_data_dir
dataset_id
version
```

a nie przez ręczne podawanie ścieżek do wewnętrznych plików datasetu.

Obecne `load_dataset`:

* odczytuje `metadata.json`,
* odczytuje `validation_report.json`,
* odczytuje `normalized/candles.csv`,
* zwraca `DatasetLoadResult`,
* nie waliduje datasetu,
* nie zmienia metadanych,
* nie zapisuje plików,
* nie wybiera najnowszej wersji datasetu.

Obecne `validate_dataset`:

* waliduje `normalized/candles.csv`,
* zapisuje wynik do `validation_report.json`,
* zwraca `ValidationReport`,
* aktualizuje status życia datasetu w `metadata.json`.

Mapowanie statusu walidacji na status życia datasetu:

```text
validation_report.status = valid
    -> metadata.status = VALIDATED

validation_report.status = valid_with_warnings
    -> metadata.status = VALIDATED

validation_report.status = invalid
    -> metadata.status = QUARANTINED
```

Publiczne `validate_dataset` nie nadaje automatycznie statusu `ACCEPTED` ani `REJECTED`.

`ACCEPTED` i `REJECTED` pozostają statusami świadomej decyzji wyższej warstwy systemu.

Data Engine v0.2.0 nie posiada jeszcze funkcji:

* `update_dataset`,
* `overwrite_dataset`,
* `get_latest_valid_dataset`,
* porównywania źródeł,
* rankingu datasetów,
* obsługi wielu providerów naraz,
* backtestingu,
* strategii,
* agentów AI,
* live tradingu.

Publiczny interfejs powinien operować na pojęciach domenowych, takich jak dataset, `dataset_id`, version, provider, instrument, interval i time range, a nie na szczegółach konkretnego API.

Szczegóły providera powinny być ukryte w konektorach.

### 11. Minimalna struktura modułów

Docelowa minimalna struktura kodu Data Engine może obejmować:

```text
src/tradinglab/data_engine/
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

Stan implementacji:

Obecna struktura jest inna i obejmuje między innymi:

```text
src/tradinglab/data_engine/
  __init__.py
  dataset_builder.py
  dataset_id.py
  data_file.py
  engine.py
  metadata.py
  models.py
  ohlcv_validation.py
  sample_dataset.py
  status.py
  storage.py
  validation_report.py
```

Różnica między strukturą docelową a obecną nie jest błędem. Obecny kod został rozbity na mniejsze moduły w trakcie implementacji i testowania.

Nie tworzymy na zapas modułów strategii, backtestingu, agentów AI, rankingu źródeł, brokerów ani live tradingu.

### 12. Testy

Testy Data Engine v0.2.0 mają działać lokalnie i powtarzalnie.

Testy nie mogą wymagać:

* prawdziwego API key,
* internetu,
* dostępności zewnętrznego providera,
* limitów API,
* prawdziwego katalogu roboczego `data/datasets/`.

Do testów używane są fixtures i katalogi tymczasowe tworzone przez pytest.

Minimalny zakres testów obejmuje:

* generowanie `dataset_id`,
* tworzenie struktury katalogów datasetu,
* zapis i odczyt raw data,
* zapis i odczyt normalized candles,
* zapis i odczyt `metadata.json`,
* zapis i odczyt `validation_report.json`,
* walidację poprawnego pliku `candles.csv`,
* walidację błędnego pliku `candles.csv`,
* tworzenie kolejnych wersji bez nadpisywania,
* odczyt datasetu przez jawne wskazanie `dataset_id` i version,
* podstawową obsługę błędnych żądań wejściowych,
* brak sekretów w metadanych.

Funkcjonalność Data Engine uznajemy za gotową dopiero wtedy, gdy przechodzi testy automatyczne.

### 13. Kompatybilność wsteczna

Rozwój Data Engine powinien zachowywać kompatybilność wsteczną.

Nowe funkcje nie mogą:

* unieważniać istniejących datasetów,
* zmieniać znaczenia wcześniejszych wersji,
* wymuszać modyfikacji danych już zapisanych,
* nadpisywać istniejących wersji datasetów,
* zmieniać znaczenia istniejących operacji publicznego interfejsu.

Jeżeli w przyszłości konieczna będzie zmiana niekompatybilna wstecznie, musi zostać wcześniej opisana w dokumentacji albo ADR oraz powinna mieć jasną ścieżkę migracji.

## Konsekwencje

### Pozytywne

* Data Engine v0.2.0 ma jasny, ograniczony zakres.
* Projekt zaczyna od jednego prostego kierunku źródła danych.
* Dane są od początku wersjonowane.
* Raw data są chronione przed modyfikacją.
* Testy offline chronią projekt przed niestabilnością zewnętrznego API.
* Architektura nie zamyka drogi do kolejnych providerów.
* Dataset jest projektowany jako obiekt możliwy do odtworzenia i audytu.
* Przyszły rozwój ma odbywać się bez rozwalania wcześniejszych, działających wersji.
* ADR odróżnia decyzje docelowe od obecnego stanu implementacji.

### Negatywne

* v0.2.0 nie rozwiązuje jeszcze problemu pełnej jakości danych Forex.
* v0.2.0 nie obsługuje jeszcze wielu źródeł danych.
* v0.2.0 nie zawiera jeszcze rankingu źródeł.
* v0.2.0 nie zawiera jeszcze backtestingu ani strategii.
* CSV jest prosty, ale nie jest najlepszym formatem dla dużych datasetów.
* Brak katalogu `latest` wymaga jawnego wskazywania wersji datasetu.
* Część decyzji architektonicznych nadal wymaga osobnych mikro-kroków implementacyjnych.

### Ryzyka

* Darmowy plan Polygon/Massive może mieć ograniczenia, które będą wymagały zmiany podejścia w przyszłości.
* Dane Forex mogą różnić się między providerami.
* Pole `volume` w danych Forex może mieć różne znaczenie zależnie od źródła.
* Rozbudowa Data Engine może wymagać nowych formatów zapisu, dokładniejszej walidacji i katalogu datasetów.
* Przedwczesne uznanie decyzji docelowych za gotowy kod może prowadzić do błędnych założeń w dalszych pracach.

## Alternatywy rozważane

### Stooq jako pierwsze źródło danych

Odrzucone jako pierwszy wybór dla v0.2.0, ponieważ pierwsze testy mają dotyczyć EUR/USD, a Polygon/Massive daje czytelniejszy model pierwszego konektora API.

### Dukascopy jako pierwsze źródło danych

Odrzucone jako pierwszy wybór dla v0.2.0, ponieważ Dukascopy może wymagać większej pracy po stronie pobierania, normalizacji i ewentualnej agregacji ticków.

Dukascopy pozostaje kandydatem na kolejne darmowe źródło danych historycznych Forex.

### Parquet jako pierwszy format znormalizowanych danych

Odrzucone dla v0.2.0, ponieważ wymaga dodatkowych zależności i jest mniej czytelne ręcznie niż CSV.

Parquet pozostaje kandydatem na przyszły format analityczny.

### UUID jako główny dataset_id

Odrzucone dla v0.2.0, ponieważ czytelny deterministyczny `dataset_id` lepiej wspiera ręczną kontrolę katalogów i debugowanie.

W przyszłości możliwe jest dodanie fingerprintu albo hasha parametrów pobrania.

## Powiązane dokumenty

* `dokumentacja/architektura/DATA_ENGINE.md`
* `dokumentacja/architektura/DATA_ENGINE_IMPLEMENTACJA_V0_2.md`
* `dokumentacja/architektura/KONSTYTUCJA.md`
* `dokumentacja/architektura/ARCHITEKTURA.md`
* `dokumentacja/mapa_drogowa/ROADMAP.md`
* `dokumentacja/decyzje/ADR-0001-fundamenty-projektu.md`
* `dokumentacja/decyzje/ADR-0002-narzedzia-testow-i-jakosci-kodu.md`