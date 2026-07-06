# TradingLab Vision

Status: roboczy  
Krok: 75A-DOC  
Zakres: decyzja projektowa o kierunku rozwoju TradingLab

## 1. Cel dokumentu

Ten dokument opisuje aktualną wizję projektu TradingLab po zmianie priorytetu rozwoju.

TradingLab nie jest projektowany wyłącznie jako klasyczny bot tradingowy ani wyłącznie jako platforma quantowa. Docelowo ma być systemem wspierającym podejmowanie decyzji inwestycyjnych przez łączenie danych historycznych, badań ilościowych, analizy rynku, researchu narracyjnego oraz zapisywania historii hipotez.

Nowa wizja projektu:

**TradingLab = Trading Intelligence System**

Oznacza to system, który nie tylko testuje strategie na danych historycznych, ale również pomaga wykrywać, opisywać, porównywać i później rozliczać okazje inwestycyjne.

## 2. Dwa filary projektu

TradingLab rozwija się docelowo w dwóch równoległych filarach:

1. Quant Research Lab
2. Opportunity Intelligence

Oba filary mają inne zadania, ale powinny docelowo współpracować.

Quant Research Lab odpowiada na pytanie:

> Co pokazują dane historyczne?

Opportunity Intelligence odpowiada na pytanie:

> Czy gdzieś na rynku dzieje się coś, czemu warto poświęcić uwagę?

## 3. Quant Research Lab

Quant Research Lab to dotychczasowy kierunek projektu.

Obejmuje między innymi:

- Data Engine,
- Feature Engine,
- Label / Target Engine,
- Backtest Engine,
- Strategy Discovery,
- automatyczne generowanie hipotez,
- testowanie strategii,
- walidację historyczną.

Ten filar pozostaje częścią TradingLab.

Obecny Data Engine nie jest porzucany. Zostaje jako stabilny fundament techniczny do dalszych prac nad danymi, datasetami, walidacją, backtestami i badaniami ilościowymi.

Pauza w pracach nad Data Engine jest świadomą decyzją projektową, a nie wycofaniem się z tego kierunku.

## 4. Opportunity Intelligence

Opportunity Intelligence staje się pierwszym priorytetem dalszego rozwoju projektu.

Celem tego filaru nie jest stworzenie strategii, która generuje codziennie mechaniczne sygnały kupna lub sprzedaży.

Celem jest stworzenie systemu, który pomaga wykrywać wyjątkowe okazje inwestycyjne, opisywać je w ustrukturyzowany sposób, śledzić ich rozwój i później oceniać jakość pierwotnej hipotezy.

Filozofia tego filaru nie brzmi:

> Jaki sygnał dzisiaj kupić?

Tylko:

> Czy gdzieś na rynku dzieje się coś, czemu warto poświęcić uwagę?

## 5. Opportunity jako główny obiekt

Głównym obiektem Opportunity Intelligence będzie:

**Opportunity**

Opportunity oznacza zapisaną okazję inwestycyjną lub hipotezę rynkową.

Przykładowe informacje zapisywane w Opportunity:

- instrument,
- typ okazji,
- teza,
- argumenty za,
- argumenty przeciw,
- źródła,
- oczekiwany scenariusz,
- warunki potrzebne do potwierdzenia hipotezy,
- warunki unieważnienia hipotezy,
- horyzont czasowy,
- status,
- wynik po czasie,
- wnioski po zakończeniu obserwacji.

Celem jest budowanie pamięci decyzji i hipotez, a nie tylko chwilowe generowanie sygnałów.

## 6. Wstępne tryby Opportunity Huntera

Pierwszym modułem w filarze Opportunity Intelligence będzie:

**Opportunity Hunter Agent**

Jego zadaniem będzie wyszukiwanie i porządkowanie potencjalnych okazji inwestycyjnych.

Wstępnie ustalone tryby pracy Opportunity Huntera:

### 6.1. Ride the Wave

Szukanie dużych fal, silnych trendów lub ruchów, do których potencjalnie można się podłączyć po odpowiednim potwierdzeniu.

### 6.2. Smart Money Tracker

Śledzenie działań dużego kapitału, istotnych uczestników rynku, funduszy, insiderów, instytucji lub innych źródeł mogących wskazywać na nietypową aktywność.

### 6.3. Catalyst Hunter

Szukanie sytuacji przed ważnym katalizatorem, takim jak decyzje regulacyjne, wyniki finansowe, publikacje danych, premiery produktów, zmiany technologiczne lub inne wydarzenia mogące istotnie wpłynąć na instrument.

### 6.4. Event Volatility Hunter

Analiza wydarzeń typu stopy procentowe, dane makroekonomiczne, wyniki spółek lub inne zdarzenia powodujące wysoką zmienność.

Celem nie jest granie każdego wydarzenia.

Celem jest znalezienie nietypowego układu oczekiwań, pozycjonowania, narracji i potencjalnej reakcji rynku.

### 6.5. Panic Hunter

Szukanie przesadnych reakcji, paniki, gwałtownej wyprzedaży lub silnego strachu, które mogą tworzyć potencjalną okazję po odpowiedniej weryfikacji.

### 6.6. Crowd Exhaustion

Szukanie sytuacji, w których istniejący ruch może dochodzić do ekstremum.

Nie chodzi o prostą zasadę:

> Większość się myli.

Chodzi raczej o pytanie:

> Czy fala jest już tak jednostronna, że rynek może być podatny na odwrócenie, korektę lub rozczarowanie?

### 6.7. Structural Change Hunter

Szukanie dużych zmian strukturalnych, takich jak nowe technologie, regulacje, zmiany gospodarcze, zmiany sektorowe lub trwałe przesunięcia w zachowaniu rynku.

### 6.8. Disagreement Hunter

Szukanie sytuacji, w których dobrzy uczestnicy rynku są mocno podzieleni, a różnica opinii może wskazywać na ważny punkt decyzyjny lub niedoszacowane ryzyko.

## 7. Rola AI Research Agenta

AI w TradingLab nie ma samodzielnie przewidywać rynku ani podejmować decyzji inwestycyjnych.

AI ma pełnić rolę:

- analityka,
- researchera,
- drugiego mózgu,
- narzędzia do porządkowania informacji,
- narzędzia do wykrywania sprzeczności,
- narzędzia do generowania hipotez.

Przykładowe zadania AI Research Agenta:

- czytanie źródeł internetowych,
- analiza narracji rynkowych,
- śledzenie opinii,
- wyszukiwanie sprzeczności,
- grupowanie argumentów,
- porównywanie scenariuszy,
- tłumaczenie sytuacji człowiekowi,
- przygotowywanie ustrukturyzowanych opisów Opportunity.

Decyzje inwestycyjne, kontrola ryzyka i ostateczna ocena pozostają po stronie człowieka oraz procesu walidacji.

## 8. Guru Tracker

Dodatkową koncepcją w ramach Opportunity Intelligence jest:

**Guru Tracker**

Guru Tracker ma śledzić osoby publikujące hipotezy inwestycyjne, takie jak traderzy, analitycy, inwestorzy, twórcy internetowi lub komentatorzy rynku.

System nie zakłada, że te osoby mają rację.

System ma budować historię:

- kto opublikował hipotezę,
- kiedy ją opublikował,
- jakiego instrumentu dotyczyła,
- czy hipoteza była mierzalna,
- jaki był zakładany scenariusz,
- co miało potwierdzić hipotezę,
- co miało ją unieważnić,
- jaki był późniejszy wynik.

Celem Guru Trackera jest rozliczalność opinii i budowanie własnej bazy obserwacji, a nie ślepe podążanie za autorytetami.

## 9. Dev Agent

Równolegle do Opportunity Intelligence projektowana będzie koncepcja Dev Agenta.

Powodem jest obecny sposób pracy, który wymaga wielu ręcznych operacji między ChatGPT, VS Code, PowerShellem i Gitem.

Docelowy Dev Agent ma pomagać w pracy developerskiej poprzez:

- czytanie repozytorium,
- analizę aktualnego stanu projektu,
- proponowanie małych zmian,
- edycję plików,
- uruchamianie ruff,
- uruchamianie pytest,
- pokazywanie git diff,
- pokazywanie wyników kontroli,
- czekanie na akceptację człowieka.

Dev Agent nie powinien samodzielnie podejmować decyzji architektonicznych ani automatycznie pushować zmian bez zatwierdzenia.

## 10. Relacja między filarami

Quant Research Lab i Opportunity Intelligence nie są konkurencyjnymi kierunkami.

Docelowo mają się uzupełniać.

Przykładowa współpraca:

- Opportunity Hunter wykrywa potencjalną okazję,
- Data Engine dostarcza dane,
- Feature Engine buduje cechy,
- Backtest Engine sprawdza historyczne analogie,
- Validation Engine ocenia jakość hipotezy,
- Opportunity zapisuje decyzję, argumenty i późniejszy wynik.

W ten sposób TradingLab może łączyć research jakościowy, dane ilościowe i historię decyzji.

## 11. Aktualny priorytet

Od kroku 75A priorytetem projektowym jest rozpoczęcie prac nad Opportunity Intelligence.

Nie oznacza to usunięcia ani porzucenia Data Engine.

Oznacza to, że dalszy rozwój zostaje czasowo skierowany na zaprojektowanie pierwszej wersji Opportunity Huntera i modelu Opportunity.

## 12. Zasady dalszej pracy

Dalsze prace powinny zachować dotychczasowe zasady projektu:

- małe, bezpieczne kroki,
- najpierw dokumentacja,
- potem kontrakt,
- potem test,
- potem implementacja,
- bez dublowania istniejącej logiki,
- jeden plik lub jeden mały zakres na raz,
- każda zmiana weryfikowana przez git diff,
- testy i ruff uruchamiane wtedy, gdy zmiana tego wymaga,
- commit po zakończeniu stabilnego kroku,
- push po zatwierdzeniu zmiany.

## 13. Najbliższe następne kroki

Po dodaniu tego dokumentu kolejne kroki powinny dotyczyć już projektowania Opportunity Intelligence.

Proponowana kolejność:

1. 75B-DOC — dopisać nową wizję do głównej dokumentacji architektury lub mapy drogowej.
2. 75C-DOC — opisać model Opportunity w dokumentacji.
3. 75D-CONTRACT — zaprojektować minimalny kontrakt danych dla Opportunity.
4. 75E-TEST — dodać pierwszy test modelu Opportunity.
5. 75F-CODE — dodać minimalną implementację modelu Opportunity.

Na tym etapie nie zaczynamy jeszcze implementacji.
