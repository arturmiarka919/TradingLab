# ADR-0001 — Fundamenty projektu TradingLab

## Status

Zaakceptowana

## Data

2026-06-27

## Kontekst

TradingLab jest projektem długoterminowym, którego celem jest stworzenie platformy badawczej prowadzącej docelowo do automatycznego systemu transakcyjnego.

Projekt ma być rozwijany w sposób uporządkowany, modułowy i możliwy do utrzymania przez wiele lat.

Na początku projektu podjęto zestaw decyzji dotyczących fundamentów technicznych, organizacyjnych i dokumentacyjnych.

## Decyzje

### Język programowania

TradingLab będzie tworzony w języku Python.

Uzasadnienie:

* Python posiada bardzo rozwinięty ekosystem do analizy danych.
* Python dobrze nadaje się do pracy z danymi finansowymi, backtestami i automatyzacją.
* Python umożliwia szybkie prototypowanie oraz późniejszy rozwój systemu.

### Zarządzanie środowiskiem i zależnościami

Projekt będzie używał narzędzia `uv`.

Uzasadnienie:

* szybkie tworzenie środowiska,
* szybka instalacja zależności,
* prostsze odtwarzanie projektu na innym komputerze,
* możliwość późniejszego uruchomienia projektu na serwerze.

### Kontrola wersji

Projekt będzie używał Git.

Repozytorium centralne znajduje się na GitHubie.

Uzasadnienie:

* pełna historia zmian,
* możliwość cofania zmian,
* kopia projektu poza komputerem lokalnym,
* przygotowanie pod przyszłą pracę na serwerze lub z innymi osobami.

### Edytor

Podstawowym edytorem projektu będzie Visual Studio Code.

Uzasadnienie:

* dobra obsługa Pythona,
* dobra integracja z Git,
* wygodna praca z dokumentacją Markdown,
* możliwość rozwoju projektu w jednym środowisku.

### Struktura kodu

Projekt używa układu `src layout`.

Kod aplikacji znajduje się w katalogu:

```text
src/tradinglab
```

Uzasadnienie:

* lepszy porządek w projekcie,
* rozdzielenie kodu aplikacji od dokumentacji, testów i danych,
* zgodność z dobrymi praktykami projektów Python.

### Język kodu i dokumentacji

Kod projektu będzie pisany po angielsku.

Dokumentacja projektowa będzie pisana po polsku.

Komentarze mogą być pisane po polsku, jeżeli wyjaśniają złożoną logikę.

Uzasadnienie:

* kod po angielsku lepiej współgra z bibliotekami, dokumentacją techniczną i narzędziami AI,
* dokumentacja po polsku jest bardziej czytelna dla właściciela projektu,
* taki podział łączy dobre praktyki techniczne z wygodą pracy.

### Zasada projekt przed implementacją

Każda istotna funkcjonalność musi zostać najpierw zaprojektowana, a dopiero później zaimplementowana.

Uzasadnienie:

* ograniczenie chaotycznych zmian,
* mniejsze ryzyko przebudowy fundamentów,
* większa kontrola nad rozwojem projektu,
* zgodność z długoterminową wizją TradingLab.

### Dokumentacja jako część projektu

Dokumentacja jest integralną częścią repozytorium.

Każda istotna decyzja, proces lub element architektury powinien być zapisany w dokumentacji.

Uzasadnienie:

* ważne ustalenia nie mogą istnieć wyłącznie w historii rozmów,
* dokumentacja ma odzwierciedlać aktualny stan projektu,
* repozytorium ma być źródłem prawdy o TradingLab.

## Konsekwencje

TradingLab będzie rozwijany wolniej na początku, ale w bardziej uporządkowany sposób.

Każda większa decyzja techniczna powinna zostać zapisana w kolejnych dokumentach ADR.

Projekt od początku posiada jasne fundamenty techniczne, językowe i organizacyjne.
