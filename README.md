!["demopic 1](images/demopic1.PNG?raw=true )
!["demopic 2](images/demogif1.gif?raw=true )

- Реализация анализатора спектра на чипе Semtech SX127x (Lora/FSK-трансивер)
- Cборка сконфигурирована для контроллера ESP32S2 в среде Platformio
- Данные забираются через последовательный порт python-скриптом: src/python/sweep.py - выбор порта и диапазона  частот, шага и количества шагов вписаны в скрипте в процедуре main
- Визуализация - Numpy и Matplotlib (зря)






