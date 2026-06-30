# Data Engine

## Dokument implementacyjny

Szczegółowy projekt implementacji Data Engine v0.2.0 znajduje się w dokumencie:

- [DATA_ENGINE_IMPLEMENTACJA_V0_2.md](DATA_ENGINE_IMPLEMENTACJA_V0_2.md)

## Status dokumentu

Dokument architektoniczny dla etapu:

**v0.2.0 — Data Engine**

Ten dokument opisuje cel, odpowiedzialności, granice i kierunek rozwoju modułu Data Engine w projekcie TradingLab.

Dokument nie opisuje jeszcze szczegółowej implementacji kodu. Implementacja powinna wynikać z ustaleń architektonicznych zapisanych w tym dokumencie.

---

## 1. Cel Data Engine

Data Engine jest modułem odpowiedzialnym za cały cykl życia danych rynkowych wykorzystywanych w TradingLab.

Jego podstawowym celem jest dostarczenie danych, które są:

* uporządkowane,
* sprawdzalne,
* odtwarzalne,
* audytowalne,
* opisane metadanymi,
* możliwe do wykorzystania przez kolejne moduły systemu,
* bezpieczne z punktu widzenia badań i przyszłego handlu automatycznego.

Data Engine nie jest jednorazowym skryptem do pobierania danych. Jest fundamentem danych dla całej platformy TradingLab.

---

## 2. Wizja docelowa

Docelowo Data Engine powinien stać się profesjonalnym, rozszerzalnym i niezależnym od konkretnego dostawcy silnikiem danych.

W przyszłości Data Engine powinien umożliwiać obsługę między innymi:

* wielu źródeł danych,
* wielu klas aktywów,
* wielu typów danych,
* danych historycznych,
* danych przyrostowych,
* danych live,
* danych świecowych OHLCV,
* danych tickowych,
* danych order book,
* danych fundamentalnych,
* danych makroekonomicznych,
* danych alternatywnych,
* wielu interwałów czasowych,
* różnych kalendarzy sesyjnych,
* różnych stref czasowych,
* kontroli jakości danych,
* wersjonowania datasetów,
* porównywania danych z wielu źródeł,
* audytu pochodzenia danych,
* powiązania wyników badań z konkretną wersją danych,
* przyszłej integracji z kontrolowanymi agentami AI.

Pierwsza implementacja może być prosta, ale decyzje architektoniczne nie powinny blokować przyszłego rozwoju Data Engine do znacznie bardziej zaawansowanego poziomu.

---

## 3. Zakres v0.2.0

Wersja v0.2.0 obejmuje minimalny, ale solidny fundament Data Engine.

Zakres v0.2.0:

* zaprojektowanie modułu Data Engine,
* obsługa historycznych danych świecowych OHLCV,
* pobieranie danych z pierwszego źródła danych,
* zapis danych surowych,
* zapis metadanych datasetu,
* podstawowa walidacja jakości danych,
* zapis raportu walidacji,
* nadanie statusu datasetu,
* możliwość odtworzenia źródła danych,
* przygotowanie struktury pod dalszy rozwój.

Poza zakresem v0.2.0 pozostają:

* dane tickowe,
* order book,
* dane live,
* dane fundamentalne,
* dane makroekonomiczne,
* automatyczny harmonogram pobierania danych,
* backtesting,
* strategie inwestycyjne,
* wykonywanie transakcji,
* zarządzanie ryzykiem,
* dashboard,
* agenci AI,
* pełna hurtownia danych.

---

## 4. Odpowiedzialności Data Engine

Data Engine odpowiada za:

* pobieranie danych rynkowych ze źródeł danych,
* zapis danych surowych,
* zachowanie nietykalności danych surowych,
* opisanie danych metadanymi,
* walidację jakości danych,
* zapis raportów walidacji,
* nadawanie statusów datasetom,
* wersjonowanie datasetów,
* udostępnianie danych innym modułom TradingLab,
* umożliwienie odtworzenia źródła danych,
* przygotowanie danych do użycia w badaniach, backtestach i walidacji.

Data Engine jest odpowiedzialny za to, aby inne moduły TradingLab nie musiały zgadywać:

* skąd pochodzą dane,
* jaki mają zakres,
* kiedy zostały pobrane,
* jaką mają jakość,
* czy były walidowane,
* czy są dopuszczone do użycia,
* czy istnieją znane problemy jakościowe,
* jaka wersja danych została użyta.

---

## 5. Czego Data Engine nie robi

Data Engine nie odpowiada za:

* generowanie sygnałów kupna lub sprzedaży,
* tworzenie strategii,
* ocenę skuteczności strategii,
* wykonywanie backtestów,
* wykonywanie transakcji,
* zarządzanie ryzykiem,
* podejmowanie decyzji inwestycyjnych,
* optymalizację parametrów strategii,
* interpretację wyników inwestycyjnych,
* obchodzenie procesu badawczego,
* automatyczne poprawianie danych surowych bez śladu.

Data Engine nie może być miejscem, w którym ukryta logika inwestycyjna miesza się z logiką danych.

---

## 6. Miejsce Data Engine w architekturze TradingLab

Data Engine jest jednym z głównych modułów typu Engine w architekturze TradingLab.

Jego zadaniem jest dostarczenie danych dla kolejnych modułów, takich jak:

* Strategy Engine,
* Backtesting Engine,
* Research Engine,
* Validation Engine,
* Analytics Engine,
* Trading Engine.

Data Engine powinien być możliwie niezależny od pozostałych modułów.

Pozostałe moduły nie powinny bezpośrednio zależeć od fizycznego formatu zapisu danych. Powinny korzystać z danych przez jasno określone interfejsy Data Engine.

---

## 7. Podstawowe pojęcia

### 7.1. Dataset

Dataset to logiczny zestaw danych rynkowych wraz z informacjami potrzebnymi do jego identyfikacji, walidacji, audytu i ponownego użycia.

Dataset to nie tylko plik z cenami.

Dataset składa się z:

* danych,
* metadanych,
* raportu walidacji,
* statusu,
* wersji,
* informacji o źródle,
* informacji o pochodzeniu,
* historii przetwarzania, jeśli dane były przetwarzane.

Minimalna definicja datasetu nie zamyka możliwości dodawania kolejnych elementów w przyszłości.

---

### 7.2. Raw data

Raw data to dane zapisane dokładnie w postaci otrzymanej ze źródła lub w najbliższej możliwej postaci technicznej, bez merytorycznej ingerencji w ich treść.

Raw data są nietykalne.

Po zapisaniu dane surowe nie powinny być modyfikowane.

Jeżeli dane wymagają oczyszczenia, uzupełnienia, transformacji lub korekty, powinien powstać nowy dataset albo nowa wersja datasetu.

---

### 7.3. Metadata

Metadata to informacje opisujące dataset.

Metadane odpowiadają na pytania:

* co to za dane,
* skąd pochodzą,
* czego dotyczą,
* jaki mają zakres,
* kiedy zostały pobrane,
* jak zostały pobrane,
* gdzie są zapisane,
* jaka jest ich wersja,
* jaki jest ich status,
* czy przeszły walidację.

---

### 7.4. Validation report

Validation report to raport opisujący wynik walidacji danych.

Raport walidacji powinien zawierać konkretne wyniki reguł walidacyjnych, a nie tylko ogólną informację, że dane są dobre albo złe.

Raport walidacji powinien być możliwy do odczytania przez człowieka oraz w przyszłości przez kontrolowanego agenta AI.

### 7.4.1. Standard testowania walidacji danych

Walidacja danych w Data Engine musi być testowana restrykcyjnie.

Nie wystarczy sprawdzić, że poprawny dataset otrzymuje status `validated`.

Każdy walidator danych powinien posiadać testy obejmujące co najmniej:

* poprawny dataset,
* błędną strukturę pliku,
* błędne wartości pól,
* niespójności logiczne danych,
* przypadki graniczne,
* dane puste lub niekompletne,
* dataset zawierający jednocześnie poprawne i błędne rekordy,
* poprawność pól raportu walidacji, w szczególności statusu, listy błędów, ostrzeżeń oraz liczników sprawdzonych, poprawnych i błędnych rekordów.

Dla danych OHLCV oznacza to między innymi testowanie poprawności relacji `open`, `high`, `low`, `close`, poprawności wolumenu, kolejności czasu oraz duplikatów timestampów.


---

### 7.5. Dataset status

Dataset status określa stan datasetu w cyklu życia danych.

Status nie zastępuje raportu walidacji.

Status odpowiada głównie na pytanie:

> Co wolno zrobić z tym datasetem?

Raport walidacji odpowiada na pytanie:

> Jakie dokładnie problemy zostały wykryte?

---

## 8. Pierwszy obsługiwany typ danych

W v0.2.0 pierwszym obsługiwanym typem danych są historyczne dane świecowe OHLCV.

Minimalna struktura rekordu OHLCV:

```text
timestamp
open
high
low
close
volume
```

Znaczenie pól:

* `timestamp` — czas świecy,
* `open` — cena otwarcia,
* `high` — najwyższa cena w świecy,
* `low` — najniższa cena w świecy,
* `close` — cena zamknięcia,
* `volume` — wolumen, jeśli jest dostępny w źródle.

Architektura Data Engine nie powinna jednak zakładać, że OHLCV będzie jedynym typem danych w przyszłości.

---

## 9. Przyszłe typy danych

Data Engine powinien być projektowany tak, aby w przyszłości można było dodać inne typy danych bez przebudowy całej architektury.

Potencjalne przyszłe typy danych:

* tick data,
* bid/ask data,
* order book,
* trades,
* funding rates,
* open interest,
* dane fundamentalne,
* dane makroekonomiczne,
* kalendarze ekonomiczne,
* newsy,
* dane alternatywne,
* dane brokerskie,
* dane wykonania transakcji,
* dane portfela,
* dane ryzyka.

Każdy typ danych może wymagać własnej struktury rekordu, własnych metadanych i własnych reguł walidacji.

---

## 10. Źródła danych i konektory

Data Engine nie powinien być trwale powiązany z jednym dostawcą danych.

Dostęp do źródeł danych powinien odbywać się przez konektory.

Konektor odpowiada za komunikację z konkretnym źródłem danych.

Przykładowe źródła danych w przyszłości:

* giełda kryptowalut,
* broker,
* dostawca danych rynkowych,
* plik lokalny,
* API zewnętrzne,
* baza danych,
* źródło testowe.

W v0.2.0 może istnieć jeden pierwszy konektor referencyjny.

Nie oznacza to jednak, że Data Engine jest projektowany pod jedno konkretne źródło danych.

---

## 11. Minimalne metadane datasetu

Każdy dataset musi posiadać minimalny zestaw metadanych.

Minimalne metadane są wymaganym fundamentem, a nie zamkniętą listą na zawsze.

Minimalny zestaw metadanych dla v0.2.0:

```text
dataset_id
source
symbol
market
timeframe
data_type
date_from
date_to
timezone
downloaded_at
data_version
raw_path
validation_status
```

Znaczenie pól:

* `dataset_id` — unikalny identyfikator datasetu,
* `source` — źródło danych,
* `symbol` — symbol instrumentu,
* `market` — rynek lub klasa rynku,
* `timeframe` — interwał danych,
* `data_type` — typ danych, np. OHLCV,
* `date_from` — początek zakresu danych,
* `date_to` — koniec zakresu danych,
* `timezone` — strefa czasowa danych,
* `downloaded_at` — czas pobrania danych,
* `data_version` — wersja datasetu,
* `raw_path` — lokalizacja danych surowych,
* `validation_status` — status walidacji.

---

## 12. Rozszerzalność metadanych

W przyszłości dataset może posiadać dodatkowe metadane.

Przykładowe przyszłe metadane:

```text
exchange
asset_class
provider_endpoint
request_parameters
provider_response_id
instrument_id
price_adjustment_type
session_calendar
trading_hours
currency
base_currency
quote_currency
data_license
checksum
file_format
schema_version
ingestion_run_id
parent_dataset_id
transformation_history
quality_score
```

Dodanie nowych metadanych nie powinno unieważniać istniejących datasetów ani wyników badań.

Jeżeli zmienia się struktura metadanych, powinna istnieć możliwość wskazania wersji schematu metadanych.

---

## 13. Walidacja jakości danych

Data Engine powinien walidować dane przed dopuszczeniem ich do użycia w badaniach.

W v0.2.0 walidacja dotyczy historycznych danych świecowych OHLCV.

Minimalne reguły walidacji dla v0.2.0:

* sprawdzenie, czy dane istnieją,
* sprawdzenie, czy wymagane kolumny są dostępne,
* sprawdzenie, czy timestampy są poprawne,
* sprawdzenie, czy timestampy są uporządkowane rosnąco,
* wykrycie duplikatów timestampów,
* wykrycie brakujących świec,
* sprawdzenie zgodności interwału z metadanymi,
* sprawdzenie zgodności zakresu dat z metadanymi,
* sprawdzenie brakujących wartości OHLC,
* sprawdzenie, czy ceny nie są ujemne,
* sprawdzenie, czy `high >= low`,
* sprawdzenie, czy `open` mieści się między `low` i `high`,
* sprawdzenie, czy `close` mieści się między `low` i `high`.

Minimalna walidacja jest pierwszym zestawem reguł i nie ogranicza przyszłego rozwoju systemu walidacji.

---

## 14. Rozszerzalność walidacji

Walidacja danych powinna być projektowana jako zestaw reguł, które można rozszerzać.

Każda reguła walidacyjna powinna zwracać co najmniej:

```text
rule_id
result
severity
message
details
```

Przykład:

```text
rule_id: missing_candles
result: failed
severity: WARNING
message: Wykryto brakujące świece.
details: Brakuje 4 świec w zakresie 2024-01-01 10:00–14:00.
```

Przyszłe reguły walidacji mogą obejmować:

* wykrywanie anomalii cenowych,
* porównanie danych z innym źródłem,
* wykrywanie świec poza godzinami sesji,
* obsługę świąt i dni bez handlu,
* kontrolę stref czasowych,
* kontrolę zmiany czasu DST,
* analizę nietypowego wolumenu,
* wykrywanie stale data,
* kontrolę spreadu bid/ask,
* kontrolę korekt splitów i dywidend,
* walidację danych tickowych,
* walidację order book,
* walidację danych po transformacji.

---

## 15. Wagi problemów walidacyjnych

Problemy wykryte podczas walidacji powinny mieć określoną wagę.

Podstawowe poziomy severity:

```text
INFO
WARNING
ERROR
CRITICAL
```

Znaczenie:

* `INFO` — informacja techniczna, nie wpływa bezpośrednio na użyteczność datasetu,
* `WARNING` — problem, który może mieć znaczenie, ale nie zawsze blokuje użycie datasetu,
* `ERROR` — problem poważny, który zwykle powinien blokować dopuszczenie datasetu,
* `CRITICAL` — problem krytyczny, który powinien zatrzymać dalsze użycie datasetu do czasu wyjaśnienia.

Severity nie jest tym samym co status datasetu.

---

## 16. Statusy datasetów

Podstawowy cykl życia datasetu powinien być prosty, ale rozszerzalny.

Statusy datasetów w v0.2.0:

```text
RAW
VALIDATED
ACCEPTED
QUARANTINED
REJECTED
DEPRECATED
```

Znaczenie statusów:

* `RAW` — dane zostały pobrane i zapisane jako surowe,
* `VALIDATED` — walidacja została wykonana,
* `ACCEPTED` — dataset został dopuszczony do użycia,
* `QUARANTINED` — dataset wymaga wyjaśnienia,
* `REJECTED` — dataset został odrzucony,
* `DEPRECATED` — dataset został zastąpiony nowszą wersją albo nie powinien być używany w nowych badaniach.

Status datasetu mówi, co wolno zrobić z datasetem.

Szczegółowe informacje o problemach jakościowych znajdują się w raporcie walidacji.

---

## 17. Wersjonowanie datasetów

Data Engine powinien umożliwiać wersjonowanie datasetów.

Wersjonowanie jest konieczne, ponieważ wyniki badań muszą być możliwe do powiązania z konkretną wersją danych.

Nowa wersja datasetu powinna powstać między innymi wtedy, gdy:

* dane zostały pobrane ponownie,
* dane pochodzą z innego źródła,
* zakres danych został rozszerzony,
* dane zostały przetworzone,
* dane zostały oczyszczone,
* dane zostały uzupełnione,
* zmienił się sposób walidacji,
* zmienił się schemat danych,
* zmieniły się metadane istotne dla odtworzenia datasetu.

Starsze wersje datasetów nie powinny być usuwane tylko dlatego, że pojawiła się nowa wersja.

---

## 18. Zasada nietykalności danych surowych

Dane surowe są nietykalne.

Data Engine nie powinien modyfikować danych zapisanych jako raw.

Jeżeli dane wymagają zmiany, powinien powstać nowy dataset lub nowa wersja datasetu.

Każda transformacja danych powinna być możliwa do prześledzenia.

Niedopuszczalne jest ciche poprawianie danych historycznych bez śladu.

---

## 19. Przechowywanie danych

Fizyczny format zapisu danych jest szczegółem implementacyjnym Data Engine.

Pozostałe moduły TradingLab nie powinny bezpośrednio zależeć od tego, czy dane są przechowywane jako:

* CSV,
* Parquet,
* SQLite,
* PostgreSQL,
* inna baza danych,
* inny format plikowy.

W v0.2.0 dopuszcza się prosty format plikowy, jeśli pozwala on szybko i bezpiecznie zbudować pierwszy fundament Data Engine.

Architektura nie powinna jednak zamykać możliwości przejścia w przyszłości na bardziej profesjonalny format przechowywania danych.

---

## 20. Proponowana struktura katalogów danych

Przykładowa struktura katalogów:

```text
data/
  raw/
  processed/
  validated/
  metadata/
  validation_reports/
```

Bardziej szczegółowa struktura może w przyszłości uwzględniać źródło, symbol, interwał i wersję datasetu.

Przykład:

```text
data/
  raw/
    source_name/
      symbol/
        timeframe/
          dataset_version/
  metadata/
    source_name/
      symbol/
        timeframe/
          dataset_version/
  validation_reports/
    source_name/
      symbol/
        timeframe/
          dataset_version/
```

Struktura katalogów może zostać doprecyzowana na etapie implementacji, ale musi zachować możliwość identyfikacji i odtworzenia datasetu.

---

## 21. Wejścia Data Engine

Data Engine może przyjmować jako wejście między innymi:

* nazwę źródła danych,
* symbol instrumentu,
* rynek,
* typ danych,
* interwał,
* zakres dat,
* konfigurację pobierania,
* konfigurację walidacji,
* lokalizację zapisu danych,
* tryb pobierania danych.

W v0.2.0 minimalne wejście powinno pozwalać pobrać historyczne dane OHLCV dla wybranego symbolu, interwału i zakresu dat.

---

## 22. Wyjścia Data Engine

Data Engine powinien zwracać lub zapisywać:

* dataset,
* dane surowe,
* metadane datasetu,
* raport walidacji,
* status datasetu,
* informacje o błędach,
* informacje o źródle danych,
* informacje potrzebne do późniejszego odtworzenia danych.

Inne moduły TradingLab powinny korzystać z danych dopuszczonych do użycia, a nie bezpośrednio z nieopisanych plików surowych.

---

## 23. Odtwarzalność danych

Data Engine musi umożliwiać odtworzenie pochodzenia datasetu.

Dla każdego datasetu powinno być możliwe ustalenie:

* z jakiego źródła pochodzi,
* kiedy został pobrany,
* jaki zakres obejmuje,
* jakiego instrumentu dotyczy,
* jaki interwał zawiera,
* jaka była konfiguracja pobrania,
* gdzie zapisano dane surowe,
* czy dane były walidowane,
* jaki był wynik walidacji,
* jaka wersja danych została użyta.

Odtwarzalność danych jest warunkiem wiarygodnych badań.

---

## 24. Powiązanie z procesem badawczym

Każdy wynik badania, backtestu lub walidacji powinien być możliwy do powiązania z konkretnym datasetem i jego wersją.

Badanie bez informacji o danych wejściowych nie powinno być traktowane jako wiarygodne.

Data Engine powinien wspierać zasadę:

> Ten sam kod, ta sama konfiguracja i ta sama wersja danych powinny prowadzić do tego samego wyniku.

---

## 25. Przyszła współpraca z agentami AI

Agenci AI nie są częścią Data Engine w v0.2.0.

Data Engine powinien być jednak projektowany tak, aby w przyszłości jego metadane, raporty walidacji, statusy datasetów i logi mogły być analizowane przez kontrolowanych agentów AI.

Potencjalny przyszły agent w kontekście Data Engine może:

* analizować raporty walidacji,
* klasyfikować problemy z danymi,
* wskazywać ryzyka jakościowe,
* sugerować możliwe działania,
* przygotowywać opis problemów,
* pomagać w przygotowaniu raportów dla użytkownika.

Agent AI w kontekście Data Engine nie może:

* modyfikować danych surowych,
* usuwać danych,
* nadpisywać datasetów,
* ukrywać problemów jakościowych,
* zmieniać reguł walidacji bez jawnej decyzji projektowej,
* samodzielnie dopuszczać danych do badań poza określonym procesem,
* podejmować decyzji inwestycyjnych.

Agent AI może pomagać, ale nie może obchodzić architektury, walidacji ani procesu badawczego.

---

## 26. Zasady jakości Data Engine

Data Engine powinien być rozwijany zgodnie z następującymi zasadami:

* najpierw projekt, potem implementacja,
* dane mają pierwszeństwo przed opiniami,
* raw data są nietykalne,
* każda istotna decyzja powinna zostawiać ślad,
* dataset musi być identyfikowalny,
* dataset musi być możliwy do odtworzenia,
* walidacja powinna być jawna,
* błędy jakościowe nie mogą być ukrywane,
* metadane są częścią datasetu,
* raport walidacji jest częścią datasetu,
* format fizyczny danych nie powinien blokować architektury,
* minimalny zakres v0.2.0 nie może blokować przyszłego rozwoju.

---

## 27. Zasady dalszego rozwoju

Data Engine powinien być rozwijany etapami.

Każdy kolejny etap może rozszerzać:

* typy danych,
* źródła danych,
* konektory,
* metadane,
* reguły walidacji,
* statusy datasetów,
* formaty przechowywania,
* sposób aktualizacji danych,
* sposób udostępniania danych,
* integrację z innymi modułami,
* integrację z agentami AI.

Rozwój Data Engine powinien być prowadzony tak, aby nie unieważniać wcześniejszych wyników badań.

Jeżeli zmiana wpływa na sposób interpretacji danych, powinna być jawna i możliwa do prześledzenia.

---

## 28. Decyzje projektowe dla v0.2.0

Na potrzeby v0.2.0 przyjmuje się następujące decyzje:

1. Pierwszym obsługiwanym typem danych są historyczne dane świecowe OHLCV.
2. Data Engine korzysta z konektorów do źródeł danych.
3. W v0.2.0 może istnieć jeden pierwszy konektor referencyjny.
4. Dataset oznacza dane wraz z metadanymi, raportem walidacji, statusem i wersją.
5. Minimalne metadane są wymaganym fundamentem, a nie zamkniętą listą na przyszłość.
6. Minimalna walidacja jest pierwszym zestawem reguł, a nie pełnym docelowym systemem jakości danych.
7. Status datasetu nie zastępuje raportu walidacji.
8. Raw data są nietykalne.
9. Format fizycznego zapisu danych jest szczegółem implementacyjnym Data Engine.
10. Agenci AI nie są częścią v0.2.0, ale Data Engine powinien być przygotowany na przyszłą analizę agentową.

---

## 29. Otwarte decyzje na etap implementacji

Ten dokument nie rozstrzyga jeszcze wszystkich decyzji technicznych.

Do ustalenia na etapie projektowania implementacji pozostają między innymi:

* pierwsze źródło danych,
* pierwszy format zapisu danych,
* dokładna struktura katalogów,
* format pliku metadanych,
* format raportu walidacji,
* sposób generowania `dataset_id`,
* sposób oznaczania wersji datasetu,
* sposób uruchamiania pobierania danych,
* sposób uruchamiania walidacji,
* minimalny interfejs Data Engine dla innych modułów.

Te decyzje powinny wynikać z architektury opisanej w tym dokumencie i nie powinny naruszać zasad Data Engine.

---

## 30. Podsumowanie

Data Engine jest fundamentem danych w TradingLab.

Jego pierwsza wersja ma być prosta, ale nie może być prowizoryczna.

Celem v0.2.0 jest stworzenie pierwszego stabilnego fundamentu:

* pobrać dane,
* zapisać dane surowe,
* opisać je metadanymi,
* zwalidować,
* nadać status,
* zapisać raport,
* umożliwić późniejsze odtworzenie źródła danych.

Docelowo Data Engine powinien rozwijać się w kierunku profesjonalnego silnika danych, który będzie podstawą wiarygodnych badań, backtestów, walidacji, agentów AI i przyszłego automatycznego tradingu.
