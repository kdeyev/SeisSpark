from typing import Dict
from dataclasses import dataclass # Remove after porting to Python >= 3.7

from enum import Enum

class SEGYTraceHeaderEntryType(Enum):
    int16 = 1
    int32 = 2
    uint16 = 3
    uint32 = 4
    char = 5
    uchar = 6
    float = 7
    ibm = 8


class SEGYTraceHeaderEntryName(Enum):
    TraceSequenceLine = 0
    TraceSequenceFile = 4
    FieldRecord = 8
    TraceNumber = 12
    EnergySourcePoint = 16
    cdp = 20
    cdpTrace = 24
    TraceIdenitifactionCode = 28  # 'int16'); % 28
    
    NSummedTraces = 30 # 'int16'); % 30
    NStackedTraces = 32 # 'int16'); % 32
    DataUse = 34 # 'int16'); % 34
    offset = 36  # 'int32');             %36
    ReceiverGroupElevation = 40  # 'int32');             %40
    SourceSurfaceElevation = 44  # 'int32');             %44
    SourceDepth = 48  # 'int32');             %48
    ReceiverDatumElevation = 52  # 'int32');             %52
    SourceDatumElevation = 56  # 'int32');             %56
    SourceWaterDepth = 60  # 'int32');  %60
    GroupWaterDepth = 64  # 'int32');  %64
    ElevationScalar = 68 # 'int16');  %68
    SourceGroupScalar = 70 # 'int16');  %70
    SourceX = 72  # 'int32');  %72
    SourceY = 76  # 'int32');  %76
    GroupX = 80  # 'int32');  %80
    GroupY = 84  # 'int32');  %84
    CoordinateUnits = 88 # 'int16');  %88
    WeatheringVelocity = 90 # 'int16');  %90
    SubWeatheringVelocity = 92 # 'int16');  %92
    SourceUpholeTime = 94 # 'int16');  %94
    GroupUpholeTime = 96 # 'int16');  %96
    SourceStaticCorrection = 98 # 'int16');  %98
    GroupStaticCorrection = 100 # 'int16');  %100
    TotalStaticApplied = 102 # 'int16');  %102
    LagTimeA = 104 # 'int16');  %104
    LagTimeB = 106 # 'int16');  %106
    DelayRecordingTime = 108 # 'int16');  %108
    MuteTimeStart = 110 # 'int16');  %110
    MuteTimeEND = 112 # 'int16');  %112
    ns = 114  # 'uint16');  %114
    dt = 116  # 'uint16');  %116
    GainType = 119 # 'int16');  %118
    InstrumentGainConstant = 120 # 'int16');  %120
    InstrumentInitialGain = 122 # 'int16');  %%122
    Correlated = 124 # 'int16');  %124
    
    SweepFrequenceStart = 126 # 'int16');  %126
    SweepFrequenceEnd = 128 # 'int16');  %128
    SweepLength = 130 # 'int16');  %130
    SweepType = 132 # 'int16');  %132

    SweepTraceTaperLengthStart = 134 # 'int16');  %134
    SweepTraceTaperLengthEnd = 136 # 'int16');  %136
    TaperType = 138 # 'int16');  %138

    AliasFilterFrequency = 140 # 'int16');  %140
    AliasFilterSlope = 142 # 'int16');  %142
    NotchFilterFrequency = 144 # 'int16');  %144
    NotchFilterSlope = 146 # 'int16');  %146
    LowCutFrequency = 148 # 'int16');  %148
    HighCutFrequency = 150 # 'int16');  %150
    LowCutSlope = 152 # 'int16');  %152
    HighCutSlope = 154 # 'int16');  %154
    YearDataRecorded = 156 # 'int16');  %156
    DayOfYear = 158 # 'int16');  %158
    HourOfDay = 160 # 'int16');  %160
    MinuteOfHour = 162 # 'int16');  %162
    SecondOfMinute = 164 # 'int16');  %164
    TimeBaseCode = 166 # 'int16');  %166
    TraceWeightningFactor = 168 # 'int16');  %170
    GeophoneGroupNumberRoll1 = 170 # 'int16');  %172
    GeophoneGroupNumberFirstTraceOrigField = 172 # 'int16');  %174
    GeophoneGroupNumberLastTraceOrigField = 174 # 'int16');  %176
    GapSize = 176 # 'int16');  %178
    OverTravel = 178 # 'int16');  %178
    cdpX = 180  # 'int32');  %180
    cdpY = 184  # 'int32');  %184
    Inline3D = 188  # 'int32');  %188
    Crossline3D = 192  # 'int32');  %192
    ShotPoint = 192  # 'int32');  %196
    ShotPointScalar = 200 # 'int16');  %200
    TraceValueMeasurementUnit = 202 # 'int16');  %202
    TransductionConstantMantissa = 204  # 'int32');  %204
    TransductionConstantPower = 208 # 'int16'); %208
    TransductionUnit = 210 # 'int16');  %210
    TraceIdentifier = 212 # 'int16');  %212
    ScalarTraceHeader = 214 # 'int16');  %214
    SourceType = 216 # 'int16');  %216

    SourceEnergyDirectionMantissa = 218  # 'int32');  %218
    SourceEnergyDirectionExponent = 222 # 'int16');  %222
    SourceMeasurementMantissa = 224  # 'int32');  %224
    SourceMeasurementExponent = 228 # 'int16');  %228
    SourceMeasurementUnit = 230 # 'int16');  %230
    UnassignedInt1 = 232  # 'int32');  %232
    UnassignedInt2 = 236  # 'int32');  %236

@dataclass
class SEGYTraceHeaderEntry:
    position: int
    type: SEGYTraceHeaderEntryType

SEGY_TRACE_HEADER_ENTRYS: Dict[SEGYTraceHeaderEntryName, SEGYTraceHeaderEntry] = {}

SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceSequenceLine] = SEGYTraceHeaderEntry(position=0, type=SEGYTraceHeaderEntryType.int32)
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceSequenceFile] = SEGYTraceHeaderEntry(position=4, type=SEGYTraceHeaderEntryType.int32)
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.FieldRecord] = SEGYTraceHeaderEntry(position=8, type=SEGYTraceHeaderEntryType.int32)
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceNumber] = SEGYTraceHeaderEntry(position=12, type=SEGYTraceHeaderEntryType.int32)
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.EnergySourcePoint] = SEGYTraceHeaderEntry(position=16, type=SEGYTraceHeaderEntryType.int32)
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.cdp] = SEGYTraceHeaderEntry(position=20, type=SEGYTraceHeaderEntryType.int32)
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.cdpTrace] = SEGYTraceHeaderEntry(position=24, type=SEGYTraceHeaderEntryType.int32)
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceIdenitifactionCode] = SEGYTraceHeaderEntry(position=28, type=SEGYTraceHeaderEntryType.uint16)  # 'int16'); % 28
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceIdenitifactionCode"]["descr"] = {0: {
#     1: "Seismic data",
#     2: "Dead",
#     3: "Dummy",
#     4: "Time Break",
#     5: "Uphole",
#     6: "Sweep",
#     7: "Timing",
#     8: "Water Break)}
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceIdenitifactionCode"]["descr"][1] = {
#     -1: "Other",
#     0: "Unknown",
#     1: "Seismic data",
#     2: "Dead",
#     3: "Dummy",
#     4: "Time break",
#     5: "Uphole",
#     6: "Sweep",
#     7: "Timing",
#     8: "Waterbreak",
#     9: "Near-field gun signature",
#     10: "Far-field gun signature",
#     11: "Seismic pressure sensor",
#     12: "Multicomponent seismic sensor - Vertical component",
#     13: "Multicomponent seismic sensor - Cross-line component",
#     14: "Multicomponent seismic sensor - In-line component",
#     15: "Rotated multicomponent seismic sensor - Vertical component",
#     16: "Rotated multicomponent seismic sensor - Transverse component",
#     17: "Rotated multicomponent seismic sensor - Radial component",
#     18: "Vibrator reaction mass",
#     19: "Vibrator baseplate",
#     20: "Vibrator estimated ground force",
#     21: "Vibrator reference",
#     22: "Time-velocity pairs)
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.NSummedTraces] = SEGYTraceHeaderEntry(position=30, type=SEGYTraceHeaderEntryType.int16)  # 'int16'); % 30
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.NStackedTraces] = SEGYTraceHeaderEntry(position=32, type=SEGYTraceHeaderEntryType.int16)  # 'int16'); % 32
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.DataUse] = SEGYTraceHeaderEntry(position=34, type=SEGYTraceHeaderEntryType.int16)  # 'int16'); % 34
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.DataUse"]["descr"] = {0: {
#     1: "Production",
#     2: "Test)}
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.DataUse"]["descr"][1] = SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.DataUse"]["descr"][0]
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.offset] = SEGYTraceHeaderEntry(position=36, type=SEGYTraceHeaderEntryType.int32)  # 'int32');             %36
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.ReceiverGroupElevation] = SEGYTraceHeaderEntry(position=40, type=SEGYTraceHeaderEntryType.int32)  # 'int32');             %40
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceSurfaceElevation] = SEGYTraceHeaderEntry(position=44, type=SEGYTraceHeaderEntryType.int32)  # 'int32');             %44
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceDepth] = SEGYTraceHeaderEntry(position=48, type=SEGYTraceHeaderEntryType.int32)  # 'int32');             %48
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.ReceiverDatumElevation] = SEGYTraceHeaderEntry(position=52, type=SEGYTraceHeaderEntryType.int32)  # 'int32');             %52
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceDatumElevation] = SEGYTraceHeaderEntry(position=56, type=SEGYTraceHeaderEntryType.int32)  # 'int32');             %56
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceWaterDepth] = SEGYTraceHeaderEntry(position=60, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %60
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GroupWaterDepth] = SEGYTraceHeaderEntry(position=64, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %64
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.ElevationScalar] = SEGYTraceHeaderEntry(position=68, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %68
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceGroupScalar] = SEGYTraceHeaderEntry(position=70, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %70
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceX] = SEGYTraceHeaderEntry(position=72, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %72
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceY] = SEGYTraceHeaderEntry(position=76, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %76
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GroupX] = SEGYTraceHeaderEntry(position=80, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %80
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GroupY] = SEGYTraceHeaderEntry(position=84, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %84
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.CoordinateUnits] = SEGYTraceHeaderEntry(position=88, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %88
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.CoordinateUnits"]["descr"] = {1: {
#     1: "Length (meters or feet)",
#     2: "Seconds of arc)}
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.CoordinateUnits"]["descr"][1] = {
#     1: "Length (meters or feet)",
#     2: "Seconds of arc",
#     3: "Decimal degrees",
#     4: "Degrees, minutes, seconds (DMS))
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.WeatheringVelocity] = SEGYTraceHeaderEntry(position=90, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %90
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SubWeatheringVelocity] = SEGYTraceHeaderEntry(position=92, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %92
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceUpholeTime] = SEGYTraceHeaderEntry(position=94, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %94
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GroupUpholeTime] = SEGYTraceHeaderEntry(position=96, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %96
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceStaticCorrection] = SEGYTraceHeaderEntry(position=98, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %98
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GroupStaticCorrection] = SEGYTraceHeaderEntry(position=100, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %100
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TotalStaticApplied] = SEGYTraceHeaderEntry(position=102, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %102
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.LagTimeA] = SEGYTraceHeaderEntry(position=104, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %104
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.LagTimeB] = SEGYTraceHeaderEntry(position=106, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %106
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.DelayRecordingTime] = SEGYTraceHeaderEntry(position=108, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %108
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.MuteTimeStart] = SEGYTraceHeaderEntry(position=110, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %110
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.MuteTimeEND] = SEGYTraceHeaderEntry(position=112, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %112
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.ns] = SEGYTraceHeaderEntry(position=114, type=SEGYTraceHeaderEntryType.uint16)  # 'uint16');  %114
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.dt] = SEGYTraceHeaderEntry(position=116, type=SEGYTraceHeaderEntryType.uint16)  # 'uint16');  %116
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GainType] = SEGYTraceHeaderEntry(position=119, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %118
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GainType"]["descr"] = {0: {
#     1: "Fixes",
#     2: "Binary",
#     3: "Floating point)}
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GainType"]["descr"][1] = SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GainType"]["descr"][0]
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.InstrumentGainConstant] = SEGYTraceHeaderEntry(position=120, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %120
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.InstrumentInitialGain] = SEGYTraceHeaderEntry(position=122, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %%122
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.Correlated] = SEGYTraceHeaderEntry(position=124, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %124
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.Correlated"]["descr"] = {0: {
#     1: "No",
#     2: "Yes)}
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.Correlated"]["descr"][1] = SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.Correlated"]["descr"][0]

SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SweepFrequenceStart] = SEGYTraceHeaderEntry(position=126, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %126
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SweepFrequenceEnd] = SEGYTraceHeaderEntry(position=128, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %128
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SweepLength] = SEGYTraceHeaderEntry(position=130, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %130
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SweepType] = SEGYTraceHeaderEntry(position=132, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %132
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SweepType"]["descr"] = {0: {
#     1: "linear",
#     2: "parabolic",
#     3: "exponential",
#     4: "other)}
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SweepType"]["descr"][1] = SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SweepType"]["descr"][0]

SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SweepTraceTaperLengthStart] = SEGYTraceHeaderEntry(position=134, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %134
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SweepTraceTaperLengthEnd] = SEGYTraceHeaderEntry(position=136, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %136
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TaperType] = SEGYTraceHeaderEntry(position=138, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %138
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TaperType"]["descr"] = {0: {
#     1: "linear",
#     2: "cos2c",
#     3: "other)}
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TaperType"]["descr"][1] = SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TaperType"]["descr"][0]

SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.AliasFilterFrequency] = SEGYTraceHeaderEntry(position=140, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %140
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.AliasFilterSlope] = SEGYTraceHeaderEntry(position=142, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %142
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.NotchFilterFrequency] = SEGYTraceHeaderEntry(position=144, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %144
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.NotchFilterSlope] = SEGYTraceHeaderEntry(position=146, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %146
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.LowCutFrequency] = SEGYTraceHeaderEntry(position=148, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %148
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.HighCutFrequency] = SEGYTraceHeaderEntry(position=150, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %150
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.LowCutSlope] = SEGYTraceHeaderEntry(position=152, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %152
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.HighCutSlope] = SEGYTraceHeaderEntry(position=154, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %154
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.YearDataRecorded] = SEGYTraceHeaderEntry(position=156, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %156
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.DayOfYear] = SEGYTraceHeaderEntry(position=158, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %158
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.HourOfDay] = SEGYTraceHeaderEntry(position=160, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %160
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.MinuteOfHour] = SEGYTraceHeaderEntry(position=162, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %162
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SecondOfMinute] = SEGYTraceHeaderEntry(position=164, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %164
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TimeBaseCode] = SEGYTraceHeaderEntry(position=166, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %166
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TimeBaseCode"]["descr"] = {0: {
#     1: "Local",
#     2: "GMT",
#     3: "Other)}
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TimeBaseCode"]["descr"][1] = {
#     1: "Local",
#     2: "GMT",
#     3: "Other",
#     4: "UTC)
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceWeightningFactor] = SEGYTraceHeaderEntry(position=168, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %170
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GeophoneGroupNumberRoll1] = SEGYTraceHeaderEntry(position=170, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %172
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GeophoneGroupNumberFirstTraceOrigField] = SEGYTraceHeaderEntry(position=172, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %174
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GeophoneGroupNumberLastTraceOrigField] = SEGYTraceHeaderEntry(position=174, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %176
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.GapSize] = SEGYTraceHeaderEntry(position=176, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %178
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.OverTravel] = SEGYTraceHeaderEntry(position=178, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %178
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.OverTravel"]["descr"] = {0: {
#     1: "down (or behind)",
#     2: "up (or ahead)",
#     3: "other)}
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.OverTravel"]["descr"][1] = SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.OverTravel"]["descr"][0]

SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.cdpX] = SEGYTraceHeaderEntry(position=180, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %180
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.cdpY] = SEGYTraceHeaderEntry(position=184, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %184
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.Inline3D] = SEGYTraceHeaderEntry(position=188, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %188
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.Crossline3D] = SEGYTraceHeaderEntry(position=192, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %192
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.ShotPoint] = SEGYTraceHeaderEntry(position=192, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %196
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.ShotPointScalar] = SEGYTraceHeaderEntry(position=200, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %200
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceValueMeasurementUnit] = SEGYTraceHeaderEntry(position=202, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %202
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceValueMeasurementUnit"]["descr"] = {1: {
#     -1: "Other",
#     0: "Unknown (should be described in Data Sample Measurement Units Stanza) ",
#     1: "Pascal (Pa)",
#     2: "Volts (V)",
#     3: "Millivolts (v)",
#     4: "Amperes (A)",
#     5: "Meters (m)",
#     6: "Meters Per Second (m/s)",
#     7: "Meters Per Second squared (m/&s2)Other",
#     8: "Newton (N)",
#     9: "Watt (W))}
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TransductionConstantMantissa] = SEGYTraceHeaderEntry(position=204, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %204
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TransductionConstantPower] = SEGYTraceHeaderEntry(position=208, type=SEGYTraceHeaderEntryType.int16)  # 'int16'); %208
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TransductionUnit] = SEGYTraceHeaderEntry(position=210, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %210
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TransductionUnit"]["descr"] = SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceValueMeasurementUnit"]["descr"]
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.TraceIdentifier] = SEGYTraceHeaderEntry(position=212, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %212
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.ScalarTraceHeader] = SEGYTraceHeaderEntry(position=214, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %214
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceType] = SEGYTraceHeaderEntry(position=216, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %216
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceType"]["descr"] = {1: {
#     -1: "Other (should be described in Source Type/Orientation stanza)",
#     0: "Unknown",
#     1: "Vibratory - Vertical orientation",
#     2: "Vibratory - Cross-line orientation",
#     3: "Vibratory - In-line orientation",
#     4: "Impulsive - Vertical orientation",
#     5: "Impulsive - Cross-line orientation",
#     6: "Impulsive - In-line orientation",
#     7: "Distributed Impulsive - Vertical orientation",
#     8: "Distributed Impulsive - Cross-line orientation",
#     9: "Distributed Impulsive - In-line orientation)}

SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceEnergyDirectionMantissa] = SEGYTraceHeaderEntry(position=218, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %218
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceEnergyDirectionExponent] = SEGYTraceHeaderEntry(position=222, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %222
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceMeasurementMantissa] = SEGYTraceHeaderEntry(position=224, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %224
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceMeasurementExponent] = SEGYTraceHeaderEntry(position=228, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %228
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceMeasurementUnit] = SEGYTraceHeaderEntry(position=230, type=SEGYTraceHeaderEntryType.int16)  # 'int16');  %230
# SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.SourceMeasurementUnit"]["descr"] = {1: {
#     -1: "Other (should be described in Source Measurement Unit stanza)",
#     0: "Unknown",
#     1: "Joule (J)",
#     2: "Kilowatt (kW)",
#     3: "Pascal (Pa)",
#     4: "Bar (Bar)",
#     4: "Bar-meter (Bar-m)",
#     5: "Newton (N)",
#     6: "Kilograms (kg))}
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.UnassignedInt1] = SEGYTraceHeaderEntry(position=232, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %232
SEGY_TRACE_HEADER_ENTRYS[SEGYTraceHeaderEntryName.UnassignedInt2] = SEGYTraceHeaderEntry(position=236, type=SEGYTraceHeaderEntryType.int32)  # 'int32');  %236
