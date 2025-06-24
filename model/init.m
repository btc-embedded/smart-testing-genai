SeatOccupied = Simulink.Signal;
SeatOccupied.CoderInfo.StorageClass = 'ExportedGlobal';
SeatOccupied.Description = '';
SeatOccupied.DataType = 'boolean';
SeatOccupied.Min = [];
SeatOccupied.Max = [];

PowerMgtState = Simulink.Signal;
PowerMgtState.CoderInfo.StorageClass = 'ExportedGlobal';
PowerMgtState.Description = '';
PowerMgtState.DataType = 'Enum: EnumPowerState';
PowerMgtState.Min = [];
PowerMgtState.Max = [];

ErrorStatus = Simulink.Signal;
ErrorStatus.CoderInfo.StorageClass = 'ExportedGlobal';
ErrorStatus.Description = '';
ErrorStatus.DataType = 'uint8';
ErrorStatus.Min = [];
ErrorStatus.Max = [];

ButtonPressed = Simulink.Signal;
ButtonPressed.CoderInfo.StorageClass = 'ExportedGlobal';
ButtonPressed.Description = '';
ButtonPressed.DataType = 'boolean';
ButtonPressed.Min = [];
ButtonPressed.Max = [];


LEDFeedback = Simulink.Signal;
LEDFeedback.CoderInfo.StorageClass = 'ExportedGlobal';
LEDFeedback.Dimensions = 3;
LEDFeedback.InitialValue = "[0 0 0]";
LEDFeedback.Description = '';
LEDFeedback.DataType = 'boolean';
LEDFeedback.Min = [];
LEDFeedback.Max = [];


Set_Heating_Coil = Simulink.Signal;
Set_Heating_Coil.CoderInfo.StorageClass = 'ExportedGlobal';
Set_Heating_Coil.Description = '';
Set_Heating_Coil.DataType = 'uint8';
Set_Heating_Coil.Min = [];
Set_Heating_Coil.Max = [];
Set_Heating_Coil.Unit = '°C';


TempStg_Low = Simulink.Parameter;
TempStg_Low.Value = 30;
TempStg_Low.CoderInfo.StorageClass = 'ExportedGlobal';
TempStg_Low.Description = '';
TempStg_Low.DataType = 'uint8';
TempStg_Low.Min = [];
TempStg_Low.Max = [];
TempStg_Low.Unit = '°C';

TempStg_Med = Simulink.Parameter;
TempStg_Med.Value = 35;
TempStg_Med.CoderInfo.StorageClass = 'ExportedGlobal';
TempStg_Med.Description = '';
TempStg_Med.DataType = 'uint8';
TempStg_Med.Min = [];
TempStg_Med.Max = [];
TempStg_Med.Unit = '°C';

TempStg_High = Simulink.Parameter;
TempStg_High.Value = 45;
TempStg_High.CoderInfo.StorageClass = 'ExportedGlobal';
TempStg_High.Description = '';
TempStg_High.DataType = 'uint8';
TempStg_High.Min = [];
TempStg_High.Max = [];
TempStg_High.Unit = '°C';


try
    seat_heating_control_defineIntEnumTypes
end

SystemActive = Simulink.Signal;
SystemActive.CoderInfo.StorageClass = 'ExportedGlobal';
SystemActive.CoderInfo.Identifier = 'SystemActive';
SystemActive.Description = '';
SystemActive.DataType = 'boolean';
SystemActive.Min = [];
SystemActive.Max = [];

TemperatureStage = Simulink.Signal;
TemperatureStage.CoderInfo.StorageClass = 'ExportedGlobal';
TemperatureStage.CoderInfo.Identifier = 'TermperatureStage';
TemperatureStage.Description = '';
TemperatureStage.DataType = 'uint8';
TemperatureStage.Min = [];
TemperatureStage.Max = [];