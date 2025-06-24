# Smart Testing with Gen-AI example repository
This example is used to demonstrate how to run an efficient unit test for Simulink models or C-code using BTC EmbeddedPlatform and Gen-AI.

### CI Status & Test Report
![CI](https://github.com/btc-embedded/smart-testing-genai/actions/workflows/pipeline.yml/badge.svg)

[BTC Test Report](https://btc-embedded.github.io/smart-testing-genai/report.html)

### Requirements

| ID      | Title                | Description                                                                                                                                                                                                                   |
|---------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| SEAT-79 | Activation Conditions| The system shall only be active while the following conditions are met: the seat is occupied, the power status reads OK, and there is no error (error flag: 0).                                                               |
| SEAT-80 | Reactivation         | When the system is reactivated (activation conditions are once again met), it shall return to the same temperature stage that was active before.                                                                               |
| SEAT-81 | Initial Request      | When the system is active but the button has not been pressed, it shall initially be in the NO HEATING temperature stage.                                                                                                     |
| SEAT-82 | Heating Cycle        | When active, the system shall cycle through the temperature stages and move from one stage to the next on each button press: high temperature, medium temperature, low temperature, no heating.                              |
| SEAT-83 | No Heating           | When the system is active and is in the NO HEATING temperature stage: it shall request no temperature and all LEDs shall be disabled.                                                                                         |
| SEAT-84 | Low Heating          | When the system is active and is in the LOW temperature stage: it shall request the low temperature level based on the parameter "TempStg_Low" and only the first LED shall be enabled.                                      |
| SEAT-85 | Medium Heating       | When the system is active and is in the MEDIUM temperature stage: it shall request the medium temperature level based on the parameter "TempStg_Med" and only the first two LEDs shall be enabled.                         |
| SEAT-86 | High Heating         | When the system is active and is in the HIGH temperature stage: it shall request the high temperature level based on the parameter "TempStg_High" and all three LEDs shall be enabled.                                      |
