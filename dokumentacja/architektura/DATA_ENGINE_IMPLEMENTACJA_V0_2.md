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

### 4.1. Plan przejścia do pierwszego realnego pobrania danych po publicznym loaderze

Po mikro-krokach 74B.1 i 74D.1 Data Engine posiada już mały publiczny przepływ pracy z datasetem:

```text
create_dataset
    -> validate_dataset
    -> load_dataset
```

Oznacza to, że przed rozpoczęciem pracy nad pierwszym prawdziwym providerem istnieje już stabilny fundament:

* deterministyczne `dataset_id`,
* wersjonowanie datasetów,
* docelowa struktura katalogów `raw/` i `normalized/`,
* zapis `metadata.json`,
* zapis `validation_report.json`,
* walidacja `normalized/candles.csv`,
* publiczny odczyt pełnej wersji datasetu przez `load_dataset`,
* widoczny przepływ demonstracyjny w `scripts/create_sample_dataset.py`.

Kolejny etap po publicznym loaderze powinien prowadzić do pierwszego realnego pobrania danych z providera, ale nadal mikro-krokami.

Docelowym pierwszym providerem dla tego etapu pozostaje:

```text
Polygon/Massive Forex API
```

Docelowym pierwszym instrumentem pozostaje:

```text
EUR/USD
```

Docelowym pierwszym typem danych pozostają:

```text
historyczne świece OHLCV
```

Przejście do prawdziwego providera powinno zostać podzielone na małe kroki:

1. zaprojektować minimalny kontrakt konektora providera,
2. dodać minimalną strukturę katalogu `connectors/`,
3. dodać testy offline dla kontraktu konektora,
4. przygotować normalizację przykładowej odpowiedzi providera do `OhlcvBar`,
5. testować parser i normalizator na lokalnym fixture albo danych wpisanych w testach,
6. dopiero później dodać ręczny skrypt pobrania małego zakresu danych z Polygon/Massive,
7. zapisać prawdziwą odpowiedź providera do `raw/response.json`,
8. zapisać znormalizowane świece do `normalized/candles.csv`,
9. uruchomić `validate_dataset`,
10. odczytać wynik przez `load_dataset`,
11. wypisać krótkie podsumowanie pobranego datasetu w terminalu.

Testy automatyczne dla konektora i normalizacji nie powinny wymagać:

* prawdziwego API key,
* internetu,
* dostępności Polygon/Massive,
* limitów API,
* lokalnego katalogu `data/datasets/`.

Prawdziwe pobranie danych powinno pozostać operacją ręczną, uruchamianą świadomie przez skrypt i zależną od lokalnej konfiguracji albo zmiennej środowiskowej z API key.

Mikro-kroki przejścia do providera nie powinny jeszcze wprowadzać:

* wielu providerów,
* rankingu źródeł danych,
* wyboru najlepszego datasetu,
* katalogu `latest`,
* statusów `ACCEPTED` ani `REJECTED`,
* backtestingu,
* strategii,
* live tradingu,
* agentów AI,
* automatycznego pobierania danych podczas testów.

Celem najbliższych kroków po 74E.0 nie jest jeszcze pełny konektor produkcyjny, tylko bezpieczna ścieżka do pierwszego małego, kontrolowanego i możliwego do zweryfikowania datasetu pobranego z prawdziwego źródła.

### 4.2. Minimalny kontrakt konektora providera

Po mikro-kroku 74E.1 minimalny kontrakt konektora providera jest traktowany jako warstwa przejściowa między zewnętrznym źródłem danych a istniejącym przepływem Data Engine.

Konektor providera nie powinien zastępować istniejących elementów Data Engine. Jego zadaniem nie jest walidacja datasetu, zapis plików ani wybór wersji danych. Konektor ma jedynie dostarczyć surową odpowiedź providera albo umożliwić jej kontrolowane przetworzenie do wspólnego modelu świec OHLCV.

Minimalny planowany przepływ wygląda następująco:

```text
DatasetRequest
    -> ProviderOhlcvConnector
    -> ProviderRawResponse
    -> normalizer odpowiedzi providera
    -> list[OhlcvBar]
    -> zapis raw/response.json i normalized/candles.csv
    -> validate_dataset
    -> load_dataset
```

Minimalny kontrakt konektora powinien być ograniczony do danych OHLCV.

Planowana odpowiedzialność konektora:

* przyjąć request opisujący providera, instrument, interwał i zakres dat,
* pobrać albo zwrócić surową odpowiedź providera,
* zachować informację, z jakiego providera pochodzi odpowiedź,
* nie ukrywać surowego payloadu,
* nie podejmować decyzji o jakości datasetu,
* nie zapisywać datasetu na dysku,
* nie uruchamiać walidacji datasetu,
* nie nadawać statusów `VALIDATED`, `ACCEPTED` ani `REJECTED`.

Planowana odpowiedzialność normalizatora odpowiedzi providera:

* przyjąć surowy payload providera,
* odczytać z niego świece OHLCV,
* zamienić dane na listę `OhlcvBar`,
* nie zapisywać plików,
* nie wykonywać połączeń sieciowych,
* nie walidować całego datasetu,
* pozostawić walidację świec istniejącemu przepływowi Data Engine.


Elementy kontraktu po 74E.2 i robocze elementy przyszłej implementacji:

```text
src/tradinglab/data_engine/connectors/base.py                 -> zaimplementowane po 74E.2
tests/data_engine/test_provider_connector_contract.py          -> zaimplementowane po 74E.2
src/tradinglab/data_engine/connectors/polygon_forex.py         -> przyszły krok
tests/data_engine/test_polygon_forex_normalization.py          -> przyszły krok
```

Roboczy kontrakt logiczny konektora:

```text
ProviderOhlcvConnector.fetch_ohlcv(request) -> ProviderRawResponse
```

Roboczy kontrakt logiczny normalizatora:

```text
normalize_provider_ohlcv_response(raw_response) -> list[OhlcvBar]
```

`ProviderRawResponse` powinien być minimalnym obiektem opisującym odpowiedź providera. Na tym etapie wystarczające pola to:

* nazwa providera,
* request, dla którego pobrano dane,
* surowy payload providera.

W testach automatycznych konektor nie powinien wykonywać prawdziwych połączeń sieciowych. Testy powinny opierać się na lokalnym fixture, słowniku Python albo ręcznie zdefiniowanym przykładzie odpowiedzi providera.

Testy kontraktu i normalizacji powinny potwierdzać, że:

* konektor ma stabilny publiczny kształt,
* odpowiedź providera można reprezentować bez zapisu na dysku,
* normalizator potrafi zamienić przykładowy payload na `OhlcvBar`,
* wynik normalizacji można później zapisać jako `normalized/candles.csv`,
* testy nie wymagają API key,
* testy nie wymagają internetu,
* testy nie zapisują prawdziwego datasetu w `data/datasets/`.

Pierwszy prawdziwy konektor powinien dotyczyć tylko jednego zakresu:

```text
provider: Polygon/Massive Forex API
instrument: EUR/USD
data_type: OHLCV
tryb: historyczne świece
```

Po mikro-kroku 74E.2 bazowy kontrakt konektora został zaimplementowany w `src/tradinglab/data_engine/connectors/base.py` jako `ProviderRawResponse` oraz `ProviderOhlcvConnector`.

Ten krok nadal nie implementuje prawdziwego konektora Polygon/Massive, normalizacji odpowiedzi providera ani pobierania danych z internetu. Testy pozostają offline i potwierdzają tylko stabilny kształt kontraktu oraz możliwość reprezentowania surowej odpowiedzi providera bez zapisu datasetu na dysku.

Następny krok kodowy powinien dotyczyć provider-specific normalizacji przykładowej odpowiedzi Polygon/Massive do `OhlcvBar`, nadal bez API key i bez internetu.

### 4.3. Projekt normalizacji przykładowej odpowiedzi Polygon/Massive do `OhlcvBar`

Po mikro-kroku 74E.3 normalizacja odpowiedzi Polygon/Massive jest zaprojektowana jako osobna warstwa między `ProviderRawResponse` a istniejącym modelem `OhlcvBar`.

Ten krok nie implementuje jeszcze normalizatora. Dokumentuje jedynie mały, offline'owy zakres następnego kroku kodowego.

Pierwszy normalizator powinien dotyczyć wyłącznie odpowiedzi typu Forex Custom Bars dla:

```text
provider: Polygon/Massive Forex API
instrument: EUR/USD
ticker providera: C:EURUSD
data_type: OHLCV
tryb: historyczne świece
```

Roboczy payload testowy powinien być lokalny i wpisany w teście albo fixture. Nie powinien pochodzić z prawdziwego połączenia sieciowego.

Minimalny przykład roboczego payloadu:

```text
{
    "adjusted": true,
    "queryCount": 2,
    "request_id": "offline-test-request",
    "results": [
        {
            "c": 1.17721,
            "h": 1.18305,
            "l": 1.17560,
            "n": 125329,
            "o": 1.17921,
            "t": 1626912000000,
            "v": 125329,
            "vw": 1.17890
        },
        {
            "c": 1.18010,
            "h": 1.18400,
            "l": 1.17650,
            "n": 125330,
            "o": 1.17721,
            "t": 1626998400000,
            "v": 125330,
            "vw": 1.18000
        }
    ],
    "resultsCount": 2,
    "status": "OK",
    "ticker": "C:EURUSD"
}
```

Mapowanie pól z payloadu providera do `OhlcvBar` powinno być jawne:

```text
t -> timestamp
o -> open
h -> high
l -> low
c -> close
v -> volume
```

Pola `n`, `vw`, `adjusted`, `queryCount`, `request_id`, `resultsCount`, `status` i `ticker` nie powinny być na tym etapie mapowane do `OhlcvBar`. Mogą pozostać w `ProviderRawResponse.raw_payload`, ponieważ surowa odpowiedź providera ma być zachowana bez ukrywania payloadu.

Pierwszy normalizator powinien przyjąć `ProviderRawResponse` i zwrócić listę `OhlcvBar`.

Roboczy kontrakt logiczny:

```text
normalize_polygon_forex_ohlcv_response(raw_response) -> list[OhlcvBar]
```

Normalizator powinien:

* sprawdzić, czy `raw_response.provider` odpowiada providerowi Polygon/Massive,
* odczytać listę świec z pola `results`,
* dla każdej świecy odczytać pola `t`, `o`, `h`, `l`, `c`, `v`,
* zamienić timestamp providera z milisekund Unix na `datetime`,
* utworzyć listę `OhlcvBar`,
* zachować kolejność świec z payloadu,
* nie wykonywać połączeń sieciowych,
* nie wymagać API key,
* nie zapisywać plików,
* nie tworzyć katalogu `data/datasets/`,
* nie uruchamiać `validate_dataset`,
* nie uruchamiać `load_dataset`,
* nie nadawać statusów datasetu.

Na tym etapie normalizator nie powinien jeszcze obsługiwać:

* innych providerów,
* innych klas aktywów,
* wielu formatów odpowiedzi,
* paginacji,
* `next_url`,
* retry,
* limitów API,
* autoryzacji,
* walidacji kompletności całego datasetu,
* korekt stref czasowych poza jawną konwersją timestampu z payloadu.

Testy offline następnego kroku kodowego powinny potwierdzać, że:

* przykładowy payload `C:EURUSD` zwraca listę dwóch `OhlcvBar`,
* pola OHLCV są mapowane bez zmiany wartości,
* timestamp w milisekundach Unix jest zamieniany na `datetime`,
* wynik zachowuje kolejność świec,
* normalizator nie tworzy plików ani katalogu `data/datasets/`,
* normalizator nie wymaga API key,
* normalizator nie wykonuje połączeń sieciowych.


Elementy normalizacji po 74E.4:

```text
src/tradinglab/data_engine/connectors/polygon_forex.py          -> zaimplementowane po 74E.4
tests/data_engine/test_polygon_forex_normalization.py           -> zaimplementowane po 74E.4
```

Po mikro-kroku 74E.4 offline'owy normalizator przykładowej odpowiedzi Polygon/Massive do `OhlcvBar` został zaimplementowany jako `normalize_polygon_forex_ohlcv_response`.

Ten krok nadal nie wykonuje połączeń sieciowych, nie wymaga API key, nie zapisuje plików, nie tworzy katalogu `data/datasets/`, nie uruchamia `validate_dataset`, nie uruchamia `load_dataset` i nie nadaje statusów datasetu.

Następny krok powinien pozostać mały: audyt po 74E.4, a dopiero później decyzja, czy iść w zapis znormalizowanych świec do istniejącego przepływu datasetu, czy najpierw doprecyzować obsługę błędnych payloadów providera.

### 4.4. Polityka błędnych payloadów providera i granica zabezpieczeń

Po mikro-kroku 74E.5 projekt rozróżnia dwie warstwy zabezpieczeń dla danych pochodzących od providera:

```text
warstwa 1: minimalna bramka bezpieczeństwa przed zapisem datasetu
warstwa 2: przyszła pełna obsługa produkcyjnego API providera
```

To rozróżnienie jest ważne, ponieważ obecny normalizator Polygon/Massive ma być bezpiecznym elementem offline, ale nie jest jeszcze pełnym produkcyjnym konektorem API.

Zabezpieczenia minimalne mają chronić przed przekazaniem ewidentnie błędnego payloadu dalej do zapisu datasetu.

Nie oznaczają jeszcze pełnej obsługi wszystkich problemów, które mogą wystąpić przy prawdziwym pobieraniu danych z internetu.

#### Warstwa 1 — minimalna bramka bezpieczeństwa przed zapisem datasetu

Minimalna bramka bezpieczeństwa dotyczy normalizatora:

```text
normalize_polygon_forex_ohlcv_response(raw_response) -> list[OhlcvBar]
```

Jej celem jest upewnienie się, że z surowej odpowiedzi providera można bezpiecznie utworzyć listę `OhlcvBar`.

Na tym etapie normalizator powinien sprawdzać tylko podstawowy kształt payloadu i podstawową możliwość konwersji danych.

Minimalne zabezpieczenia powinny obejmować:

* `raw_response.provider` musi wskazywać obsługiwanego providera, czyli `polygon_massive`,
* `raw_response.raw_payload` musi być słownikiem albo obiektem typu mapping,
* payload musi zawierać pole `results`,
* `results` musi być listą,
* każdy element `results` musi być słownikiem albo obiektem typu mapping,
* każda świeca musi zawierać pola `t`, `o`, `h`, `l`, `c`, `v`,
* pole `t` musi dać się zamienić z milisekund Unix na `datetime` UTC,
* pola `o`, `h`, `l`, `c`, `v` muszą dać się zamienić na `Decimal`.

Zasada błędu w tej warstwie:

```text
błędny payload = przerwać normalizację jasno i głośno
```

Normalizator nie powinien:

* pomijać błędnych świec po cichu,
* zwracać częściowej listy świec, jeśli jedna świeca jest błędna,
* poprawiać danych providera na podstawie domysłów,
* zapisywać częściowych danych na dysku,
* tworzyć katalogu `data/datasets/`,
* uruchamiać `validate_dataset`,
* uruchamiać `load_dataset`,
* nadawać statusów datasetu.

Jeżeli jedna świeca w payloadzie jest błędna, cała normalizacja powinna zostać przerwana.

To podejście jest bezpieczniejsze na obecnym etapie niż ciche pomijanie błędnych rekordów, ponieważ projekt nie ma jeszcze warstwy raportowania jakości odpowiedzi providera.

#### Warstwa 2 — przyszła pełna obsługa produkcyjnego API providera

Pełna obsługa produkcyjnego API nie należy jeszcze do mikro-kroków 74E.5 ani 74E.6.

Ta warstwa będzie potrzebna dopiero wtedy, gdy projekt przejdzie od offline normalizacji do prawdziwego pobierania danych z Polygon/Massive.

Przyszła pełna obsługa produkcyjna powinna objąć osobne decyzje i testy dla takich tematów jak:

* status odpowiedzi API,
* błędy autoryzacji,
* brak albo niepoprawny API key,
* limity API,
* timeouty,
* retry,
* paginacja,
* `next_url`,
* puste odpowiedzi,
* niepełny zakres dat,
* duplikaty świec,
* luki w danych,
* różnice stref czasowych,
* kontrola kompletności datasetu,
* raportowanie jakości odpowiedzi providera,
* decyzja, czy pusty wynik jest błędem, czy poprawną odpowiedzią bez danych,
* decyzja, czy częściowo poprawna odpowiedź może być zapisana do `raw/response.json`,
* decyzja, czy częściowo poprawna odpowiedź może tworzyć `normalized/candles.csv`.

Te tematy nie powinny być mieszane z minimalnym offline normalizatorem.

#### Granica odpowiedzialności obecnego etapu

Mikro-krok 74E.5 nie zmienia kodu.

Mikro-krok 74E.6 powinien wdrożyć tylko minimalną bramkę bezpieczeństwa dla błędnych payloadów providera.

Po 74E.6 normalizator powinien być wystarczająco bezpieczny, żeby nie przepuścić ewidentnie błędnych danych do kolejnego etapu projektu.

Nie powinien być jednak opisywany jako pełna produkcyjna obsługa API Polygon/Massive.

Najważniejsza zasada tego etapu:

```text
minimalne zabezpieczenia przed zapisem datasetu teraz,
pełna obsługa produkcyjnego API później
```

Po mikro-kroku 74E.6 normalizator posiada czytelne błędy dla nieobsługiwanego providera, niepoprawnego typu payloadu, braku pola `results`, niepoprawnego typu `results`, niepoprawnego typu pojedynczej świecy, brakujących pól `t`, `o`, `h`, `l`, `c`, `v`, błędnej konwersji timestampu oraz błędnej konwersji wartości OHLCV do `Decimal`.

Ten krok nadal nie wykonuje połączeń sieciowych, nie wymaga API key, nie zapisuje plików, nie tworzy katalogu `data/datasets/`, nie uruchamia `validate_dataset`, nie uruchamia `load_dataset` i nie nadaje statusów datasetu.

### 4.5. Plan offline zapisu znormalizowanych świec providera do datasetu

Po mikro-krokach 74E.4-74E.6 projekt ma już bezpieczny offline normalizator odpowiedzi Polygon/Massive Forex do listy `OhlcvBar`.

Następny etap nie powinien jeszcze pobierać danych z internetu.

Najpierw projekt powinien umieć przeprowadzić pełny przepływ datasetu na lokalnym, testowym payloadzie providera.

Planowany przepływ offline:

```text
ProviderRawResponse
-> normalize_polygon_forex_ohlcv_response(raw_response)
-> list[OhlcvBar]
-> zapis raw/response.json
-> zapis normalized/candles.csv
-> validate_dataset
-> load_dataset
```

Celem tego etapu jest sprawdzenie, czy dane znormalizowane z formatu providera mogą wejść do tego samego przepływu datasetu, który jest już używany dla danych przykładowych.

Ten etap powinien korzystać z istniejących elementów Data Engine wszędzie tam, gdzie to możliwe.

Nie powinien tworzyć równoległego systemu zapisu danych.

#### Granica etapu 74F

Etap 74F nadal pozostaje etapem offline.

W tym etapie nie wolno jeszcze:

* wykonywać połączeń sieciowych,
* wymagać API key,
* pobierać danych z realnego Polygon/Massive API,
* obsługiwać paginacji,
* obsługiwać `next_url`,
* obsługiwać retry,
* obsługiwać timeoutów,
* budować pełnej produkcyjnej obsługi błędów API,
* uruchamiać automatycznego harmonogramu pobierania danych,
* mieszać danych testowych z realnymi danymi pobranymi z internetu.

Dane wejściowe w 74F powinny pochodzić z lokalnego, kontrolowanego payloadu testowego.

#### Zakładany minimalny efekt po etapie 74F

Po zakończeniu etapu 74F projekt powinien umieć utworzyć dataset z payloadu providera offline.

Minimalny widoczny efekt:

```text
data/datasets/<dataset_id>/
├── metadata.json
├── raw/
│   └── response.json
├── normalized/
│   └── candles.csv
└── validation/
    └── report.json
```

Po utworzeniu datasetu powinno być możliwe użycie publicznego loadera:

```text
load_dataset(dataset_id)
```

Oczekiwany wynik:

```text
status datasetu: VALIDATED
status walidacji: valid
liczba świec: zgodna z payloadem testowym
```

#### Zasady bezpieczeństwa zapisu

Zapis datasetu powinien nastąpić dopiero po poprawnym zakończeniu normalizacji.

Jeżeli normalizator zgłosi `PolygonForexPayloadError`, etap zapisu nie powinien tworzyć częściowego datasetu.

W szczególności błędny payload nie powinien tworzyć:

* częściowego `normalized/candles.csv`,
* częściowego `metadata.json`,
* częściowego `validation/report.json`,
* datasetu oznaczonego jako poprawny.

Najważniejsza zasada:

```text
najpierw pełna poprawna normalizacja,
dopiero potem zapis datasetu
```

#### Plan mikro-kroków dla 74F

Etap 74F powinien być podzielony na małe kroki:

```text
74F.0-DOC  -> plan offline zapisu znormalizowanych świec do datasetu
74F.1-AUDIT -> sprawdzenie istniejących funkcji zapisu datasetu i sample flow
74F.2-CODE -> test offline dla przepływu: payload providera -> dataset
74F.3-CODE -> implementacja minimalnego zapisu znormalizowanych świec przez istniejący mechanizm datasetu
74F.4-CODE -> mały skrypt/manualny przykład tworzący dataset z payloadu providera offline
74F.5-AUDIT -> audyt pełnego offline przepływu providera
```

Kolejny krok po 74F.0 powinien być audytem istniejącego kodu zapisu datasetu, żeby nie dublować logiki i nie tworzyć drugiego systemu zapisu danych.

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
timestamp,open,high,low,close,volume
2024-01-02T00:00:00+00:00,1.1034,1.1048,1.0921,1.0945,12345
```

Kolumny:

* `timestamp`,
* `open`,
* `high`,
* `low`,
* `close`,
* `volume`.

Kolumna `timestamp` przechowuje czas świecy. W obecnej implementacji Data Engine nazwa kolumny w pliku CSV jest zgodna z modelem `OhlcvBar.timestamp` oraz z nagłówkiem używanym przez helpery zapisu i odczytu OHLCV CSV.

Wartość timestampu powinna być zapisywana w formacie ISO 8601. Dla danych z czasem UTC obecny format zapisu używa jawnego offsetu, na przykład:

```text
2024-01-02T00:00:00+00:00
```

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

W poprzednich mikro-krokach implementacja Data Engine używała uproszczonego artefaktu:

```text
data.csv
```

Ten plik pełnił rolę tymczasowego pliku ze znormalizowanymi świecami OHLCV. Nie był docelową strukturą datasetu v0.2.0.

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

Migracja z uproszczonego `data.csv` do docelowej struktury była wykonywana mikro-krokami:

1. zapisać decyzję architektoniczną w dokumentacji,
2. dodać helpery storage dla `raw/` i `normalized/`,
3. dodać testy nowych helperów storage,
4. przepiąć `create_dataset` na tworzenie katalogów `raw/` i `normalized/`,
5. przepiąć zapis OHLCV z `data.csv` na `normalized/candles.csv`,
6. dodać przejściowy zapis `raw/response.json` dla sample datasetu,
7. przepiąć walidator i sample dataset na `normalized/candles.csv`,
8. wygasić tworzenie tymczasowego `data.csv`,
9. usunąć legacy helper `build_data_path`,
10. zaktualizować testy i dokumentację po zakończeniu migracji.

Po mikro-kroku 71G `data.csv` nie jest już tworzony przez `create_dataset` ani przez sample dataset.

Po mikro-kroku 71H helper `build_data_path()` został usunięty ze storage. Data Engine nie udostępnia już helpera prowadzącego do legacy ścieżki:

```text
data/datasets/{dataset_id}/{version}/data.csv
```

Docelową ścieżką dla znormalizowanych świec OHLCV jest:

```text
data/datasets/{dataset_id}/{version}/normalized/candles.csv
```

Pozostałe wystąpienia nazwy `data.csv` w testach mogą oznaczać lokalne, tymczasowe pliki CSV używane wewnątrz testów jednostkowych. Nie są one artefaktem struktury datasetu Data Engine.

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

Do testów automatycznych używane są małe dane tworzone bezpośrednio w testach, katalogi tymczasowe pytest, na przykład `tmp_path`, albo przyszłe jawnie dodane fixtures.

Na obecnym etapie repozytorium nie posiada katalogu:

```text
tests/fixtures/data_engine/
```

Jeżeli w przyszłości pojawi się potrzeba utrzymywania stałych fixtures, katalog testowy powinien zostać dodany osobnym mikro-krokiem razem z testami, które faktycznie go wykorzystują.

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

## 19. Minimalny publiczny interfejs Data Engine

Ten rozdział rozdziela:

1. obecnie zaimplementowany publiczny interfejs Data Engine,
2. docelowy minimalny publiczny interfejs dla pełniejszego zakresu v0.2.0,
3. zasady dalszego rozwoju publicznego interfejsu.

Obecny publiczny eksport z `tradinglab.data_engine` obejmuje:

```text
create_dataset
generate_dataset_id
validate_dataset
load_dataset
load_metadata
load_validation_report
load_normalized_candles
DatasetRequest
DatasetMetadata
DatasetBuildResult
DatasetLoadResult
OhlcvBar
ValidationReport
```

Docelowy minimalny publiczny interfejs Data Engine dla pełniejszego zakresu v0.2.0 obejmuje:

```text
create_dataset
validate_dataset
load_dataset
load_metadata
load_validation_report
load_normalized_candles
```

Po mikro-kroku 73A.1 publiczny odczyt metadanych, raportu walidacji i znormalizowanych świec został zaimplementowany.

Po mikro-kroku 73B.1 publiczna funkcja `validate_dataset` została zaimplementowana.

Po mikro-kroku 73C.1 `validate_dataset` wykonuje techniczną walidację znormalizowanego pliku OHLCV, zapisuje `validation_report.json` i aktualizuje status życia datasetu w `metadata.json`.

Po mikro-kroku 74B.1 publiczna funkcja `load_dataset` została zaimplementowana jako zbiorczy odczyt istniejącej wersji datasetu. Funkcja zwraca `DatasetLoadResult` zawierający metadane, raport walidacji, znormalizowane świece OHLCV oraz ścieżki artefaktów datasetu.

### 19.1. create_dataset

`create_dataset` jest obecnie publiczną funkcją tworzącą katalog wersji datasetu i początkowe artefakty.

Obecny zakres:

* tworzy katalog `data/datasets/{dataset_id}/{version}/`,
* zapisuje `metadata.json`,
* zapisuje początkowy `validation_report.json`,
* tworzy katalog `raw/`,
* tworzy katalog `normalized/`,
* zapisuje pusty `normalized/candles.csv`,
* zwraca `DatasetBuildResult`,
* nadaje datasetowi status życia `RAW`,
* nadaje początkowemu raportowi walidacji status `not_validated`.

### 19.2. validate_dataset

`validate_dataset` jest publiczną funkcją walidacji istniejącej wersji datasetu.

Obecny podpis funkcji:

```text
validate_dataset(*, base_data_dir, dataset_id, version)
```

Funkcja:

* przyjmuje katalog bazowy danych,
* przyjmuje `dataset_id`,
* przyjmuje `version`,
* buduje ścieżkę do wersji datasetu,
* waliduje plik `normalized/candles.csv`,
* zapisuje wynik walidacji do `validation_report.json`,
* aktualizuje `metadata.status` według wyniku walidacji,
* zwraca `ValidationReport`.

Funkcja jest zaimplementowana w:

```text
src/tradinglab/data_engine/engine.py
```

i eksportowana z:

```text
tradinglab.data_engine
```

Po mikro-kroku 73C.1 `validate_dataset` aktualizuje `metadata.status` według wyniku walidacji:

```text
validation_report.status = valid
    -> metadata.status = VALIDATED

validation_report.status = valid_with_warnings
    -> metadata.status = VALIDATED

validation_report.status = invalid
    -> metadata.status = QUARANTINED
```

`validate_dataset` nie nadaje automatycznie statusu `ACCEPTED` ani `REJECTED`.

`ACCEPTED` powinien oznaczać świadome dopuszczenie datasetu do użycia badawczego albo strategicznego.

`REJECTED` powinien oznaczać świadomą decyzję o odrzuceniu datasetu, a nie sam techniczny wynik walidacji.

### 19.3. load_metadata

`load_metadata` jest publiczną funkcją odczytu metadanych datasetu.

Obecny podpis funkcji:

```text
load_metadata(*, base_data_dir, dataset_id, version)
```

Funkcja:

* przyjmuje katalog bazowy danych,
* przyjmuje `dataset_id`,
* przyjmuje `version`,
* buduje ścieżkę do wersji datasetu,
* odczytuje `metadata.json`,
* zwraca `DatasetMetadata`.

Funkcja jest zaimplementowana w:

```text
src/tradinglab/data_engine/engine.py
```

i eksportowana z:

```text
tradinglab.data_engine
```

Odczyt przez bezpośrednią ścieżkę do pliku nadal istnieje technicznie w module `metadata.py`, ale publiczny interfejs domenowy powinien używać `base_data_dir + dataset_id + version`.

### 19.4. load_validation_report

`load_validation_report` jest publiczną funkcją odczytu raportu walidacji datasetu.

Obecny podpis funkcji:

```text
load_validation_report(*, base_data_dir, dataset_id, version)
```

Funkcja:

* przyjmuje katalog bazowy danych,
* przyjmuje `dataset_id`,
* przyjmuje `version`,
* buduje ścieżkę do wersji datasetu,
* odczytuje `validation_report.json`,
* zwraca `ValidationReport`.

Funkcja jest zaimplementowana w:

```text
src/tradinglab/data_engine/engine.py
```

i eksportowana z:

```text
tradinglab.data_engine
```

Odczyt przez bezpośrednią ścieżkę do pliku nadal istnieje technicznie w module `validation_report.py`, ale publiczny interfejs domenowy powinien używać `base_data_dir + dataset_id + version`.

### 19.5. load_normalized_candles

`load_normalized_candles` jest publiczną funkcją odczytu znormalizowanych świec OHLCV datasetu.

Obecny podpis funkcji:

```text
load_normalized_candles(*, base_data_dir, dataset_id, version)
```

Funkcja:

* przyjmuje katalog bazowy danych,
* przyjmuje `dataset_id`,
* przyjmuje `version`,
* buduje ścieżkę do wersji datasetu,
* odczytuje `normalized/candles.csv`,
* zwraca krotkę obiektów `OhlcvBar`.

Funkcja jest zaimplementowana w:

```text
src/tradinglab/data_engine/engine.py
```

i eksportowana z:

```text
tradinglab.data_engine
```

### 19.6. load_dataset

`load_dataset` jest publiczną funkcją zbiorczego odczytu istniejącej wersji datasetu.

Obecny podpis funkcji:

```text
load_dataset(*, base_data_dir, dataset_id, version)
```

Funkcja:

* przyjmuje katalog bazowy danych,
* przyjmuje `dataset_id`,
* przyjmuje `version`,
* buduje ścieżkę do wersji datasetu,
* odczytuje `metadata.json`,
* odczytuje `validation_report.json`,
* odczytuje `normalized/candles.csv`,
* zwraca `DatasetLoadResult`.

`DatasetLoadResult` zawiera:

```text
dataset_id
version
dataset_path
data_path
metadata_path
validation_report_path
metadata
validation_report
normalized_candles
status
```

Pole `status` w `DatasetLoadResult` oznacza status życia datasetu i jest zgodne z `metadata.status`.

`load_dataset` nie wykonuje walidacji, nie zmienia metadanych, nie zapisuje plików, nie wybiera najnowszej wersji datasetu i nie nadaje statusów `ACCEPTED` ani `REJECTED`.

Funkcja jest zaimplementowana w:

```text
src/tradinglab/data_engine/engine.py
```

i eksportowana z:

```text
tradinglab.data_engine
```

Publiczny interfejs Data Engine jest pokryty testami w:

```text
tests/data_engine/test_engine.py
```

### 19.7. Dalszy rozwój publicznego interfejsu

Publiczny interfejs Data Engine powinien pozostać mały, stabilny i domenowy.

Nowe funkcje publiczne powinny być dodawane dopiero wtedy, gdy:

* istnieje realna potrzeba użycia ich przez inny moduł projektu,
* ich zachowanie jest pokryte testami,
* ich nazwa i podpis nie ujawniają niepotrzebnie szczegółów technicznych,
* nie dublują istniejących funkcji technicznych bez jasnego celu,
* nie wymuszają zmiany znaczenia wcześniej dodanych funkcji publicznych.

Publiczny interfejs powinien operować na pojęciach domenowych:

```text
base_data_dir
dataset_id
version
DatasetMetadata
ValidationReport
OhlcvBar
DatasetLoadResult
```

a nie na przypadkowych ścieżkach do plików wewnętrznych.

Moduły techniczne, takie jak `metadata.py`, `validation_report.py`, `data_file.py`, `ohlcv_validation.py` i `storage.py`, mogą nadal istnieć jako warstwa niższego poziomu. Ich funkcje nie muszą być automatycznie eksportowane jako publiczne API pakietu.

Dalsze rozszerzenia publicznego interfejsu powinny być prowadzone mikro-krokami, bez mieszania ich ze zmianami statusów, zmianami formatu metadanych, zmianami walidatora albo implementacją konektorów providera.

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

## 23. Struktura modułów w src/tradinglab

Ten rozdział opisuje różnicę między:

1. obecną strukturą kodu Data Engine,
2. docelowym kierunkiem rozwoju struktury modułów.

Obecna implementacja Data Engine v0.2.0 jest bardziej rozbita na małe moduły niż pierwotny szkic architektoniczny. To nie jest błąd. Taki podział powstał w trakcie bezpiecznej implementacji mikro-krokami i pozwolił utrzymać testowalność oraz ograniczać wpływ zmian na inne obszary.

Obecna struktura kodu:

```text
src/
  tradinglab/
    __init__.py
    main.py
    data_engine/
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

Obecne odpowiedzialności:

| Plik / katalog | Odpowiedzialność |
| --- | --- |
| `data_engine/` | główny moduł Data Engine |
| `data_engine/__init__.py` | aktualny eksport technicznego interfejsu pakietu |
| `dataset_builder.py` | tworzenie katalogu wersji datasetu i początkowych artefaktów |
| `dataset_id.py` | generowanie deterministycznego `dataset_id` |
| `data_file.py` | zapis i odczyt plików OHLCV CSV |
| `engine.py` | publiczny domenowy interfejs Data Engine, w tym osobne odczyty, zbiorczy `load_dataset` i `validate_dataset` |
| `metadata.py` | serializacja, zapis i techniczny odczyt `metadata.json` |
| `models.py` | modele danych Data Engine |
| `ohlcv_validation.py` | walidacja lokalnych danych OHLCV CSV |
| `sample_dataset.py` | tworzenie przykładowego datasetu Data Engine |
| `status.py` | stałe statusów życia datasetu i statusów walidacji |
| `storage.py` | budowanie ścieżek i katalogów datasetu |
| `validation_report.py` | serializacja, zapis i techniczny odczyt `validation_report.json` |
| `main.py` | na razie minimalny plik wejściowy projektu |

Pierwotny szkic docelowy zakładał strukturę:

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

Ten szkic należy traktować jako kierunek architektoniczny, a nie jako opis aktualnego kodu.

Po mikro-kroku 73A.1 plik `engine.py` zawierał publiczny interfejs odczytu. Po mikro-kroku 73B.1 zawiera również publiczną funkcję `validate_dataset`. Po mikro-kroku 73C.1 `validate_dataset` aktualizuje także status życia datasetu w `metadata.json`. Po mikro-kroku 74B.1 zawiera również publiczne `load_dataset`, czyli zbiorczy odczyt metadanych, raportu walidacji, znormalizowanych świec i ścieżek artefaktów datasetu.

Na obecnym etapie nie istnieją jeszcze:

* `validation.py`,
* `connectors/base.py`,
* `connectors/polygon_forex.py`,
* publiczny konektor `PolygonForexConnector`.

Decyzje dotyczące tych elementów powinny być podejmowane osobnymi mikro-krokami, gdy będą wynikały z realnej potrzeby implementacyjnej.

Możliwy kierunek dalszego rozwoju:

| Docelowy element | Obecny stan | Decyzja |
| --- | --- | --- |
| `engine.py` | istnieje | Rozbudowywać ostrożnie jako publiczny interfejs Data Engine, bez przenoszenia do niego całej logiki technicznej. |
| `validation.py` | brak; istnieje `ohlcv_validation.py` | Nie tworzyć na siłę. Obecny walidator OHLCV działa w osobnym module. |
| `connectors/base.py` | brak | Dodać dopiero przed pierwszym prawdziwym konektorem providera. |
| `connectors/polygon_forex.py` | brak | Dodać dopiero przy implementacji pobierania danych z Polygon/Massive. |
| `PolygonForexConnector` | brak | Nadal jest docelowym konektorem referencyjnym, ale nie częścią obecnego kodu. |

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

* dodanie pierwszego konektora Polygon/Massive nie powinno wymagać przebudowy obecnych fundamentów datasetu,
* dodanie Dukascopy nie powinno zmieniać działania datasetów utworzonych wcześniej z innego providera,
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
| OHLCV-020 | Sample dataset generowany skryptem projektu | raport walidacji `valid`, brak błędów; metadata i wynik datasetu `VALIDATED` | sprawdzane testem i ręcznie |

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

* przyjęcie `DatasetRequest`,
* zbudowanie deterministycznego `dataset_id`,
* wyznaczenie katalogu wersji datasetu,
* utworzenie katalogów `raw/` i `normalized/`,
* zbudowanie ścieżek do `raw/response.json`, `normalized/candles.csv`, `metadata.json` i `validation_report.json`,
* zapis początkowego `metadata.json`,
* zapis początkowego `validation_report.json`,
* zapis pustego `normalized/candles.csv` z nagłówkiem OHLCV,
* zwrócenie `DatasetBuildResult`.

Warstwa buildera nie tworzy już przejściowego pliku `data.csv`. Docelowym plikiem danych znormalizowanych jest `normalized/candles.csv`.

Macierz scenariuszy dla budowania datasetu:

| ID | Scenariusz | Oczekiwany wynik | Status |
| ------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| DATASET_BUILDER-001 | Utworzenie datasetu na podstawie poprawnego `DatasetRequest` | Funkcja zwraca `DatasetBuildResult` i tworzy katalog wersji datasetu | pokryte testem |
| DATASET_BUILDER-002 | Zbudowanie ścieżek artefaktów datasetu | Wynik zawiera ścieżkę danych do `normalized/candles.csv` oraz ścieżki do `metadata.json` i `validation_report.json` | pokryte testem |
| DATASET_BUILDER-003 | Zapis początkowego `metadata.json` | Plik metadata istnieje i zawiera oczekiwane dane ze statusem `RAW` | pokryte testem |
| DATASET_BUILDER-004 | Zapis początkowego `validation_report.json` | Plik raportu walidacji istnieje i zawiera status `not_validated` oraz zerowe liczniki | pokryte testem |
| DATASET_BUILDER-005 | Zapis pustego `normalized/candles.csv` | Główny plik danych istnieje w `normalized/candles.csv` i zawiera wyłącznie nagłówek OHLCV | pokryte testem |
| DATASET_BUILDER-006 | Utworzenie początkowych artefaktów i katalogów datasetu | Katalog wersji zawiera `metadata.json`, `validation_report.json`, `raw/` i `normalized/` | pokryte testem |
| DATASET_BUILDER-007 | Próba utworzenia istniejącej wersji datasetu | Funkcja kończy się błędem i nie nadpisuje istniejącego katalogu wersji | pokryte testem |
| DATASET_BUILDER-008 | Utworzenie datasetu w nieistniejącym katalogu bazowym | Funkcja tworzy brakujące katalogi nadrzędne | pokryte testem |
| DATASET_BUILDER-009 | Utworzenie nowej wersji dla istniejącego `dataset_id` | Funkcja tworzy nowy katalog wersji bez naruszania poprzedniej wersji | pokryte testem |
| DATASET_BUILDER-010 | Rozdzielenie początkowych statusów między wynikiem, metadata i raportem walidacji | `DatasetBuildResult` i `metadata.json` mają status `RAW`, a `validation_report.json` ma status `not_validated` | pokryte testem |
| DATASET_BUILDER-011 | Utworzenie katalogów `raw/` i `normalized/` oraz pustego `normalized/candles.csv` | Katalog `raw/` istnieje i jest pusty, a katalog `normalized/` zawiera pusty plik `candles.csv` z nagłówkiem OHLCV | pokryte testem |
| DATASET_BUILDER-012 | Usunięcie przejściowego `data.csv` z buildera | `create_dataset` nie tworzy już pliku `data.csv` w katalogu wersji datasetu | pokryte testem |

Na obecnym etapie obszar budowania datasetu można uznać za domknięty dla zakresu v0.2.0.

Przyszłe rozszerzenia mogą obejmować obsługę częściowo utworzonych datasetów po błędzie zapisu, transakcyjność tworzenia artefaktów, dodatkowe klasy datasetów, walidację parametrów wejściowych oraz osobne strategie nadpisywania lub inkrementacji wersji. Nie należą one jednak do obecnego mikro-kroku domykania istniejącej warstwy budowania datasetu.

### 25.7. Macierz scenariuszy przykładowego datasetu

Warstwa przykładowego datasetu jest małym obszarem demonstracyjnym Data Engine.

Ten obszar odpowiada za:

* zbudowanie deterministycznego `DatasetRequest` dla przykładowych danych OHLCV,
* zbudowanie przykładowych świec OHLCV,
* utworzenie datasetu przez `create_dataset`,
* zapis przejściowej surowej odpowiedzi do `raw/response.json`,
* zapis przykładowych świec do `normalized/candles.csv`,
* uruchomienie publicznego `validate_dataset`,
* zapis finalnego `validation_report.json` przez publiczny przepływ walidacji,
* aktualizację `metadata.status` przez publiczny przepływ walidacji,
* odczyt aktualnego statusu datasetu przez publiczne `load_metadata`,
* zwrócenie `DatasetBuildResult` ze statusem zgodnym z `metadata.status`,
* opcjonalne usunięcie istniejącej wersji datasetu przy `overwrite=True`.

Warstwa sample datasetu nie tworzy już przejściowego pliku `data.csv`. Przykładowe świece są zapisywane do docelowego pliku `normalized/candles.csv`.

Po mikro-kroku 74A.1 warstwa sample datasetu nie powiela ręcznie logiki walidacji i aktualizacji metadanych. Po zapisaniu przykładowych świec korzysta z publicznego `validate_dataset`, a status zwracanego `DatasetBuildResult` ustala na podstawie `metadata.status` odczytanego przez publiczne `load_metadata`.

Po mikro-kroku 74D.1 pierwsze praktyczne użycie publicznego `load_dataset` poza testami publicznego interfejsu Data Engine zostało zaimplementowane w skrypcie przykładowego datasetu.

Pierwszym miejscem użycia jest skrypt:

```text
scripts/create_sample_dataset.py
```

Celem tego użycia jest pokazanie pełnego, małego przepływu demonstracyjnego:

```text
create_sample_ohlcv_dataset
    -> validate_dataset
    -> load_dataset
    -> krótkie podsumowanie załadowanego datasetu w terminalu
```

Ten przepływ ma potwierdzać, że utworzony i zwalidowany dataset może zostać odczytany przez publiczne API jako spójny `DatasetLoadResult`, bez ręcznego składania metadanych, raportu walidacji i znormalizowanych świec przez użytkownika skryptu.

Zakres 74D.1 pozostał mały:

* użyć `load_dataset` w `scripts/create_sample_dataset.py`,
* wypisać status życia datasetu z `DatasetLoadResult.status`,
* wypisać status walidacji z `DatasetLoadResult.validation_report.status`,
* wypisać liczbę świec z `DatasetLoadResult.normalized_candles`,
* zaktualizować test skryptu, aby potwierdzał nowe linie wyjścia.

Mikro-krok 74D.1 nie wprowadził:

* modułu research,
* modułu backtestingu,
* modułu strategii,
* wyboru najnowszej wersji datasetu,
* statusów `ACCEPTED` ani `REJECTED`,
* konektora providera,
* pobierania danych z internetu,
* zmian w formacie datasetu.

Macierz scenariuszy dla przykładowego datasetu:

| ID | Scenariusz | Oczekiwany wynik | Status |
| ------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| SAMPLE_DATASET-001 | Utworzenie przykładowego datasetu OHLCV | Katalog wersji zawiera `metadata.json`, `validation_report.json`, `raw/` i `normalized/` | pokryte testem |
| SAMPLE_DATASET-002 | Zapis znormalizowanych świec OHLCV | Odczyt `normalized/candles.csv` zwraca dokładnie świece z `build_sample_ohlcv_bars` | pokryte testem |
| SAMPLE_DATASET-003 | Walidacja sample datasetu przez publiczny przepływ walidacji | Metadata i wynik datasetu mają status `VALIDATED`, a raport walidacji ma status `valid` | pokryte testem |
| SAMPLE_DATASET-004 | Raport walidacji dla przykładowych świec | Raport ma 2 sprawdzone wiersze, 2 poprawne wiersze, 0 błędnych wierszy oraz brak błędów i ostrzeżeń | pokryte testem |
| SAMPLE_DATASET-005 | Uruchomienie skryptu `scripts/create_sample_dataset.py` | Skrypt kończy się sukcesem, wypisuje ścieżki artefaktów i tworzy katalog `data/datasets` | pokryte testem |
| SAMPLE_DATASET-006 | Deterministyczny `DatasetRequest` przykładowego datasetu | Request ma oczekiwane pola providera, instrumentu, typu danych, interwału i zakresu dat | pokryte testem |
| SAMPLE_DATASET-007 | Deterministyczne przykładowe świece OHLCV | Funkcja zwraca oczekiwane wartości timestampów, cen i wolumenów | pokryte testem |
| SAMPLE_DATASET-008 | Domyślna wersja przykładowego datasetu | Dataset jest tworzony z wersją `v001` | pokryte testem |
| SAMPLE_DATASET-009 | Utworzenie przykładowego datasetu z niestandardową wersją | Dataset, metadata i raport walidacji używają przekazanej wersji, np. `v002` | pokryte testem |
| SAMPLE_DATASET-010 | Próba ponownego utworzenia datasetu bez `overwrite` | Funkcja kończy się błędem istniejącej wersji i nie nadpisuje danych | pokryte testem |
| SAMPLE_DATASET-011 | Ponowne utworzenie datasetu z `overwrite=True` | Istniejąca wersja datasetu zostaje usunięta i odtworzona z poprawnymi artefaktami | pokryte testem |
| SAMPLE_DATASET-012 | Spójność pól metadata z przykładowym requestem | `metadata.json` zachowuje pola z `build_sample_dataset_request` i status po walidacji | pokryte testem |
| SAMPLE_DATASET-013 | Spójność ścieżek i statusów wyniku | `DatasetBuildResult` wskazuje `normalized/candles.csv`, ma status zgodny z `metadata.status`, a raport walidacji ma status `valid` | pokryte testem |
| SAMPLE_DATASET-014 | Zapis przejściowego `raw/response.json` | Plik `raw/response.json` istnieje i zawiera wynik `build_sample_raw_response` | pokryte testem |
| SAMPLE_DATASET-015 | Zapis `normalized/candles.csv` w sample dataset | Plik `normalized/candles.csv` istnieje i zawiera przykładowe świece OHLCV | pokryte testem |
| SAMPLE_DATASET-016 | Brak przejściowego `data.csv` w sample dataset | Katalog wersji sample datasetu nie zawiera już pliku `data.csv` | pokryte testem |
| SAMPLE_DATASET-017 | Użycie publicznego `load_dataset` w skrypcie przykładowego datasetu | Skrypt po utworzeniu datasetu ładuje go przez publiczne `load_dataset` i wypisuje status datasetu, status walidacji oraz liczbę świec | pokryte testem po 74D.1 |

Po mikro-kroku 74D.1 obszar przykładowego datasetu pozostaje domknięty dla dotychczas zaimplementowanego zakresu v0.2.0 i posiada mały krok demonstracyjny `SAMPLE_DATASET-017`, który pokazuje użycie publicznego `load_dataset` w skrypcie przykładowego datasetu.

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
* katalogu danych surowych `raw/`,
* pliku surowej odpowiedzi providera `raw/response.json`,
* katalogu danych znormalizowanych `normalized/`,
* pliku znormalizowanych świec OHLCV `normalized/candles.csv`,
* pliku metadanych `metadata.json`,
* pliku raportu walidacji `validation_report.json`.

Warstwa storage nie tworzy katalogów, nie zapisuje plików, nie odczytuje plików i nie waliduje nazw. Te odpowiedzialności należą do innych warstw albo przyszłych rozszerzeń.

Legacy helper `build_data_path()` został usunięty po mikro-kroku 71H. Storage nie udostępnia już helpera prowadzącego do ścieżki `{dataset_path}/data.csv`.

Macierz scenariuszy dla ścieżek storage:

| ID | Scenariusz | Oczekiwany wynik | Status |
| ------------ | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| STORAGE-001 | Zbudowanie ścieżki katalogu wersji datasetu | Funkcja zwraca ścieżkę `{base_data_dir}/datasets/{dataset_id}/{version}` | pokryte testem |
| STORAGE-002 | Zbudowanie ścieżki `metadata.json` | Funkcja zwraca ścieżkę `{dataset_path}/metadata.json` | pokryte testem |
| STORAGE-003 | Zbudowanie ścieżki `validation_report.json` | Funkcja zwraca ścieżkę `{dataset_path}/validation_report.json` | pokryte testem |
| STORAGE-004 | Zbudowanie ścieżki katalogu `raw/` | Funkcja zwraca ścieżkę `{dataset_path}/raw` | pokryte testem |
| STORAGE-005 | Zbudowanie ścieżki `raw/response.json` | Funkcja zwraca ścieżkę `{dataset_path}/raw/response.json` | pokryte testem |
| STORAGE-006 | Zbudowanie ścieżki katalogu `normalized/` | Funkcja zwraca ścieżkę `{dataset_path}/normalized` | pokryte testem |
| STORAGE-007 | Zbudowanie ścieżki `normalized/candles.csv` | Funkcja zwraca ścieżkę `{dataset_path}/normalized/candles.csv` | pokryte testem |
| STORAGE-008 | Helpery storage nie tworzą katalogów ani plików | Samo zbudowanie ścieżek nie powoduje efektów ubocznych w systemie plików | pokryte testem |
| STORAGE-009 | Obsługa niestandardowego katalogu bazowego | Ścieżka wersji datasetu jest budowana względem przekazanego `base_data_dir` | pokryte testem |
| STORAGE-010 | Obsługa niestandardowej wersji datasetu | Ścieżka wersji datasetu zawiera dokładnie przekazany numer wersji, np. `v002` | pokryte testem |
| STORAGE-011 | Spójność nazw artefaktów storage z `DatasetBuildResult` | `DatasetBuildResult.data_path` wskazuje `normalized/candles.csv`, a pozostałe ścieżki wskazują `metadata.json` i `validation_report.json` | pokryte testem |
| STORAGE-012 | Obsługa docelowych ścieżek `raw/` i `normalized/` w storage | Warstwa storage udostępnia helpery dla `raw/`, `raw/response.json`, `normalized/` i `normalized/candles.csv` | pokryte testem |

Na obecnym etapie obszar ścieżek storage można uznać za domknięty dla zakresu v0.2.0.

Po mikro-kroku 71H storage udostępnia helpery dla docelowych ścieżek `raw/`, `raw/response.json`, `normalized/` i `normalized/candles.csv`. Legacy helper `build_data_path()` został usunięty i nie powinien wracać bez osobnej decyzji projektowej.

Przyszłe rozszerzenia storage mogą obejmować formaty inne niż CSV oraz walidację bezpieczeństwa ścieżek. Nie należą one jednak do obecnego zakresu domykania migracji z przejściowego `data.csv` na docelowe `normalized/candles.csv`.

### 25.10. Macierz scenariuszy statusów Data Engine

Statusy Data Engine są osobnym obszarem, ponieważ w projekcie występują dwa różne pojęcia:

1. status życia datasetu,
2. status wyniku walidacji.

Status życia datasetu jest zapisywany w `metadata.json`.

Status wyniku walidacji jest zapisywany w `validation_report.json`.

`DatasetBuildResult.status` oznacza status życia datasetu, a nie status wyniku walidacji.

Docelowe statusy życia datasetu:

| Status | Znaczenie |
| --- | --- |
| `RAW` | Dataset został utworzony i zawiera artefakty startowe albo dane źródłowe. |
| `VALIDATED` | Dataset przeszedł proces walidacji i może być dalej rozpatrywany. |
| `ACCEPTED` | Dataset został zaakceptowany do dalszego użycia. |
| `QUARANTINED` | Dataset wymaga uwagi, ale nie musi być od razu odrzucony. |
| `REJECTED` | Dataset nie powinien być używany. |
| `DEPRECATED` | Dataset został zastąpiony albo uznany za przestarzały. |

Docelowe statusy wyniku walidacji:

| Status | Znaczenie |
| --- | --- |
| `not_validated` | Raport walidacji istnieje technicznie, ale właściwa walidacja nie została jeszcze wykonana. |
| `valid` | Dane przeszły walidację bez błędów. |
| `valid_with_warnings` | Dane są technicznie używalne, ale mają ostrzeżenia. |
| `invalid` | Dane nie przeszły walidacji technicznej. |

Decyzja projektowa po migracji statusów:

1. `metadata.status` używa wyłącznie statusów życia datasetu.
2. `DatasetBuildResult.status` używa wyłącznie statusów życia datasetu.
3. `validation_report.status` używa wyłącznie statusów walidacji.
4. Status `invalid` nie jest statusem życia datasetu.
5. Legacy stałe `DATASET_STATUS_CREATED`, `DATASET_STATUS_VALIDATED`, `DATASET_STATUS_INVALID` oraz `LEGACY_DATASET_STATUSES` zostały usunięte po mikro-kroku 71P.
6. Status początkowy datasetu po `create_dataset` to `RAW`.
7. Status sample datasetu po udanej walidacji to `VALIDATED`, nadawany przez publiczny przepływ `validate_dataset`.
8. Migracja statusów nie obejmowała przebudowy schematu `metadata.json`, przebudowy `validation_report.json`, publicznego API ani konektorów providera.

Mapowanie wykonanej migracji:

| Dawny legacy status | Docelowy kierunek | Stan po migracji |
| --- | --- | --- |
| `created` | `RAW` | Zastąpiony w builderze po 71N. |
| `validated` | `VALIDATED` | Zastąpiony w sample dataset po 71O. |
| `invalid` | Status walidacji `invalid` | Usunięty jako status życia datasetu po 71P. |

Wykonane mikro-kroki migracji statusów legacy:

| Mikro-krok | Zakres | Wynik |
| --- | --- | --- |
| 71M | Dokumentacja | Zaprojektowano mapowanie legacy statusów na docelowe statusy życia datasetu. |
| 71N | Kod i testy buildera | `create_dataset` używa `RAW` zamiast `created`. |
| 71O | Kod i testy sample datasetu | Sample dataset po udanej walidacji używa `VALIDATED` zamiast `validated`. |
| 71P | Kod i testy statusów | Usunięto legacy stałe statusów datasetu. |
| 71Q | Dokumentacja końcowa | Dokumentacja opisuje stan po usunięciu legacy statusów. |

Macierz scenariuszy dla statusów Data Engine:

| ID | Scenariusz | Oczekiwany wynik | Status |
| --- | --- | --- | --- |
| STATUS-001 | Kod posiada osobne stałe statusów życia datasetu | Dostępne są stałe `DATASET_LIFECYCLE_STATUS_*` | pokryte testem |
| STATUS-002 | Kod posiada osobne stałe statusów walidacji | Dostępne są stałe `VALIDATION_STATUS_*`, w tym `VALIDATION_STATUS_NOT_VALIDATED` | pokryte testem |
| STATUS-003 | Statusy życia datasetu są unikalne | Lista `DATASET_LIFECYCLE_STATUSES` nie zawiera duplikatów | pokryte testem |
| STATUS-004 | Statusy walidacji są unikalne | Lista `VALIDATION_STATUSES` nie zawiera duplikatów | pokryte testem |
| STATUS-005 | Statusy życia datasetu i statusy walidacji nie mieszają się | Zbiory `DATASET_LIFECYCLE_STATUSES` i `VALIDATION_STATUSES` są rozłączne | pokryte testem |
| STATUS-006 | Legacy statusy datasetu nie są częścią kodu docelowego | `DATASET_STATUS_CREATED`, `DATASET_STATUS_VALIDATED`, `DATASET_STATUS_INVALID` i `LEGACY_DATASET_STATUSES` nie są już eksportowane z `status.py` | domknięte po 71P |
| STATUS-007 | `metadata.status` używa statusu życia datasetu | `metadata.json` korzysta ze statusów życia datasetu, np. `RAW` albo `VALIDATED` | pokryte testami buildera i sample datasetu |
| STATUS-008 | `validation_report.status` używa statusu walidacji | `validation_report.json` korzysta z `not_validated`, `valid`, `valid_with_warnings` albo `invalid` | pokryte testem |
| STATUS-009 | `DatasetBuildResult.status` oznacza status życia datasetu | Wynik budowania datasetu nie używa statusu walidacji jako statusu datasetu | pokryte testami buildera i sample datasetu |
| STATUS-010 | Początkowy dataset po `create_dataset` otrzymuje status życia `RAW` | `DatasetBuildResult.status` i `metadata.status` po utworzeniu datasetu wskazują `RAW` | pokryte testem |
| STATUS-011 | Dataset po udanej walidacji otrzymuje status życia `VALIDATED` | Sample dataset oraz publiczne `validate_dataset` po wyniku walidacji `valid` ustawiają `metadata.status` na `VALIDATED` | pokryte testami |
| STATUS-012 | Nieudana walidacja nie używa `invalid` jako statusu życia datasetu | Publiczne `validate_dataset` po wyniku walidacji `invalid` zapisuje `validation_report.status = invalid` i ustawia `metadata.status` na `QUARANTINED` | pokryte testem |

Po mikro-krokach 68 i 69 status raportu walidacji został oddzielony od statusu datasetu.

Po mikro-krokach 71M–71P usunięto tymczasowe statusy legacy i przepięto obecny kod na docelowe statusy życia datasetu w zakresie obsługiwanym przez v0.2.0.

Obszar statusów można uznać za domknięty dla obecnego zakresu v0.2.0 pod warunkiem, że:

1. `create_dataset` nadal używa `RAW` jako początkowego statusu życia datasetu,
2. sample dataset po udanej walidacji nadal używa `VALIDATED` jako statusu życia datasetu i pobiera ten status z `metadata.status`,
3. `validation_report.status` nadal używa wyłącznie statusów walidacji,
4. legacy statusy nie wracają bez osobnej decyzji projektowej,
5. przyszłe scenariusze nieudanej walidacji datasetu zostaną zaprojektowane osobno przed implementacją.

## 26. Struktura testów

Ten rozdział rozdziela:

1. obecną strukturę testów,
2. możliwy kierunek dalszego rozwoju testów.

Obecna struktura testów Data Engine:

```text
tests/
  test_smoke.py
  data_engine/
    test_create_sample_dataset_script.py
    test_data_file.py
    test_dataset_build_result_model.py
    test_dataset_builder.py
    test_dataset_id.py
    test_engine.py
    test_metadata.py
    test_models.py
    test_ohlcv_bar_model.py
    test_ohlcv_validation.py
    test_sample_dataset.py
    test_status.py
    test_storage.py
    test_validation_report.py
    test_validation_report_model.py
```

Obecne testy używają przede wszystkim:

* małych danych tworzonych bezpośrednio w testach,
* katalogów tymczasowych pytest, na przykład `tmp_path`,
* lokalnych tymczasowych plików CSV,
* przykładowego datasetu generowanego przez kod projektu.

Na obecnym etapie nie istnieje katalog:

```text
tests/fixtures/data_engine/
```

Na obecnym etapie nie istnieje jeszcze plik:

```text
tests/data_engine/test_validation.py
```

Brak tego pliku nie jest błędem. Obecna implementacja ma rozdzielone testy zgodnie z faktycznymi modułami kodu, między innymi `dataset_builder.py`, `engine.py`, `ohlcv_validation.py`, `metadata.py`, `validation_report.py`, `storage.py`, `sample_dataset.py` i `status.py`.

Plik `tests/data_engine/test_engine.py` istnieje od mikro-kroku 73A.1. Po mikro-kroku 73B.1 pokrywa publiczny interfejs odczytu Data Engine oraz publiczną funkcję `validate_dataset`. Po mikro-kroku 73C.1 pokrywa również aktualizację `metadata.status` po walidacji. Po mikro-kroku 74B.1 pokrywa także publiczne `load_dataset`.

Możliwy kierunek dalszego rozwoju testów:

```text
tests/
  data_engine/
    test_public_api.py
    test_connectors_base.py
    test_polygon_forex_connector.py
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

Ten kierunek należy traktować jako plan na przyszłość, a nie jako opis aktualnego repozytorium.

Nowe fixtures, testy publicznego API, testy konektorów i testy providera powinny być dodawane dopiero wtedy, gdy powstanie odpowiadająca im funkcjonalność w kodzie.

Testy automatyczne Data Engine nadal nie powinny wymagać:

* prawdziwego API key,
* internetu,
* dostępności zewnętrznego providera,
* limitów API,
* ręcznie przygotowanego lokalnego katalogu `data/datasets/`.

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
