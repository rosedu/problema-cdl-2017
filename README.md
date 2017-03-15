# Nu uitati de uitati sa completati [formularul de inscriere](https://docs.google.com/forms/d/e/1FAIpQLSejjNZjNdyGQGj4IrsfLOY1vuCXT_9Ki_08ahntiakWTJsJ3A/viewform?c=0&w=1)!

# UPDATE: A fost lansat checker-ul pe vmchecker. Puteti sa va submiteti solutiile acolo pentru notare.

# UPDATE: Au fost publicate testele

## Apache log parser

Gigel si-a deschis site de vandut masini virtuale la mana a doua si vrea sa vada cand e cel mai accesat. Pentru asta el se uita la log-urile server-ului apache. El observa ca in perioade de trafic mai intens apar si erori de accesare si vrea sa verifice rata de succes in acele perioade, pentru a-si face o idee in ce cazuri merge mai rau si ce fel de optimizari ar fi necesare.

Gigel, din pacate, nu are mult timp la dispozitie deoarece are de pregatit masinile virtuale care vor fi vandute. Din acest motiv Gigel te-a rugat sa il ajuti prin realizarea unei statistici pentru o perioada de trafic intens, stabilind cate requesturi au avut succes, ordonate dupa data si endpoint.

## Format log-uri

Acesta e un exemplu de log preluat de la un server Apache. Partile importante sunt:

* timestamp-ul `[22/Feb/2017:18:45:02 +0000]`
* endpoint-ul `/ubuntu.html`
* status code (urmeaza imediat dupa sectiunea de endpoint) `503`
    

Formatul log-urilor lui Gigel este descris mai pe larg [aici](https://httpd.apache.org/docs/1.3/logs.html).

    10.10.10.10 - - [22/Feb/2017:18:45:02 +0000] "GET /fedora.html?user=gheorghe HTTP/1.1" 401 533 "-" "python-requests/2.12.4"
    10.10.10.10 - - [22/Feb/2017:18:45:13 +0000] "GET /ubuntu.html HTTP/1.1" 200 1303 "-" "python-requests/2.12.4"
    10.10.10.10 - - [22/Feb/2017:18:45:24 +0000] "GET /centos.html#enunt HTTP/1.1" 200 1160 "-" "python-requests/2.12.4"
    10.10.10.10 - - [22/Feb/2017:18:45:34 +0000] "GET /ubuntu.html HTTP/1.1" 200 1303 "-" "python-requests/2.12.4"
    192.168.100.25 - - [22/Feb/2017:18:45:45 +0000] "GET /fedora.html?user=dorel HTTP/1.1" 401 1160 "-" "python-requests/2.12.4"
    192.168.100.25 - - [22/Feb/2017:18:45:49 +0000] "GET /fedora.html?user=gigel HTTP/1.1" 200 1160 "-" "python-requests/2.12.4"
    192.168.100.25 - - [22/Feb/2017:18:45:55 +0000] "GET /centos.html#pret HTTP/1.1" 503 1160 "-" "python-requests/2.12.4"
    192.168.100.25 - - [22/Feb/2017:18:46:06 +0000] "GET /centos.html HTTP/1.1" 200 1160 "-" "python-requests/2.12.4"
    192.168.100.25 - - [22/Feb/2017:18:46:16 +0000] "GET /fedora.html?user=dorel HTTP/1.1" 401 533 "-" "python-requests/2.12.4"
    1.2.3.4 - - [22/Feb/2017:18:46:27 +0000] "GET /fedora.html HTTP/1.1" 404 533 "-" "python-requests/2.12.4"
    1.2.3.4 - - [22/Feb/2017:18:46:37 +0000] "GET /fedora.html HTTP/1.1" 404 533 "-" "python-requests/2.12.4"
    1.2.3.4 - - [22/Feb/2017:18:46:48 +0000] "GET /centos.html HTTP/1.1" 200 1160 "-" "python-requests/2.12.4"

**Atentie!** Pentru randul `192.168.100.25 - - [22/Feb/2017:18:46:16 +0000] "GET /fedora.html?user=dorel HTTP/1.1" 401 533 "-" "python-requests/2.12.4"`, endpoint-ul este doar  `/fedora.html`. Se ignora parametrii de query si ancorele din URL (adica partile de dupa `?` sau `#`).

Intrarile din log-uri vor fi ordonate cronologic.

## Format statistici

###UPDATE: intervalele de statistici nu sunt neaparat continue unul dupa altul. Daca intr-un interval de X minute nu a fost niciun entry pentru un anumit endpoint, atunci acesta nu va aparea in statistici, iar urmatorul interval va incepe de la cel mai apropiat entry.

###UPDATE2: intervalele sunt determinate pentru fiecare endpoint in parte.

Gigel va cere de fapt sa calculati rata de succes per endpoint per numar de minute prestabilit (de exemplu per un minut). Componentele unui rand de output sunt:

* data, in format `%an-%luna-%ziT%ora:%minut`. T-ul de la mijloc are doar rol de separator.
* durata intervalului, exprimata intr-un numar intreg, pozitiv de minute
* endpoint-ul
* rata de succes, ce reprezinta procentul de status code-uri ce incep cu `2` (de forma `2XX`, exemplu `200`), din intervalul curent. Aceasta va fi rotunjita la 2 zecimale

Rezultatele vor fi sortate mai intai dupa timestamp si apoi lexicografic dupa endpoint.

Un exemplu de output pentru log-ul de mai sus, in care durata intervalului este setata la 1 minut:

    2017-02-22T18:45 1 /centos.html 50.0
    2017-02-22T18:45 1 /fedora.html 33.33
    2017-02-22T18:45 1 /ubuntu.html 100.0
    2017-02-22T18:46 1 /centos.html 100.0
    2017-02-22T18:46 1 /fedora.html 0.0


Sau cu durata intervalului setata la 2 minute:

    2017-02-22T18:45 2 /centos.html 75.0
    2017-02-22T18:45 2 /fedora.html 16.67
    2017-02-22T18:45 2 /ubuntu.html 100.0

**Atentie!** Un request primit la `18:45:59` nu va fi considerat in acelasi minut cu un alt request primit la `18:46:00`, desi diferenta de timp dintre cele doua evenimente este mai mica de 60 de secunde. Va fi luat in considerare doar minutul din timestamp-ul unui request.

## Punctaj

Aveti de implementat in **orice** limbaj de programare un program care sa prelucreze log-urile lui Gigel. Acesta va fi punctat astfel:

* pentru intervale de 1 minut -> `40%` din punctaj
* pentru intervale de oricate minute -> `40%` din punctaj
* pentru prelucrarea request-urilor doar dintr-un anumit interval -> `20%` din punctaj

Numarul de minute dintr-un interval va fi transmis ca parametru in linia de comanda, ca de exemplu: `./log_stats --interval 2`. Parametrul poate lipsi, considerandu-se ca valoare implicita `1`.

Inceputul si sfarsitul unui interval vor fi de asemenea transmisi in linia de comanda: `./log_stats --start 2017-02-22T18:45 --end 2017-02-22T18:48`. **Atentie!** Parametrii `--start` si `--end` pot aparea si separati, reprezentand doar un capat al intervalului, celalalt fiind considerat cel mai vechi/nou log. Parametrii --start/--end au formatul $dataT$ora:$minut.

Parametrii din linia de comanda pot aparea in orice ordine.


**Puteti sa va folositi de biblioteci existente pentru a implementa diferite parti din functionalitate (de exemplu, prelucrarea datelor calendaristice si a diferentelor intre ele). Nu aveti in schimb voie sa folositi un parser de log-uri deja implementat.**

## Bonus

Dupa ce a vazut Gigel ce treaba buna ai facut s-a gandit sa foloseasca scriptul tau pentru a depana anumite probleme ce tin de logica aplicatiei. Prin urmare s-a gandit sa extinda programul initial cu optiunea de a primi ca argumente o lista de coduri HTTP, pe care le considera succes, restul fiind failure. De asemenea in lista de parametrii, pot aparea si numere de forma `20X`, unde `X` reprezinta posibilitatea oricarui digit `(0-9)`.

`20X -> [200, 201, ... ,209]`

Exemplu rulare: `./log_stats --start 2017-02-22T18:45 --end 2017-02-22T18:48 --success 20X,401,3X0`

## Testare

Testarea va fi efectuata cu checker-ul din repository (fisierul `checker.py`). Acesta se asteapta sa gaseasca in directorul curent alte doua directoare, `tests` si `reference`. Checker-ul va genera output-urile voastre in directorul `output` si diferentele dintre output si referinta in directorul `diff`.

Pentru a rula checker-ul aveti nevoie de `python3`. Un exemplu de rulare in Linux: `python3 checker.py`.

Daca aveti nelamuriri in legatura cu checker-ul, cu testele sau considerati ca exista greseli in output-ul de referinta, creati un issue nou si va vom raspunde acolo.

## Punctare

Solutiile voastre trebuie submise pe vmchecker [la acest link](https://vmchecker.cs.pub.ro/ui/#CDL). Pe platforma veti primi nota si eventual feedback pe baza codului.
