*STLC (Software Testing Life Cycle) — жизненный цикл ТЕСТИРОВАНИЯ (не всей разработки — это SDLC). 6 фаз:*

Requirement Analysis — что тестируем; security: security-требования
Test Planning — как/чем/кто; security: план SAST/DAST/SCA, скоуп по риску
Test Case Development — тест-кейсы; security: abuse cases («что НЕ должно работать»: ' OR 1=1 → отказ, чужой id → 403)
Test Environment Setup — стенд; security: окружение для сканеров, изолированный стенд
Test Execution — прогон + баги; security: гоняем сканеры, триаж находок (severity, TP/FP)
Test Cycle Closure — отчёт, итоги; security: отчёт по уязвимостям, метрики
Главное: security встроен в КАЖДУЮ фазу (shift-left), не в конце.
SDLC vs STLC: SDLC — весь цикл разработки (тестирование — одна фаза); STLC разворачивает эту фазу в 6 подэтапов. STLC живёт ВНУТРИ SDLC.