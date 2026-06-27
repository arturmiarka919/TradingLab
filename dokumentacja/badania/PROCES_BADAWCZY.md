# Proces badawczy

## 1. Cel procesu badawczego

Celem procesu badawczego w TradingLab jest przekształcanie pomysłów inwestycyjnych w zweryfikowane strategie, które mogą zostać obiektywnie ocenione na podstawie danych.

Proces badawczy ma chronić projekt przed podejmowaniem decyzji na podstawie intuicji, emocji lub pojedynczych przypadków. Każda strategia musi przejść uporządkowaną ścieżkę od hipotezy, przez test historyczny, aż do walidacji na rynku bieżącym.

TradingLab nie zakłada, że każda hipoteza musi zostać potwierdzona. Odrzucenie hipotezy jest pełnoprawnym wynikiem badania, jeżeli dane nie potwierdzają jej skuteczności.

Celem procesu badawczego nie jest dopasowywanie strategii do historii, lecz sprawdzenie, czy dana koncepcja posiada realną i powtarzalną przewagę.


## 2. Cykl życia hipotezy

Każda strategia w TradingLab zaczyna się jako hipoteza badawcza.

Hipoteza nie jest traktowana jako prawda, lecz jako założenie wymagające sprawdzenia na danych.

Podstawowy cykl życia hipotezy wygląda następująco:

1. Pomysł inwestycyjny.
2. Hipoteza badawcza.
3. Projekt eksperymentu.
4. Pobranie i przygotowanie danych.
5. Budowa strategii.
6. Backtest.
7. Analiza wyników.
8. Decyzja badawcza.
9. Walidacja na koncie demonstracyjnym.
10. Przejście do systemu automatycznego albo odrzucenie.
  

Hipoteza może zakończyć się jednym z kilku statusów:

* odrzucona,
* do poprawy,
* zaakceptowana do dalszych badań,
* zaakceptowana do walidacji,
* zaakceptowana do handlu rzeczywistego,
* wycofana z użycia.

Odrzucenie hipotezy nie jest porażką projektu. Jest wartościowym wynikiem badania, ponieważ pozwala ograniczyć ryzyko wdrożenia strategii, która nie posiada wystarczającej przewagi.


## 3. Formułowanie hipotez

Hipoteza badawcza powinna być sformułowana w sposób jasny, możliwy do sprawdzenia i możliwy do odrzucenia.

Hipoteza nie może być ogólnym stwierdzeniem typu:

- „ta strategia działa”,
- „RSI dobrze pokazuje wejścia”,
- „trend following zarabia”.

Poprawna hipoteza powinna określać:

- jaki rynek lub instrument badamy,
- jaki okres danych analizujemy,
- jakie warunki muszą wystąpić,
- jaka decyzja ma zostać podjęta,
- jaki wynik uznamy za potwierdzenie hipotezy,
- jakie warunki spowodują odrzucenie hipotezy.

Przykład hipotezy:

> Jeżeli na rynku EUR/USD występuje silny trend mierzony nachyleniem średniej kroczącej, to strategia podążania za trendem powinna osiągać lepszy wynik niż strategia losowego wejścia, po uwzględnieniu spreadu i kosztów transakcyjnych.

Każda hipoteza powinna mieć własny identyfikator, na przykład:

- H-0001,
- H-0002,
- H-0003.

Dzięki temu wyniki badań, backtesty, walidacje i decyzje będą mogły być jednoznacznie przypisane do konkretnej hipotezy.

## 4. Projekt eksperymentu

Każda hipoteza przed rozpoczęciem testów musi mieć określony plan eksperymentu.

Projekt eksperymentu powinien jasno opisywać:

* co dokładnie testujemy,
* na jakich danych testujemy,
* jakie są warunki wejścia w pozycję,
* jakie są warunki wyjścia z pozycji,
* jakie koszty transakcyjne uwzględniamy,
* jakie ryzyko przyjmujemy,
* jakie metryki będą oceniane,
* jakie kryteria oznaczają sukces,
* jakie kryteria oznaczają odrzucenie hipotezy.

Eksperyment musi być możliwy do powtórzenia.

Oznacza to, że uruchomienie tego samego eksperymentu na tych samych danych, z tą samą konfiguracją i tą samą wersją strategii powinno prowadzić do identycznych wyników.

Projekt eksperymentu powinien chronić przed dopasowywaniem strategii do historii.

Nie wolno zmieniać kryteriów sukcesu po zobaczeniu wyników tylko po to, aby hipoteza wyglądała lepiej.


## 5. Pozyskanie danych

Dane są fundamentem całego procesu badawczego.

Każda hipoteza musi być testowana na danych, których źródło, zakres i jakość są znane.

Dla każdego eksperymentu należy określić:

* źródło danych,
* instrument finansowy,
* interwał czasowy,
* zakres dat,
* strefę czasową,
* sposób uwzględniania spreadu,
* sposób uwzględniania prowizji,
* sposób obsługi brakujących danych,
* sposób obsługi nietypowych świec lub błędnych wartości.

Dane wykorzystywane w badaniach powinny być przechowywane w sposób umożliwiający powtórzenie eksperymentu w przyszłości.

Nie wolno opierać wniosków na danych, których pochodzenia nie można zweryfikować.

Jeżeli dane zostaną pobrane ponownie z innego źródła lub w innej wersji, należy traktować je jako osobny zestaw danych.

TradingLab powinien umożliwiać rozróżnienie danych:

* surowych,
* przetworzonych,
* testowych,
* walidacyjnych,
* bieżących.

Każdy wynik badania musi być możliwy do powiązania z konkretną wersją danych, na których został uzyskany.


## 6. Budowa strategii

Strategia jest techniczną realizacją hipotezy badawczej.

Nie należy budować strategii bez wcześniej opisanej hipotezy oraz projektu eksperymentu.

Każda strategia powinna mieć jasno określone:

* warunki wejścia w pozycję,
* warunki wyjścia z pozycji,
* sposób zarządzania pozycją,
* sposób obliczania wielkości pozycji,
* reguły zarządzania ryzykiem,
* instrumenty, na których może działać,
* interwały czasowe, dla których została zaprojektowana,
* parametry konfiguracyjne.

Strategia nie powinna zawierać logiki odpowiedzialnej za pobieranie danych, wykonywanie transakcji, raportowanie ani komunikację z brokerem.

Strategia powinna odpowiadać wyłącznie za generowanie decyzji inwestycyjnych na podstawie dostarczonych danych i konfiguracji.

Dzięki temu ta sama strategia może być użyta w:

* backteście,
* walidacji na koncie demonstracyjnym,
* systemie automatycznym działającym na rachunku rzeczywistym.

Strategia musi być możliwa do uruchomienia w sposób powtarzalny.

Zmiana parametrów strategii powinna być zapisana w konfiguracji, a nie ukryta bezpośrednio w kodzie.


## 7. Backtest

Backtest jest testem strategii na danych historycznych.

Celem backtestu nie jest udowodnienie, że strategia działa, lecz sprawdzenie, jak zachowywałaby się strategia, gdyby była stosowana w przeszłości zgodnie z określonymi zasadami.

Backtest powinien uwzględniać:

* dane historyczne,
* spread,
* prowizje,
* poślizg cenowy, jeżeli jest możliwy do oszacowania,
* zasady zarządzania pozycją,
* zasady zarządzania ryzykiem,
* ograniczenia kapitału,
* godziny handlu,
* typy zleceń,
* warunki zamknięcia pozycji.

Backtest musi być powtarzalny.

Ten sam backtest uruchomiony na tych samych danych, z tą samą konfiguracją i tą samą wersją strategii musi dawać identyczny wynik.

Wynik backtestu nie jest jeszcze dowodem, że strategia będzie działać na rynku rzeczywistym.

Pozytywny backtest oznacza jedynie, że strategia może przejść do dalszej analizy lub walidacji.

Negatywny backtest może oznaczać:

* odrzucenie hipotezy,
* konieczność poprawy założeń,
* konieczność zmiany parametrów,
* konieczność wykonania dodatkowych badań.

Nie wolno dopasowywać strategii do danych historycznych wyłącznie po to, aby poprawić wynik backtestu.


## 8. Analiza wyników

Analiza wyników ma na celu ocenę, czy strategia posiada realną, powtarzalną i możliwą do uzasadnienia przewagę.

Nie wystarczy, że strategia osiągnęła dodatni wynik finansowy w pojedynczym backteście.

Analiza powinna uwzględniać między innymi:

* wynik netto,
* maksymalne obsunięcie kapitału,
* stosunek zysku do ryzyka,
* liczbę transakcji,
* skuteczność transakcji,
* średni zysk na transakcję,
* średnią stratę na transakcję,
* stabilność wyników w czasie,
* zachowanie strategii w różnych warunkach rynkowych,
* wpływ spreadu, prowizji i poślizgu cenowego,
* okresy stratne,
* odporność strategii na zmianę parametrów.

Szczególną uwagę należy zwracać na strategie, które osiągają bardzo dobre wyniki tylko dla wąskiego zestawu parametrów.

Taki wynik może oznaczać przeoptymalizowanie strategii do danych historycznych.

Po analizie wyników hipoteza może otrzymać jedną z decyzji:

* odrzucona,
* wymaga poprawy,
* wymaga dodatkowych badań,
* zaakceptowana do walidacji na koncie demonstracyjnym.

Decyzja badawcza musi wynikać z danych, a nie z chęci utrzymania strategii przy życiu.


## 9. Walidacja na koncie demonstracyjnym

Walidacja na koncie demonstracyjnym jest etapem pośrednim pomiędzy backtestem a handlem na rachunku rzeczywistym.

Celem walidacji jest sprawdzenie, czy strategia zachowuje się poprawnie na bieżącym rynku, bez ryzykowania prawdziwych środków.

Walidacja powinna odbywać się z wykorzystaniem konta demonstracyjnego brokera lub innego środowiska paper trading, które umożliwia pracę na aktualnych danych rynkowych.

Na tym etapie oceniane są między innymi:

* zgodność działania strategii z wynikami backtestu,
* poprawność generowania sygnałów,
* poprawność otwierania i zamykania pozycji,
* wpływ spreadu i warunków rynkowych,
* stabilność działania systemu,
* obsługa błędów,
* czas reakcji systemu,
* jakość logów i możliwość odtworzenia decyzji.

Strategia nie może przejść do handlu rzeczywistego wyłącznie na podstawie dobrego backtestu.

Pozytywna walidacja na koncie demonstracyjnym jest obowiązkowym warunkiem dalszego rozwoju strategii w kierunku systemu automatycznego.

Jeżeli strategia w walidacji zachowuje się inaczej niż w backteście, należy zatrzymać proces i wyjaśnić przyczynę różnicy przed podjęciem kolejnych decyzji.


## 10. Przejście do systemu automatycznego

Przejście strategii do systemu automatycznego może nastąpić dopiero po pozytywnej walidacji na koncie demonstracyjnym.

Na tym etapie strategia może zostać przygotowana do działania na rachunku rzeczywistym, ale nie oznacza to automatycznego uruchomienia jej z pełnym kapitałem.

Przed dopuszczeniem strategii do handlu rzeczywistego należy określić:

* instrumenty, na których strategia może działać,
* maksymalne ryzyko na transakcję,
* maksymalną stratę dzienną,
* maksymalną stratę tygodniową lub miesięczną,
* maksymalną liczbę otwartych pozycji,
* maksymalną liczbę transakcji w danym okresie,
* zasady zatrzymania strategii,
* zasady awaryjnego wyłączenia systemu,
* sposób monitorowania działania strategii.

Pierwsze uruchomienie strategii na rachunku rzeczywistym powinno odbywać się z ograniczonym ryzykiem.

Celem pierwszego etapu handlu rzeczywistego nie jest maksymalizacja zysku, lecz potwierdzenie, że strategia działa poprawnie w środowisku realnym.

Każda decyzja strategii działającej automatycznie musi być rejestrowana w sposób umożliwiający późniejsze odtworzenie:

* jakie dane widziała strategia,
* jaki sygnał został wygenerowany,
* jaka decyzja została podjęta,
* jakie ryzyko zostało przyjęte,
* jakie zlecenie zostało wysłane do brokera,
* jaki był wynik realizacji zlecenia.

Jeżeli strategia w handlu rzeczywistym zachowuje się inaczej niż w walidacji, powinna zostać zatrzymana do czasu wyjaśnienia przyczyny.


## 11. Odrzucenie lub rozwój strategii

Każda strategia po zakończeniu badania, backtestu lub walidacji musi otrzymać decyzję dotyczącą dalszego postępowania.

Możliwe decyzje to:

* odrzucenie strategii,
* skierowanie strategii do poprawy,
* skierowanie strategii do dodatkowych badań,
* dopuszczenie strategii do walidacji,
* dopuszczenie strategii do ograniczonego handlu rzeczywistego,
* wycofanie strategii z użycia.

Odrzucenie strategii nie jest porażką projektu.

Strategia powinna zostać odrzucona, jeżeli:

* dane nie potwierdzają istnienia przewagi,
* wynik jest niestabilny,
* strategia działa tylko dla wąskiego zestawu parametrów,
* wynik zależy zbyt mocno od pojedynczego okresu rynkowego,
* strategia nie zachowuje się poprawnie podczas walidacji,
* ryzyko jest zbyt wysokie w stosunku do potencjalnego zysku,
* nie da się wyjaśnić decyzji podejmowanych przez strategię.

Strategia może zostać skierowana do dalszego rozwoju, jeżeli wyniki wskazują na możliwą przewagę, ale wymagają dodatkowego potwierdzenia.

Każda decyzja dotycząca strategii powinna być zapisana razem z uzasadnieniem.

TradingLab powinien przechowywać historię strategii, także tych odrzuconych, ponieważ wiedza o tym, co nie działa, jest tak samo ważna jak wiedza o tym, co działa.

Nie należy usuwać wyników nieudanych eksperymentów, jeżeli zostały przeprowadzone poprawnie. Powinny one pozostać częścią historii badawczej projektu.
