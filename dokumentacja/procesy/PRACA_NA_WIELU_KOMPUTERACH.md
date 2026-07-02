# Praca na wielu komputerach

Ten dokument opisuje bezpieczną procedurę pracy nad projektem TradingLab na więcej niż jednym komputerze.

Celem procedury jest uniknięcie sytuacji, w której jeden komputer pracuje na starszym stanie repozytorium albo zmiany lokalne nie zostały wypchnięte na GitHub przed rozpoczęciem pracy na drugim komputerze.

## Zasada główna

Źródłem prawdy dla projektu jest zdalny branch:

```text
origin/main
```

Przed rozpoczęciem pracy trzeba upewnić się, że lokalny branch `main` jest zgodny z `origin/main`.

Po zakończeniu pracy trzeba upewnić się, że commit został wypchnięty na GitHub i że lokalny `HEAD` jest zgodny ze zdalnym `origin/main`.

## Sygnały robocze w rozmowie z ChatGPT

W pracy nad projektem TradingLab można używać dwóch krótkich sygnałów wpisywanych w rozmowie z ChatGPT.

Nie są to komendy PowerShell.

Są to wiadomości do ChatGPT, które mają uruchomić odpowiednią procedurę kontroli repozytorium.

W tym dokumencie słowo „asystent” oznacza ChatGPT albo inny model AI prowadzący użytkownika krok po kroku przez pracę nad projektem TradingLab.

### Sygnał: przechodzę

Sygnału `przechodzę` używa się na komputerze, na którym kończy się bieżącą pracę.

Oznacza to:

1. sprawdzenie stanu repozytorium,
2. uruchomienie testów,
3. uruchomienie ruffa,
4. sprawdzenie diffu,
5. wykonanie commita,
6. wykonanie pusha,
7. potwierdzenie, że lokalny `HEAD` i zdalny `origin/main` mają ten sam hash.

Standardowy zestaw komend przed commitem:

```powershell
git status
uv run pytest
uv run ruff check .
git diff --stat
git diff --check
git diff
```

Po zaakceptowaniu diffu:

```powershell
git add .
git commit -m "Krótki opis zmiany"
git status
git push
```

Po pushu:

```powershell
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Hashe muszą być identyczne.

Dopiero wtedy można uznać, że praca została bezpiecznie przekazana na GitHub i można kontynuować na innym komputerze.

### Sygnał: przeszedłem

Sygnału `przeszedłem` używa się na komputerze, na którym rozpoczyna się pracę.

Oznacza to:

1. pobranie aktualnego stanu z GitHuba,
2. sprawdzenie brancha,
3. sprawdzenie czystości repozytorium,
4. porównanie lokalnego `HEAD` z `origin/main`,
5. ewentualne wykonanie `git pull --ff-only`,
6. rozpoczęcie pracy dopiero po potwierdzeniu zgodności.

Standardowy zestaw komend:

```powershell
cd C:\Projekty\TradingLab

git fetch origin --prune
git status
git branch -vv
git log --oneline -8 --decorate
git rev-parse HEAD
git rev-parse origin/main
git ls-remote origin refs/heads/main
git status --porcelain -uall
```

Warunki bezpiecznego startu:

1. `git status` pokazuje czyste drzewo robocze.
2. `git status --porcelain -uall` nic nie zwraca.
3. `git rev-parse HEAD` i `git rev-parse origin/main` pokazują ten sam hash.
4. `git ls-remote origin refs/heads/main` pokazuje ten sam hash dla zdalnego brancha `main`.

Jeżeli lokalny branch jest za `origin/main`, należy wykonać:

```powershell
git pull --ff-only
git status
git log --oneline -8 --decorate
```

Jeżeli `git pull --ff-only` przejdzie poprawnie i drzewo robocze jest czyste, można rozpocząć pracę.

Jeżeli `git pull --ff-only` nie przejdzie, należy uruchomić procedurę STOP.

## Codzienny skrót pracy

Normalny cykl pracy wygląda tak:

1. Na komputerze A:
   - praca nad zmianą,
   - testy,
   - ruff,
   - diff,
   - commit,
   - push,
   - kontrola hashy.

2. Na komputerze B:
   - `git fetch origin --prune`,
   - kontrola branchy i hashy,
   - ewentualnie `git pull --ff-only`,
   - start pracy dopiero po potwierdzeniu zgodności.

W rozmowie z ChatGPT wystarczy używać haseł:

```text
przechodzę
```

oraz:

```text
przeszedłem
```

ChatGPT ma wtedy prowadzić użytkownika krok po kroku i nie powinien zakładać, że lokalny stan jest aktualny bez sprawdzenia GitHub / `origin/main`.

## Procedura STOP

Nie wolno zaczynać zmian, jeżeli:

1. `git status` pokazuje lokalne zmiany, których pochodzenie nie jest jasne.
2. `git status --porcelain -uall` pokazuje nieśledzone pliki, które powinny być częścią projektu.
3. `HEAD` różni się od `origin/main`.
4. `git pull --ff-only` nie przechodzi.
5. Nie wiadomo, czy ostatnia praca z drugiego komputera została wypchnięta na GitHub.
6. Lokalny branch nie jest `main`.
7. Remote `origin` wskazuje na inne repozytorium niż oczekiwane.

W takiej sytuacji należy najpierw wykonać diagnostykę:

```powershell
git status
git branch -vv
git remote -v
git log --oneline --decorate --graph --all -15
git ls-remote origin refs/heads/main
```

Dopiero po wyjaśnieniu rozjazdu można kontynuować pracę.

## Edycja dokumentacji i plików z polskimi znakami

Dokumentację projektową oraz inne pliki tekstowe zawierające polskie znaki należy edytować w VS Code.

Nie należy tworzyć długich plików dokumentacji przez `Set-Content`, `Add-Content` ani wielolinijkowe here-stringi w PowerShellu, jeżeli plik zawiera polskie znaki.

Bezpieczna procedura edycji dokumentacji:

1. Otworzyć plik w VS Code komendą `code`.
2. Wkleić treść bezpośrednio w edytorze.
3. Zapisać plik w kodowaniu UTF-8.
4. Sprawdzić diff przed commitem.

Przykład:

```powershell
code dokumentacja\procesy\PRACA_NA_WIELU_KOMPUTERACH.md
```

Jeżeli nowy plik dokumentacji ma zostać utworzony, PowerShell może służyć do utworzenia folderu, ale sama treść dokumentu powinna zostać wklejona i zapisana w VS Code.

## Pliki ignorowane

Procedura dotyczy plików śledzonych przez Git.

Pliki ignorowane, takie jak `.venv`, cache, lokalne ustawienia edytora albo tymczasowe pliki narzędzi, nie są traktowane jako źródło prawdy projektu i nie muszą być zgodne między komputerami.
