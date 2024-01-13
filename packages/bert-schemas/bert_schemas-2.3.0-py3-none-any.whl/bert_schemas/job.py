# type: ignore
import warnings
from datetime import datetime
from enum import Enum
from typing import Annotated
from uuid import UUID

import scipy as sp
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    computed_field,
    conlist,
    field_validator,
    model_validator,
)
from typing_extensions import TypedDict

from .qpu import QPUBase, QPUName


class JobOrigin(str, Enum):
    WEB = "WEB"
    OQTAPI = "OQTAPI"


class JobType(str, Enum):
    BEC = "BEC"
    BARRIER = "BARRIER"
    BRAGG = "BRAGG"
    TRANSISTOR = "TRANSISTOR"
    PAINT_1D = "PAINT_1D"

    def __str__(self):
        return str(self.value)


class ImageType(str, Enum):
    IN_TRAP = "IN_TRAP"
    TIME_OF_FLIGHT = "TIME_OF_FLIGHT"

    def __str__(self):
        return str(self.value)


class OutputJobType(str, Enum):
    IN_TRAP = "IN_TRAP"
    NON_IN_TRAP = "NON_IN_TRAP"

    def __str__(self):
        return str(self.value)


class JobStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    INCOMPLETE = "INCOMPLETE"

    def __str__(self):
        return str(self.value)


class RfInterpolationType(str, Enum):
    LINEAR = "LINEAR"
    STEP = "STEP"
    OFF = "OFF"
    PREVIOUS = "PREVIOUS"  # assumes value of previous data point

    def __str__(self):
        return str(self.value)


class InterpolationType(str, Enum):
    LINEAR = "LINEAR"
    SMOOTH = "SMOOTH"
    STEP = "STEP"
    OFF = "OFF"
    # native scipy options
    ZERO = "ZERO"  # spline interpolation at zeroth order
    SLINEAR = "SLINEAR"  # spline interpolation at first order
    QUADRATIC = "QUADRATIC"  # spline interpolation at second order
    CUBIC = "CUBIC"  # spline interpolation at third order
    # LINEAR = "LINEAR"         # self explanatory
    NEAREST = "NEAREST"  # assumes value of nearest data point
    PREVIOUS = "PREVIOUS"  # assumes value of previous data point
    NEXT = "NEXT"  # assumes value of next data point

    def __str__(self):
        return str(self.value)


class LaserType(str, Enum):
    TERMINATOR = "TERMINATOR"
    BRAGG = "BRAGG"

    def __str__(self):
        return str(self.value)


class ShapeType(str, Enum):
    GAUSSIAN = "GAUSSIAN"
    LORENTZIAN = "LORENTZIAN"
    SQUARE = "SQUARE"

    def __str__(self):
        return str(self.value)


JobName = Annotated[str, StringConstraints(min_length=1, max_length=50)]

JobNote = Annotated[str, StringConstraints(max_length=500)]


class Image(BaseModel):
    pixels: list[float]
    rows: int
    columns: int
    pixcal: float | None = 1.0
    model_config = ConfigDict(validate_assignment=True)


class Point(TypedDict):
    x: float
    y: float


class LineChart(BaseModel):
    points: list[dict[str, float]]
    model_config = ConfigDict(validate_assignment=True)


class RfEvaporation(BaseModel):
    # times_ms upper range can be no larger than end_time_ms of job (80 ms is upper default)
    times_ms: Annotated[
        list[Annotated[int, Field(ge=-2000, le=80)]],
        Field(min_length=1, max_length=20),
    ] = list(range(-1600, 400, 400))
    frequencies_mhz: Annotated[
        list[Annotated[float, Field(ge=0.0, le=25.0)]],
        Field(min_length=1, max_length=20),
    ]
    powers_mw: Annotated[
        list[Annotated[float, Field(ge=0.0, le=1000.0)]],
        Field(min_length=1, max_length=20),
    ]
    interpolation: RfInterpolationType
    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode="after")
    def cross_validate(self) -> "RfEvaporation":
        assert (
            len(self.times_ms) == len(self.frequencies_mhz) == len(self.powers_mw)
        ), "RfEvaporation data lists must have the same length."

        if self.times_ms != sorted(self.times_ms):
            warnings.warn(
                "Evaporation times_ms list must be naturally ordered, re-ordering.",
                stacklevel=2,
            )
            self.times_ms, self.frequencies_mhz, self.powers_mw = zip(
                *sorted(
                    zip(
                        self.times_ms,
                        self.frequencies_mhz,
                        self.powers_mw,
                    )
                )
            )
        return self


class Landscape(BaseModel):
    # time_ms upper range can be no larger than end_time_ms of job (80 ms is upper default)
    time_ms: Annotated[float, Field(ge=0.0, le=80.0)]
    potentials_khz: Annotated[
        list[Annotated[float, Field(ge=0.0, le=100.0)]],
        Field(min_length=2, max_length=121),
    ]
    positions_um: Annotated[
        list[Annotated[float, Field(ge=-60.0, le=60.0)]],
        Field(min_length=2, max_length=121),
    ]
    spatial_interpolation: InterpolationType

    @model_validator(mode="after")
    def cross_validate(self):
        assert len(self.positions_um) == len(
            self.potentials_khz
        ), "Landscape data lists must have the same length."

        if self.positions_um != sorted(self.positions_um):
            warnings.warn(
                "Landscape positions_um list must be naturally ordered, re-ordering.",
                stacklevel=2,
            )
            self.positions_um, self.potentials_khz = zip(
                *sorted(zip(self.positions_um, self.potentials_khz))
            )
        return self

    def __lt__(self, other):
        return self.time_ms < other.time_ms


class OpticalLandscape(BaseModel):
    interpolation: InterpolationType = InterpolationType.LINEAR
    landscapes: Annotated[list[Landscape], Field(min_length=1, max_length=5)]
    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode="after")
    def cross_validate(self):
        # ensure the individual Landscape objects are far enough apart in time and naturally (time) ordered
        if len(self.landscapes) > 1:
            if sorted(self.landscapes) != self.landscapes:
                self.landscapes = sorted(
                    self.landscapes, key=lambda landscape: landscape.time_ms
                )

            dts_ms = [
                self.landscapes[i + 1].time_ms - self.landscapes[i].time_ms
                for i in range(len(self.landscapes) - 1)
            ]
            assert all(
                dt > 1 for dt in dts_ms
            ), "Constituent Landscape object time_ms values must differ by >= 1 ms"
        return self


class TofFit(BaseModel):
    gaussian_od: float
    gaussian_sigma_x: float
    gaussian_sigma_y: float
    tf_od: float
    tf_x: float
    tf_y: float
    x_0: float
    y_0: float
    offset: float
    model_config = ConfigDict(validate_assignment=True)


class Barrier(BaseModel):
    # times_ms upper range can be no larger than end_time_ms of job (80 ms is upper default)
    times_ms: Annotated[
        list[Annotated[float, Field(ge=0.0, le=80.0)]],
        Field(min_length=2, max_length=20),
    ] = list(sp.arange(1, 12, 1.0))
    positions_um: Annotated[
        list[Annotated[float, Field(ge=-60.0, le=60.0)]],
        Field(min_length=2, max_length=20),
    ] = list(sp.arange(1, 12, 1.0))
    heights_khz: Annotated[
        list[Annotated[float, Field(ge=0.0, le=100.0)]],
        Field(min_length=2, max_length=20),
    ] = [10.0] * 11
    widths_um: Annotated[
        list[Annotated[float, Field(ge=0.5, le=50.0)]],
        Field(min_length=2, max_length=20),
    ] = [1.0] * 11
    interpolation: InterpolationType = InterpolationType.LINEAR
    shape: ShapeType = ShapeType.GAUSSIAN
    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode="after")
    def cross_validate(self):
        assert (
            len(self.times_ms)
            == len(self.positions_um)
            == len(self.heights_khz)
            == len(self.widths_um)
        ), "Barrier data lists must have the same length."

        if self.times_ms != sorted(self.times_ms):
            warnings.warn(
                "Barrier times_ms list must be naturally ordered, re-ordering.",
                stacklevel=2,
            )
            (self.times_ms, self.positions_um, self.heights_khz, self.widths_um,) = zip(
                *sorted(
                    zip(
                        self.times_ms,
                        self.positions_um,
                        self.heights_khz,
                        self.widths_um,
                    )
                )
            )
        return self


class Pulse(BaseModel):
    # times_ms upper range can be no larger than end_time_ms of job (80.0 ms is upper default)
    times_ms: Annotated[
        list[Annotated[float, Field(ge=0.0, le=80.0)]],
        Field(min_length=1, max_length=10),
    ]
    intensities_mw_per_cm2: Annotated[
        list[Annotated[float, Field(ge=0.0, le=1000.0)]],
        Field(min_length=1, max_length=10),
    ]
    detuning_mhz: Annotated[float, Field(ge=-100.0, le=100.0)]
    interpolation: InterpolationType
    model_config = ConfigDict(validate_assignment=True)

    @model_validator(mode="before")
    @classmethod
    def cross_validate(cls, values):
        assert len(values["times_ms"]) == len(
            values["intensities_mw_per_cm2"]
        ), "Pulse data lists must have the same length."
        return values

    @field_validator("times_ms")
    @classmethod
    def naturally_order_times(cls, v):
        assert v == sorted(v), "Pulse times must be naturally ordered."
        return v

    def __lt__(self, other):
        return min(self.times_ms) < min(other.times_ms)


class Laser(BaseModel):
    type: LaserType
    pulses: Annotated[list[Pulse], Field(min_length=1, max_length=10)]
    model_config = ConfigDict(validate_assignment=True)

    @field_validator("pulses")
    @classmethod
    def pulses_overlap(cls, v):
        for index, pulse in enumerate(v):
            if index < len(v) - 1:
                dt_ms = min(v[index + 1].times_ms) - max(v[index].times_ms)
                assert (
                    dt_ms >= 1
                ), "Distinct pulses features too close together in time (< 1 ms)"
        return v


class NonPlotOutput(BaseModel):
    mot_fluorescence_image: Image
    tof_image: Image
    tof_fit_image: Image
    tof_fit: TofFit
    tof_x_slice: LineChart
    tof_y_slice: LineChart
    total_mot_atom_number: int
    tof_atom_number: int
    thermal_atom_number: int
    condensed_atom_number: int
    temperature_nk: int
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)


class PlotOutput(BaseModel):
    it_plot: Image
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)


class Output(BaseModel):
    input_id: int | None = None
    values: PlotOutput | NonPlotOutput
    model_config = ConfigDict(validate_assignment=True)


class JobOutput(Output):
    ...


class BecOutput(Output):
    values: NonPlotOutput


class BarrierOutput(Output):
    values: NonPlotOutput | PlotOutput


class InputValues(BaseModel):
    end_time_ms: Annotated[int, Field(ge=0, le=80)]
    image_type: ImageType
    time_of_flight_ms: Annotated[int, Field(ge=2, le=20)]
    rf_evaporation: RfEvaporation
    optical_barriers: Annotated[
        list[Barrier], Field(min_length=1, max_length=5)
    ] | None = None
    optical_landscape: OpticalLandscape | None = None
    lasers: Annotated[list[Laser], Field(min_length=1, max_length=1)] | None = None

    @model_validator(mode="after")
    def cross_validate(self):
        if list(
            filter(
                lambda time_ms: time_ms > self.end_time_ms,
                self.rf_evaporation.times_ms,
            )
        ):
            raise ValueError(
                "rf_evaporation.times_ms max values cannot exceed end_time_ms"
            )
        if self.optical_barriers:
            for index, optical_barrier in enumerate(self.optical_barriers):
                if list(
                    filter(
                        lambda time_ms: time_ms > self.end_time_ms,
                        optical_barrier.times_ms,
                    )
                ):
                    raise ValueError(
                        f"optical_barriers[{index}].times_ms max values cannot exceed end_time_ms"
                    )
        if self.optical_landscape:
            for index, landscape in enumerate(self.optical_landscape.landscapes):
                if landscape.time_ms > self.end_time_ms:
                    raise ValueError(
                        f"optical_landscape.landscapes[{index}].time_ms max value cannot exceed end_time_ms"
                    )
        if self.lasers:
            for laser_index, laser in enumerate(self.lasers):
                for pulse_index, pulse in enumerate(laser.pulses):
                    if list(
                        filter(
                            lambda time_ms: time_ms > self.end_time_ms,
                            pulse.times_ms,
                        )
                    ):
                        raise ValueError(
                            f"lasers[{laser_index}].pulses[{pulse_index}].times_ms max values cannot exceed end_time_ms"
                        )
        return self


class Input(BaseModel):
    job_id: int | None = None
    run: int | None = None
    values: InputValues
    output: Output | None = None
    notes: JobNote | None = None
    model_config = ConfigDict(validate_assignment=True)


class InputWithoutOutput(Input):
    output: Output = Field(exclude=True)


class JobBase(BaseModel):
    name: JobName
    origin: JobOrigin | None = None
    status: JobStatus = JobStatus.PENDING
    display: bool = True
    qpu_name: QPUName = QPUName.UNDEFINED
    model_config = ConfigDict(use_enum_values=True, validate_assignment=True)


# needed for post fixtures
class JobPost(JobBase):
    inputs: conlist(
        Input,
        min_length=1,
        max_length=30,
    )


class JobCreate(JobBase):
    inputs: conlist(
        Input,
        min_length=1,
        max_length=30,
    )

    @computed_field
    @property
    def job_type(self) -> JobType:
        input_values = self.inputs[0].values
        if input_values.optical_landscape:
            return JobType.PAINT_1D
        elif (
            input_values.optical_barriers
            or input_values.image_type == ImageType.IN_TRAP
        ):
            return JobType.BARRIER
        else:
            return JobType.BEC

    @computed_field
    @property
    def input_count(self) -> int:
        return len(self.inputs)

    @model_validator(mode="after")
    def run(self):
        for i, _ in enumerate(self.inputs):
            if not self.inputs[i].run:
                self.inputs[i].run = i + 1
        return self


class ResponseInput(BaseModel):
    job_id: int | None = None
    run: int | None = None
    values: object
    # values: InputValues
    output: JobOutput | None = None
    notes: JobNote | None = None
    model_config = ConfigDict(from_attributes=True)


class JobResponse(JobBase):
    external_id: UUID
    job_type: JobType
    input_count: int | None = None
    status: JobStatus
    qpu: QPUBase | None = None
    time_submit: datetime
    time_start: datetime | None = None
    time_complete: datetime | None = None
    inputs: list[ResponseInput]
    failed_inputs: list[int] = []


class JobInputsResponse(JobResponse):
    qpu_name: QPUName = QPUName.UNDEFINED
    inputs: list[InputWithoutOutput]


class PaginatedJobsResponse(JobBase):
    job_type: JobType
    external_id: UUID
    time_submit: datetime
    time_start: datetime | None = None
    time_complete: datetime | None = None
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)


class Job(JobBase):
    job_id: UUID
    status: JobStatus = JobStatus.PENDING
    display: bool = True


class ExternalId(BaseModel):
    id: UUID


class UpdateJobDisplay(BaseModel):
    job_external_id: UUID
    display: bool = True
    model_config = ConfigDict(validate_assignment=True)


class JobCreateResponse(BaseModel):
    job_id: UUID
    queue_position: int
    est_time: int


class JobExternalIdsList(BaseModel):
    external_ids: list[UUID]
