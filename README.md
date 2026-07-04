# TradingLab

TradingLab to platforma badawczo-inżynierska służąca do projektowania, testowania, walidacji i docelowo automatycznego wykonywania strategii inwestycyjnych na rynkach finansowych.

Projekt rozwijany jest etapowo:

1. **Laboratorium** — dane, hipotezy, strategie, backtesty i analiza wyników.
2. **Walidacja** — testowanie strategii na bieżącym rynku z wykorzystaniem kont demonstracyjnych.
3. **Trader** — automatyczny system transakcyjny działający na rachunku rzeczywistym.

## Cel projektu

Celem TradingLab jest stworzenie uporządkowanego środowiska, w którym strategie inwestycyjne są rozwijane na podstawie danych, powtarzalnych eksperymentów i jasno opisanych zasad, a nie intuicji lub emocji.

## Dokumentacja

Najważniejsze dokumenty projektu:

* [Konstytucja projektu](dokumentacja/architektura/KONSTYTUCJA.md)
* [Architektura systemu](dokumentacja/architektura/ARCHITEKTURA.md)
* [Proces badawczy](dokumentacja/badania/PROCES_BADAWCZY.md)
* [Data Engine](dokumentacja/architektura/DATA_ENGINE.md)
* [Implementacja Data Engine v0.2.0](dokumentacja/architektura/DATA_ENGINE_IMPLEMENTACJA_V0_2.md)
* [Praca z asystentem](dokumentacja/procesy/PRACA_Z_ASYSTENTEM.md)
* [Mapa drogowa](dokumentacja/mapa_drogowa/ROADMAP.md)

## Decyzje architektoniczne

* [ADR-0001 — Fundamenty projektu](dokumentacja/decyzje/ADR-0001-fundamenty-projektu.md)
* [ADR-0002 — Narzędzia testów i jakości kodu](dokumentacja/decyzje/ADR-0002-narzedzia-testow-i-jakosci-kodu.md)
* [ADR-0003 — Data Engine v0.2.0 — implementacja](dokumentacja/decyzje/ADR-0003-data-engine-v0-2-implementacja.md)

## Standard projektu

* Kod projektu pisany jest po angielsku.
* Dokumentacja projektowa pisana jest po polsku.
* Każda istotna decyzja architektoniczna jest zapisywana w ADR.
* Projektowanie poprzedza implementację.
* Dokumentacja jest częścią repozytorium, a nie dodatkiem do projektu.

## Status

Aktualny etap projektu: **v0.2.0 — Data Engine**

Status etapu: **w trakcie implementacji**

Poprzedni etap: **v0.1.0 — Fundamenty projektu — zakończony**

W ramach wersji v0.1.0 przygotowano:

* repozytorium Git i GitHub,
* środowisko Python,
* konfigurację `uv`,
* podstawową strukturę projektu,
* dokumentację projektową,
* ADR-0001 i ADR-0002,
* mapę drogową projektu,
* narzędzia testów i jakości kodu,
* pierwszy test techniczny.

W ramach wersji v0.2.0 rozwijany jest moduł Data Engine, odpowiedzialny za tworzenie, zapisywanie, walidację i odczyt datasetów używanych w dalszych etapach projektu.
