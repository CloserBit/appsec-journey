*STLC (Software Testing Life Cycle) — жизненный цикл ТЕСТИРОВАНИЯ (не всей разработки — это SDLC). 6 фаз:*

1. Requirement Analysis — что тестируем; security: security-требования
2. Test Planning — как/чем/кто; security: план SAST/DAST/SCA, скоуп по риску
3. Test Case Development — тест-кейсы; security: abuse cases («что НЕ должно работать»: ' OR 1=1 → отказ, чужой id → 403)
4. Test Environment Setup — стенд; security: окружение для сканеров, изолированный стенд
5. Test Execution — прогон + баги; security: гоняем сканеры, триаж находок (severity, TP/FP)
6. Test Cycle Closure — отчёт, итоги; security: отчёт по уязвимостям, метрики
Главное: security встроен в КАЖДУЮ фазу (shift-left), не в конце.
SDLC vs STLC: SDLC — весь цикл разработки (тестирование — одна фаза); STLC разворачивает эту фазу в 6 подэтапов. STLC живёт ВНУТРИ SDLC.

*SCA (Software Composition Analysis)* — анализ СТОРОННИХ зависимостей/библиотек на известные уязвимости (CVE). Мой код чист, но подключённая старая библиотека с публичной дырой → SCA ловит, сверяя версии с базами CVE. Инструменты: Trivy, Grype, Snyk, Dependabot. Относится к Supply Chain Security.
Тройка: SAST=мой код, DAST=работающее приложение, SCA=чужие библиотеки.