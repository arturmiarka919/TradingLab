# Dev Agent — obserwacje proceduralne

Status: roboczy
Krok: 75A.1-DOC
Zakres: żywy dokument obserwacji proceduralnych dla przyszłego Dev Agenta

## 1. Cel dokumentu

Ten dokument zapisuje obserwacje proceduralne z pracy nad projektem TradingLab, które mają zostać wykorzystane przy projektowaniu i implementacji Dev Agenta.

Dokument nie dotyczy wyłącznie jednego kroku projektu.

Krok 75A-DOC jest pierwszym opisanym przypadkiem praktycznym, ponieważ podczas jego realizacji pojawiły się konkretne sytuacje, które Dev Agent musi obsługiwać proceduralnie.

Dokument ma być rozwijany przy kolejnych krokach projektu. Jeżeli podczas pracy pojawi się nowa sytuacja, dla której nie istnieje procedura, najpierw aktualizowana jest dokumentacja, potem kontrakt, potem test, a dopiero na końcu implementacja Dev Agenta.

## 2. Główna zasada Dev Agenta

Dev Agent nie jest projektowany jako swobodny agent decyzyjny.

Dev Agent jest projektowany jako proceduralny wykonawca opisanych workflow.

Podstawowa zasada:

**Dev Agent wykonuje tylko procedury, które są opisane.**

Jeżeli pojawia się sytuacja, dla której nie ma opisanej procedury, Dev Agent ma obowiązek zatrzymać pracę.

W takiej sytuacji obowiązuje kolejność:

1. STOP,
2. opisanie nowej sytuacji w dokumentacji,
3. aktualizacja kontraktu Dev Agenta,
4. dodanie lub zmiana testu,
5. zmiana implementacji Dev Agenta.

Dev Agent NIE MOŻE zgadywać brakującej procedury.

Dev Agent NIE MOŻE samodzielnie rozszerzać swoich kompetencji.

Dev Agent NIE MOŻE samodzielnie uznać, że nowa sytuacja jest „podobna” do istniejącej procedury, jeżeli procedura tego nie opisuje.

## 3. Słownik wymagań proceduralnych

W dokumentacji Dev Agenta obowiązują następujące znaczenia słów:

* **MUSI** — czynność obowiązkowa.
* **NIE MOŻE** — czynność zakazana.
* **MOŻE TYLKO** — czynność dozwolona wyłącznie po spełnieniu opisanych warunków.
* **STOP** — obowiązkowe zatrzymanie pracy i przekazanie decyzji człowiekowi.

W dokumentacji Dev Agenta nie należy używać miękkich sformułowań typu:

* powinien,
* nie powinien,
* dobrze byłoby,
* warto,
* można rozważyć.

Jeżeli coś jest regułą agenta, musi być zapisane jako obowiązek, zakaz, warunek albo STOP.

## 4. Pierwszy przypadek praktyczny: 75A-DOC

Pierwszym opisanym przypadkiem praktycznym jest krok 75A-DOC.

Zakres zmiany:

* dodanie nowego pliku `dokumentacja/architektura/TRADINGLAB_VISION.md`,
* zapisanie decyzji projektowej o wizji TradingLab jako Trading Intelligence System,
* commit,
* push,
* końcowa weryfikacja hashy.

Krok 75A-DOC był zmianą dokumentacyjną, ale pokazał pełny workflow, który Dev Agent musi umieć prowadzić proceduralnie.

## 5. Workflow wykonany ręcznie w 75A-DOC

W kroku 75A-DOC wykonano następujące działania:

1. sprawdzono `git status`,
2. sprawdzono lokalny `HEAD`,
3. sprawdzono `origin/main`,
4. potwierdzono zgodność lokalnego repo z GitHubem,
5. potwierdzono czysty working tree,
6. uruchomiono `ruff`,
7. uruchomiono `pytest`,
8. dodano nowy plik dokumentacji,
9. sprawdzono status Git,
10. zauważono, że nowy plik jest `untracked`,
11. sprawdzono `git diff`,
12. zauważono, że zwykły `git diff` nie pokazuje treści nowego pliku,
13. dodano plik do indeksu przez `git add`,
14. sprawdzono treść przez `git diff --cached`,
15. sprawdzono `git diff --check`,
16. wykonano commit,
17. wykonano push,
18. sprawdzono końcowy `git status`,
19. sprawdzono lokalny hash,
20. sprawdzono hash `origin/main`.

## 6. Ważna lekcja: plik untracked

Podczas kroku 75A-DOC pojawiła się ważna sytuacja proceduralna.

Nowy plik dokumentacji był widoczny w `git status` jako `untracked`.

W tej sytuacji zwykłe polecenie:

`git diff -- dokumentacja/architektura/TRADINGLAB_VISION.md`

nie pokazało treści pliku.

Dopiero po wykonaniu:

`git add dokumentacja/architektura/TRADINGLAB_VISION.md`

można było sprawdzić treść nowego pliku przez:

`git diff --cached -- dokumentacja/architektura/TRADINGLAB_VISION.md`

Ta sytuacja musi zostać obsłużona przez Dev Agenta jako osobna procedura.

Dev Agent MUSI rozróżniać:

* plik zmodyfikowany,
* plik nowy i jeszcze `untracked`,
* plik dodany do indeksu,
* plik gotowy do commita.

Dev Agent NIE MOŻE uznać pustego `git diff` za brak zmian, jeżeli `git status` pokazuje plik `untracked`.

## 7. Procedura dla nowego pliku dokumentacji

Dla nowego pliku dokumentacji obowiązuje minimalna procedura:

1. Dev Agent MUSI sprawdzić `git status`.
2. Dev Agent MUSI upewnić się, że working tree był czysty przed zmianą.
3. Dev Agent MOŻE TYLKO wskazać człowiekowi utworzenie polskiego pliku dokumentacji w VS Code.
4. Dev Agent NIE MOŻE zapisać polskiej dokumentacji przez PowerShell.
5. Po zapisaniu pliku Dev Agent MUSI sprawdzić `git status`.
6. Jeżeli plik jest `untracked`, Dev Agent NIE MOŻE traktować pustego `git diff` jako braku zmian.
7. Dev Agent MUSI wykonać lub wskazać `git add` dla tego pliku.
8. Dev Agent MUSI pokazać `git diff --cached`.
9. Dev Agent MUSI wykonać lub wskazać `git diff --check`.
10. Dev Agent MUSI uruchomić wymagane kontrole.
11. Dev Agent MOŻE TYLKO przygotować commit po poprawnym diffie i poprawnych kontrolach.
12. Dev Agent MOŻE TYLKO wykonać commit po jawnej akceptacji człowieka.
13. Dev Agent MOŻE TYLKO wykonać push po jawnej akceptacji człowieka.
14. Po pushu Dev Agent MUSI sprawdzić końcowy `git status`.
15. Po pushu Dev Agent MUSI sprawdzić zgodność lokalnego `HEAD` z `origin/main`.

## 8. Zasada STOP

Dev Agent MUSI zatrzymać pracę, jeżeli wystąpi jedna z poniższych sytuacji:

* working tree nie jest czysty przed rozpoczęciem zmiany,
* lokalny `HEAD` różni się od `origin/main` i nie wykonano świadomej synchronizacji,
* `git pull --ff-only` nie może zostać wykonany,
* `ruff` zwraca błąd,
* `pytest` zwraca błąd,
* `git diff --check` zwraca błąd,
* diff pokazuje zmianę poza zakresem aktualnego kroku,
* pojawia się sytuacja, dla której nie ma opisanej procedury,
* człowiek nie zaakceptował commita,
* człowiek nie zaakceptował pusha.

W przypadku STOP Dev Agent MUSI opisać problem i czekać na decyzję człowieka.

Dev Agent NIE MOŻE kontynuować pracy po STOP bez nowej decyzji człowieka.

## 9. Zakazy Dev Agenta

Dev Agent NIE MOŻE:

* rozszerzać zakresu kroku,
* modyfikować wielu plików, jeżeli krok dotyczy jednego pliku,
* podejmować decyzji architektonicznych,
* zmieniać dokumentacji poza ustalonym zakresem,
* ukrywać błędów testów,
* ignorować błędów ruff,
* ignorować błędów pytest,
* ignorować błędów `git diff --check`,
* zakładać, że brak diffu oznacza brak zmian przy pliku `untracked`,
* wykonywać commit bez jawnej akceptacji człowieka,
* wykonywać push bez jawnej akceptacji człowieka,
* traktować nieopisanego przypadku jako dozwolonego.

## 10. Polska dokumentacja i PowerShell

W projekcie obowiązuje osobna zasada dotycząca dokumentacji z polskimi znakami.

Dev Agent NIE MOŻE zapisywać polskiej dokumentacji przez PowerShell za pomocą:

* `Set-Content`,
* `Add-Content`,
* `Out-File`,
* here-stringów,
* innych komend mogących powodować problemy z kodowaniem.

Dla dokumentacji w języku polskim obowiązuje workflow:

1. otwarcie pliku w VS Code,
2. ręczne wklejenie pełnego bloku przez człowieka,
3. zapisanie pliku w VS Code,
4. kontrola przez Git.

Dev Agent MUSI znać ten wyjątek.

## 11. Minimalny kierunek implementacji

Pierwsza implementacja Dev Agenta NIE MOŻE edytować plików automatycznie.

Minimalna pierwsza wersja Dev Agenta ma obsługiwać wyłącznie rozpoznawanie stanu i wybór następnego kroku.

Minimalna pierwsza wersja Dev Agenta MUSI umieć:

* przyjąć wynik `git status`,
* rozpoznać stan repozytorium,
* rozpoznać przypadek `working tree clean`,
* rozpoznać przypadek `untracked file`,
* rozpoznać przypadek `changes to be committed`,
* wybrać opisaną procedurę,
* zwrócić następny bezpieczny krok,
* zatrzymać się, jeśli nie zna procedury.

Pierwsza implementacja Dev Agenta NIE MOŻE:

* edytować plików,
* wykonywać commitów,
* wykonywać pusha,
* samodzielnie naprawiać błędów,
* samodzielnie aktualizować dokumentacji,
* samodzielnie rozszerzać procedur.

## 12. Reguła rozwoju Dev Agenta

Dev Agent ma być rozwijany według tej samej zasady, według której rozwijany jest TradingLab:

1. dokumentacja,
2. kontrakt,
3. test,
4. implementacja,
5. kontrola `git diff`,
6. kontrola `ruff`,
7. kontrola `pytest`,
8. commit,
9. push.

Każda nowa sytuacja proceduralna MUSI najpierw trafić do dokumentacji.

Dopiero potem można zmieniać kontrakt, testy i kod Dev Agenta.

## 13. Następny krok

Po dodaniu tego dokumentu następnym logicznym krokiem jest przygotowanie minimalnego kontraktu Dev Agenta.

Proponowany krok:

**75A.2-CONTRACT — Minimal procedural contract for Dev Agent**

Zakres tego kroku obejmuje tylko kontrakt, bez implementacji pełnego agenta.

Minimalny kontrakt ma opisywać:

* wejście agenta,
* możliwe stany repozytorium,
* możliwe decyzje agenta,
* przypadki STOP,
* wybór procedury,
* format odpowiedzi z następnym krokiem.
