# Dev Agent — minimalny kontrakt proceduralny

Status: roboczy
Krok: 75A.8A-DOC
Zakres: minimalny kontrakt proceduralny Dev Agenta, przenośność i autonomia pakietowa

## 1. Cel dokumentu

Ten dokument opisuje minimalny kontrakt proceduralny Dev Agenta.

Kontrakt określa:

* jakie dane wejściowe Dev Agent przyjmuje,
* jakie stany repozytorium rozpoznaje,
* jakie decyzje zwraca,
* kiedy wykonuje STOP,
* jaki format ma odpowiedź agenta,
* jakich działań pierwsza wersja Dev Agenta NIE MOŻE wykonywać,
* dlaczego Dev Agent ma być docelowo przenośny między projektami,
* jak Dev Agent ma docelowo wykonywać zatwierdzone pakiety małych kroków,
* jak Dev Agent ma pracować na pełnej treści pliku dostarczonej przez człowieka.

Ten dokument nie opisuje jeszcze pełnej implementacji Dev Agenta.

## 2. Relacja do obserwacji proceduralnych

Ten kontrakt wynika z dokumentu:

`dokumentacja/procesy/DEV_AGENT_OBSERWACJE.md`

Jeżeli podczas pracy nad projektem pojawi się sytuacja nieopisana w tym kontrakcie, obowiązuje kolejność:

1. STOP,
2. aktualizacja obserwacji proceduralnych,
3. aktualizacja kontraktu,
4. test,
5. implementacja.

Dev Agent NIE MOŻE obsługiwać sytuacji, która nie ma opisu w dokumentacji i kontrakcie.

## 3. Główna zasada kontraktu

Dev Agent jest proceduralnym wykonawcą opisanych workflow.

Dev Agent NIE JEST autonomicznym decydentem architektonicznym.

Dev Agent NIE MOŻE zgadywać procedury.

Dev Agent NIE MOŻE samodzielnie rozszerzać zakresu kroku.

Dev Agent NIE MOŻE samodzielnie uznać nieopisanego przypadku za dozwolony.

### 3.1. Zasada przenośności Dev Agenta

Dev Agent NIE MOŻE być projektowany jako narzędzie trwale przywiązane wyłącznie do TradingLab.

TradingLab jest pierwszym projektem referencyjnym i poligonem testowym Dev Agenta.

Docelowo Dev Agent ma być możliwy do użycia także w innych projektach programistycznych.

Dlatego architektura Dev Agenta MUSI rozdzielać:

* uniwersalny rdzeń proceduralny,
* konfigurację konkretnego projektu,
* adapter konkretnego projektu,
* lokalnego runnera wykonującego dozwolone komendy,
* opcjonalną warstwę AI odpowiedzialną za język, planowanie i generowanie propozycji.

Uniwersalny rdzeń Dev Agenta MUSI zawierać logikę niezależną od konkretnego projektu.

Do uniwersalnego rdzenia należą między innymi:

* rozpoznawanie stanu repozytorium,
* rozpoznawanie `clean`, `untracked`, `unstaged`, `staged` i `unknown`,
* kontrola zgodności `HEAD` z `origin/main`,
* kontrola zakresu zmian względem `allowed_paths`,
* obsługa decyzji `NEXT_STEP`,
* obsługa decyzji `STOP`,
* obsługa decyzji `READY_FOR_HUMAN_APPROVAL`,
* obsługa decyzji `DONE`,
* wymuszanie jawnej akceptacji człowieka przy działaniach wymagających zgody,
* wymuszanie STOP przy braku danych, nieznanym stanie albo przekroczeniu zakresu.

Konfiguracja projektu MUSI zawierać informacje zależne od konkretnego repozytorium.

Do konfiguracji projektu należą między innymi:

* nazwa projektu,
* ścieżka repozytorium,
* domyślna gałąź,
* komenda testów,
* komenda lintowania,
* komenda formatowania, jeżeli istnieje,
* lista wymaganych kontroli jakości,
* lista chronionych ścieżek,
* reguły językowe dokumentacji,
* reguły językowe kodu,
* reguły commitów,
* profile uprawnień agenta.

Komendy specyficzne dla TradingLab, takie jak `uv run pytest` albo `uv run ruff check .`, NIE MOGĄ być na stałe zaszyte w uniwersalnym rdzeniu Dev Agenta.

Dev Agent Core MUSI oczekiwać logicznych wyników kontroli.

Project Adapter albo Project Config MUSI określać, jak te wyniki mają zostać uzyskane w konkretnym projekcie.

### 3.2. Zasada autonomii pakietowej bez utraty kontroli

Docelowo Dev Agent ma przyspieszać pracę przez wykonywanie zatwierdzonych pakietów małych kroków.

Dev Agent NIE MA zastępować człowieka jako właściciela kierunku projektu.

Człowiek nadal decyduje:

* co ma zostać zbudowane,
* jaki pakiet kroków wolno wykonać,
* jakie pliki wolno zmieniać,
* jakie komendy wolno uruchamiać,
* jakie są warunki STOP,
* jaki poziom autonomii agent otrzymuje.

Dev Agent może docelowo samodzielnie wykonywać serię małych kroków tylko w granicach zatwierdzonego planu wykonania.

Plan wykonania MUSI określać co najmniej:

* identyfikator pakietu pracy,
* listę kroków do wykonania,
* dozwolone pliki albo katalogi,
* wymagane kontrole jakości,
* dozwolone akcje Git,
* warunki STOP,
* oczekiwany raport końcowy.

Dev Agent NIE MOŻE samodzielnie rozszerzyć pakietu pracy.

Dev Agent NIE MOŻE samodzielnie zmienić decyzji architektonicznej.

Dev Agent NIE MOŻE kontynuować pracy, jeżeli wykonanie kroku wymaga decyzji człowieka.

Docelowy model pracy pakietowej:

```text
Człowiek zatwierdza kierunek i granice pakietu.
Dev Agent wykonuje powtarzalną procedurę małych kroków.
Dev Agent wykonuje kontrole jakości.
Dev Agent tworzy commity zgodne z pakietem.
Dev Agent pushuje zmiany tylko wtedy, gdy profil i procedura na to pozwalają.
Dev Agent generuje raport audytowy.
Człowiek audytuje raport i podejmuje decyzje wyższego poziomu.
```

Raport audytowy pakietu MUSI zawierać co najmniej:

* identyfikator pakietu,
* listę wykonanych kroków,
* listę commitów,
* skróty commitów,
* listę zmienionych plików,
* wyniki kontroli jakości,
* końcowy stan repozytorium,
* informację, czy `HEAD` jest równy `origin/main`,
* listę sytuacji STOP, jeżeli wystąpiły,
* listę ryzyk albo decyzji wymagających człowieka.

Dev Agent ma mieć autonomię operacyjną w granicach zatwierdzonego pakietu.

Dev Agent NIE MA mieć autonomii decyzyjnej nad kierunkiem projektu.

### 3.3. Procedura pracy na pełnej treści pliku

Dev Agent MUSI obsługiwać tryb pracy, w którym człowiek wkleja pełną aktualną treść pliku.

Ten tryb jest szczególnie ważny przy pracy nad dokumentacją i pojedynczymi plikami kodu.

Jeżeli człowiek dostarcza pełną aktualną treść pliku, Dev Agent MUSI traktować tę treść jako aktualny punkt odniesienia dla danego kroku.

Dev Agent NIE MOŻE zakładać, że zna aktualny stan pliku lepiej niż treść dostarczona przez człowieka.

W tym trybie Dev Agent MOŻE zwrócić tylko jeden z jawnych trybów zmiany:

* `WHOLE_FILE_REPLACEMENT`,
* `FULL_SECTION_REPLACEMENT`,
* `FULL_FUNCTION_REPLACEMENT`,
* `INSERT_BLOCK_BEFORE`,
* `INSERT_BLOCK_AFTER`.

Dla dokumentacji po polsku Dev Agent POWINIEN preferować `WHOLE_FILE_REPLACEMENT`, jeżeli zmiana dotyczy większej części dokumentu albo wielu sekcji jednocześnie.

Dev Agent NIE MOŻE zwracać niejednoznacznych instrukcji typu „dopisz coś podobnego” albo „zmień odpowiedni fragment”.

Dev Agent MUSI jasno wskazać:

* który plik jest edytowany,
* jaki tryb zmiany jest używany,
* czy człowiek ma podmienić cały plik, sekcję, funkcję czy blok,
* od którego nagłówka albo fragmentu zaczyna się podmiana,
* przed którym nagłówkiem albo fragmentem kończy się podmiana,
* jakie kontrole należy uruchomić po zapisaniu pliku.

Jeżeli Dev Agent zwraca blok do kopiuj/wklej, blok MUSI być kompletny.

Kompletny blok oznacza, że:

* ma jednoznaczny początek,
* ma jednoznaczny koniec,
* nie jest podzielony na kilka niezależnych fragmentów bez wyraźnej procedury,
* nie zawiera dwóch alternatywnych wersji tej samej zmiany,
* nie miesza treści pliku z instrukcjami poza treścią pliku,
* nie zawiera niedomkniętych bloków markdown,
* nie wymaga domyślania się brakującej końcówki.

Jeżeli Dev Agent nie jest w stanie wygenerować kompletnego bloku, MUSI wykonać STOP i poprosić o zawężenie zakresu zmiany.

Jeżeli zmiana dotyczy polskiej dokumentacji, Dev Agent NIE MOŻE używać PowerShell do zapisu treści pliku.

Dla polskiej dokumentacji Dev Agent MUSI preferować:

* otwarcie pliku w VS Code,
* ręczne wklejenie pełnego bloku,
* zapisanie pliku przez człowieka,
* kontrolę `git diff`,
* kontrolę `git diff --check`.

Celem tej procedury jest ograniczenie ręcznego łatania plików linia po linii.

Dev Agent ma prowadzić człowieka przez pełne, sprawdzalne bloki zmian.

## 4. Zakres pierwszej wersji

Pierwsza wersja Dev Agenta ma być wyłącznie proceduralnym analizatorem stanu i wyborem następnego kroku.

Pierwsza wersja Dev Agenta MUSI obsługiwać:

* analizę przekazanego stanu repozytorium,
* rozpoznanie znanych przypadków,
* wybór następnego bezpiecznego kroku,
* zwrócenie komunikatu STOP dla przypadków nieznanych,
* zwrócenie instrukcji dla człowieka.

Pierwsza wersja Dev Agenta NIE MOŻE:

* edytować plików,
* zapisywać dokumentacji,
* uruchamiać komend w systemie,
* wykonywać `git add`,
* wykonywać `git commit`,
* wykonywać `git push`,
* wykonywać `git pull`,
* samodzielnie naprawiać błędów,
* samodzielnie aktualizować dokumentacji,
* samodzielnie aktualizować kontraktu,
* samodzielnie aktualizować testów,
* samodzielnie podejmować decyzji architektonicznych.

## 5. Dane wejściowe

Minimalne wejście Dev Agenta składa się z opisu aktualnego kroku oraz wyników komend dostarczonych przez człowieka albo przez przyszłego lokalnego runnera.

Dev Agent MUSI przyjmować następujące dane logiczne:

* identyfikator kroku,
* cel kroku,
* dozwolony zakres zmiany,
* lista plików objętych krokiem,
* wynik `git status`,
* lokalny hash `HEAD`,
* hash `origin/main`,
* wynik `git diff`,
* wynik `git diff --cached`,
* wynik `git diff --check`,
* wynik lintowania,
* wynik testów.

Dla TradingLab aktualne kontrole jakości to:

* `git diff --check`,
* `uv run ruff check .`,
* `uv run pytest`.

Te komendy są szczegółem projektu TradingLab.

Uniwersalny rdzeń Dev Agenta NIE MOŻE zakładać, że każdy projekt używa `uv`, `ruff` albo `pytest`.

Nie każde wejście musi być dostępne w każdym momencie procedury.

Jeżeli wymagane wejście dla danej procedury nie zostało dostarczone, Dev Agent MUSI zwrócić następny krok polegający na dostarczeniu tego wejścia.

Dev Agent NIE MOŻE zakładać wyniku komendy, której nie otrzymał.

## 6. Stan repozytorium

Dev Agent MUSI rozpoznawać co najmniej następujące stany repozytorium:

### 6.1. CLEAN_SYNCED

Repozytorium jest gotowe do rozpoczęcia kroku.

Warunki:

* `git status` wskazuje czysty working tree,
* lokalny `HEAD` jest równy `origin/main`.

Decyzja:

* Dev Agent MOŻE TYLKO wskazać następny krok zgodny z procedurą aktualnego zadania.

### 6.2. CLEAN_UNKNOWN_REMOTE

Working tree jest czysty, ale Dev Agent nie ma informacji o zgodności `HEAD` z `origin/main`.

Warunki:

* `git status` wskazuje czysty working tree,
* brakuje lokalnego hash `HEAD` albo hash `origin/main`.

Decyzja:

* Dev Agent MUSI poprosić o wykonanie komend sprawdzających lokalny `HEAD` i `origin/main`.

### 6.3. CLEAN_NOT_SYNCED

Working tree jest czysty, ale lokalny `HEAD` różni się od `origin/main`.

Warunki:

* `git status` wskazuje czysty working tree,
* lokalny `HEAD` różni się od `origin/main`.

Decyzja:

* Dev Agent MUSI wykonać STOP,
* Dev Agent MUSI wskazać potrzebę świadomej synchronizacji,
* Dev Agent NIE MOŻE kontynuować zmiany bez nowego wyniku synchronizacji.

### 6.4. UNTRACKED_FILES

Repozytorium zawiera nowe pliki nieśledzone przez Git.

Warunki:

* `git status` zawiera sekcję `Untracked files`.

Decyzja:

* Dev Agent MUSI rozpoznać listę plików nieśledzonych,
* Dev Agent NIE MOŻE uznać pustego `git diff` za brak zmian,
* Dev Agent MUSI wybrać procedurę dla nowego pliku, jeżeli taka procedura istnieje,
* jeżeli procedura dla nowego pliku nie istnieje, Dev Agent MUSI wykonać STOP.

### 6.5. STAGED_CHANGES

Repozytorium zawiera zmiany dodane do indeksu.

Warunki:

* `git status` zawiera sekcję `Changes to be committed`.

Decyzja:

* Dev Agent MUSI wymagać kontroli `git diff --cached`,
* Dev Agent NIE MOŻE przejść do commita bez pokazania diffu staged,
* Dev Agent NIE MOŻE przejść do commita bez pozytywnych kontroli wymaganych przez procedurę.

### 6.6. UNSTAGED_CHANGES

Repozytorium zawiera zmiany nieprzygotowane do commita.

Warunki:

* `git status` zawiera sekcję `Changes not staged for commit`.

Decyzja:

* Dev Agent MUSI wymagać kontroli `git diff`,
* Dev Agent MUSI sprawdzić, czy zmiany mieszczą się w zakresie kroku,
* jeżeli zakres nie jest zgodny, Dev Agent MUSI wykonać STOP.

### 6.7. UNKNOWN_STATE

Repozytorium ma stan, którego Dev Agent nie rozpoznaje.

Decyzja:

* Dev Agent MUSI wykonać STOP,
* Dev Agent MUSI poinformować, że brakuje procedury dla tego stanu,
* Dev Agent NIE MOŻE kontynuować pracy.

## 7. Decyzje Dev Agenta

Dev Agent może zwrócić tylko jeden z opisanych typów decyzji.

### 7.1. NEXT_STEP

Decyzja oznacza, że istnieje znana procedura i można wykonać następny krok.

Wymagane pola:

* typ decyzji,
* nazwa procedury,
* opis następnego kroku,
* komenda lub instrukcja dla człowieka,
* warunek przejścia dalej.

### 7.2. STOP

Decyzja oznacza obowiązkowe zatrzymanie pracy.

Wymagane pola:

* typ decyzji,
* powód STOP,
* dane, które spowodowały STOP,
* informacja, jakiego fragmentu procedury brakuje albo jaki warunek nie został spełniony,
* instrukcja dla człowieka.

### 7.3. READY_FOR_HUMAN_APPROVAL

Decyzja oznacza, że procedura doszła do punktu wymagającego jawnej akceptacji człowieka.

Wymagane pola:

* typ decyzji,
* nazwa procedury,
* podsumowanie wykonanych kontroli,
* proponowana następna czynność,
* informacja, że Dev Agent NIE MOŻE kontynuować bez akceptacji człowieka.

### 7.4. DONE

Decyzja oznacza, że procedura została zakończona i potwierdzona.

Wymagane pola:

* typ decyzji,
* nazwa procedury,
* końcowy `git status`,
* lokalny hash `HEAD`,
* hash `origin/main`,
* potwierdzenie zgodności hashy.

## 8. Procedura PREFLIGHT_REPOSITORY_CHECK

Ta procedura sprawdza, czy można rozpocząć nowy krok.

Wymagane wejścia:

* wynik `git status`,
* lokalny hash `HEAD`,
* hash `origin/main`.

Warunki przejścia:

* working tree jest czysty,
* lokalny `HEAD` jest równy `origin/main`.

Jeżeli warunki są spełnione, Dev Agent zwraca decyzję `NEXT_STEP`.

Jeżeli brakuje lokalnego hash `HEAD` albo hash `origin/main`, Dev Agent zwraca decyzję `NEXT_STEP` z instrukcją dostarczenia brakujących danych.

Jeżeli working tree nie jest czysty, Dev Agent zwraca decyzję `STOP`.

Jeżeli lokalny `HEAD` różni się od `origin/main`, Dev Agent zwraca decyzję `STOP`.

## 9. Procedura NEW_POLISH_DOCUMENTATION_FILE

Ta procedura dotyczy dodania albo aktualizacji pliku dokumentacji w języku polskim.

Wymagane warunki startowe:

* procedura `PREFLIGHT_REPOSITORY_CHECK` zakończona pozytywnie,
* zakres kroku obejmuje jawnie wskazany plik dokumentacji,
* plik należy do katalogu `dokumentacja`.

Kroki procedury:

1. Dev Agent MUSI wskazać otwarcie pliku w VS Code.
2. Dev Agent MUSI dostarczyć jeden pełny blok dokumentu albo jeden precyzyjny blok sekcji do ręcznego wklejenia.
3. Dev Agent NIE MOŻE użyć PowerShell do zapisu dokumentacji.
4. Po zapisaniu pliku Dev Agent MUSI wymagać `git status`.
5. Jeżeli plik jest `untracked`, Dev Agent MUSI wskazać `git add` dla tego pliku.
6. Po `git add` Dev Agent MUSI wymagać `git diff --cached`.
7. Dev Agent MUSI sprawdzić, czy staged diff obejmuje tylko dozwolony zakres.
8. Dev Agent MUSI wymagać `git diff --check`.
9. Dev Agent MUSI wymagać lintowania właściwego dla projektu.
10. Dev Agent MUSI wymagać testów właściwych dla projektu.
11. Jeżeli kontrole są poprawne, Dev Agent zwraca `READY_FOR_HUMAN_APPROVAL` dla commita.
12. Po commicie Dev Agent MUSI wymagać `git push`.
13. Po pushu Dev Agent MUSI wymagać końcowego `git status`, lokalnego hash `HEAD` i hash `origin/main`.
14. Jeżeli końcowy `HEAD` jest równy `origin/main`, Dev Agent zwraca `DONE`.

Warunki STOP:

* plik nie znajduje się w katalogu `dokumentacja`,
* staged diff obejmuje więcej plików niż zakres kroku,
* `git diff --check` zgłasza błąd,
* lintowanie zgłasza błąd,
* testy zgłaszają błąd,
* człowiek nie zaakceptował commita,
* człowiek nie zaakceptował pusha.

## 10. Format odpowiedzi Dev Agenta

Minimalna odpowiedź Dev Agenta ma mieć strukturę logiczną:

* decyzja,
* procedura,
* powód,
* następny krok,
* wymagane dane wejściowe,
* warunek przejścia dalej.

Przykład logiczny:

```text
decyzja: NEXT_STEP
procedura: PREFLIGHT_REPOSITORY_CHECK
powód: brakuje hash origin/main
następny krok: wykonaj git ls-remote origin refs/heads/main
wymagane dane wejściowe: hash origin/main
warunek przejścia dalej: lokalny HEAD musi być równy origin/main
```

## 11. Minimalne przypadki testowe wynikające z kontraktu

Pierwsze testy Dev Agenta mają obejmować wyłącznie analizę stanu i wybór następnego kroku.

Minimalne przypadki testowe:

1. clean synced repository zwraca `NEXT_STEP`,
2. clean repository bez hash `origin/main` zwraca `NEXT_STEP` z żądaniem brakującego hasha,
3. clean repository z różnym `HEAD` i `origin/main` zwraca `STOP`,
4. untracked file przy pustym `git diff` nie jest traktowany jako brak zmian,
5. staged new documentation file wymaga `git diff --cached`,
6. staged diff poza zakresem kroku zwraca `STOP`,
7. nieznany stan repozytorium zwraca `STOP`,
8. czysty `git diff --check` pozwala przejść do kontroli lintowania,
9. błąd `git diff --check` zwraca `STOP`,
10. błąd lintowania zwraca `STOP`,
11. błąd testów zwraca `STOP`,
12. komplet poprawnych kontroli zwraca `READY_FOR_HUMAN_APPROVAL`.

## 12. Granice bezpieczeństwa

Dev Agent MUSI działać w granicach jawnie opisanych procedur.

Dev Agent NIE MOŻE wykonać żadnej akcji, która zmienia repozytorium, w pierwszej wersji implementacji.

Dev Agent NIE MOŻE wykonać commita ani pusha w żadnej wersji bez jawnej akceptacji człowieka.

Dev Agent NIE MOŻE podejmować decyzji inwestycyjnych.

Dev Agent NIE MOŻE podejmować decyzji architektonicznych.

Dev Agent NIE MOŻE ukrywać lub pomijać błędów.

Dev Agent NIE MOŻE interpretować braku danych jako sukcesu.

Dev Agent NIE MOŻE traktować komend specyficznych dla TradingLab jako uniwersalnych zasad rdzenia.

## 13. Następny krok

Po aktualizacji kontraktu najbliższym krokiem technicznym jest obsługa etapu po `READY_FOR_HUMAN_APPROVAL`.

Proponowany krok:

**75A.9-TEST — Add Dev Agent human approval and completion flow**

Zakres testu:

* przyjęcie decyzji człowieka dotyczącej commita,
* STOP, gdy człowiek odrzuci commit,
* NEXT_STEP, gdy człowiek zaakceptuje commit,
* żądanie końcowego `git status`, `HEAD` i `origin/main`,
* STOP przy końcowym nieczystym working tree,
* STOP przy końcowej różnicy `HEAD` i `origin/main`,
* `DONE` przy końcowym clean working tree i `HEAD == origin/main`.
