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
- `art/looks.py` — сітки всіх 10 костюмів на одному силуеті клоуна + палітри (`looks.json` → `LOOKGRID`/`LOOKPAL`/`HEADPH` в `index.html`). Лук 0 — «Жебрак» (голий торс). `grids_side` (руки трохи в боки, підйом стрибка) і `grids_up` (руки вгору, політ на ракеті/Гордон) на кожен лук (`LOOKGRIDSIDE`/`LOOKGRIDUP`, `redkaChar(...,pose)`); `jumpPose()` у `index.html` дає позу й стискання (`.24`). Обличчя завжди `felix*.png`, геометрія в `REDKA_FACE`.
- `art/catbus.py` — піксельний кіт-автобус «Шакалячий експрес» 48×32, 2 кадри (`catbus.json` → `BUS` в `index.html`; `BUS_SPR` ×3 для польоту, `BUS_ICON` ×1 для предмета/HUD/довідки). Редька стоїть на даху: лінія ніг героя = рядок 6 сітки; замість полум'я — пил із лап (`puff` з `dust`).
- `art/jackals.py` — сітки шакалів (`jackals.json` → `JACKAL`): 4 кадри галопу × закрита/відкрита паща, палітри gold/grey/dark.
- `art/achs.py` — піксельні іконки нових ачивок (`kyiv`, `chain3`, `armor`, `bus10`, `lang5`) і `exp3` (кіт-автобус) у `art/achs/`; решта іконок — старі ілюстрації. Назви етапів у `ZONES` без років.
- `art/enemies.py` — тіла хейтерів без піксельних голів (піксельна голова Скасовувача — лише fallback, якщо немає `cancel.png`).
- `*.py` — генератори піксельних сіток тіл і предметів.
- `README.md` — баланс, пороги і де що лежить.

## Нюанси

- Обличчя накладаються на тіла без голови через `makeChar()`. Персонажі збираються в CK-разовій роздільності, щоб пікселі обличчя лишались цілими. Усі луки — одна сітка-силует клоуна з різною палітрою/візерунком; золотий лук має `gold:1`. Луки купуються квитками (`LOOKS[].cost`); `LOOKS[].at` лише мігрує старі сейви в `STATS.owned`. Некуплене в гардеробі — подарункова коробка, `???`, ціна. Одягнений лук — `STATS.wear` / `lookIdx`.
- Шакалячий експрес: `drawChaseDogs()` малює трьох шакалів позаду кіт-автобуса, на якому їде Редька (`chase[]`, ліниво ініціюється, скидається в `stopDogs()`); гавкіт йде за годинником `dogs.mp3` (`BARK_AT`, `dogsClock()`), а в бульбашках — випадкові ярлики (`chaseCall()`), не «гав»; `jackalPack()` (WebAudio) — лише запасний звук, якщо `play()` відхилено.
- Інтро — живий канвас (`attractInit/attractFrame` у `mode==='start'`) + HTML-оверлей `#startScr` (логотип, лічильник, док). Правила/бонуси/«Про гру» — у нижньому шиті `#helpScr`. Хейтерів на старті немає: вони відкриваються в грі (`STATS.met`) і з'являються в «Колекції → Хейтери». Гордон у правилах — «секретний гість». Невикуплені костюми — «подарунок» (`GIFT`), назва `???`.
- Лідерборд: `functions/api/scores.js` (KV `LEADERBOARD`; імʼя до 12 символів, до 15 для нового загальному рекорду №1 — `lbGlobal` на клієнті), клієнт `lb*()` в `index.html`; після забігу великий банер `#recordBadge` («НОВИЙ РЕКОРД!» / «ЗАГАЛЬНИЙ РЕКОРД!»); внизу інтро — плашка звання `#rankLine`; без бекенду — локальний топ-10 (`redkaLocalTop`). `localStorage`: `redkaName`, `redkaPid`.
- Інтро Гордона грає через WebAudio (`decodeAudioData`) лише в режимі Гордона, гучність 0.7, швидкість 1.2. `primeGordonAudio()` на «Стрибати» розблоковує HTMLAudio muted+pause без звуку; `stopGordonMusic()` тільки pause, без повторного `play()`. HTMLAudio — запасний шлях, якщо буфер ще не розкодовано.
- Пауза: `mode='pause'`, `openPause` / `resumePlay` / `quitToStart` (без `saveRun`). Гардероб з паузи — `openCol('ward','pause')`. `update` і `draw` лише коли `mode==='play'`. Згортання вкладки (`visibilitychange`) теж ставить паузу. «На старт» викликає `wipeCanvas()`.
- HUD: один ряд — рахунок, `#hudTix`, «Меню». Підказка `#steerHint` якщо `STATS.steerN < 3`; `steerN++` лише на реальний ввід. Ігрові тости малюються під HUD (`toastY()`).
- Картка шерингу: `makeCard()` (аркадний «GAME OVER», 1080×1350) бере чистий `END_ART[causeKind]` через `drawCover()`/`END_FOCUS`; `scene()` на фіналі малює той самий кадр без штампів і баблів. Помічники картки `cText`/`cPlate`/`cStamp`. Кнопка «Поділитись» → лист `#shareSheet` (share/зберегти/копіювати), `closeShare()`. Текст — `shareText()` з `lastScore`/`lbRankLast`. У `?qa=1` є `__g.cardTest(o)` для рендера картки з довільними даними.
- Канонічне посилання `GAME_LINK` (`https://redkajump.fun/`) іде в текст «Поділитись». На живому http(s) — поточний origin. У «Про гру» чіп Threads `@saintfame23` (`window.open`, бо `touch-action:none` на `#wrap`). Живий хост — Cloudflare Pages (`redkajump`), не GitHub Pages.
- `og:image` — `https://redkajump.fun/art/og.png` (1200×630). PostHog EU: `POSTHOG_KEY` / `POSTHOG_HOST`. Події `play_start`, `game_over`/`run_abandon` (знімок), віхи механік, `threads_click`. Баланс для Cursor: `analytics/optimize.md`. `loadEnds()` через `loadImg()` (retry `?r=1`).
- `window.__g` і `jumpTo` лише за `?qa=1`. Кнопки DEMO немає.
- ♪/♫ на старті й у паузі (`[data-mute]` / `[data-bgm]`, `touch-action:manipulation`, JS click/pointerup). Перший жест на `#wrap` — `unlockAudio()` (`audioOn` + `primeBgm` + `syncBgm`). Якщо ♫ увімкнена, але трек ще не грає, тап лише стартує, не вимикає. Оверлеї `z-index:6`, HUD `4`.
- Повідомлення про етапи, образи, хейтерів і ачивки йдуть чергою тостів під HUD. Плавальний текст лишається лише для «+2500» і комбо.
- `localStorage`: `redkaBest`, `redkaMute`, `redkaBgm`, `redkaStats` (`tickets`, `owned`, `wear`), `redkaAch`. Квитки пишуться одразу при підборі.
- Тур-плашок міст немає. `achCount` = `ACH.length` (24). Експрес: `EXPRESS_FROM=60000`, `EXPRESS_CD=70000`, окремий рол ~5–9%.
- Стрибок і хейтери — короткі `tone()`/`noise()` з `SFX_VOL`, чути над BGM. Mute ♪ глушить SFX і ставить BGM на паузу.
- Усіх хейтерів топчуть зверху через `stompHater` (`+2500`, `STOMP_Q`); боковий удар — смерть.
- Фонова музика (`art/springy-lead.mp3`) має окрему кнопку ♫ і не залежить від mute звуків. На iPhone її теж треба праймити в тапі (`primeBgm()` / `unlockAudio()`). Під час Гордона фон ставиться на паузу. Unmute ♪ знову кличе `syncBgm()`.

- Хейтери й Гордон: `tryShield()` (Бронювання), `chainN/chainT` (ланцюг у `stompHater`), Гордон через «директор» `heat`/`gordonNextGs`/`gordonPendStep` (`scheduleNextGordon()`, `gordonMode`: interview/live/exclusive). Подій: `shield_get`, `shield_save`, `chain`, `gordon{result,mode,heat,nth}`.
- Бронювання: поки `shield>0||shieldGrace>0` Редька малюється з обличчям `felix-armor` (той самий `felix-fly.png`, але масштаб 4 як у звичайного, `redkaChar(...,'felix-armor',pose,outline)`), обводка синя `#3d8bff`, під час невразливості блимає. Складність: `breath`/`lastGap`/`lastHaterStep` у `genStep`.
