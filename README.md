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
* [Praca na wielu komputerach](dokumentacja/procesy/PRACA_NA_WIELU_KOMPUTERACH.md)
* [Mapa drogowa](dokumentacja/mapa_drogowa/ROADMAP.md)
* [ADR-0001 — Fundamenty projektu](dokumentacja/decyzje/ADR-0001-fundamenty-projektu.md)

## Standard projektu

* Kod projektu pisany jest po angielsku.
* Dokumentacja projektowa pisana jest po polsku.
* Każda istotna decyzja architektoniczna jest zapisywana w ADR.
* Projektowanie poprzedza implementację.
* Dokumentacja jest częścią repozytorium, a nie dodatkiem do projektu.

## Status

Aktualna wersja projektu: **v0.1.0 — Fundamenty projektu**

Status wersji: **zakończona**

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

Następny etap: **v0.2.0 — Data Engine**
