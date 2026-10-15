# Редька Джамп

Піксельний дудл-джамп в одному `index.html`: Редька стрибає по ярликах кенселів до мільйона підписників. Без збірки і пакетного менеджера. Шрифти — Google Fonts.

## Команди

- Локально: `python3 -m http.server` у корені репозиторію. Відкривати файлом не можна: фото і звук вантажаться з `art/`.
- Збірки, тестів і лінтера немає. Перевірка синтаксису: витягни вміст `<script>` і запусти `node --check`.

## Структура

- `index.html` — уся гра: звук, спрайти, рівні, фізика, рендер, стартовий, колекція і фінальний екрани.
- `art/faces/` — піксельні обличчя персонажів (`felix`, `felix-fail` на фейлі, `felix-fly` у польоті, `stuk`, `koms`, `threads`, `cancel`). Мовний патруль — лише піксельний спрайт.
- `art/bg/` — ілюстровані фони семи етапів.
- `art/achs/` — іконки досягнень (`art/achs/<id>.png`).
- `art/gordon/` і `gordon-intro.mp3` — режим Гордона.
- `art/ends/` — фінальні ілюстрації (`fall`, `stuk`, `threads`, `koms`, `cancel`, `lang`).
- `art/springy-lead.mp3` — фонова тема, цикл, гучність 0.63. `SFX_VOL=5`.
- `art/looks.py` — сітки костюмів (`REDKA`, клоун, Одіссей). Унікальні луки мають `body` + `cut`; обличчя завжди `felix*.png`.
- `art/enemies.py` — тіла хейтерів без піксельних голів (піксельна голова Скасовувача — лише fallback, якщо немає `cancel.png`).
- `*.py` — генератори піксельних сіток тіл і предметів.
- `README.md` — баланс, пороги і де що лежить.

## Нюанси

- Обличчя накладаються на тіла без голови через `makeChar()`. Персонажі збираються в CK-разовій роздільності, щоб пікселі обличчя лишались цілими. Клоун і Одіссей — окремі сітки; золотий лук має `gold:1`. Луки купуються квитками (`LOOKS[].cost`); `LOOKS[].at` лише мігрує старі сейви в `STATS.owned`. Некуплене в гардеробі — силует лука 0, `???`, ціна. Одягнений лук — `STATS.wear` / `lookIdx`.
- Інтро Гордона грає через WebAudio (`decodeAudioData`) лише в режимі Гордона, гучність 0.7, швидкість 1.2. `primeGordonAudio()` на «Стрибати» розблоковує HTMLAudio muted+pause без звуку; `stopGordonMusic()` тільки pause, без повторного `play()`. HTMLAudio — запасний шлях, якщо буфер ще не розкодовано.
- Пауза: `mode='pause'`, `openPause` / `resumePlay` / `quitToStart` (без `saveRun`). Гардероб з паузи — `openCol('ward','pause')`. `update` і `draw` лише коли `mode==='play'`. Згортання вкладки (`visibilitychange`) теж ставить паузу. «На старт» викликає `wipeCanvas()`.
- HUD: один ряд — рахунок, `#hudTix`, «Меню». Підказка `#steerHint` якщо `STATS.steerN < 3`; `steerN++` лише на реальний ввід. Ігрові тости малюються під HUD (`toastY()`).
- Канонічне посилання `GAME_LINK` (`https://redkajump.fun/`) іде в текст «Поділитись». На живому http(s) — поточний origin. У «Про гру» чіп Threads `@saintfame23` (`window.open`, бо `touch-action:none` на `#wrap`). Живий хост — Cloudflare Pages (`redkajump`), не GitHub Pages.
- `og:image` — `https://redkajump.fun/art/og.png` (1200×630). PostHog: `POSTHOG_KEY` / `POSTHOG_HOST` у `<head>`; порожній ключ — no-op `capture`. Події `play_start`, `game_over`, `share`. `loadEnds()` вантажить `art/ends/` через `loadImg()` (один retry `?r=1`).
- `window.__g` і `jumpTo` лише за `?qa=1`. Кнопки DEMO немає.
- ♪/♫ на старті й у паузі (`[data-mute]` / `[data-bgm]`, `touch-action:manipulation`, JS click/pointerup). Перший жест на `#wrap` — `unlockAudio()` (`audioOn` + `primeBgm` + `syncBgm`). Якщо ♫ увімкнена, але трек ще не грає, тап лише стартує, не вимикає. Оверлеї `z-index:6`, HUD `4`.
- Повідомлення про етапи, образи, хейтерів і ачивки йдуть чергою тостів під HUD. Плавальний текст лишається лише для «+2500» і комбо.
- `localStorage`: `redkaBest`, `redkaMute`, `redkaBgm`, `redkaStats` (`tickets`, `owned`, `wear`), `redkaAch`. Квитки пишуться одразу при підборі.
- Тур-плашок міст немає. `achCount` = `ACH.length` (19). Експрес: `EXPRESS_FROM=60000`, `EXPRESS_CD=50000`, окремий рол ~5–9%.
- Стрибок і хейтери — короткі `tone()`/`noise()` з `SFX_VOL`, чути над BGM. Mute ♪ глушить SFX і ставить BGM на паузу.
- Усіх хейтерів топчуть зверху через `stompHater` (`+2500`, `STOMP_Q`); боковий удар — смерть.
- Фонова музика (`art/springy-lead.mp3`) має окрему кнопку ♫ і не залежить від mute звуків. На iPhone її теж треба праймити в тапі (`primeBgm()` / `unlockAudio()`). Під час Гордона фон ставиться на паузу. Unmute ♪ знову кличе `syncBgm()`.
