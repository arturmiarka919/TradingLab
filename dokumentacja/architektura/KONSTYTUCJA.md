# Konstytucja projektu TradingLab

## 1. Misja projektu

Misją projektu TradingLab jest stworzenie platformy badawczej umożliwiającej systematyczne odkrywanie, weryfikowanie i rozwijanie strategii inwestycyjnych, aby w długim terminie osiągać stabilne zyski na rynkach finansowych.

TradingLab nie służy do poszukiwania "magicznych" strategii. Jego celem jest budowanie wiedzy opartej na danych, eksperymentach i powtarzalnych badaniach.

---

## 2. Wizja projektu

TradingLab będzie rozwijany etapowo.

### Etap I – Laboratorium

Celem pierwszego etapu jest stworzenie środowiska badawczego umożliwiającego:

* pobieranie i zarządzanie danymi rynkowymi,
* budowę strategii,
* przeprowadzanie backtestów,
* analizę wyników,
* rozwijanie strategii posiadających przewagę statystyczną.

### Etap II – Walidacja

Celem drugiego etapu jest weryfikacja strategii na bieżących danych rynkowych z wykorzystaniem kont demonstracyjnych (paper trading).

Strategie są oceniane pod kątem stabilności, poprawności działania oraz zgodności wyników z rezultatami backtestów.

### Etap III – Trader

Ostatnim etapem rozwoju projektu jest stworzenie w pełni automatycznego systemu transakcyjnego.

System będzie odpowiedzialny za:

* komunikację z brokerem,
* automatyczne składanie zleceń,
* zarządzanie pozycjami,
* kontrolę ryzyka,
* pracę w trybie 24/7.

---

## 3. Podstawowe zasady

### Projekt poprzedza implementację.

### Dane mają pierwszeństwo przed opiniami i intuicją.

### Każda strategia przechodzi pełny proces: Laboratorium → Walidacja → Trader.

### Żadna strategia nie trafia na rachunek rzeczywisty bez pozytywnej walidacji.

### Każda decyzja systemu musi być możliwa do wyjaśnienia.

### Każdy eksperyment musi być powtarzalny.

### Dokumentacja jest integralną częścią projektu.

### Architektura ma być modułowa i umożliwiać rozwój przez wiele lat.

### Każda istotna decyzja architektoniczna jest zapisywana w ADR.

### TradingLab jest platformą, a nie pojedynczym algorytmem.

---

## 4. Zasady projektowania oprogramowania

* Każdy moduł posiada jedną odpowiedzialność.
* Moduły są możliwie luźno powiązane.
* Każda większa funkcjonalność jest projektowana przed implementacją.
* Czytelność kodu ma pierwszeństwo przed sprytnymi rozwiązaniami.
* Konfiguracja ma pierwszeństwo przed wartościami wpisanymi na stałe.
* Każdy moduł powinien być możliwy do przetestowania niezależnie.
* Projekt ma być rozwijalny bez przebudowy fundamentów.
* Każda istotna decyzja systemu musi być możliwa do prześledzenia.
* Te same dane i ta sama konfiguracja muszą zawsze prowadzić do identycznych wyników.

---

## 5. Standard testowania i jakości

Testy są bramką jakości projektu.

Żadna istotna funkcjonalność nie jest uznawana za domkniętą wyłącznie dlatego, że działa dla poprawnego przykładu.

Każdy moduł, walidator, parser, konektor, silnik obliczeniowy i element raportowania powinien posiadać restrykcyjne testy adekwatne do swojego etapu rozwoju.

Testy powinny obejmować wszystkie znane, uzasadnione i przewidywalne scenariusze na danym etapie, w szczególności:

* scenariusz poprawny,
* scenariusze błędne,
* przypadki graniczne,
* dane puste lub niekompletne,
* dane niespójne logicznie,
* zachowanie statusów, liczników i raportów,
* przypadki mieszane, w których część danych jest poprawna, a część błędna,
* przypadki regresji wykryte podczas rozwoju projektu.

Ręczne sprawdzenie działania nie zastępuje testu automatycznego, jeśli dany przypadek można sensownie przetestować automatycznie.

Brak testu dla oczywistego scenariusza błędu jest traktowany jako dług techniczny.
