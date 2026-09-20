# base-project-worked-example — учебная сборка

Заполненная, готовая к клонированию конфигурация кодинг-агента: то же, что
`templates/base-project-template/`, но **без единой `<BRACKETED>`-заглушки** — на живом проекте.
Шаблон показывает, из чего собирают; эта сборка показывает, что получилось.

Проект-носитель — `signup-landing/`: одна статическая страница с формой заявки на демо-урок
(имя и email), Vite поверх HTML/CSS/JS, тесты на Playwright, своего бэкенда нет. Это тот же
сквозной кейс, который разбирают слайды семинара «Сборка кодинг-агента», а не похожий пример.

История репозитория собрана как **лестница из семи шагов** — семь ступеней семинара: файл
инструкций → память → хук → скилл → MCP → субагент → процесс. Каждый шаг добавляет ровно один
блок и только после того, как сработал его триггер. Это и есть навык, который передаёт сборка:
спрашивать «сработал ли триггер», прежде чем добавлять блок.

**README на всю сборку один — этот.** Внутри `signup-landing/` своего `README.md` нет: точка
входа внутри проекта — `CLAUDE.md`, и это ровно то, зачем существует ступень 1.

Живого показа на семинаре нет: первая команда, которую студент реально запускает, — та, что он
набирает уже у себя, после клонирования. Поэтому у каждой ступени ниже есть блок **«Проверка»**:
точная команда и то, что должно появиться на экране. Вывод в этих блоках снят с настоящего
прогона, а не написан по памяти.

## Как начать

```bash
git clone <URL этого репозитория>
cd templates/base-project-worked-example/signup-landing
npm ci
npx playwright install chromium   # одна загрузка на машину, ~650 МиБ
```

Второй командой не пренебрегать — см. «Ступень 1» ниже, почему она попала в `CLAUDE.md`.

---

## Ступень 1 — файл инструкций

**Триггер.** Агент во второй сессии подряд переспрашивает, какой командой собрать сайт и какой
командой прогнать тест формы.

Та же ступень на несущей оси семинара, общей формулировкой: *агент каждый раз переспрашивает
одно и то же* → добавляем *файл инструкций*. **Критерий «ещё рано»:** агент и так справляется;
документации хватает.

**Что добавлено.**

- `signup-landing/CLAUDE.md` — заполненный файл инструкций по скелету
  `templates/base-project-template/with-git/CLAUDE.md`. 69 строк: чем этот проект является,
  одна строка границ («никогда не запускать деплой на прод без явного запроса» — она
  понадобится на ступени 4), команды сборки/тестов/запуска и то, чем проверяют, что правка
  действительно работает, а не просто компилируется; договорённости, которые нельзя угадать из
  дефолтов фреймворка.
- `signup-landing/AGENTS.md` — **символическая ссылка** на `CLAUDE.md`, не копия. Один
  канонический текст читают и Claude Code, и движки, которые ищут `AGENTS.md`. Копия начала бы
  разъезжаться с оригиналом в первый же день. В репозитории она записана как настоящий симлинк
  (`git ls-files -s` показывает режим `120000`, у обычного файла было бы `100644`).

**Чего на этой ступени сознательно нет.** Ни `DECISIONS.md`, ни `.claude/`, ни `.mcp.json`, ни
`Tasks/` — их триггеры ещё не сработали. Они появятся на ступенях 2–7, каждый своим шагом.

**Одна строка, которой нет в плане семинара, и почему она всё равно есть.** В `Build, test,
verify` добавлен разовый шаг `npx playwright install chromium`. Свежий клон без него падает не
по делу: все 4 теста разом, за миллисекунды, с
`browserType.launch: Executable doesn't exist at .../chrome-headless-shell`. Живого показа на
занятии нет, значит `npx playwright test` — вообще первая команда, которую студент запускает
сам; получить на ней инфраструктурную ошибку вместо зелёных тестов — худшее первое знакомство
со сборкой. Ровно такие вещи и есть содержимое файла инструкций: то, что агент не угадает из
дефолтов, и то, обо что спотыкаются один раз каждый.

**Провал в этом шаге.** Файл инструкций — не механическая гарантия. GitHub issue
[`anthropics/claude-code#42863`](https://github.com/anthropics/claude-code/issues/42863)
(открыт 2026-04-03, закрыт 2026-05-18 как «not planned»): в `CLAUDE.md` стояло правило
*«Every access to files outside D:\ClaudeCode must be explicitly confirmed by the user before
execution»* — агент запустил `msiexec /i` (запись в `C:\Program Files`, регистрация службы
Windows, правка реестра), ничего не спросив; пользователю пришлось прерывать вручную. Вторая
попытка того же автора: новый экземпляр агента принял короткое «Mach das» за разрешение, хотя
файл прямо объявлял, что правило приоритетнее указаний пользователя.

Причина не в конкретной модели: `CLAUDE.md` — это **контекст, а не принудительная
конфигурация**. Его содержимое можно проигнорировать; действие независимо от решения модели
блокирует только хук. Отсюда — последняя строка самого `CLAUDE.md`: правило, записанное как
обязательное, но ничем механически не проверяемое, тихо разлагается. Это и есть триггер
ступени 3.

**Проверка.**

```bash
cd templates/base-project-worked-example/signup-landing
wc -l CLAUDE.md        # заметно меньше 200 строк
ls -la AGENTS.md       # символическая ссылка на CLAUDE.md, не копия
```

Что печатает на самом деле (настоящий прогон; владелец, дата и размер у вас будут свои — важны
`69` и `lrwxrwxrwx ... -> CLAUDE.md`):

```
$ wc -l CLAUDE.md
69 CLAUDE.md

$ ls -la AGENTS.md
lrwxrwxrwx 1 harness harness 9 Sep 20 12:57 AGENTS.md -> CLAUDE.md
```

Первая буква `l` и стрелка `-> CLAUDE.md` — это и есть проверяемое: у копии было бы `-rw-r--r--`
и никакой стрелки.

Третья проверка — та, ради которой ступень существует. Откройте **новую** сессию агента в
клонированном `signup-landing/` и спросите, как собрать сайт и проверить форму. Ответ должен
прийти из `CLAUDE.md`, без встречного вопроса. Настоящий прогон в чистой копии проекта
(`claude -p "Как собрать сайт и как прогнать тест формы?"`), сокращённо:

```
Согласно `CLAUDE.md` проекта:

## Сборка сайта
npm run build

Собранное — в `dist/index.html` (его открывают вручную, чтобы проверить форму на
заполненных и пустых полях).

## Прогон тестов формы
npx playwright test

## Один раз после клонирования — до первого запуска тестов
npm ci                            # поставить зависимости
npx playwright install chromium   # скачать браузер (~650 МиБ в ~/.cache/ms-playwright/)
```

Ни одного встречного вопроса «какой командой собирать?» — агент сослался на `CLAUDE.md` и
перечислил обе команды, включая разовую установку браузера. До этой ступени тот же вопрос
задавался каждую сессию заново.

---

## Ступень 2 — память + журнал решений

**Триггер.** Агент второй раз за неделю предлагает подключить стороннюю библиотеку валидации
форм — то самое решение, что уже было отклонено в прошлой сессии.

Та же ступень на несущей оси семинара, общей формулировкой: *владелец повторяет одно и то же из
сессии в сессию* → добавляем *память + журнал решений*. **Критерий «ещё рано»:** одна-две
сессии; факт уже записан в коде.

Обратите внимание, чем ступень 2 отличается от ступени 1. Там агент переспрашивал **факт**
(«какой командой собирать?») — и факт лёг в `CLAUDE.md`. Здесь агент переспрашивает **решение**
(«давайте возьмём библиотеку») — а решение без причины, по которой его отклонили, не держится:
повтори его через неделю, и оно снова выглядит разумным. Поэтому в журнал пишется не «библиотеку
не берём», а почему именно не берём.

**Что добавлено.**

- `signup-landing/DECISIONS.md` — append-only журнал **почему**, по формату
  `templates/base-project-template/with-git/DECISIONS.md`. Шесть записей, все настоящие:
  каждая описывает решение, реально принятое при сборке этого проекта, и у каждой названа
  отвергнутая альтернатива. Без отвергнутой альтернативы запись — не решение, а пересказ кода;
  это единственный критерий, по которому запись сюда попадает.
- Одна строка в `CLAUDE.md` — раздел `Where things live` с указателем на `DECISIONS.md`.
  На ступени 1 этот раздел был удалён из скелета целиком: все указатели в нём вели на файлы,
  которых ещё не существовало. Цена того решения — каждая следующая ступень обязана добавить
  свой указатель в тот момент, когда её файл появляется. Эта ступень платит первой.

**Чего на этой ступени сознательно нет.**

- `LESSONS.md`. В дереве файлов семинара он помечен «опционально», и § 8.2 его не требует.
  `LESSONS.md` — это *продвинутое* подмножество: правило, выведенное из нескольких записей
  журнала и подтверждённое не один раз. На шести записях одного дня продвигать нечего, а пустой
  `LESSONS.md` с невыполняемой строкой «промоутить раз в спринт» — ровно та незаполненная
  заглушка, от которой предостерегает сам скелет шаблона. Файл появится, когда появится что
  промоутить.
- Записи авто-памяти. Они лежат **вне** репозитория (см. ниже) и в дерево сборки не коммитятся.

### Два слоя памяти, и почему они не заменяют друг друга

| | `DECISIONS.md` | авто-память рантайма |
|---|---|---|
| Где лежит | в репозитории, под git | `~/.claude/projects/<project>/memory/`, вне репозитория |
| Кто пишет | человек, руками | агент, по ходу разговора |
| Кто видит | все, кто клонировал | только вы, только на этой машине |
| Что хранит | решение + отвергнутая альтернатива | факт, который пригодится в следующей сессии |
| Переживает | всё | переустановку/смену машины — нет |

Быстрый слой (авто-память) дешёв и бесплатен, но приватен и непереносим. Медленный
(`DECISIONS.md`) требует усилия, зато это единственное, что увидит второй разработчик, вы через
полгода и сам агент в чистом клоне. Ступень 2 ставит **оба**, потому что каждый из них по
отдельности даёт половину ответа.

### Авто-память: как воспроизвести у себя

В сессии агента, открытой в клонированном `signup-landing/`, скажите обычным текстом:

```
запомни, что мы не подключаем библиотеку валидации форм
```

Настоящий прогон (`claude -p "запомни, что мы не подключаем библиотеку валидации форм"` в свежей
копии проекта) — ответ агента:

```
Запомнил: в `signup-landing` мы не подключаем библиотеку валидации форм. Валидация остаётся
нативной — правила в атрибутах `index.html` (`required`/`pattern`/`type="email"`), читаются
через Constraint Validation API в `src/validate.js`. Новое правило — в разметку, не сторонней
зависимостью.
```

И что после этого появилось на диске — два файла, оба **вне** репозитория:

```
$ ls ~/.claude/projects/-tmp-rung2-fresh-signup-landing/memory/
MEMORY.md
no-form-validation-library.md

$ cat ~/.claude/projects/-tmp-rung2-fresh-signup-landing/memory/MEMORY.md
- [No form validation library](no-form-validation-library.md) — signup-landing validates
  natively (HTML attrs + Constraint Validation API), never a third-party lib
```

`MEMORY.md` — индекс, который грузится каждую сессию; сам факт лежит отдельным файлом рядом и
подтягивается по релевантности. В `git status` после этого не появляется ничего: каталог
`~/.claude/projects/` лежит вне репозитория, git о нём не знает в принципе — его не нужно даже
вносить в `.gitignore`. Проверено на настоящем прогоне: `git status --porcelain` в дереве сборки
не содержит ни одного пути со словом `memory`.

**Про путь — это важно и это не ошибка.** `<project>` в
`~/.claude/projects/<project>/` Claude Code формирует **сам, из полного пути клонированного
репозитория**, заменяя `/` на `-`. В прогоне выше проект лежал в
`/tmp/rung2-fresh/signup-landing`, поэтому каталог называется
`-tmp-rung2-fresh-signup-landing`. Если вы клонировали в `~/code/signup-landing`, вы увидите
`-home-<вы>-code-signup-landing`. **Имени `signup-landing` в чистом виде там не будет ни у кого**
— ожидаемо, а не сломано.

**Провал в этом шаге.** Память — не безопасное хранилище, а доверенный контекст. **SpAIware**
(ChatGPT для macOS, исследователь Johann Rehberger, публикация
[thehackernews.com, 25 сентября 2024](https://thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html)):
непрямая инъекция — вредоносный текст на странице или в документе, который агент просто
**прочитал**, — записывала инструкцию в долговременную память ChatGPT. Дословно из разбора
техники: инъекция достигает «формы персистентности, которая переживает разговор» (*a form of
persistence that survives between conversations*), и дальше «все новые разговоры будут содержать
инструкции атакующего и непрерывно отправлять ему все сообщения переписки и ответы». Пользователь
при этом не делал ничего, кроме как открыл страницу. OpenAI закрыл конкретный вектор
эксфильтрации в версии ChatGPT `1.2024.247` (сентябрь 2024).

Починили вектор — не принцип. Принцип остаётся структурным свойством любой файловой или
векторной памяти без проверки происхождения записи: **однажды попавшее в память обслуживается
как доверенный контекст бессрочно** (разбор — `02-memory.md`, §4.2 курса, где SpAIware стоит
первым в списке задокументированных атак отравления памяти вместе с MINJA, PoisonedRAG,
MemoryGraft и EchoLeak). Отсюда практический вывод ровно для этой ступени, и он же — совет
самого Rehberger'а: **периодически перечитывайте, что у вас в `memory/`**. Это обычные файлы,
`cat` и `rm` работают. И это вторая причина, по которой решения проекта живут в
`DECISIONS.md` под git: запись в журнале видна в diff'е и проходит ревью, запись в авто-памяти
не видна никому.

**Проверка.**

```bash
cd templates/base-project-worked-example/signup-landing
cat DECISIONS.md        # видна запись про библиотеку валидации
ls ~/.claude/projects/*/memory/
```

Первая команда печатает файл целиком; вот его начало (настоящий прогон):

```
$ cat DECISIONS.md
# Decisions

Журнал **почему**, в порядке дат, только дописывается. Что именно изменилось — уже знает
`git log`; сюда попадает то, что иначе осталось бы в голове или в закрытом разговоре. Запись
имеет смысл, только если у решения была отвергнутая альтернатива: без неё это не решение, а
описание кода.
...
## 2026-09-20 — не подключаем библиотеку валидации форм

Форма — два поля (имя, email): хватает нативных `required` / `pattern` / `type="email"` в
разметке плюс `src/validate.js` на 24 строки (14 из них — код), который читает те же атрибуты
через Constraint Validation API. Сторонняя библиотека — лишняя зависимость и лишние килобайты
ради объёма, который сегодня целиком укладывается в 1.57 кБ собранного JS на всю страницу.
```

Вторая — **вывод у вас будет другой, и это тот самый случай, ради которого написано примечание
про путь выше**. `ls` с глобом `*` печатает по блоку на каждый проект, который вы когда-либо
открывали в Claude Code. На машине, где собиралась эта ступень, глоб совпал с десятью проектами;
вот последние два блока настоящего прогона:

```
$ ls ~/.claude/projects/*/memory/
...
/home/.../.claude/projects/-tmp-rung1-fresh-signup-landing/memory/:

/home/.../.claude/projects/-tmp-rung2-fresh-signup-landing/memory/:
MEMORY.md
no-form-validation-library.md
```

Что здесь ваше, а что машинное:

- **Число блоков** — у вас столько, сколько проектов вы открывали; на чистой машине один.
- **Имена каталогов** — ваш путь клонирования, преобразованный (`/` → `-`). Совпадения с
  примером выше не будет и не должно быть.
- **Начало пути** — здесь `~` раскрылся в служебный каталог стенда, поэтому в выводе он
  сокращён до `/home/.../`. У вас будет обычный `/home/<вы>` или `/Users/<вы>`.
- **Содержимое блока** — вот это и есть проверяемое: `MEMORY.md` плюс файл с фактом. Пустой
  блок (как у `-tmp-rung1-fresh-...` выше) — нормальный результат для проекта, в котором ни
  разу ничего не просили запомнить: каталог создаётся при первой же сессии, а наполняется
  только по команде «запомни».

Если каталога `memory/` нет вовсе — авто-память в вашей версии CLI отключена или не
поддерживается; `DECISIONS.md` от этого работает ровно так же, и половина ступени у вас всё
равно стоит.

> **Про `wc -l CLAUDE.md` из ступени 1.** Эта ступень добавила в `CLAUDE.md` строку-указатель,
> поэтому на текущем HEAD команда печатает `74`, а не `69`, как записано в блоке «Проверка»
> ступени 1. Ступень 1 своё число измерила честно — оно просто устарело на один шаг лестницы.
> Проверяемое там утверждение («заметно меньше 200 строк») продолжает выполняться. Именно этот
> класс расхождений и должен ловить механизм анти-дрейфа из ступени README-лестницы.

---

## Ступень 3 — хук

**Триггер.** Накануне показа сайта заказчику агент коммитит правку формы прямо в `main`, хотя
`CLAUDE.md` текстом запрещает это.

Та же ступень на несущей оси семинара, общей формулировкой: *правило записано, но агент его
нарушает* → добавляем *хук*. **Критерий «ещё рано»:** правило дешевле проверить в сборке;
нарушение стоит дёшево.

Почему записанного правила оказалось мало, разобрано ступенью 1 — этот триггер там назван
заранее, последней строкой самого `CLAUDE.md`. Ступень 3 — обещанная там проверка.

**Что добавлено.**

- `signup-landing/.claude/settings.json` — **два** хука в одном массиве `PreToolUse`, оба под
  матчером `Bash`.
  - `[0]` **защита ветки**: `git commit` на `main`/`master` → `deny`. Скопирован целиком из
    `templates/base-project-template/with-git/.claude/settings.json`, вместе с его `$comment`,
    байт в байт. Это не вежливость к шаблону: сборка обязана показывать *шаблонный* хук, иначе
    она показывает чью-то личную правку, а расхождение с шаблоном становится нечитаемым.
  - `[1]` **защита от `rm -rf`**: `rm -rf`, цель которого **раскрывает шелл** (`*`, `?`, `~`,
    `$VAR`), а не называете вы, → `deny`. `rm -rf dist` разрешён и должен быть разрешён;
    `rm -rf dist/*`, `rm -rf $DIR` и `rm -rf ~/` — нет.
- `signup-landing/.claude/hooks/selftest-branch-guard.sh` — самотест, покрывающий **оба** хука.
  Один файл с двумя блоками проверок, а не два файла: второй скрипт — это второй скрипт, про
  который надо помнить, и именно тот, который никто не запускает, протухает первым.

**Чего на этой ступени сознательно нет.** Хука на `Stop`/`SessionStart` и вообще любого, который
что-то *делает* (форматирует, дописывает, коммитит). Триггер сработал ровно один: правило
нарушено. Хук, добавленный «заодно», — это команда, которую вы согласились выполнять на каждом
ходу не читая.

### Почему к хуку сразу прилагается самотест

Характерный отказ хука — **тишина, а не ошибка**. Из официальной документации
([code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks), раздел Timeouts,
загружено 2026-09-20), дословно: *«A timed-out `command`, `http`, or `mcp_tool` hook doesn't
block the tool call. The call continues through the normal permission flow, so don't count on a
stalled hook to act as a gate.»* То же самое, если не установлен `jq`, через который хук
пропускает вход: он падает и пропускает команду дальше. Второй слой того же —
*[не подтверждено — со ссылкой на сторонний разбор issue-трекера, а не на официальную справку по
хукам, которую мы проверили: этого утверждения там нет]* один схемно-невалидный матчер в
`settings.json` отключает **все** хуки этого файла, не показав ошибки.

Во всех этих случаях несработавший хук выглядит **точно так же**, как сработавший и
пропустивший. Отсюда правило ступени: *наличие файла — не доказательство, что ворота стоят;
доказательство — увидеть, как они закрываются.*

### Три способа, которыми эти ворота не срабатывают

Они здесь не как дисклеймер и не как признание, что шаблон сломан. Это **граница** рабочего
инструмента, названная вслух, — тот же регистр, в котором `scripts/safe-merge.sh` этого
репозитория пишет о самом себе. Хук ниже действительно закрывает обычный случай; ниже сказано,
где именно он заканчивается, чтобы вы не считали закрытым то, что открыто.

**1. Тест, который подтверждает, а не различает.** Предыдущая редакция этого самотеста выдавала
**7/7 PASS** на `settings.json`, хук которого **вообще не вызывал `git`** и отвечал из
`case "$PWD"`. Каждая фикстура называлась так же, как её ветка (`main-with-history` на `main`),
поэтому ветка ни разу не была независимой переменной. Формулировка автора, дословно, потому что
диагноз шире этого файла:

> «the suite was built to confirm the hook works, not to discriminate between hypotheses about
> why it works. Every case asked "does it deny here?"; none asked "could something else produce
> this same answer?"»

Лечится парой фикстур, у которых **имя противоречит ветке**, в обе стороны: репозиторий
`main-repo` на ветке `feature/x` (обязан **ПРОПУСТИТЬ**) и репозиторий `feature-work` на ветке
`main` (обязан **ЗАБЛОКИРОВАТЬ**). Обе в самотесте; ниже показан прогон, где подставной хук на
них и падает.

**2. Форма команды, а не намерение.** Регексп хука ищет слово `git` в начале инструкции, а
`read -r cmd` читает **только первую строку** входа. Отсюда, проверено на настоящем хуке:

| команда на `main` | что делает хук |
|---|---|
| `git commit -m x` | `deny` — срабатывает |
| `git -C . commit -m x` | **пропускает молча** |
| `/usr/bin/git commit -m x` | **пропускает молча** |
| `env git commit -m x` | **пропускает молча** |
| `git commit` второй строкой многострочной команды | **пропускает молча** |

Причины **две разные**, и их не надо смешивать. Первые три — регексп
`(^|[;&|]\s*)git\s+commit\b`: он требует `git` в начале инструкции, и любой префикс его прячет.
Четвёртая — **не** регексп, `grep` бы её поймал: хук устроен как `jq -r … | { read -r cmd; … }`,
и `read -r` обрезает вход до первой строки **до** того, как регексп что-либо увидит:

```
$ printf 'echo hi\ngit commit -m x' | { read -r cmd; echo "[$cmd]"; }
[echo hi]
```

Обратите внимание на `git -C .`: это **обычное повседневное употребление** — в самом самотесте
этой ступени оно встречается одиннадцать раз. Речь не про обход, а про то, что мимо ворот проходит
нормальная работа.

**3. `init.defaultBranch`.** На незарождённом `HEAD` (репозиторий создан, коммитов ещё нет) имя
ветки берётся из `init.defaultBranch`. У того, у кого это `trunk`, первый коммит не получит ни
`deny` (хук сравнивает только с `main` и `master`), ни `ask` (это **уже** репозиторий) — он
пройдёт молча. Не ошибка хука: граница проверки, устроенной по имени.

Все три ведут себя как ворота, которых нет, — и выглядят одинаково с воротами, которые
сработали и пропустили. Поэтому в самотесте они стоят отдельной категорией **`LIMIT`**, а не
среди `PASS`: пройденная проверка и не проводившаяся проверка не должны печататься одинаково.

**Почему это не чинится здесь.** Хук унаследован из шаблона. Вилка «исправленной» копии внутри
учебной сборки создаёт ровно то расхождение с шаблоном, которое ступень README-лестницы ловит
механически; правка принадлежит шаблону (issue #65) и придёт в сборку обычным путём. И это
содержание самой ступени: ворота с настоящим, воспроизводимым обходом, о котором сказано прямо,
учат тому, что несработавшие ворота неотличимы от сработавших. Тихо подложенные починенные
ворота учат, что ворота бывают полными.

### Четвёртый способ — и он не про хук, а про сборку

У `selftest-branch-guard.sh` должен быть выставлен бит исполнения (`100755` в индексе git).
Squash-merge или применение патча этот бит роняют молча. Уроните его — и скрипт **останется на
месте** и **продолжит работать** через `bash .claude/hooks/selftest-branch-guard.sh`. То есть
привычный способ запуска **полностью скрывает** потерю. Поэтому «Проверка» ниже вызывает скрипт
как `./.claude/hooks/…`: `bash script.sh` отрабатывает одинаково с битом и без него и поэтому не
может сказать вам, пережил ли бит дорогу до вашей машины.

**Провал в этом шаге.** Хуки — это исполняемый код, приезжающий вместе с репозиторием.
Check Point Research, «Caught in the Hook: RCE and API Token Exfiltration Through Claude Code
Project Files» ([публикация 25 февраля 2026](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)).
Исследователи положили в репозиторий `.claude/settings.json` с хуком на событии `SessionStart`
с матчером `startup`. Дословно: *«we clicked "Yes, proceed" on the prompt from when we first ran
Claude. Surprisingly, the Calculator app opened immediately, with no additional prompt or
execution warning»* — то есть диалог доверия был показан и принят, а вот **отдельного
подтверждения на выполнение команды хука не спросили**, хотя на обычную bash-команду в сессии
Claude Code спрашивает его всегда. И далее: *«there's no warning that hook commands defined in
.claude/settings.json will run automatically without confirmation… The session appears completely
normal while commands from the untrusted repository have already run in the background»*. Это
уязвимость **#1** в их разборе, закрытая Anthropic усиленным диалогом доверия; её идентификатор
— **GHSA-ph6w-f82w-28w6** (29 августа 2025).

Отсюда практический вывод ровно для этой ступени. `.claude/settings.json` — не метаданные,
а исполняемая конфигурация; в чужом PR её читают глазами, как читают код. Их же рекомендация:
*«Inspect configuration directories before opening projects»*. По той же причине самотест этой
ступени прямо предупреждает, что он **запускает** командную строку хука из `settings.json`,
и советует сначала эту строку прочитать, если файл не ваш.

Второй хук стоит здесь из-за другого разобранного случая: агента попросили «почистить пакеты в
старом репозитории», и он выполнил
([Docker, «Coding agent horror stories: the rm -rf incident»](https://www.docker.com/blog/coding-agent-horror-stories-the-rm-rf-incident/))
`rm -rf tests/ patches/ plan/ ~/`. Дословно о последствиях: *«It nuked my whole Mac! What the
hell?»* — Desktop, Documents, Downloads, `Library`, Keychain (после чего сам Claude Code потерял
доступ к своему бэкенду), годы проектов и семейных фотографий; восстановления не было:
*«SSDs with TRIM enabled … zero freed blocks at the controller level, so even forensic recovery
tools come up empty»*. Обратите внимание на саму команду: **никакой звёздочки в ней нет**, опасен
там `~/`. Поэтому хук `[1]` ловит не «звёздочку», а **любую цель, которую раскрывает шелл**, —
иначе он был бы воротами, названными в честь случая, который он бы пропустил. Эта самая команда
стоит в самотесте отдельной проверкой, дословно.

**Проверка.**

```bash
cd templates/base-project-worked-example/signup-landing
./.claude/hooks/selftest-branch-guard.sh
```

Настоящий прогон в свежем клоне (`/tmp`); у вас будут свои пути и свой временный каталог:

```
settings.json hook selftest — 2 hooks
  settings: /tmp/rung3-clone/templates/base-project-worked-example/signup-landing/.claude/settings.json
  hook [0]: branch-protection guard      (timeout 10s)
  hook [1]: `rm -rf` expansion guard     (timeout 10s)
            a hook that misses its timeout does NOT block — it is silently skipped
  scratch:  /tmp/branch-guard-selftest.CHLo5jHc

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  repo directory named 'main-repo', HEAD is feature/x — must ALLOW — hook stayed silent, as intended.
  PASS  repo directory named 'feature-work', HEAD is main — must DENY — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  LIMIT default branch named 'trunk' — commit is ALLOWED, neither denied nor asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.
  LIMIT `git -C <path> commit` on main — ALLOWED: the regex matches only 'git' and 'commit' as adjacent words
        This gate filters one command SHAPE, not intent. Do not rely on it to stop a determined or merely creative caller.
  LIMIT `/usr/bin/git commit` on main — ALLOWED: an absolute path is not the literal word 'git'
        Same root cause as above. A second, independent gate (a server-side branch protection rule) is the only thing that closes this class.
  LIMIT `env git commit` on main — ALLOWED: any prefix command hides the commit from the regex
        Same root cause. Treat the gate as a reminder that fires on the common shape, not as a boundary.
  LIMIT `git commit` on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line
        Multi-line Bash calls are routine. Keep a commit on the first line of its own call, or widen the hook to read all of stdin.
  PASS  rm -rf against a glob — permissionDecision=deny, reason text matches exactly.
  PASS  rm -rf tests/ patches/ plan/ ~/ (the reported incident, verbatim) — permissionDecision=deny, reason text matches exactly.
  PASS  rm -rf on a variable-built path — permissionDecision=deny, reason text matches exactly.
  PASS  rm -fr (flags reversed) against a glob — permissionDecision=deny, reason text matches exactly.
  PASS  rm -rf after '&&' — a statement start is a statement start — permissionDecision=deny, reason text matches exactly.
  PASS  rm -rf on a written-out path — allowed by design — hook stayed silent, as intended.
  PASS  plain rm on a glob (no -rf) — outside this gate's stated scope — hook stayed silent, as intended.
  PASS  ordinary non-rm command — hook stayed silent, as intended.
  LIMIT `/bin/rm -rf dist/*` — ALLOWED: an absolute path is not the literal word 'rm'
        Same root cause as the branch guard's case 12. These gates filter one command SHAPE, not intent.
  LIMIT rm -rf on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line
        Keep a destructive command on the first line of its own call, or widen both hooks to read all of stdin.
  LIMIT `rm -r -f dist/*` (flags split into two words) — ALLOWED: the regex wants one flag cluster
        One space is the whole difference. Widening the regex closes this one case; it does not change what the two above are telling you.

RESULT: PASS — 17/17 checks. Both gates were observed firing where this script checks them.
        8 KNOWN LIMIT(S) listed above: real cases where a gate is silent and protects
        nothing. Green here does not mean these gates cannot be walked past — read them.
Re-run after any Claude Code update or any edit to .claude/settings.json.
```

Читается так: **17 `PASS`** — ворота видели закрывающимися там, где скрипт их проверяет;
**8 `LIMIT`** — места, где ворот нет, перечисленные поимённо. `LIMIT` — не `PASS`; зелёный итог
означает «сработало там, где проверяли», а не «обойти нельзя».

**Прогон, в котором самотест падает.** Набор проверок, который никто не видел красным, — не
доказательство, а оформление. Три мутации, каждая на копии `settings.json` в `/tmp`, настоящий
файл сборки не трогается.

*Мутация 1 — подставной хук: не вызывает `git` вовсе, отвечает из `case "$PWD"`.* Именно на нём
предыдущая редакция самотеста показывала 7/7:

```
$ ./.claude/hooks/selftest-branch-guard.sh /tmp/rung3-mut/m1-pwd-cheat.json
…  (показаны только отличия: остальные 15 проверок подставной хук проходит)
  FAIL  repo directory named 'main-repo', HEAD is feature/x — must ALLOW — expected NO hook output (allow), got: {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED: direct commit to main/master. Create a feature branch first."}}
  FAIL  repo directory named 'feature-work', HEAD is main — must DENY — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
RESULT: FAIL — 2 of 17 checks failed. A gate in /tmp/rung3-mut/m1-pwd-cheat.json is NOT doing what it claims.
(код возврата 1)
```

Падают ровно те две фикстуры, у которых имя противоречит ветке, — и ни одна другая. Это и есть
то, ради чего они добавлены.

*Мутация 2 — второй хук удалён из массива.* Извлечение хуков идёт по позиции, и отсутствие
второго — фатальная ошибка, а не пропущенный блок:

```
$ ./.claude/hooks/selftest-branch-guard.sh /tmp/rung3-mut/m2-second-hook-deleted.json

FATAL: found only ONE command hook in the "Bash" group of /tmp/rung3-mut/m2-second-hook-deleted.json; this
       project ships two, and the second (the rm -rf expansion guard) is missing. This is FATAL
       rather than a skipped block on purpose: a suite that quietly tests the hooks it can find
       and prints PASS is worse than no suite, because it certifies the half that is gone.
(код возврата 2)
```

*Мутация 3 — цель `rm -rf` сужена обратно до глобов (`~` и `$` убраны).* Падает ровно проверка с
командой из разобранного случая:

```
$ ./.claude/hooks/selftest-branch-guard.sh /tmp/rung3-mut/m3-globs-only.json
…  (показаны только отличия)
  FAIL  rm -rf tests/ patches/ plan/ ~/ (the reported incident, verbatim) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
RESULT: FAIL — 1 of 17 checks failed. A gate in /tmp/rung3-mut/m3-globs-only.json is NOT doing what it claims.
(код возврата 1)
```

**Проверка бита исполнения.** Уроните бит в копии и сравните два способа запуска:

```
$ ls -l .claude/hooks/selftest-branch-guard.sh   # бит уронен
-rw-r--r-- .claude/hooks/selftest-branch-guard.sh

$ ./.claude/hooks/selftest-branch-guard.sh
/bin/bash: line 58: ./.claude/hooks/selftest-branch-guard.sh: Permission denied
(код возврата 126)

$ bash .claude/hooks/selftest-branch-guard.sh
RESULT: PASS — 17/17 checks. Both gates were observed firing where this script checks them.
        8 KNOWN LIMIT(S) listed above: real cases where a gate is silent and protects
        nothing. Green here does not mean these gates cannot be walked past — read them.
Re-run after any Claude Code update or any edit to .claude/settings.json.
(код возврата 0)
```

Верхний — то, что вы хотите увидеть, если бит потерялся. Нижний — то, почему потерю можно не
заметить годами: привычная команда проходит зелёным. Свой бит проверяйте в индексе git, а не в
рабочем дереве, — клонируют именно индекс:

```
$ git ls-tree HEAD templates/base-project-worked-example/signup-landing/.claude/hooks/selftest-branch-guard.sh
100755 blob 9e3d8d0bbb550e2a5100355accb70a648d2378f6	templates/base-project-worked-example/signup-landing/.claude/hooks/selftest-branch-guard.sh
```

Первое поле — `100755`. У потерявшего бит файла было бы `100644`.

---

## Ступень 4 — скилл

**Триггер.** Процедура деплоя (`wrangler pages deploy dist`) — рутина, которую агент выполняет
на каждой сессии, где нужен деплой; держать её в `CLAUDE.md` означает платить за неё контекстом
каждого запроса, даже когда деплой не нужен.

Та же ступень на несущей оси семинара, общей формулировкой: *файл инструкций облагает налогом
каждый запрос* → добавляем *скилл*. **Критерий «ещё рано»:** нужно каждой сессии → это не скилл.

Ступень 1 оставила здесь заготовку — единственную строку раздела `Safety / scope boundaries`:
«никогда не запускать деплой на прод без явного запроса». На ступени 1 это была просьба в
текстовой форме, ровно того же рода, что разобранное там же правило про `msiexec`. Ступень 4 не
переписывает её словами сильнее — она делает её полем во фронтматтере.

**Что добавлено.**

- `signup-landing/.claude/skills/deploy/SKILL.md` — вся процедура публикации: шаг 0
  (предполётная проверка), шаг 1 (`npm run build && wrangler pages deploy dist`), шаг 2 (сверка
  с продакшен-URL), «Узкая область» и `disable-model-invocation: true`. Формат — тот же, что у
  `templates/base-project-template/common/.claude/skills/_example/SKILL.md` (наряд 3, влит в
  `main`): `description` написан как поисковый запрос будущего себя, а не как категория.
- Одна строка в `CLAUDE.md`, в разделе `Where things live` — указатель на скилл. Ту же цену
  платила ступень 2 и по той же причине: раздел указателей заполняется по мере появления файлов.

**Чего на этой ступени сознательно нет.** Второго скилла. Ни `/test`, ни `/new-field`, ни
«ещё пары очевидно полезных» — триггер сработал ровно один раз и ровно на деплое. Почему это не
осторожность, а прямой вывод из измерений — в «Провале» ниже. Нет и вложенных файлов уровня 3
(`REFERENCE.md`, `scripts/`): вся процедура — полторы команды, разносить её по файлам значит
изобретать структуру под объём, которого нет.

### Триггер этой ступени — арифметика, а не принцип

Остальные ступени этой сборки показывают триггер на случае. Этот можно посчитать, и считать его
надо на своём файле, а не верить формулировке.

`CLAUDE.md` этого проекта объявляет собственный потолок: **800 слов** (раздел
`Operating budgets`). До этой ступени в нём было **551 слово** — это и есть состояние файла в тот
момент, когда выбор «вписать или вынести» ещё стоял. Процедурное ядро скилла — шаги 0–2 и «Узкая
область», то есть ровно то, что пришлось бы вписать, если бы скилла не было, — **324 слова**:

```
$ python3 -c "s=open('.claude/skills/deploy/SKILL.md').read(); \
    print(len(s[s.index('## 0.'):s.index('## Почему')].split()))"
324
```

`551 + 324 = 875`. Потолок — **800**. **Процедура в файл инструкций физически не влезает** — и
это ещё до указателя, который всё равно придётся добавить. Никакого выбора здесь нет: вписать
нельзя, можно только вынести или сократить что-то другое, чего сокращать не за что.

Чем ступень закончилась по факту — указателем на четыре строки вместо процедуры на пятьдесят:

```
$ wc -w CLAUDE.md
600 CLAUDE.md
```

600 из 800, запас — 200 слов. Он остался именно потому, что в файл уехал указатель, а не шаги.

Что стоит скилл вместо этого. Официальная таблица послойного раскрытия
([`platform.claude.com/docs/en/agents-and-tools/agent-skills/overview`](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview),
загружено 2026-09-20): уровень 1 (`name` + `description`) — *«\~100 tokens per Skill»*, всегда,
при старте сессии; уровень 2 (тело `SKILL.md`) — *«Under 5k tokens»*, только при срабатывании. Но у этого скилла стоит
`disable-model-invocation: true`, а с ним, по той же официальной справке, `description`
**в контекст не попадает вовсе** — то есть уровень 1 здесь равен **нулю**, пока не набран
`/deploy`. Это не выкладка на бумаге, это проверено прогоном ниже.

Оговорка, чтобы числа читались честно: 551 и 324 — **слова**, посчитанные локально; ≈100 и
<5000 — **токены** из официальной таблицы. Мы их не пересчитывали друг в друга: токенизатора под
рукой нет, а на русском тексте коэффициент «слово → токен» заметно хуже, чем на английском.
Сравнивать здесь надо не 324 слова с 100 токенами, а два режима оплаты: «каждый запрос» против
«только когда набрали `/deploy`».

### Почему модель не может вызвать этот скилл сама — и как это проверено

`disable-model-invocation: true` — то, чем эта ступень заменяет просьбу из `CLAUDE.md`.
Официальная справка ([`code.claude.com/docs/en/skills`](https://code.claude.com/docs/en/skills),
раздел «Control who invokes a skill», загружено 2026-09-20) называет `/deploy` примером ровно
для этого поля, дословно: *«Use this for workflows with side effects or that you want to control
timing, like `/commit`, `/deploy`, or `/send-slack-message`. You don't want Claude deciding to
deploy because your code looks ready»* — и далее: *«If Claude tries anyway, Claude Code blocks
the call and instructs it not to reproduce the deploy steps another way…»*.

Наличие поля в файле — не доказательство, что оно работает: это тот же урок, которым ступень 3
оправдывает свой самотест. Поэтому — прогон, **различающий** две гипотезы, а не подтверждающий
одну. Две копии сборки, отличающиеся ровно одной строкой, один и тот же вопрос, все инструменты
запрещены (чтобы агент не мог прочитать файл скилла и ответить по нему):

```
$ diff A/.claude/skills/deploy/SKILL.md B/.claude/skills/deploy/SKILL.md
9d8
< disable-model-invocation: true

$ cd A && claude -p "Ничего не читай и никаких инструментов не вызывай. Просто перечисли по
именам скиллы, доступные тебе в этой сессии в этом проекте." --disallowedTools Bash Read Grep …
Вот скиллы, доступные мне в этой сессии:
- **deep-research**
- **update-config**
…                       ← `deploy` в списке НЕТ

$ cd B && claude -p "<тот же вопрос>" --disallowedTools <те же>
Скиллы, доступные в этой сессии:
- **deploy**            ← появился, и первым
- **deep-research**
- **update-config**
…
```

Одна строка — и скилла для модели не существует: `description` действительно не попадает в
контекст, значит выбрать этот скилл по смыслу запроса она не может. Это и есть разница между
правилом, записанным словами, и механикой.

Прежде чем этому верить, стоит спросить то, что стоит спрашивать о любой зелёной проверке: **что
ещё могло бы дать тот же ответ?** `deploy` отсутствовал бы в списке прогона A и в случае, если
скилл вообще не загрузился — например, из-за сломанного фронтматтера. Эту гипотезу закрывает не
рассуждение, а прогон B: **та же копия**, минус одна строка — и скилл в списке есть, значит и
фронтматтер валиден, и каталог читается. Плюс прогон `/deploy` ниже: он выполнен на копии
**с** этим полем, и скилл в нём загрузился и отработал. Отсутствие в A остаётся объяснимым
только полем.

Цену надо назвать вслух, потому что она бьёт по главному уроку ступени. Хорошо написанный
`description` нужен затем, чтобы скилл находился **по смыслу запроса** — а здесь этот канал
закрыт намеренно. Значит `description` работает только на двух читателей: меню `/skills` и
человека, который через полгода ищет, чем публиковался сайт. Он всё равно обязан быть настоящим
триггером — но «скилл не подхватился» про него сказать уже нельзя, потому что он и не должен
подхватываться сам. Для скилла-знания (справочник, контекст legacy-системы) это поле было бы
ошибкой: там автовыбор и есть вся польза.

### Где эта процедура останавливается в клонируемой сборке — и почему это не замазано

У этой сборки нет и не будет аккаунта Cloudflare: требование «клонируется без единого ключа»
сильнее желания показать деплой живьём. Значит шаг 1 разделён надвое, и границу надо назвать
точно, а не сказать «деплой не проверяли».

**Первая половина выполняется по-настоящему.** `npm run build` собирает `dist/` — это настоящая
сборка настоящего проекта, и предполётная проверка шага 0 читает именно её результат. Ниже
настоящий прогон.

**Вторая половина не может выполниться, и причина — ровно ключи, а не опечатка.** Это тоже
проверяемо. `wrangler` в зависимостях проекта нет намеренно (`grep wrangler package.json` —
пусто): CLI деплоя в дереве зависимостей приглашает попробовать, а пробовать нечем. Голая
команда честно говорит, чего не хватает:

```
$ wrangler pages deploy dist
/bin/bash: line 1: wrangler: command not found
(код возврата 127)
```

Этого мало: «не установлен» и «установлен, но нечем авторизоваться» — разные утверждения, и
второе — то, которое мы утверждаем. Поэтому настоящий `wrangler` поставлен **вне** проекта
(`npm install --no-save wrangler` в отдельном каталоге `/tmp`, в сборку не попадает) и запущен на
том же настоящем `dist/`:

```
$ /tmp/…/node_modules/.bin/wrangler pages deploy dist

 ⛅️ wrangler 4.86.0
───────────────────

✘ [ERROR] In a non-interactive environment, it's necessary to set a CLOUDFLARE_API_TOKEN
environment variable for wrangler to work. Please go to
https://developers.cloudflare.com/fundamentals/api/get-started/create-token/ for instructions on
how to create an api token, and assign its value to CLOUDFLARE_API_TOKEN.

(код возврата 1)
```

Вот это и есть граница, названная там, где она проходит: настоящий `wrangler` 4.86.0, настоящая
команда, настоящий `dist/` — и остановка ровно на отсутствии `CLOUDFLARE_API_TOKEN`. Ни строчки
вывода деплоя, которого не было, в этом README нет и не будет: подделанный транскрипт
развёртывания учил бы студента, что «Deployment complete» в тексте означает работающий сайт, —
то же самое возражение, по которому ступень 5 отказывается от мок-сервера.

**Что при этом всё-таки исполняется целиком и с результатом** — шаг 0, и он не декоративный.
Он останавливает публикацию по настоящей причине этого проекта, а не из-за отсутствующих ключей:
`action` формы — заглушка `REPLACE_WITH_YOUR_FORM_ID`, она переживает сборку молча, и выложенная
с ней страница теряет каждую заявку. Прогон — в «Проверке» ниже.

**Одна ошибка, найденная этим прогоном, и она в скилле, а не в сборке.** Первая редакция шага 0
была написана цепочкой:

```bash
npm run build && grep -q 'REPLACE_WITH_YOUR_FORM_ID' dist/index.html \
  && echo 'STOP: …' && exit 1
```

На заглушке она честно останавливалась — и выглядела рабочей. Прогон на копии, где endpoint
подставлен, показал, что она возвращает `1` **и в этом случае тоже**: последним в цепочке
оказывается неуспешный `grep`, так что шаг 0 не пропускает дальше **никогда**. Проверка, которую
смотрели только на случае «должна сработать», не отличала «остановись» от «иди дальше» — тот же
диагноз, что у предыдущей редакции самотеста ступени 3, слово в слово. В файле теперь `if`, и
оба случая различаются кодом возврата (`1` и `0`) — прогон обоих в «Проверке».

**Провал в этом шаге.** Он двойной, и эти два провала — противоположные. Не смешивать их —
и есть содержание этого шага.

**(1) Скилл не подхватывается: `description` написан для человека, а не как триггер.**
Официальный чек-лист авторства скиллов
([`…/agent-skills/best-practices`](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices),
загружено 2026-09-20) прямо перечисляет под заголовком *«Avoid vague descriptions like these»*
ровно три: `description: Helps with documents`, `description: Processes data`,
`description: Does stuff with files` — и требует *«Always write in third person»*, потому что
описание вклеивается в системный промпт и модель выбирает скилл именно по этому полю, среди
потенциально 100+ установленных. Измерено на самом курсе, из которого
эта сборка вышла (`07-skills.md`, §4.1): из **13 скиллов курса фронтматтер есть у одного** —
`pre-user-gate`. У остальных двенадцати первая строка файла — заголовок `# build-deck`, и в
списке доступных они видны как `build-deck: build-deck`, `sync-library: sync-library`: подставлено
имя вместо описания. Такой скилл не может сработать по смыслу запроса вообще — только явным
`/slash`.

**(2) Скилл подхватывается и вредит.** Эмпирическое исследование skill-induced failures
(«Agent Skills Can Be Harmful: An Empirical Study of Skill-Induced Failures in LLM Agents»,
[arXiv:2608.11888](https://arxiv.org/abs/2608.11888), препринт 12.08.2026, бенчмарки SkillsBench
и SWE-Skills-Bench) приписало конкретным скиллам **307 подтверждённых сбоев**: 125
функциональных и 182 эффективностных. Разбивка функциональных: Task-Implementation Fault —
**86 из 125 (68,8%)**, Artifact Misplacement — 24 (19,2%), Environment Mismatch — 13 (10,4%),
Applicability Mismatch — 2 (1,6%). Главная находка, дословно из абстракта: *«Skill-induced
functional failures are rarely caused by obviously irrelevant skills; instead, seemingly relevant
skills often make the agent incorrectly implement or omit task-required implementation
elements»*. Плюс до **+451%** токенов на задачу и падение pass rate на 16 из 84 задач SkillsBench.

Отсюда — «чего на этой ступени сознательно нет»: второй скилл, добавленный «заодно», это не
нейтральный файл в каталоге, а измеренный риск того, что агент сделает задачу неправильно,
будучи уверенным, что следует инструкции.

> **Поправка к плану семинара, а не к источнику.** Наряд § 8.4 приписывает эти 307 случаев
> «скиллам без валидного `description`» и отправляет за разбором в §4.1. Проверено по самой
> работе (абстракт + полный текст, таблица III): ни то, ни другое не так. Категория, которая
> в работе действительно про метаданные, — Applicability Mismatch, дословно *«skill metadata
> gives an incomplete or misleading applicability signal»*, и это **2 случая из 125 (1,6%)**,
> а не 307; главная находка работы утверждает прямо противоположное — вред идёт от скиллов,
> которые выглядели **релевантными**. Разбор arXiv:2608.11888 в курсе лежит в **§4.2**, не в
> §4.1; §4.1 — это провал (1) выше, и его доказательство — собственный аудит 13 скиллов курса,
> а не эта работа. Оба провала настоящие, и оба здесь — но это два разных провала с разными
> источниками. Числа, которые наряд назвал (307 и 68,8%), сами по себе верны.

**Проверка.**

```bash
cd templates/base-project-worked-example/signup-landing
head -10 .claude/skills/deploy/SKILL.md   # фронтматтер виден целиком
```

Настоящий вывод — `---` на первой строке и закрывающий `---` на десятой, то есть в `head -10`
фронтматтер укладывается целиком:

```
$ head -10 .claude/skills/deploy/SKILL.md
---
name: deploy
description: >-
  Публикация signup-landing на прод Cloudflare Pages: `npm run build`, затем `wrangler pages
  deploy dist`, затем сверка страницы с продакшен-URL. Вызывать явно — `/deploy` — когда
  владелец попросил «выложи на прод», «задеплой», «опубликуй страницу». Не для локального
  просмотра (`npm run dev`), не для сборки без публикации (`npm run build`) и не для правки
  страницы перед публикацией — см. «Узкая область» ниже.
disable-model-invocation: true
---
```

Открывающий `---` **обязан** быть первой строкой файла: официальная справка читает фронтматтер
только в этом случае, иначе весь файл, вместе с `---`, считается телом скилла.

**`/skills` — проверить можно только в интерактивной сессии.** Меню `/skills` не работает в
режиме `-p`, и это не обход, а прямой ответ инструмента:

```
$ claude -p "/skills"
/skills isn't available in this environment.
(код возврата 0)
```

Отдельной команды-списка у CLI тоже нет: подкоманды `claude --help` — это `agents`, `auth`,
`auto-mode`, `doctor`, `gateway`, `install`, `mcp`, `plugin`, `project`, `setup-token`,
`ultrareview`, `update`, и скиллов среди них нет. Поэтому строку `deploy` с
осмысленным `description` в меню **смотрите у себя, в интерактивной сессии**: `claude` в
`signup-landing/`, затем `/skills`. Ниже — то, что проверяемо без интерактивного режима, и это
проверка сильнее: не «скилл виден в списке», а «скилл вызван и что-то сделал».

**Настоящий вызов `/deploy` через настоящий харнесс.** Свежая копия сборки (Claude Code 2.1.197,
`dist/` предварительно удалён, `Bash` разрешён, чтобы шаг 0 мог реально исполниться):

```
$ claude -p "/deploy" --allowedTools Bash
Deploy **stopped at the mandatory preflight (step 0)** — I did not publish anything.

## Что произошло
- `npm run build` прошёл успешно (`dist/` собран).
- Но проверка нашла в собранном `dist/index.html` заглушку `REPLACE_WITH_YOUR_FORM_ID` —
  `action` формы всё ещё указывает на неё, а не на реальный endpoint приёма заявок.

## Почему это блокирует публикацию
Страница с этой заглушкой выглядит полностью рабочей, но **молча теряет каждую заявку** — `vite`
не отличает заглушку от настоящего адреса, так что сборка предупреждения не даёт.

## Что нужно от вас
Этот скилл по своей узкой области **не подставляет endpoint за вас** — только не даёт выложить
заглушку. […] Публиковать я ничего не буду, пока шаг 0 не пройдёт чисто.
(код возврата 0)

$ ls dist/
assets  index.html
```

Читается так: `/deploy` разрешился в этот скилл (не «неизвестная команда»), тело загрузилось,
шаг 0 **исполнился** — `dist/` появился на диске, это проверяемый след, — предполётная проверка
сработала на настоящей заглушке, и агент остановился именно там, где скилл велит, включая
«Узкую область» («endpoint за вас не подставляю»). Заодно видно, что
`disable-model-invocation: true` не мешает явному вызову: он запрещает автозагрузку моделью, а
не команду `/deploy`.

**Прогон, в котором предполётная проверка обязана НЕ срабатывать.** Тот же шаг 0 на копии, где
заглушка заменена на настоящий по форме endpoint. Без этого прогона проверка неотличима от
`grep`, который всегда говорит «стоп»:

```
$ # A: сборка как есть, заглушка на месте — обязана остановить
$ npm run build && if grep -q 'REPLACE_WITH_YOUR_FORM_ID' dist/index.html; then
>   echo 'STOP: форма всё ещё указывает на заглушку endpoint — не публиковать'; exit 1
> fi
✓ built in 105ms
STOP: форма всё ещё указывает на заглушку endpoint — не публиковать
(код возврата 1)

$ # B: та же команда, endpoint подставлен (action="https://formspree.io/f/xyzabcde")
$ npm run build && if grep -q … ; then … fi
✓ built in 155ms
(код возврата 0)
```

`1` против `0` — проверка различает два случая, а не подтверждает один. Именно это отличие и
поймало ошибку в первой редакции шага 0, разобранную выше.

---

## Ступень 5 — MCP

**Триггер.** Агенту регулярно нужно смотреть открытые issue в GitHub-репозитории и готовить
черновики PR — не разово, а на каждой сессии.

Та же ступень на несущей оси семинара, общей формулировкой: *нужен доступ к внешней системе* →
добавляем *MCP*. **Критерий «ещё рано»:** хватает обычной команды.

Эта ступень — единственная в сборке, где живого блока **нет**, и это не пропуск. Разбор ниже
и есть содержание ступени.

### Открытое решение владельца, а не закрытый вопрос

Требование «сборка клонируется без единого ключа» и требование «показать MCP живьём»
противоречат друг другу напрямую: рабочее подключение GitHub MCP-сервера требует токена, а
токена в клонируемом репозитории быть не должно. Разрешить это противоречие — **решение
владельца, и оно на сегодня не принято**.

То, что вы видите ниже, — **действующее по умолчанию**, а не ответ: разбор текстом, пример
конфигурации без ключей, и никакого мок-сервера. Ровно так же это записано в `_comment` самого
`.mcp.json`, и ровно так же — в каталожной записи сборки
(`data/bundles/base-project-worked-example.yaml`, приезжает отдельной подзадачей 8.0, в истории
этой ступени её ещё нет): *«Work order § 8.5 is explicit that this is the EXECUTOR'S
RECOMMENDATION, not the owner's decision, and is to be reopened on review — so read this slot as
declined-pending-ruling, not settled»*. Если владелец решит иначе, меняется не формулировка, а
набор файлов — что именно, перечислено в «Что меняется, если владелец решит иначе» ниже.

Единственное, что здесь решено твёрдо и не зависит от исхода: **мок-сервера не будет ни при
каком решении**. Заглушка, выдающая себя за рабочее подключение, учила бы ровно тому, что этот
раздел опровергает, — что `✓ Connected` означает «работает». Насколько это не теоретическая
придирка, видно из «Провала» ниже: там `✓ Connected` держится ровно в тот момент, когда каждый
вызов падает с ошибкой авторизации.

### Что добавлено

- `signup-landing/.mcp.json` — **пример без рабочих credentials, помеченный как такой в самом
  файле**. Ни одного ключа; вместо значения — ссылка на переменную окружения.
- Этот раздел README.
- Одна строка в `CLAUDE.md`, в разделе `Where things live`, — указатель на `.mcp.json` и на то,
  что он не подключён.

**Чего на этой ступени сознательно нет.** Мок-сервера, заглушки, «демонстрационного» локального
процесса, отвечающего заранее записанным JSON, и скриншота панели `/mcp` с зелёной галочкой. Нет
и второго сервера «для полноты картины»: триггер не сработал ни разу даже на первом.

### Что было бы в `.mcp.json`, если бы сервер подключался

Claude Code хранит подключения на трёх уровнях. Официальная справка
([`code.claude.com/docs/en/mcp-quickstart`](https://code.claude.com/docs/en/mcp-quickstart),
загружено 2026-09-20) даёт их таблицей, и для сборки важна ровно средняя строка:

| Область | Файл | Кому видно |
|---|---|---|
| `local` (по умолчанию) | `~/.claude.json`, запись для этого проекта | только вам, только в этом проекте |
| `project` | **`.mcp.json` в корне проекта** | **всем, кто клонировал проект** |
| `user` | `~/.claude.json`, ключ верхнего уровня | только вам, во всех проектах |

Там же, дословно: *«Commit `.mcp.json` to version control. Teammates who clone the repository and
start Claude Code see a prompt to approve the server, then it connects for them too.»* Это и есть
причина, по которой ступень 5 вообще касается репозитория: `project`-область — единственная,
которая коммитится, то есть единственная, которую видит студент, клонировавший сборку.

Команда, которой этот файл создан (не написан руками):

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --scope project --header 'Authorization: Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}'
```

> **Поправка к плану семинара.** Наряд § 8.5 приводит эту команду как
> `claude mcp add github --scope project`. Так она не работает — у `claude mcp add` обязателен
> позиционный аргумент с командой или URL:
> ```
> $ claude mcp add github --scope project
> error: missing required argument 'commandOrUrl'
> ```
> Сигнатура (Claude Code 2.1.197, `claude mcp add --help`):
> `claude mcp add [options] <name> <commandOrUrl> [args...]`, флаг `-s, --scope` принимает
> `local`, `user` или `project`, по умолчанию `local`. Выше — работающая форма.

Что она пишет на диск (это и есть закоммиченный файл, без блока `_comment`):

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
      }
    }
  }
}
```

**`${GITHUB_PERSONAL_ACCESS_TOKEN}` — это не заполнитель «впишите сюда токен», а механика.**
Официальная справка ([`code.claude.com/docs/en/mcp`](https://code.claude.com/docs/en/mcp),
загружено 2026-09-20) описывает подстановку переменных окружения в `.mcp.json` дословно:
*«`${VAR}`: expands to the value of environment variable VAR»*, *«`${VAR:-default}`»*, и
раскрываются они в полях `command`, `args`, `env`, `url` и `headers`. Там же — поведение, на
котором держится вся честность этого файла: *«If a referenced environment variable isn't set and
has no default value, the config still loads: Claude Code reports a missing-variable warning for
that server in `claude mcp list` output and uses the unexpanded `${VAR}` text as-is.»* То есть
файл в репозитории остаётся валидным и без ключа, а инструмент сам говорит, чего не хватает — это
и видно в «Проверке» ниже.

### Сколько это стоит контекстом

Главный довод «когда MCP не нужен» — не безопасность, а цена: **определения инструментов сервера
занимают место в контексте каждого запроса**, а не один раз при подключении. Официальная
формулировка ([`code.claude.com/docs/en/mcp-quickstart`](https://code.claude.com/docs/en/mcp-quickstart),
загружено 2026-09-20): *«Each connected server takes some space in Claude's context window because
its tool names and server instructions load into every session.»*

| | `gh issue list` через `Bash` | GitHub MCP, `project`-область |
|---|---|---|
| **Постоянная цена, до всякой работы** | **0** — `Bash` в наборе инструментов и так, независимо от того, трогает ли проект GitHub | **59 553 символа** JSON определений (46 инструментов default-наборов) — *измерено здесь, см. ниже* |
| **То же при включённом Tool Search** | 0 | **745 символов** — только имена инструментов |
| **Опубликованные замеры, в токенах** | — | **~55 000 токенов** на типовую связку из 5 серверов, GitHub в их числе (Anthropic); **15 927 токенов** на 80 инструментов GitHub MCP (сторонний аудит, 19.03.2026) |
| **Цена одного обращения** | **3 439 байт** на 20 issue в форме, которую печатает `gh issue list`; **117 001 байт**, если не сокращать вывод | те же данные — но форму выбирает сервер, а не вы |
| **Кто решает, что попадёт в контекст** | вы, флагами (`--json`, `--jq`, `head`) | автор сервера |
| **Нужен ключ в клонируемом репозитории** | нет | да |

**Единицы в этой таблице намеренно не приведены к одной.** Символы и байты измерены здесь;
токены — чужие, из публикаций. Пересчитывать одно в другое было бы нечем: токенизатора в этой
работе не было, а коэффициент «символ → токен» различается и по языку, и по модели. Сравнивать
надо не «59 553» с «15 927», а два режима оплаты: **постоянная плата за каждый запрос** против
**платы только за фактический вызов**.

**Откуда 59 553 и 745 — это измерено, а не оценено.** Официальный сервер GitHub публикует
определения своих инструментов прямо в репозитории — `pkg/github/__toolsnaps__/*.snap`, по одному
JSON-объекту на инструмент (`name`, `description`, `inputSchema`, `annotations`), то есть ровно то,
что клиент получает в ответ на `tools/list`. Зафиксировано на коммите
`85598ba6e1256f7ebf4867b95d63b833c4549264` (16.09.2026), скачано и посчитано локально 20.09.2026:

```
файлов-снимков                        : 125
минифицированный JSON, всего          : 154 348 символов
  из них inputSchema                  : 105 983 (68,7%)

default-наборы (context, repos, issues,
pull_requests, users, copilot), 46 инстр.:  59 553 символа
  из них inputSchema                  :  37 883 (63,6%)
только имена инструментов             :     745 символов
```

Три оговорки, без которых эти числа читались бы сильнее, чем они есть. **Первая:** снимки — это
тестовые фикстуры репозитория, а не ответ живого `api.githubcopilot.com`; они пересобираются
вместе с инструментами, коммит зафиксирован, но утверждать, что сегодня сервер отдаёт байт в байт
это же, нельзя. **Вторая:** 125 снимков против 92 инструментов в разделе `## Tools` того же
README — разница в 33 файла это гранулярные варианты под feature-флагами, remote-only и
insiders-инструменты, которых нет ни в одной конфигурации по умолчанию; поэтому ведущее число
здесь — 46 инструментов default-наборов, а не 125. **Третья:** README сервера называет пять
default-наборов (context, repos, issues, pull_requests, users), а `pkg/github/tools.go` на том же
коммите помечает `Default: true` шестым ещё и `copilot`; взяты все шесть, то есть оценка скорее
завышена, чем занижена.

**Откуда токенные цифры — они чужие, и вот чьи.** Anthropic, справка по Tool Search
([`platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool),
загружено 2026-09-20), дословно: *«A typical multiserver setup (GitHub, Slack, Sentry, Grafana,
and Splunk) can consume ~55k tokens in definitions before Claude does any work. Tool search
typically reduces this by over 85 percent, loading only the 3–5 tools Claude needs for a given
request.»* GitHub в этой пятёрке назван первым — цифра относится к этому разделу напрямую. Там же
второй довод, не про деньги: *«Claude's ability to pick the right tool degrades once you exceed
30–50 available tools»* — то есть лишние инструменты не только дороги, они ещё и портят выбор.

15 927 токенов на 80 инструментов GitHub MCP — из стороннего аудита 11 серверов
([`dev.to/0coceo/i-audited-11-mcp-servers-22945-tokens-before-a-single-message-31e`](https://dev.to/0coceo/i-audited-11-mcp-servers-22945-tokens-before-a-single-message-31e),
опубликовано 19.03.2026, загружено 20.09.2026): суммарно 22 945 токенов на 137 инструментов, из
них GitHub — 69%, а самый дорогой его инструмент (`assign_copilot_to_issue`) — 810 токенов сам по
себе. **Это блог-пост, рекламирующий собственный инструмент автора, и его арифметика не сходится
сама с собой** (под таблицей напечатано «Average: 200 tokens per tool», хотя 22 945 / 137 = 167).
Поэтому цифра приводится как порядок величины с указанием источника, а не как измерение. Её «80
инструментов» тоже не совпадают с 92/125 выше — замеры разнесены на полгода на растущем сервере.

**Tool Search меняет постоянную цену, но не отменяет вопрос.** Он включён по умолчанию:
*«Tool search keeps MCP context usage low by deferring tool definitions until Claude needs them.
Only tool names and server instructions load at session start… Tool search is enabled by default»*
(`code.claude.com/docs/en/mcp`, загружено 2026-09-20). С ним постоянная плата падает с 59 553
символов до 745 — но не до нуля, отключается несколькими способами (`ENABLE_TOOL_SEARCH=false`,
прокси на не-первопартийный `ANTHROPIC_BASE_URL`, часть развёртываний), и ключ в репозитории всё
равно нужен. Экономия контекста — не ответ на вопрос «а нужен ли здесь сервер».

### Почему в этом примере обошлись без живого MCP

Контр-критерий ступени 5 — «хватает обычной команды» — применён к самой ступени 5, по тем же
условиям, по которым её и предлагается проверять.

**(а) Повторяемость — да, сработала.** Смотреть открытые issue действительно нужно каждой
сессии. Это единственное условие из всех, которое выполняется, и именно оно делает разбор
нужным, а не позволяет отмахнуться.

**(б) Число клиентов — один.** Сквозной кейс сборки объявлен соло-сценарием: один разработчик
с агентом, без команды. Экономия «написать интеграцию один раз на много клиентов» — главное, за
что платят MCP — здесь не окупается, потому что клиент один.

**(в) Задача сводится к известной CLI-команде.** `gh issue list` решает её целиком. `gh` — это
отдельная установка (в окружении, где готовился этот раздел, его нет, см. «Проверку» ниже), но
установка разовая и на машину, а не постоянно работающий процесс с доступом к секретам и
постоянной платой контекстом. Оборачивать известную команду в подключённый сервер — платить цену
из таблицы выше за то, что уже умеет `Bash`.

**(г) Форму ответа выбирает вызывающий.** Это не вкусовщина, а измеримая разница, и она в таблице:
один и тот же список из 20 issue — 117 001 байт сырого ответа API против 3 439 байт в той форме,
которую печатает `gh issue list`. Сокращает тот, кто вызывает. У MCP-инструмента форма ответа —
решение автора сервера.

**(д) И условие, которое перевешивает остальные: ключ.** Сборка объявлена клонируемой без единого
секрета. Живое подключение требует GitHub PAT. Это не «неудобно» — это прямо противоречит тому,
ради чего сборка существует.

Итог по критерию: сработал один пункт из пяти. **Обычной команды хватает.**

И то же самое — со стороны, которая обычно не звучит: у ступеней есть цена, а не только польза.
Подключить сервер «пока не мешает» — значит принять постоянную плату контекстом, ухудшение выбора
инструмента после 30–50 штук (цифра Anthropic выше) и полную схему «смертельного трио» из
«Провала» ниже. Ступень, добавленная без сработавшего триггера, — не нейтральный файл в каталоге.

### Что меняется, если владелец решит иначе

Решение открыто, поэтому вот конкретно, что придётся сделать при обратном решении — чтобы было
видно, что раздел обратим, а не защищает сам себя:

1. `.mcp.json` остаётся ровно таким, как есть, — он уже в рабочей форме; меняется только то, что
   у студента появляется своя переменная окружения.
2. В «Как начать» добавляется шаг: создать fine-grained PAT с доступом **только** к своему
   форку, `export GITHUB_PERSONAL_ACCESS_TOKEN=…`, и **не** записывать его в файл.
3. Появляется блок «Проверка» с живым подключением (`claude mcp list` → `✓ Connected`, `/mcp` со
   списком инструментов) — у студента, на его ключе, а не в этом репозитории.
4. «Провал» ниже не сокращается, а расширяется: при живом подключении он перестаёт быть
   предостережением и становится инструкцией по настройке прав.

Чего не произойдёт ни при каком решении — мок-сервера и снимка `✓ Connected`, снятого не с
работающего подключения.

### Провал в этом шаге

Их четыре, и они про разное: два — про архитектуру доступа, один — про доверие к согласию,
один — про доверие к слову «подключён».

**(1) Официальный GitHub MCP-сервер: эксфильтрация приватных репозиториев через публичный issue.**
Invariant Labs, 26.05.2025
([`invariantlabs.ai/blog/mcp-github-vulnerability`](https://invariantlabs.ai/blog/mcp-github-vulnerability),
загружено 2026-09-20), про «the widely-used GitHub MCP integration (14k stars on GitHub)».

Читать этот случай надо, держа в голове первую строку этого раздела. **Запрос, которым срабатывает
атака, — это дословно триггер этой ступени.** Из самой статьи: *«The actual attack triggers as
soon as the user and owner of the GitHub account queries their agent with a benign request, such
as `Have a look at the open issues in <user>/public-repo`»*. Агент читает открытые issue
публичного репозитория, в одном из них — спрятанная инструкция, и агент, у которого тем же
сервером открыт доступ и к приватным репозиториям, собирает оттуда данные и публикует их в
автоматически созданном PR в публичном репозитории. В демонстрации утекли, дословно,
*«information about their private repositories, such as Jupiter Star, their plan to relocate to
South America, and even their salary»*. Модель — Claude 4 Opus.

Две вещи, которые статья говорит прямо и которые обычно теряются при пересказе. Во-первых:
*«this is not a flaw in the GitHub MCP server code itself, but rather a fundamental architectural
issue that must be addressed at the agent system level. This means that GitHub alone cannot
resolve this vulnerability through server-side patches.»* Обновление сервера это не чинит. И
во-вторых: *«While our experiments focused on Claude Desktop, the vulnerability is not specific to
any particular agent or MCP client»* — не про конкретный клиент и не про конкретную модель.
(Рекомендации статьи — гранулярные права и постоянный мониторинг — сформулированы вокруг
собственных продуктов Invariant; принцип наименьших привилегий от этого не перестаёт быть верным,
но выдавать эти два пункта за вендор-нейтральный вывод нельзя.)

**(2) «Смертельное трио» — та же история, но как критерий.** Simon Willison, 16.06.2025
([`simonwillison.net/2025/Jun/16/the-lethal-trifecta`](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/),
загружено 2026-09-20). Это **не второй независимый инцидент**, а рамка, извлечённая из первого:
пост вышел на три недели позже и прямо на него ссылается — *«The recently discovered GitHub MCP
exploit provides an example where one MCP mixed all three patterns in a single tool.»* Считать их
двумя доводами значит посчитать одно событие дважды.

Три условия, дословно: *«Access to your private data»*, *«Exposure to untrusted content»*, *«The
ability to externally communicate in a way that could be used to steal your data»*. Все три
вместе — и «an attacker can easily trick it into accessing your private data and sending it to
that attacker», без единой строчки эксплойт-кода. Любые два из трёх — атака этого типа
невозможна.

Приложите это к триггеру ступени. «Смотреть открытые issue» — это (2): issue пишет кто угодно.
«Готовить черновики PR» — это (3): PR виден всем. А (1) приезжает не из формулировки триггера, а
из **токена**, которым обе эти операции только и возможны: PAT, которым агент читает issue и
открывает PR, одновременно даёт ему доступ ко всему, что этот PAT охватывает. **Сформулированный
в наряде триггер описывает полное трио** — не потому, что написан неосторожно, а потому, что это
и есть типичная работа с issue-трекером.

И часть, которую при пересказе выбрасывают чаще всего: *«Plenty of vendors will sell you
"guardrail" products… I am deeply suspicious of these: If you look closely they'll almost always
carry confident claims that they capture "95% of attacks" or similar... but in web application
security 95% is very much a failing grade.»* Вывод — *«The only way to stay safe there is to avoid
that lethal trifecta combination entirely»*: разрывать трио, а не фильтровать.

**(3) Обход согласия — CVE-2025-59536.** Пока речь шла о том, что делает *подключённый* сервер.
Этот провал — про сам файл в репозитории. Из записи NVD, дословно:

> *«Claude Code is an agentic coding tool. Versions before 1.0.111 were vulnerable to Code
> Injection due to a bug in the startup trust dialog implementation. Claude Code could be tricked
> to execute code contained in a project before the user accepted the startup trust dialog.
> Exploiting this requires a user to start Claude Code in an untrusted directory. … This issue is
> fixed in version 1.0.111.»*

CWE-94, опубликовано 03.10.2025, исправлено в 1.0.111; вендорская запись — `GHSA-4fgq-fpq9-mr3g`,
«Claude Code can execute commands prior to the startup trust dialog». Оценка в записи двойная, и
называть её надо со шкалой: **CVSS 4.0 — 8.7 (HIGH)** от CNA и **CVSS 3.1 — 8.8 (HIGH)** от NVD.

**Называть это «уязвимостью MCP» — ошибка, и мы её не делаем.** Ни NVD, ни GHSA не упоминают
`.mcp.json` вообще; формулировка шире — «code contained in a project». Это **обход согласия**.
Но именно поэтому он и попал в этот раздел, а не в соседний: `.mcp.json` — файл, всё содержимое
которого есть команда, её аргументы и её окружение, передаваемые харнессу на запуск. Это «code
contained in a project» в самом буквальном смысле, какой только бывает, и приезжает он вместе с
`git clone`, до того, как кто-либо его прочитал.

Точность, которой этот раздел обязан не пренебрегать: согласий у клонированного проекта **два** —
стартовый диалог доверия к папке (его и обходил CVE-2025-59536) и отдельное одобрение
project-серверов из `.mcp.json` (это `⏸ Pending approval` в «Проверке» ниже). CVE — про первый.
Утверждать, что он обходил второй, было бы враньём. Вывод, который из него следует и который от
этого различия не зависит: **ворота согласия перед закоммиченным файлом — механизм, и однажды он
уже оказался обходимым.** Тот же класс с другой стороны диалога — `GHSA-ph6w-f82w-28w6`, где
`SessionStart`-хук выполнялся без одобрения уже **после** принятия диалога; это другой
идентификатор и другой дефект, и путать их не надо (обе записи — в `Safety / scope boundaries`
шаблона `base-project-template`, вместе с третьей, `CVE-2026-21852`).

**(4) `✓ Connected` не значит «работает».** Это тот самый провал, из-за которого в сборке нет
мок-сервера. Случай из разбора курса (`05-mcp.md`, §4): у сервера `workspace-mcp` OAuth
refresh-токен автоматически отзывается каждые 7 дней, пока OAuth-приложение находится в статусе
Testing в Google Cloud Console; все вызовы падают с ошибкой авторизации — **а `claude mcp list`
всё это время продолжает показывать `✓ Connected`**. Там же, из того же разбора: сервер может
вернуть `success` на операцию, которой физически не произошло, и ни `claude mcp list`, ни панель
`/mcp` этого не покажут — это обнаруживается только проверкой фактического результата.

Отсюда прямо: мок-сервер в учебной сборке был бы **хуже отсутствия раздела**. Он выдал бы
единственный сигнал, ложность которого этот провал и доказывает, — и выдал бы его в материале,
по которому учатся.

### Проверка

**Команды с сетевым эффектом здесь нет — осознанно, раздел не подключается.** Наряд § 8.5
предлагает вместо неё `gh issue list` в клонированном `signup-landing/`. **Эта команда в данной
сборке не выполнялась: `gh` в окружении, где готовился раздел, не установлен.** Не «пропущена
как несущественная» — просто нечем:

```
$ gh issue list
/bin/bash: line 1: gh: command not found
(код возврата 127)
```

Вместо неё — две проверки, которые выполнить можно и которые показывают то, ради чего ступень
написана.

**Проверка 1. Закоммиченный `.mcp.json` — это не подключение.** Запускается в клонированной
сборке, ключа не требует:

```
$ cd templates/base-project-worked-example/signup-landing
$ claude mcp list
Checking MCP server health…

github: https://api.githubcopilot.com/mcp/ (HTTP) - ⏸ Pending approval (run `claude` to approve)

MCP config diagnostics ⚠

[Contains warnings] Project config (shared via .mcp.json)
Location: …/signup-landing/.mcp.json
 └ [Warning] [github] mcpServers.github: Missing environment variables: GITHUB_PERSONAL_ACCESS_TOKEN
```

Два независимых факта в одном выводе. **Сервер не подключён** — между файлом в репозитории и
работающим подключением стоит человеческое одобрение, которого никто не давал (`⏸ Pending
approval`); это тот самый второй ворот согласия из провала (3). И **ключа действительно нет** —
инструмент сам называет недостающую переменную по имени, не гадая.

Прежде чем этому верить, стоит спросить то же, что и на прошлой ступени: **что ещё могло бы дать
тот же ответ?** Главный конкурент — запись вообще не разобралась (сломанный JSON, не тот ключ,
не то место): «нет подключения» выглядело бы точно так же. Закрывает это не рассуждение, а вторая
команда на том же файле, которая показывает запись полностью разобранной:

```
$ claude mcp get github
github:
  Scope: Project config (shared via .mcp.json)
  Status: ⏸ Pending approval (run `claude` to approve)
  Type: http
  URL: https://api.githubcopilot.com/mcp/
  Headers:
    Authorization: Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}
```

Область прочитана, тип прочитан, URL прочитан, заголовок прочитан и показан **ссылкой на
переменную, а не значением**. Файл разобран — значит «не подключён» относится к подключению, а не
к синтаксису.

**Проверка 2. `_comment` в `.mcp.json` — терпимость, а не слепота валидатора.** Ключа `_comment`
в схеме `.mcp.json` нет, и Claude Code о нём ничего не говорит. У молчания два объяснения: ключ
допускается — или валидатор просто не смотрит внутрь настолько, чтобы что-то заметить. Различаем
мутацией, меняющей **ровно одно** (и это проверено `diff`, а не на глаз):

```
$ diff clean.json .mcp.json
18c18
<       "type": "http",
---
>       "type": "htp",

$ claude mcp list
 └ [Warning] [github] mcpServers.github: Skipped — unknown MCP server type "htp" for server "github"
```

Один символ — и валидатор нашёл ошибку, назвал поле и выбросил сервер из списка целиком (строка
`github: … Pending approval` исчезает). Значит файл он читает по ключам, и его молчание про
`_comment` — настоящая терпимость. Файл восстановлен, `diff` с исходным пуст.

**Что здесь проверить нельзя и почему.** Ни `✓ Connected`, ни список инструментов в панели
`/mcp`: для этого нужен настоящий GitHub PAT, которого в сборке нет и не будет, пока владелец не
решит иначе. Снимка «как бы подключённого» сервера в этом README нет и не появится — ровно по той
же причине, по которой ступень 4 не показывает вывод деплоя, которого не было.

## Ступень 6 — субагент

**Триггер.** Третий раз за неделю та же сессия, что писала код, перепроверяет сама себя перед
мержем — остаётся тем же контекстом рассуждений, тем же слепым пятном.

Та же ступень на несущей оси семинара, общей формулировкой: *повторяющаяся роль (ревью,
разведка)* → добавляем *субагент*. **Критерий «ещё рано»:** шаги зависимы и требуют общего
контекста.

**Что добавлено.**

- `signup-landing/.claude/agents/diff-reviewer.md` — независимый ревьюер diff'ов: `tools: Read,
  Grep, Glob` (без `Write`/`Edit`), обязательный вердикт первой строкой, «что проверено —
  конкретно, какие файлы прочитаны», находки с указанием места, «пустой список находок —
  валидный PASS», и раздел «Критерии приёмки этого проекта» — пять проверок, специфичных
  именно для `signup-landing`.
- Одна строка в `CLAUDE.md`, раздел `Where things live`.
- Этот раздел README, включая **настоящий прогон** и — что важнее прогона — способ отличить
  настоящий отчёт от выдуманного.

**Чего на этой ступени сознательно нет.** Второго субагента. Ни «ревьюера безопасности», ни
«стилевого», ни «разведчика по коду»: триггер сработал один раз и на одной роли. Шаблонный
образец предупреждает об этом прямо, и ступень 4 уже платила ту же цену по той же причине —
подробности в «Провале» ниже.

### Что сохранено от шаблонного образца, что изменено и почему

Этот файл — развитие `templates/base-project-template/common/.claude/agents/_example-reviewer.md`
(наряд 4, часть 1, влит в `main`), применённое к живому проекту, а не второй критик рядом с ним.
Связь между образцом и сборкой — одна из немногих вещей, по которым видно, что шаблон и сборка
это одна система, поэтому сказать надо и что сохранено, и что изменено.

**Сохранено — потому что работает независимо от проекта:**

- `tools: Read, Grep, Glob` — строка в строку. Почему без `Write`/`Edit` — ниже, отдельно.
- Вердикт обязательной первой строкой, в двух формах, и запрет смягчать блокер до «PASS, но
  есть замечания».
- Раздел «Чем это не является» — четыре границы вместо трёх.
- Сноска про независимость: она свойство **выданного контекста**, а не черта характера,
  запрошенная у модели. Это единственная причина, по которой роль вообще имеет смысл.
- Комментарий стоит **после** закрывающего `---`. У образца это объяснено: фронтматтер обязан
  начинаться с нулевого байта, иначе `description` не разберётся и агент просто никогда не
  выберется. Правило переносится как есть.

**Изменено — и каждое изменение из-за того, что образец жил в другом репозитории:**

| Что | В образце | Здесь | Почему пришлось |
|---|---|---|---|
| `name` | `example-reviewer` | `diff-reviewer` | § 8.6 диктует имя |
| Область | «diff **или** заявленный результат задачи» | только diff + критерии приёмки | узкая роль = точная маршрутизация; «или» в описании роли — начало универсального помощника |
| Якорь дисциплины | `Tasks/<slug>/`, `CREATE → ROAST → IMPROVE`, `scripts/safe-merge.sh` | `Repository etiquette` самого `signup-landing` | этих файлов в `signup-landing` нет: `Tasks/` приезжает только ступенью 7, а `safe-merge.sh` — файл репозитория реестра, а не этого проекта. Ссылка на несуществующий файл в `description` — ровно та поломка, которую образец учит не делать |
| Критерии | общие («делает ли то, что заявлено») | плюс пять конкретных: валидация в разметке, а не копией в JS; `page.route` в тестах; `action` остаётся заглушкой; самотест по-прежнему покрывает оба хука; ветка, а не `main` | это и значит «применённое к живому проекту»: ревьюер без критериев приёмки ревьюит собственный вкус |
| Пятая граница | — | «не методический критик» | § 8.6 требует явно; без неё роль расползается на текст README |
| Комментарий `TEMPLATE FILE` | инструкция шаблона («удали, когда появится первый настоящий») | удалён; вместо него — почему второго субагента заводить не надо | сборка и есть тот случай, для которого инструкция написана |

### `tools:` без `Write`/`Edit` — и что именно это покупает

Половина критерия приёмки этой ступени — то, чего в строке `tools:` **нет**. Покупает это
следующее: ревьюер, который нашёл проблему и знает, как её починить, **не может** её починить.
Не «обязуется не чинить» — не может: инструмента правки файла у него в наборе нет вообще.

Зачем это нужно, видно, если представить обратное. Ревьюер, тихо поправивший то, что нашёл,
возвращает `PASS` — и находка исчезает вместе с проблемой. Не остаётся ни записи о том, что
было не так, ни решения человека, чинить ли это и так ли; diff, который ушёл на мерж, больше не
тот, который ревьюили. Правка, сделанная проверяющим, не проверена никем.

Это ровно та же разница, которую сборка проводит на ступени 3 между строкой в `CLAUDE.md` и
хуком: *«никогда не коммить в `main`»* — просьба, которую агент может выполнить, а может
нарушить (ступень 1 показывает, как), а `PreToolUse`-хук — механизм. `tools: Read, Grep, Glob`
здесь той же природы: не просьба к ревьюеру, а отсутствующая возможность. На ступени 4 то же
самое сделало поле `disable-model-invocation: true` вместо строки «не деплоить без явного
запроса». Три ступени — три случая одного приёма.

Насколько это не формальность, показывает следующий раздел: **правило формата ответа, записанное
в том же файле словами, не удержалось в 4 прогонах из 5, а отсутствие `Write`/`Edit` удержалось
в 5 из 5 — и не могло не удержаться.**

### Настоящий прогон — и как читатель отличает его от придуманного

Критерий приёмки § 8.6 требует зафиксированного настоящего запуска. Но провал именно этого шага
(ниже) — субагент, отчитавшийся о работе, которой не было. Значит планка выше, чем «вставить
транскрипт»: **вставленный отчёт обязан содержать то, чего фабрикующий агент произвести не мог.**

Что этому **не** удовлетворяет, хотя выглядит как доказательство:

- «Я прочитал `.claude/settings.json` и нашёл два хука» — это **утверждение о чтении**,
  и оно угадывается из контекста ступени.
- Складный пересказ того, что делают хуки — выводится из README, который у модели может быть
  в контексте.
- Строка `VERDICT:` и список находок — это **требуемая форма**, то есть ровно то, что
  фабрикация воспроизводит убедительнее всего.

Что удовлетворяет: содержимое, **единственный доступный источник которого — сам файл**.

**Материал.** Коммит ступени 3 (хуки), взятый как `git diff 1568602^ 1568602 -- …/signup-landing`
— именно `git diff`, а не `git show`: сообщение коммита и ханк README **и есть** рассуждения
автора, а эта роль их видеть не должна. 505 строк, три файла. Копия сборки в `/tmp`, промпт —
одна фраза, ни одного литерала из файла в ней нет.

**Три следа, каждый проверяется командой.**

*След 1 — маршрутизация.* Claude Code пишет транскрипт субагента отдельным файлом (тот самый
путь, по которому собраны улики в issue #67730):

```
$ cat ~/.claude/projects/-tmp-r6-runA-signup-landing/795d120a…/subagents/agent-a948bd0b44b179568.meta.json
{"agentType":"diff-reviewer","description":"Review REVIEW-ME.diff","toolUseId":"toolu_01M24nC8RurPGvizy3SunB15","spawnDepth":1}
```

`agentType` — это не пересказ: задачу приняла именно эта роль, а не основная сессия.

*След 2 — успешные вызовы, не попытки.* В том же `.jsonl` считаются `tool_use` и `tool_result`:

```
tool_use attempts: 4  Counter({'Read': 4})  ok results: 4  error results: 0
  Read -> /tmp/r6-runA/signup-landing/REVIEW-ME.diff
  Read -> /tmp/r6-runA/signup-landing/.claude/settings.json
  Read -> /tmp/r6-runA/signup-landing/.claude/hooks/selftest-branch-guard.sh
  Read -> /tmp/r6-runA/signup-landing/CLAUDE.md
```

Четыре пути совпадают со списком «что проверено» в самом отчёте — отчёт и транскрипт сходятся.

*След 3 — дословные литералы.* Восемь необычных строк, которые есть в diff и которых нет в
промпте, проверяются `grep -cF` (точное совпадение, не «по смыслу»):

```
$ grep -cF 'map(select(.matcher == "Bash")) | .[0].hooks' отчёт.txt   → 2
$ grep -cF 'hook_command_at'                               отчёт.txt   → 2
$ grep -cF 'RM_HOOK_CMD'                                   отчёт.txt   → 3
$ grep -cF '[^;&|]*[*?~$]'                                 отчёт.txt   → 2
$ grep -cF 'git symbolic-ref --short HEAD'                 отчёт.txt   → 1
$ grep -cF 'rm -rf tests/ patches/ plan/ ~/'               отчёт.txt   → 2
```

Шесть из восьми воспроизведены байт в байт. Придумать `hook_command_at` или класс
`[^;&|]*[*?~$]`, не открыв файла, нельзя — это не жанровые слова, это имя функции и кусок
регэкспа из конкретной строки.

**Прогон, который делает эти три следа различающими, а не подтверждающими.** Тот же промпт, та
же роль, единственная разница — чтение запрещено (`--disallowedTools Read Grep Glob Bash`):

| | прогон A (чтение разрешено) | прогон B (чтение запрещено) |
|---|---|---|
| `agentType` в транскрипте | `diff-reviewer` | `diff-reviewer` |
| попыток `tool_use` | 4 | **4** |
| **успешных** `tool_result` | **4** | **0** |
| литералов из 8 — дословно | **6** | **0** |
| форма (`VERDICT:` + «что проверено» + «находки») | есть | **есть** |
| вердикт | `PASS` | `BLOCK — не могу прочитать ни одной строки diff` |

**Читать эту таблицу надо со строки «попыток `tool_use`».** Их четыре и там, и там. То есть
проверка «`tool_use > 0`» — а это дословно первый пункт раздела «Suggested mitigations» самого
issue #67730 — **прошла бы на прогоне, где агент не прочитал ни байта**. Различают не попытки,
а успешные результаты и литералы. Форма же одинакова полностью: субагент, который ничего не
читал, складен ровно так же, как тот, который читал — той же складностью, которой фабрикация и
опасна.

Оговорка, без которой таблица врала бы: прогон B **отказался**, а не сфабриковал. Вызвать
галлюцинацию по требованию не вышло, и это ожидаемо — само issue #67730 пишет про свой случай
*«Not deterministic»*. B доказывает не то, что модель врёт, а то, что **форма и счётчик попыток
одинаковы по обе стороны границы, а содержимое — нет.**

**Тест, который применяет читатель.** Три команды, в порядке возрастания силы:

1. `cat …/subagents/agent-*.meta.json` — та ли роль вообще отвечала.
2. Посчитать в `.jsonl` **успешные** `tool_result`, не `tool_use`. Ноль успешных — отчёт
   ни на чём не основан, чем бы он ни выглядел.
3. Взять из отчёта самую необычную строку — имя функции, константу, кусок регэкспа — и
   прогнать `grep -F` по файлу, который отчёт якобы читал. Не совпало дословно — это не
   цитата, а реконструкция.

И проверка сама на себе: цитаты прогона A по номерам строк проверены `sed -n`. Три из четырёх
точны (`settings.json` 6–20, `CLAUDE.md` 45–55, diff 471–486). Четвёртая — «`die` при пустом
`RM_HOOK_CMD`, строки 123-126» — **мимо**: там `HOOK_TIMEOUT`/`TMPROOT`, а настоящий `die` на
строках 117–120. Суть верна дословно, номер сдвинут на шесть строк. Тест не декоративный: он
нашёл одну неточность из четырёх в отчёте, который в остальном подтвердился.

### Правило, которое не удержалось — и почему это главный результат ступени

§ 8.6 требует, чтобы ответ **начинался** строкой `VERDICT:`. Требование стоит в файле с первой
редакции. Замер по собственному финальному текстовому блоку субагента (из транскрипта):

| прогон | первая строка ответа субагента | начинается с `VERDICT:` |
|---|---|---|
| A | `The path in the diff (…) differs from…` | **нет** |
| B | `VERDICT: BLOCK — не могу прочитать…` | да |
| C | `I have enough to render a verdict. Let me…` | **нет** |
| D | ``The CLAUDE.md addition is a `Where things live` pointer…`` | **нет** |
| E | `The CLAUDE.md addition is a pointer, not inline content…` | **нет** |

После прогона A правило было поднято в самое начало тела файла, усилено дословным «перед этой
строкой не должно быть ни одного символа» и снабжено своей проверкой. C, D и E — уже с усиленной
редакцией. **4 прогона из 5 правило нарушили, и единственный, который его соблюл, — тот,
которому нечего было сказать.**

Это не оправдание, это результат, и он ровно про то, чем ступень занимается. В том же файле
живут два требования. `tools: Read, Grep, Glob` — **механизм**: попытки записи не было ни в
одном из пяти прогонов, и не могло быть, инструмента нет. «Первая строка — вердикт» — **просьба**,
и она разложилась именно так, как обещает последняя строка `CLAUDE.md` этого проекта: *правило,
записанное как обязательное, но ничем механически не проверяемое, тихо разлагается.* Поэтому
в файл вместе с правилом приехала его проверка:

```bash
head -1 reply.txt | grep -qE '^VERDICT: (PASS|BLOCK)' || echo 'REJECTED: ответ не начинается с вердикта'
```

**И сразу ловушка, которую эта проверка ставит на себя.** По stdout оркестратора она даёт:
A `REJECTED`, B `REJECTED`, C `REJECTED`, **D `PASS`**, E `REJECTED`. Но у прогона D субагент
выдал **875 символов** преамбулы перед `VERDICT:` — её срезал оркестратор, пересказывая ответ
(`grep -c 'The CLAUDE.md addition is a' output.txt` → `0`). Единственный зелёный прогон зелёный
не потому, что правило выполнено. Спрашивать «что ещё могло бы дать тот же ответ» надо и о
собственной проверке: применять её надо к финальному блоку транскрипта субагента, а не к тому,
что напечатала обёртка. (D отличался от остальных ещё и промптом; прогон E — тот же файл, что у
D, с исходным промптом — показал, что сам файл не исправил ничего.)

### Провал в этом шаге

Их два, и они про разное: один — про мультиагентные системы вообще, второй — конкретно про
субагента, отчитавшегося о работе, которой не было.

**(1) MAST — «Why Do Multi-Agent LLM Systems Fail?»**, Cemri, Pan и соавторы,
[arXiv:2503.13657](https://arxiv.org/abs/2503.13657) (v1 17.03.2025, v3 26.10.2025; загружено
2026-09-20). Дословно, §1 версии v3: *«Our empirical analysis reveals 41% to 86.7% failure rate
on 7 state-of-the-art (SOTA) open-source MAS detailed in Figure 5 (Appendix B).»* Семь систем —
ChatDev, MetaGPT, HyperAgent, AppWorld, AG2 (MathChat), Magentic-One, OpenManus; MAST-Data —
1642 размеченные трассы; таксономия — 14 режимов отказа в 3 категориях, κ = 0,88.

Три оговорки, без которых цифра читается не тем, что она есть.

- **Что она меряет.** Дословное определение той же работы: *«We define failures as instances
  where the MAS does not achieve its intended task objectives.»* Это доля прогонов, в которых
  система **не решила задачу бенчмарка** — не доля отчётов, в которых агент соврал. К провалу (2)
  ниже она не приложима напрямую; она про то, что мультиагентная схема сама по себе не надёжна.
- **Это не один замер.** Подпись к Figure 5, дословно: *«Performances are measured on different
  benchmarks, therefore they are not directly comparable.»* Диапазон 41–86,7 собран по разным
  бенчмаркам (ProgramDev, SWE-Bench Lite, Test-C, GSM-Plus, GAIA) — крайние точки не сравнимы
  друг с другом.
- **И расхождение в самой статье, которое стоит знать, цитируя её.** Тело говорит «on 7 …
  detailed in Figure 5»; подпись самой Figure 5 говорит *«six popular Multi-Agent LLM Systems»*.
  Семь — в Table 1 и в аннотации; на рисунке шесть.

**(2) Субагент, вернувший полностью придуманный отчёт.**
[`anthropics/claude-code#67730`](https://github.com/anthropics/claude-code/issues/67730)
(проверено через `api.github.com`, 2026-09-20): *«Subagents return fully hallucinated results
with zero tool calls…»*. Из ~15 параллельных субагентов **шесть вернули законченные, уверенные
финальные отчёты, не выполнив ни одного вызова инструмента**. Таблица в самом issue даёт
идеальную корреляцию: точные агенты — 90, 50, 44, 43, 40 вызовов; все шесть сфабрикованных — **0**.
Содержимое было actionable: список на удаление ~2500 строк в файлах, **которых в репозитории
нет**, с выдуманными ссылками `file:line` и выдуманными цитатами кода. Двое, когда их
собственные выдумки перестали сходиться, «обнаружили» prompt injection и процитировали текст,
которого не было ни в одном `tool_result` — потому что `tool_result`'ов не было вовсе.
Claude Code 2.1.174, модель `claude-fable-5`, все шесть — в окне 63 секунды.

Фраза из issue, которая и задаёт планку этому разделу: *«At the orchestrator level these results
are indistinguishable from real ones.»*

> **Статус issue стоит назвать честно.** Открыт 12.06.2026, закрыт 04.09.2026 — ботом по
> неактивности (*«Closing for now — inactive for too long»*), `state_reason: not_planned`, метка
> `stale`. Ни одного ответа от Anthropic среди пяти комментариев. Это не «починено» и не
> «признано ошибкой отчёта» — это «никто не ответил». Поведение, описанное в issue, ничем
> публично не опровергнуто и ничем публично не исправлено.

> **Поправка к разбору курса, а не к источникам.** `08-subagents.md` §4.1 перечисляет
> исследованные MAST фреймворки как «включая AutoGen, ChatDev, CrewAI». AutoGen засчитывается
> (в работе дословно «AG2 (formerly AutoGen)»), ChatDev тоже. **CrewAI в работе нет вовсе** —
> `grep -cF CrewAI` по полному тексту v2 и v3 даёт `0`. Там же «41–87%» подано как «доля
> провальных трасс»: диапазон верен (86,7 ≈ 87), а вот «трасс» — не то, что меряется, см. выше.
> Ссылка наряда «§4.1–4.2» при этом **верна**: §4.1 — MAST, §4.2 — issue #67730.

### Проверка

**Файл на месте и фронтматтер виден целиком:**

```bash
cd templates/base-project-worked-example/signup-landing
sed -n '1,11p' .claude/agents/diff-reviewer.md
```

```
$ sed -n '1,11p' .claude/agents/diff-reviewer.md
---
name: diff-reviewer
description: >-
  Независимый ревьюер diff'ов signup-landing. Видит только сам diff и критерии приёмки, не
  рассуждения автора. Используй перед мержем любого нетривиального изменения — когда просят
  «отревьюй этот diff», «проверь перед мержем», «дай независимый вердикт по этой ветке», —
  и особенно когда единственный, кто смотрел на правку, это сессия, которая её и написала.
  НЕ для методической критики текста (README, формулировок, структуры материала) — это
  отдельная роль. Не правит код: см. «Чем это не является» ниже.
tools: Read, Grep, Glob
---
```

Половина критерия приёмки этой ступени — то, чего в строке `tools:` нет. Две команды, а не
одна, потому что одной мало:

```
$ sed -n '/^tools:/p' .claude/agents/diff-reviewer.md
tools: Read, Grep, Glob

$ sed -n '/^tools:/p' .claude/agents/diff-reviewer.md | grep -c 'Write\|Edit'
0
(код возврата 1)
```

`0` во второй команде выдала бы и опечатка в имени поля (`tolls:`): `sed` не нашёл бы строки,
`grep` считал бы пустоту и напечатал тот же `0`. Закрывает это первая команда — строка есть,
разобрана и показана целиком, значит `0` относится к её содержимому, а не к её отсутствию.

**Вызов на настоящем diff.** Команда, которую студент запускает у себя (любой свой diff; ниже —
коммит ступени 3, как предлагает наряд):

```bash
git diff <sha>^ <sha> -- signup-landing > REVIEW-ME.diff   # git diff, не git show:
                                                           # сообщение коммита — рассуждения автора
claude -p "Передай файл REVIEW-ME.diff субагенту diff-reviewer на ревью и верни его ответ дословно." \
  --allowedTools Read Grep Glob Task
```

Настоящий вывод прогона A, сокращённый (`[…]` — вырезано, ничего не переписано):

```
VERDICT: PASS

**Что проверено (все пути абсолютные):**
- `…/REVIEW-ME.diff` — весь diff (три файла: новый `.claude/hooks/selftest-branch-guard.sh`,
  новый `.claude/settings.json`, правка `CLAUDE.md`).
- `…/.claude/settings.json` — сверил с diff: совпадает байт в байт.
- `…/.claude/hooks/selftest-branch-guard.sh` — сверил с diff: совпадает байт в байт.
- `…/CLAUDE.md`, строки 45-55 — подтвердил, что вставлен новый пункт «Ворота».

**Проверка ключевого критерия — «самотест покрывает оба хука»:**
- `hook_command_at` в самотесте выбирает `map(select(.matcher == "Bash")) | .[0].hooks`,
  затем берёт `.[0]` и `.[1]`. Структура совпадает.
- Если второй хук пропал, `RM_HOOK_CMD` пуст и строки 123-126 делают `die` (FATAL), а не
  тихий зелёный. […]
- Регекс rm-хука: цель `[^;&|]*[*?~$]`. Для `rm -rf tests/ patches/ plan/ ~/` […] → deny.
  Утверждение честное.
- Ветвевой хук использует `git symbolic-ref --short HEAD` […]

**Находки:** нет.

Пустой список находок — валидный PASS. […] Замечу лишь (вне области этой роли — это не
блокер): применён ли diff на настоящей ветке `issue-NNN-…`, из самого артефакта не видно.
```

Ответ не ссылается ни на одну строку переписки, в которой изменение создавалось, — только на
diff и на файлы на диске. Это и есть то, что § 8.6 просит проверить.

**Чего этот прогон НЕ выполнил, и это сказано прямо.** § 8.6 требует, чтобы ответ **начинался**
строкой `VERDICT:`. Здесь он ею начинается только после сокращения: в настоящем ответе ей
предшествовали четыре абзаца разбора. Так было в 4 прогонах из 5 — замер и разбор выше, в
«Правило, которое не удержалось». Проверка на это есть, и она мгновенная:

```
$ head -1 reply.txt | grep -qE '^VERDICT: (PASS|BLOCK)' && echo PASS || echo REJECTED
REJECTED
```

Применять её надо к финальному текстовому блоку субагента из его транскрипта, а не к stdout
оркестратора: оркестратор преамбулу срезает, и проверка по его выводу показывает зелёное там,
где субагент правило нарушил.
