# Dev Agent — drzewo scenariuszy

Status: roboczy
Krok: 75A.6-DOC
Zakres: praktyczna mapa działania proceduralnego Dev Agenta

## 1. Cel dokumentu

Ten dokument jest krótką mapą działania Dev Agenta.

Dokument pokazuje:

* jakie scenariusze Dev Agent rozpoznaje,
* jakie decyzje zwraca,
* kiedy przechodzi dalej,
* kiedy wykonuje STOP,
* jakie kompetencje są już zaimplementowane,
* jakie kompetencje nie są jeszcze zaimplementowane.

Ten dokument ma być praktyczną ściągą przed kolejnymi zmianami w Dev Agencie.

Jeżeli dodawana jest nowa kompetencja Dev Agenta, najpierw musi być jasne, do którego miejsca w drzewie scenariuszy zostaje dopisana.

## 2. Aktualny poziom Dev Agenta

Aktualnie Dev Agent istnieje jako proceduralny rdzeń decyzyjny.

Zaimplementowany moduł:

`src/tradinglab/dev_agent/procedural_decision.py`

Główna funkcja:

`evaluate_repository_state(...)`

Dev Agent aktualnie NIE wykonuje komend.

Dev Agent aktualnie NIE edytuje plików.

Dev Agent aktualnie NIE wykonuje `git add`, `git commit`, `git push` ani `git pull`.

Dev Agent aktualnie działa wyłącznie na danych wejściowych przekazanych przez człowieka albo przyszłą warstwę wykonawczą.

## 3. Aktualne wejścia Dev Agenta

Aktualnie funkcja `evaluate_repository_state(...)` przyjmuje:

* `git_status`,
* `local_head`,
* `origin_main`,
* `git_diff`,
* `git_diff_cached`,
* `allowed_paths`.

Nie każde wejście jest wymagane w każdym scenariuszu.

Jeżeli dane wejściowe są niewystarczające dla danej procedury, Dev Agent zwraca następny wymagany krok.

Dev Agent NIE MOŻE zakładać wyniku komendy, której nie otrzymał.

## 4. Aktualne decyzje Dev Agenta

Dev Agent zwraca jedną decyzję proceduralną.

Aktualne typy decyzji:

* `NEXT_STEP`,
* `STOP`,
* `READY_FOR_HUMAN_APPROVAL`,
* `DONE`.

Na obecnym poziomie implementacji aktywnie używane są:

* `NEXT_STEP`,
* `STOP`.

`READY_FOR_HUMAN_APPROVAL` i `DONE` są częścią kontraktu, ale nie są jeszcze używane przez aktualne testy.

## 5. Aktualne stany repozytorium

Dev Agent rozpoznaje następujące stany repozytorium:

* `CLEAN_SYNCED`,
* `CLEAN_UNKNOWN_REMOTE`,
* `CLEAN_NOT_SYNCED`,
* `UNTRACKED_FILES`,
* `STAGED_CHANGES`,
* `UNSTAGED_CHANGES`,
* `UNKNOWN_STATE`.

## 6. Drzewo scenariuszy — aktualny rdzeń

```text
START
│
├── Czy git_status jest pusty, fatal albo nie wygląda jak repo Git?
│   ├── TAK
│   │   └── STOP
│   │       state: UNKNOWN_STATE
│   │       reason: unknown_repository_state
│   │
│   └── NIE
│       │
│       ├── Czy git_status pokazuje clean working tree?
│       │   ├── TAK
│       │   │   └── PREFLIGHT_REPOSITORY_CHECK
│       │   │       │
│       │   │       ├── Czy brakuje local_head i origin_main?
│       │   │       │   └── NEXT_STEP
│       │   │       │       state: CLEAN_UNKNOWN_REMOTE
│       │   │       │       next_step: provide_local_and_origin_hashes
│       │   │       │
│       │   │       ├── Czy brakuje local_head?
│       │   │       │   └── NEXT_STEP
│       │   │       │       state: CLEAN_UNKNOWN_REMOTE
│       │   │       │       next_step: provide_local_head_hash
│       │   │       │
│       │   │       ├── Czy brakuje origin_main?
│       │   │       │   └── NEXT_STEP
│       │   │       │       state: CLEAN_UNKNOWN_REMOTE
│       │   │       │       next_step: provide_origin_main_hash
│       │   │       │
│       │   │       ├── Czy local_head != origin_main?
│       │   │       │   └── STOP
│       │   │       │       state: CLEAN_NOT_SYNCED
│       │   │       │       reason: local_head_differs_from_origin_main
│       │   │       │
│       │   │       └── Czy local_head == origin_main?
│       │   │           └── NEXT_STEP
│       │   │               state: CLEAN_SYNCED
│       │   │               next_step: continue_current_procedure
│       │   │
│       │   └── NIE
│       │
│       ├── Czy git_status pokazuje Untracked files?
│       │   ├── TAK
│       │   │   └── NEW_POLISH_DOCUMENTATION_FILE
│       │   │       │
│       │   │       ├── Czy git_diff jest pusty?
│       │   │       │   └── NEXT_STEP
│       │   │       │       state: UNTRACKED_FILES
│       │   │       │       next_step: stage_untracked_documentation_file
│       │   │       │       reason: untracked_files_not_visible_in_worktree_diff
│       │   │       │
│       │   │       └── W innym przypadku
│       │   │           └── NEXT_STEP
│       │   │               state: UNTRACKED_FILES
│       │   │               next_step: stage_untracked_documentation_file
│       │   │               reason: untracked_files_require_staging
│       │   │
│       │   └── NIE
│       │
│       ├── Czy git_status pokazuje Changes to be committed?
│       │   ├── TAK
│       │   │   └── NEW_POLISH_DOCUMENTATION_FILE
│       │   │       │
│       │   │       ├── Czy brakuje git_diff_cached albo allowed_paths?
│       │   │       │   └── NEXT_STEP
│       │   │       │       state: STAGED_CHANGES
│       │   │       │       next_step: review_cached_diff
│       │   │       │       reason: staged_changes_require_cached_diff_review
│       │   │       │
│       │   │       ├── Czy git_diff_cached nie zawiera ścieżek?
│       │   │       │   └── STOP
│       │   │       │       state: STAGED_CHANGES
│       │   │       │       reason: staged_diff_has_no_paths
│       │   │       │
│       │   │       ├── Czy staged diff wychodzi poza allowed_paths?
│       │   │       │   └── STOP
│       │   │       │       state: STAGED_CHANGES
│       │   │       │       reason: staged_diff_outside_allowed_scope
│       │   │       │
│       │   │       └── Czy staged diff mieści się w allowed_paths?
│       │   │           └── NEXT_STEP
│       │   │               state: STAGED_CHANGES
│       │   │               next_step: run_diff_check
│       │   │               reason: staged_diff_matches_allowed_scope
│       │   │
│       │   └── NIE
│       │
│       ├── Czy git_status pokazuje Changes not staged for commit?
│       │   ├── TAK
│       │   │   └── NEXT_STEP
│       │   │       state: UNSTAGED_CHANGES
│       │   │       procedure: UNKNOWN
│       │   │       next_step: review_worktree_diff
│       │   │       reason: unstaged_changes_require_worktree_diff_review
│       │   │
│       │   └── NIE
│       │
│       └── Inny nierozpoznany stan
│           └── STOP
│               state: UNKNOWN_STATE
│               reason: unknown_repository_state
```

## 7. Aktualne kompetencje — Dev Agent POTRAFI

Dev Agent POTRAFI aktualnie:

* przyjąć tekstowy wynik `git status`,
* przyjąć lokalny hash `HEAD`,
* przyjąć hash `origin/main`,
* przyjąć tekstowy wynik `git diff`,
* przyjąć tekstowy wynik `git diff --cached`,
* przyjąć listę `allowed_paths`,
* rozpoznać czyste i zsynchronizowane repozytorium,
* rozpoznać czyste repozytorium z brakującymi hashami,
* rozpoznać czyste repozytorium bez synchronizacji `HEAD` i `origin/main`,
* rozpoznać nowe pliki `untracked`,
* rozpoznać staged changes,
* rozpoznać unstaged changes,
* rozpoznać podstawowy nieznany stan repozytorium,
* nie traktować pustego `git diff` jako braku zmian przy plikach `untracked`,
* wymagać `git diff --cached` przy staged changes,
* wyciągnąć ścieżki plików z `git diff --cached`,
* porównać ścieżki ze staged diff z `allowed_paths`,
* zwrócić STOP, gdy staged diff wychodzi poza zakres kroku,
* zwrócić następny krok, gdy staged diff mieści się w zakresie kroku.

## 8. Aktualne ograniczenia — Dev Agent NIE POTRAFI JESZCZE

Dev Agent NIE POTRAFI JESZCZE:

* samodzielnie uruchomić `git status`,
* samodzielnie uruchomić `git diff`,
* samodzielnie uruchomić `git diff --cached`,
* samodzielnie uruchomić `git diff --check`,
* samodzielnie uruchomić `ruff`,
* samodzielnie uruchomić `pytest`,
* samodzielnie odczytać lokalnego hash `HEAD`,
* samodzielnie odczytać hash `origin/main`,
* samodzielnie wykonać `git add`,
* samodzielnie wykonać `git commit`,
* samodzielnie wykonać `git push`,
* samodzielnie wykonać `git pull`,
* samodzielnie edytować plików,
* samodzielnie tworzyć dokumentacji,
* interpretować wyniku `git diff --check`,
* interpretować wyniku `ruff`,
* interpretować wyniku `pytest`,
* zwracać `READY_FOR_HUMAN_APPROVAL` na podstawie pełnego zestawu kontroli,
* zwracać `DONE` po końcowej weryfikacji push i hashy,
* obsługiwać wielu procedur poza minimalnym szkieletem `NEW_POLISH_DOCUMENTATION_FILE`.

## 9. Scenariusz realnej pracy — nowy plik dokumentacji

Aktualnie najpełniej opisany scenariusz dotyczy nowego pliku dokumentacji w języku polskim.

```text
START KROKU
│
├── Człowiek dostarcza git status, HEAD i origin/main
│
├── Dev Agent sprawdza PREFLIGHT_REPOSITORY_CHECK
│   ├── CLEAN_SYNCED
│   │   └── NEXT_STEP: można rozpocząć procedurę
│   └── inny stan
│       └── STOP albo żądanie brakujących danych
│
├── Człowiek tworzy dokument w VS Code
│
├── Człowiek dostarcza git status
│
├── Dev Agent widzi UNTRACKED_FILES
│   └── NEXT_STEP: stage_untracked_documentation_file
│
├── Człowiek wykonuje git add
│
├── Człowiek dostarcza git diff --cached i allowed_paths
│
├── Dev Agent widzi STAGED_CHANGES
│   ├── staged diff mieści się w allowed_paths
│   │   └── NEXT_STEP: run_diff_check
│   └── staged diff wychodzi poza allowed_paths
│       └── STOP
│
└── Dalsza część procedury nie jest jeszcze zaimplementowana
```

## 10. Najbliższa brakująca gałąź drzewa

Najbliższa brakująca gałąź dotyczy interpretacji wyników kontroli jakości.

Do dodania w kolejnym kroku:

```text
STAGED_CHANGES + staged diff mieści się w allowed_paths
│
└── NEXT_STEP: run_diff_check
    │
    ├── Czy brakuje git diff --check?
    │   └── NEXT_STEP: provide_diff_check_result
    │
    ├── Czy git diff --check ma błędy?
    │   └── STOP
    │       reason: diff_check_failed
    │
    ├── Czy brakuje ruff?
    │   └── NEXT_STEP: provide_ruff_result
    │
    ├── Czy ruff ma błędy?
    │   └── STOP
    │       reason: ruff_failed
    │
    ├── Czy brakuje pytest?
    │   └── NEXT_STEP: provide_pytest_result
    │
    ├── Czy pytest ma błędy?
    │   └── STOP
    │       reason: pytest_failed
    │
    └── Wszystkie kontrole OK
        └── READY_FOR_HUMAN_APPROVAL
            next_step: request_commit_approval
```

## 11. Zasada aktualizacji drzewa

Każda nowa kompetencja Dev Agenta MUSI mieć miejsce w tym drzewie scenariuszy.

Jeżeli nowa sytuacja nie pasuje do istniejącego drzewa, obowiązuje kolejność:

1. STOP,
2. aktualizacja obserwacji proceduralnych,
3. aktualizacja kontraktu,
4. aktualizacja drzewa scenariuszy,
5. test,
6. implementacja.

Dev Agent NIE MOŻE dostać implementacji dla sytuacji, która nie została opisana w dokumentacji proceduralnej.

## 12. Następny krok

Po dodaniu tego dokumentu najbliższym krokiem technicznym jest interpretacja wyników kontroli jakości.

Proponowany krok:

**75A.7-TEST — Add Dev Agent check result interpretation**

Zakres:

* interpretacja `git diff --check`,
* interpretacja `ruff`,
* interpretacja `pytest`,
* STOP przy błędach kontroli,
* NEXT_STEP przy brakujących wynikach,
* `READY_FOR_HUMAN_APPROVAL` przy komplecie poprawnych kontroli.

Na tym etapie Dev Agent nadal NIE uruchamia komend samodzielnie.
