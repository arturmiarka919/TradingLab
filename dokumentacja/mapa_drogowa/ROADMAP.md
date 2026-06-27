# Mapa drogowa projektu TradingLab

## Cel dokumentu

Celem niniejszego dokumentu jest opisanie planu rozwoju projektu TradingLab od pierwszych fundamentów do w pełni automatycznego systemu transakcyjnego.

Mapa drogowa nie jest sztywnym harmonogramem czasowym. Określa kolejność rozwoju systemu oraz główne cele kolejnych wersji.

---

## Zasada rozwoju

TradingLab rozwijany jest etapowo.

Każda wersja powinna dostarczać konkretną wartość i pozostawiać projekt w stabilnym stanie.

Nie przechodzimy do kolejnego etapu, jeżeli fundament poprzedniego etapu nie jest wystarczająco stabilny.

---

# Etap I — Laboratorium

## 0.1.0 — Fundamenty projektu

Cel wersji:

* utworzenie repozytorium Git,
* przygotowanie środowiska Python,
* konfiguracja `uv`,
* utworzenie podstawowej struktury projektu,
* utworzenie podstawowej dokumentacji,
* zapisanie pierwszych decyzji architektonicznych.

Status:

- zakończone.

Zakres zakończony:

- repozytorium Git i GitHub,
- środowisko Python,
- konfiguracja uv,
- dokumentacja projektowa,
- ADR-0001 i ADR-0002,
- README projektu,
- pytest,
- ruff,
- pierwszy test techniczny.

---

## 0.2.0 — Data Engine

Cel wersji:

* zaprojektowanie modułu Data Engine,
* pobieranie danych rynkowych,
* zapis danych surowych,
* podstawowa walidacja danych,
* możliwość odtworzenia źródła danych.

Efekt:

TradingLab potrafi pobrać i przechować pierwsze dane rynkowe w uporządkowany sposób.

---

## 0.3.0 — Strategy Engine

Cel wersji:

* zaprojektowanie sposobu definiowania strategii,
* stworzenie pierwszej prostej strategii testowej,
* oddzielenie logiki strategii od danych, backtestu i brokera.

Efekt:

TradingLab potrafi uruchomić strategię na dostarczonych danych.

---

## 0.4.0 — Backtesting Engine

Cel wersji:

* uruchamianie strategii na danych historycznych,
* podstawowe zarządzanie pozycją,
* uwzględnienie kosztów transakcyjnych,
* generowanie wyniku backtestu.

Efekt:

TradingLab potrafi wykonać pierwszy powtarzalny backtest.

---

## 0.5.0 — Analytics Engine

Cel wersji:

* analiza wyników backtestu,
* equity curve,
* drawdown,
* liczba transakcji,
* skuteczność,
* średni zysk i strata,
* podstawowe raportowanie.

Efekt:

TradingLab potrafi ocenić wynik strategii w sposób bardziej szczegółowy niż sam zysk netto.

---

## 0.6.0 — Research Workflow

Cel wersji:

* rejestrowanie hipotez badawczych,
* przypisywanie wyników do hipotez,
* zapisywanie decyzji badawczych,
* rozróżnienie strategii od hipotezy.

Efekt:

TradingLab zaczyna działać jako laboratorium badawcze, a nie tylko jako backtester.

---

# Etap II — Walidacja

## 0.7.0 — Validation Engine

Cel wersji:

* testowanie strategii na bieżących danych,
* przygotowanie trybu paper trading,
* monitorowanie decyzji strategii bez użycia realnych środków.

Efekt:

Strategia może być sprawdzana na rynku bieżącym bez ryzyka finansowego.

---

## 0.8.0 — Broker Connector Demo

Cel wersji:

* połączenie z kontem demonstracyjnym brokera,
* pobieranie danych z brokera,
* składanie zleceń demo,
* odbiór informacji o wykonaniu zleceń.

Efekt:

TradingLab potrafi działać na rachunku demonstracyjnym.

---

# Etap III — Trader

## 0.9.0 — Trading Engine

Cel wersji:

* przygotowanie silnika realnego handlu,
* kontrola ryzyka przed wysłaniem zlecenia,
* rejestrowanie decyzji systemu,
* mechanizmy awaryjnego zatrzymania.

Efekt:

TradingLab jest przygotowany do ograniczonych testów na rachunku rzeczywistym.

---

## 1.0.0 — Pierwsza wersja produkcyjna

Cel wersji:

* stabilne działanie systemu,
* pełny przepływ: dane → strategia → backtest → walidacja → trading,
* kontrola ryzyka,
* logowanie decyzji,
* możliwość odtworzenia działania systemu.

Efekt:

TradingLab osiąga pierwszą wersję zdolną do kontrolowanego działania na realnym rachunku.