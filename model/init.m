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

PowerMgtState_ErrorStatus = Simulink.Signal;
PowerMgtState_ErrorStatus.CoderInfo.StorageClass = 'ExportedGlobal';
PowerMgtState_ErrorStatus.Description = '';
PowerMgtState_ErrorStatus.DataType = 'uint8';
PowerMgtState_ErrorStatus.Min = [];
PowerMgtState_ErrorStatus.Max = [];

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



TemperatureStage1 = Simulink.Parameter;
TemperatureStage1.Value = 30;
TemperatureStage1.CoderInfo.StorageClass = 'ExportedGlobal';
TemperatureStage1.Description = '';
TemperatureStage1.DataType = 'uint8';
TemperatureStage1.Min = [];
TemperatureStage1.Max = [];
TemperatureStage1.DocUnits = '';

TemperatureStage2 = Simulink.Parameter;
TemperatureStage2.Value = 35;
TemperatureStage2.CoderInfo.StorageClass = 'ExportedGlobal';
TemperatureStage2.Description = '';
TemperatureStage2.DataType = 'uint8';
TemperatureStage2.Min = [];
TemperatureStage2.Max = [];
TemperatureStage2.DocUnits = '';

TemperatureStage3 = Simulink.Parameter;
TemperatureStage3.Value = 45;
TemperatureStage3.CoderInfo.StorageClass = 'ExportedGlobal';
TemperatureStage3.Description = '';
TemperatureStage3.DataType = 'uint8';
TemperatureStage3.Min = [];
TemperatureStage3.Max = [];
TemperatureStage3.DocUnits = '';

RTE_OK = 0;

try
    seat_heating_control_defineIntEnumTypes
end
