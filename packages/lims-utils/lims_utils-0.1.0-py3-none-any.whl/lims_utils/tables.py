# ruff: noqa: E501
# type: ignore

from sqlalchemy import (
    BINARY,
    DECIMAL,
    TIMESTAMP,
    Column,
    Computed,
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKeyConstraint,
    Index,
    LargeBinary,
    String,
    Table,
    Text,
    Time,
    text,
)
from sqlalchemy.dialects.mysql import (
    INTEGER,
    LONGBLOB,
    LONGTEXT,
    MEDIUMINT,
    MEDIUMTEXT,
    SMALLINT,
    TINYINT,
    TINYTEXT,
    VARCHAR,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


metadata = Base.metadata


class AdminActivity(Base):
    __tablename__ = "AdminActivity"
    __table_args__ = (
        Index("AdminActivity_FKAction", "action"),
        Index("username", "username", unique=True),
    )

    adminActivityId = Column(INTEGER(11), primary_key=True)
    username = Column(String(45), nullable=False, server_default=text("''"))
    action = Column(String(45))
    comments = Column(String(100))
    dateTime = Column(DateTime)


class AdminVar(Base):
    __tablename__ = "AdminVar"
    __table_args__ = (
        Index("AdminVar_FKIndexName", "name"),
        Index("AdminVar_FKIndexValue", "value"),
        {"comment": "ISPyB administration values"},
    )

    varId = Column(INTEGER(11), primary_key=True)
    name = Column(String(32))
    value = Column(String(1024))


class Aperture(Base):
    __tablename__ = "Aperture"

    apertureId = Column(INTEGER(10), primary_key=True)
    sizeX = Column(Float)


class AutoProc(Base):
    __tablename__ = "AutoProc"
    __table_args__ = (
        Index("AutoProc_FKIndex1", "autoProcProgramId"),
        Index(
            "AutoProc_refined_unit_cell",
            "refinedCell_a",
            "refinedCell_b",
            "refinedCell_c",
            "refinedCell_alpha",
            "refinedCell_beta",
            "refinedCell_gamma",
            "spaceGroup",
        ),
    )

    autoProcId = Column(
        INTEGER(10), primary_key=True, comment="Primary key (auto-incremented)"
    )
    autoProcProgramId = Column(INTEGER(10), comment="Related program item")
    spaceGroup = Column(String(45), comment="Space group")
    refinedCell_a = Column(Float, comment="Refined cell")
    refinedCell_b = Column(Float, comment="Refined cell")
    refinedCell_c = Column(Float, comment="Refined cell")
    refinedCell_alpha = Column(Float, comment="Refined cell")
    refinedCell_beta = Column(Float, comment="Refined cell")
    refinedCell_gamma = Column(Float, comment="Refined cell")
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")

    AutoProcScaling = relationship("AutoProcScaling", back_populates="AutoProc_")


class AutoProcProgram(Base):
    __tablename__ = "AutoProcProgram"
    __table_args__ = (
        ForeignKeyConstraint(
            ["processingJobId"],
            ["ProcessingJob.processingJobId"],
            name="AutoProcProgram_FK2",
        ),
        Index("AutoProcProgram_FK2", "processingJobId"),
    )

    autoProcProgramId = Column(
        INTEGER(10), primary_key=True, comment="Primary key (auto-incremented)"
    )
    processingCommandLine = Column(
        String(255), comment="Command line for running the automatic processing"
    )
    processingPrograms = Column(
        String(255), comment="Processing programs (comma separated)"
    )
    processingStatus = Column(TINYINT(1), comment="success (1) / fail (0)")
    processingMessage = Column(String(255), comment="warning, error,...")
    processingStartTime = Column(DateTime, comment="Processing start time")
    processingEndTime = Column(DateTime, comment="Processing end time")
    processingEnvironment = Column(String(255), comment="Cpus, Nodes,...")
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")
    processingJobId = Column(INTEGER(11))

    ProcessingJob = relationship("ProcessingJob", back_populates="AutoProcProgram_")
    Screening = relationship("Screening", back_populates="AutoProcProgram_")
    AutoProcIntegration = relationship(
        "AutoProcIntegration", back_populates="AutoProcProgram_"
    )
    AutoProcProgramAttachment = relationship(
        "AutoProcProgramAttachment", back_populates="AutoProcProgram_"
    )
    AutoProcProgramMessage = relationship(
        "AutoProcProgramMessage", back_populates="AutoProcProgram_"
    )
    PDBEntry = relationship("PDBEntry", back_populates="AutoProcProgram_")
    Tomogram = relationship("Tomogram", back_populates="AutoProcProgram_")
    zc_ZocaloBuffer = relationship("ZcZocaloBuffer", back_populates="AutoProcProgram_")
    MXMRRun = relationship("MXMRRun", back_populates="AutoProcProgram_")
    MotionCorrection = relationship(
        "MotionCorrection", back_populates="AutoProcProgram_"
    )
    PDBEntry_has_AutoProcProgram = relationship(
        "PDBEntryHasAutoProcProgram", back_populates="AutoProcProgram_"
    )
    CTF = relationship("CTF", back_populates="AutoProcProgram_")
    ParticlePicker = relationship("ParticlePicker", back_populates="AutoProcProgram_")
    RelativeIceThickness = relationship(
        "RelativeIceThickness", back_populates="AutoProcProgram_"
    )
    ParticleClassificationGroup = relationship(
        "ParticleClassificationGroup", back_populates="AutoProcProgram_"
    )
    XRFFluorescenceMapping = relationship(
        "XRFFluorescenceMapping", back_populates="AutoProcProgram_"
    )


class BFAutomationError(Base):
    __tablename__ = "BF_automationError"

    automationErrorId = Column(INTEGER(10), primary_key=True)
    errorType = Column(String(40), nullable=False)
    solution = Column(Text)

    BF_automationFault = relationship(
        "BFAutomationFault", back_populates="BF_automationError"
    )


class BFSystem(Base):
    __tablename__ = "BF_system"

    systemId = Column(INTEGER(10), primary_key=True)
    name = Column(String(100))
    description = Column(String(200))

    BF_component = relationship("BFComponent", back_populates="BF_system")
    BF_system_beamline = relationship("BFSystemBeamline", back_populates="BF_system")


class BLSample(Base):
    __tablename__ = "BLSample"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSubSampleId"], ["BLSubSample.blSubSampleId"], name="BLSample_ibfk4"
        ),
        ForeignKeyConstraint(
            ["containerId"],
            ["Container.containerId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSample_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["crystalId"],
            ["Crystal.crystalId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSample_ibfk_2",
        ),
        ForeignKeyConstraint(
            ["diffractionPlanId"],
            ["DiffractionPlan.diffractionPlanId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSample_ibfk_3",
        ),
        ForeignKeyConstraint(
            ["screenComponentGroupId"],
            ["ScreenComponentGroup.screenComponentGroupId"],
            name="BLSample_fk5",
        ),
        Index("BLSampleImage_idx1", "blSubSampleId"),
        Index("BLSample_FKIndex1", "containerId"),
        Index("BLSample_FKIndex3", "diffractionPlanId"),
        Index("BLSample_FKIndex_Status", "blSampleStatus"),
        Index("BLSample_Index1", "name"),
        Index("BLSample_fk5", "screenComponentGroupId"),
        Index("crystalId", "crystalId", "containerId"),
    )

    blSampleId = Column(INTEGER(10), primary_key=True)
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    diffractionPlanId = Column(INTEGER(10))
    crystalId = Column(INTEGER(10))
    containerId = Column(INTEGER(10))
    name = Column(String(45))
    code = Column(String(45))
    location = Column(String(45))
    holderLength = Column(Float(asdecimal=True))
    loopLength = Column(Float(asdecimal=True))
    loopType = Column(String(45))
    wireWidth = Column(Float(asdecimal=True))
    comments = Column(String(1024))
    completionStage = Column(String(45))
    structureStage = Column(String(45))
    publicationStage = Column(String(45))
    publicationComments = Column(String(255))
    blSampleStatus = Column(String(20))
    isInSampleChanger = Column(TINYINT(1))
    lastKnownCenteringPosition = Column(String(255))
    POSITIONID = Column(INTEGER(11))
    SMILES = Column(
        String(400),
        comment="the symbolic description of the structure of a chemical compound",
    )
    blSubSampleId = Column(INTEGER(11))
    lastImageURL = Column(String(255))
    screenComponentGroupId = Column(INTEGER(11))
    volume = Column(Float)
    dimension1 = Column(Float(asdecimal=True))
    dimension2 = Column(Float(asdecimal=True))
    dimension3 = Column(Float(asdecimal=True))
    shape = Column(String(15))
    packingFraction = Column(Float)
    preparationTemeprature = Column(
        MEDIUMINT(9), comment="Sample preparation temperature, Units: kelvin"
    )
    preparationHumidity = Column(Float, comment="Sample preparation humidity, Units: %")
    blottingTime = Column(INTEGER(11), comment="Blotting time, Units: sec")
    blottingForce = Column(Float, comment="Force used when blotting sample, Units: N?")
    blottingDrainTime = Column(
        INTEGER(11), comment="Time sample left to drain after blotting, Units: sec"
    )
    support = Column(String(50), comment="Sample support material")
    subLocation = Column(
        SMALLINT(5),
        comment="Indicates the sample's location on a multi-sample pin, where 1 is closest to the pin base",
    )
    staffComments = Column(String(255), comment="Any staff comments on the sample")

    BLSubSample = relationship(
        "BLSubSample", foreign_keys=[blSubSampleId], back_populates="BLSample_"
    )
    Container = relationship("Container", back_populates="BLSample_")
    Crystal = relationship("Crystal", back_populates="BLSample_")
    DiffractionPlan = relationship("DiffractionPlan", back_populates="BLSample_")
    ScreenComponentGroup = relationship(
        "ScreenComponentGroup", back_populates="BLSample_"
    )
    Project = relationship(
        "Project", secondary="Project_has_BLSample", back_populates="BLSample_"
    )
    BLSampleImage = relationship("BLSampleImage", back_populates="BLSample_")
    BLSubSample_ = relationship(
        "BLSubSample",
        foreign_keys="[BLSubSample.blSampleId]",
        back_populates="BLSample1",
    )
    BLSample_has_Positioner = relationship(
        "BLSampleHasPositioner", back_populates="BLSample_"
    )
    XRFFluorescenceMappingROI = relationship(
        "XRFFluorescenceMappingROI", back_populates="BLSample_"
    )
    BLSampleGroup_has_BLSample = relationship(
        "BLSampleGroupHasBLSample", back_populates="BLSample_"
    )
    BLSample_has_DataCollectionPlan = relationship(
        "BLSampleHasDataCollectionPlan", back_populates="BLSample_"
    )
    DataCollectionGroup = relationship(
        "DataCollectionGroup", back_populates="BLSample_"
    )
    EnergyScan = relationship("EnergyScan", back_populates="BLSample_")
    RobotAction = relationship("RobotAction", back_populates="BLSample_")
    SampleComposition = relationship("SampleComposition", back_populates="BLSample_")
    XFEFluorescenceSpectrum = relationship(
        "XFEFluorescenceSpectrum", back_populates="BLSample_"
    )
    BLSample_has_EnergyScan = relationship(
        "BLSampleHasEnergyScan", back_populates="BLSample_"
    )
    ContainerQueueSample = relationship(
        "ContainerQueueSample", back_populates="BLSample_"
    )


class BLSampleImage(Base):
    __tablename__ = "BLSampleImage"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"], ["BLSample.blSampleId"], name="BLSampleImage_fk1"
        ),
        ForeignKeyConstraint(
            ["blSampleImageScoreId"],
            ["BLSampleImageScore.blSampleImageScoreId"],
            onupdate="CASCADE",
            name="BLSampleImage_fk3",
        ),
        ForeignKeyConstraint(
            ["containerInspectionId"],
            ["ContainerInspection.containerInspectionId"],
            name="BLSampleImage_fk2",
        ),
        Index("BLSampleImage_fk2", "containerInspectionId"),
        Index("BLSampleImage_fk3", "blSampleImageScoreId"),
        Index("BLSampleImage_idx1", "blSampleId"),
        Index("BLSampleImage_imageFullPath", "imageFullPath", unique=True),
    )

    blSampleImageId = Column(INTEGER(11), primary_key=True)
    blSampleId = Column(INTEGER(11), nullable=False)
    offsetX = Column(
        INTEGER(11),
        nullable=False,
        server_default=text("0"),
        comment="The x offset of the image relative to the canvas",
    )
    offsetY = Column(
        INTEGER(11),
        nullable=False,
        server_default=text("0"),
        comment="The y offset of the image relative to the canvas",
    )
    micronsPerPixelX = Column(Float)
    micronsPerPixelY = Column(Float)
    imageFullPath = Column(String(255))
    blSampleImageScoreId = Column(INTEGER(11))
    comments = Column(String(255))
    blTimeStamp = Column(DateTime)
    containerInspectionId = Column(INTEGER(11))
    modifiedTimeStamp = Column(DateTime)

    BLSample_ = relationship("BLSample", back_populates="BLSampleImage")
    BLSampleImageScore = relationship(
        "BLSampleImageScore", back_populates="BLSampleImage_"
    )
    ContainerInspection = relationship(
        "ContainerInspection", back_populates="BLSampleImage_"
    )
    BLSubSample = relationship("BLSubSample", back_populates="BLSampleImage_")
    BLSampleImageAnalysis = relationship(
        "BLSampleImageAnalysis", back_populates="BLSampleImage_"
    )
    BLSampleImageMeasurement = relationship(
        "BLSampleImageMeasurement", back_populates="BLSampleImage_"
    )
    BLSampleImage_has_Positioner = relationship(
        "BLSampleImageHasPositioner", back_populates="BLSampleImage_"
    )
    BLSampleImage_has_AutoScoreClass = relationship(
        "BLSampleImageHasAutoScoreClass", back_populates="BLSampleImage_"
    )


class BLSampleImageAutoScoreSchema(Base):
    __tablename__ = "BLSampleImageAutoScoreSchema"
    __table_args__ = {"comment": "Scoring schema name and whether it is enabled"}

    blSampleImageAutoScoreSchemaId = Column(TINYINT(3), primary_key=True)
    schemaName = Column(
        String(25), nullable=False, comment="Name of the schema e.g. Hampton, MARCO"
    )
    enabled = Column(
        TINYINT(1),
        server_default=text("1"),
        comment="Whether this schema is enabled (could be configurable in the UI)",
    )

    BLSampleImageAutoScoreClass = relationship(
        "BLSampleImageAutoScoreClass", back_populates="BLSampleImageAutoScoreSchema_"
    )


class BLSampleImageScore(Base):
    __tablename__ = "BLSampleImageScore"

    blSampleImageScoreId = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))
    score = Column(Float)
    colour = Column(String(15))

    BLSampleImage_ = relationship("BLSampleImage", back_populates="BLSampleImageScore")


class BLSampleType(Base):
    __tablename__ = "BLSampleType"

    blSampleTypeId = Column(INTEGER(10), primary_key=True)
    name = Column(String(100))
    proposalType = Column(String(10))
    active = Column(
        TINYINT(1), server_default=text("1"), comment="1=active, 0=inactive"
    )

    BLSampleGroup_has_BLSample = relationship(
        "BLSampleGroupHasBLSample", back_populates="BLSampleType_"
    )


class BLSubSample(Base):
    __tablename__ = "BLSubSample"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"],
            ["BLSample.blSampleId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSubSample_blSamplefk_1",
        ),
        ForeignKeyConstraint(
            ["blSampleImageId"],
            ["BLSampleImage.blSampleImageId"],
            name="BLSubSample_blSampleImagefk_1",
        ),
        ForeignKeyConstraint(
            ["diffractionPlanId"],
            ["DiffractionPlan.diffractionPlanId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSubSample_diffractionPlanfk_1",
        ),
        ForeignKeyConstraint(
            ["motorPositionId"],
            ["MotorPosition.motorPositionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSubSample_motorPositionfk_1",
        ),
        ForeignKeyConstraint(
            ["position2Id"],
            ["Position.positionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSubSample_positionfk_2",
        ),
        ForeignKeyConstraint(
            ["positionId"],
            ["Position.positionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSubSample_positionfk_1",
        ),
        Index("BLSubSample_FKIndex1", "blSampleId"),
        Index("BLSubSample_FKIndex2", "diffractionPlanId"),
        Index("BLSubSample_FKIndex3", "positionId"),
        Index("BLSubSample_FKIndex4", "motorPositionId"),
        Index("BLSubSample_FKIndex5", "position2Id"),
        Index("BLSubSample_blSampleImagefk_1", "blSampleImageId"),
    )

    blSubSampleId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    blSampleId = Column(INTEGER(10), nullable=False, comment="sample")
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    diffractionPlanId = Column(INTEGER(10), comment="eventually diffractionPlan")
    blSampleImageId = Column(INTEGER(11))
    positionId = Column(INTEGER(11), comment="position of the subsample")
    position2Id = Column(INTEGER(11))
    motorPositionId = Column(INTEGER(11), comment="motor position")
    blSubSampleUUID = Column(String(45), comment="uuid of the blsubsample")
    imgFileName = Column(String(255), comment="image filename")
    imgFilePath = Column(String(1024), comment="url image")
    comments = Column(String(1024), comment="comments")
    source = Column(Enum("manual", "auto"), server_default=text("'manual'"))
    type = Column(
        String(10),
        comment="The type of subsample, i.e. roi (region), poi (point), loi (line)",
    )

    BLSample_ = relationship(
        "BLSample",
        foreign_keys="[BLSample.blSubSampleId]",
        back_populates="BLSubSample",
    )
    BLSample1 = relationship(
        "BLSample", foreign_keys=[blSampleId], back_populates="BLSubSample_"
    )
    BLSampleImage_ = relationship("BLSampleImage", back_populates="BLSubSample")
    DiffractionPlan = relationship("DiffractionPlan", back_populates="BLSubSample_")
    MotorPosition = relationship("MotorPosition", back_populates="BLSubSample_")
    Position = relationship(
        "Position", foreign_keys=[position2Id], back_populates="BLSubSample_"
    )
    Position_ = relationship(
        "Position", foreign_keys=[positionId], back_populates="BLSubSample1"
    )
    DataCollection = relationship("DataCollection", back_populates="BLSubSample_")
    BLSampleImageMeasurement = relationship(
        "BLSampleImageMeasurement", back_populates="BLSubSample_"
    )
    BLSubSample_has_Positioner = relationship(
        "BLSubSampleHasPositioner", back_populates="BLSubSample_"
    )
    EnergyScan = relationship("EnergyScan", back_populates="BLSubSample_")
    XFEFluorescenceSpectrum = relationship(
        "XFEFluorescenceSpectrum", back_populates="BLSubSample_"
    )
    ContainerQueueSample = relationship(
        "ContainerQueueSample", back_populates="BLSubSample_"
    )


class BeamCalendar(Base):
    __tablename__ = "BeamCalendar"

    beamCalendarId = Column(INTEGER(10), primary_key=True)
    run = Column(String(7), nullable=False)
    beamStatus = Column(String(24), nullable=False)
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=False)

    BLSession = relationship("BLSession", back_populates="BeamCalendar_")


class BeamlineStats(Base):
    __tablename__ = "BeamlineStats"

    beamlineStatsId = Column(INTEGER(11), primary_key=True)
    beamline = Column(String(10))
    recordTimeStamp = Column(DateTime)
    ringCurrent = Column(Float)
    energy = Column(Float)
    gony = Column(Float)
    beamW = Column(Float)
    beamH = Column(Float)
    flux = Column(Float(asdecimal=True))
    scanFileW = Column(String(255))
    scanFileH = Column(String(255))

    BeamApertures = relationship("BeamApertures", back_populates="BeamlineStats_")
    BeamCentres = relationship("BeamCentres", back_populates="BeamlineStats_")


class CalendarHash(Base):
    __tablename__ = "CalendarHash"
    __table_args__ = {
        "comment": "Lets people get to their calendars without logging in using a "
        "private (hash) url"
    }

    calendarHashId = Column(INTEGER(10), primary_key=True)
    ckey = Column(String(50))
    hash = Column(String(128))
    beamline = Column(TINYINT(1))


class ComponentSubType(Base):
    __tablename__ = "ComponentSubType"

    componentSubTypeId = Column(INTEGER(11), primary_key=True)
    name = Column(String(31), nullable=False)
    hasPh = Column(TINYINT(1), server_default=text("0"))
    proposalType = Column(String(10))
    active = Column(
        TINYINT(1), server_default=text("1"), comment="1=active, 0=inactive"
    )

    Protein = relationship(
        "Protein", secondary="Component_has_SubType", back_populates="ComponentSubType_"
    )


class ComponentType(Base):
    __tablename__ = "ComponentType"

    componentTypeId = Column(INTEGER(11), primary_key=True)
    name = Column(String(31), nullable=False)

    Component = relationship("Component", back_populates="ComponentType_")
    Protein = relationship("Protein", back_populates="ComponentType_")


class ConcentrationType(Base):
    __tablename__ = "ConcentrationType"

    concentrationTypeId = Column(INTEGER(11), primary_key=True)
    name = Column(String(31), nullable=False)
    symbol = Column(String(8), nullable=False)
    proposalType = Column(String(10))
    active = Column(
        TINYINT(1), server_default=text("1"), comment="1=active, 0=inactive"
    )

    Protein = relationship("Protein", back_populates="ConcentrationType_")
    SampleComposition = relationship(
        "SampleComposition", back_populates="ConcentrationType_"
    )
    CrystalComposition = relationship(
        "CrystalComposition", back_populates="ConcentrationType_"
    )


class ContainerRegistry(Base):
    __tablename__ = "ContainerRegistry"

    containerRegistryId = Column(INTEGER(11), primary_key=True)
    barcode = Column(String(20))
    comments = Column(String(255))
    recordTimestamp = Column(DateTime, server_default=text("current_timestamp()"))

    ContainerReport = relationship(
        "ContainerReport", back_populates="ContainerRegistry_"
    )
    ContainerRegistry_has_Proposal = relationship(
        "ContainerRegistryHasProposal", back_populates="ContainerRegistry_"
    )
    Container = relationship("Container", back_populates="ContainerRegistry_")


class ContainerType(Base):
    __tablename__ = "ContainerType"
    __table_args__ = {"comment": "A lookup table for different types of containers"}

    containerTypeId = Column(INTEGER(10), primary_key=True)
    name = Column(String(100))
    proposalType = Column(String(10))
    active = Column(
        TINYINT(1), server_default=text("1"), comment="1=active, 0=inactive"
    )
    capacity = Column(INTEGER(11))
    wellPerRow = Column(SMALLINT(6))
    dropPerWellX = Column(SMALLINT(6))
    dropPerWellY = Column(SMALLINT(6))
    dropHeight = Column(Float)
    dropWidth = Column(Float)
    dropOffsetX = Column(Float)
    dropOffsetY = Column(Float)
    wellDrop = Column(SMALLINT(6))

    Container = relationship("Container", back_populates="ContainerType_")


class CryoemInitialModel(Base):
    __tablename__ = "CryoemInitialModel"
    __table_args__ = {"comment": "Initial cryo-EM model generation results"}

    cryoemInitialModelId = Column(INTEGER(10), primary_key=True)
    resolution = Column(Float, comment="Unit: Angstroms")
    numberOfParticles = Column(INTEGER(10))

    ParticleClassification = relationship(
        "ParticleClassification",
        secondary="ParticleClassification_has_CryoemInitialModel",
        back_populates="CryoemInitialModel_",
    )


class DataAcquisition(Base):
    __tablename__ = "DataAcquisition"

    dataAcquisitionId = Column(INTEGER(10), primary_key=True)
    sampleCellId = Column(INTEGER(10), nullable=False)
    framesCount = Column(String(45))
    energy = Column(String(45))
    waitTime = Column(String(45))
    detectorDistance = Column(String(45))


class DataCollection(Base):
    __tablename__ = "DataCollection"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSubSampleId"],
            ["BLSubSample.blSubSampleId"],
            name="DataCollection_ibfk_8",
        ),
        ForeignKeyConstraint(
            ["dataCollectionGroupId"],
            ["DataCollectionGroup.dataCollectionGroupId"],
            name="DataCollection_ibfk_3",
        ),
        ForeignKeyConstraint(
            ["dataCollectionPlanId"],
            ["DiffractionPlan.diffractionPlanId"],
            name="DataCollection_dataCollectionPlanId",
        ),
        ForeignKeyConstraint(
            ["detectorId"], ["Detector.detectorId"], name="DataCollection_ibfk_2"
        ),
        ForeignKeyConstraint(
            ["endPositionId"],
            ["MotorPosition.motorPositionId"],
            name="DataCollection_ibfk_7",
        ),
        ForeignKeyConstraint(
            ["startPositionId"],
            ["MotorPosition.motorPositionId"],
            name="DataCollection_ibfk_6",
        ),
        ForeignKeyConstraint(
            ["strategySubWedgeOrigId"],
            ["ScreeningStrategySubWedge.screeningStrategySubWedgeId"],
            name="DataCollection_ibfk_1",
        ),
        Index("DataCollection_FKIndex0", "BLSAMPLEID"),
        Index("DataCollection_FKIndex00", "SESSIONID"),
        Index("DataCollection_FKIndex1", "dataCollectionGroupId"),
        Index("DataCollection_FKIndex2", "strategySubWedgeOrigId"),
        Index("DataCollection_FKIndex3", "detectorId"),
        Index("DataCollection_FKIndexDCNumber", "dataCollectionNumber"),
        Index("DataCollection_FKIndexImageDirectory", "imageDirectory"),
        Index("DataCollection_FKIndexImagePrefix", "imagePrefix"),
        Index("DataCollection_FKIndexStartTime", "startTime"),
        Index(
            "DataCollection_dataCollectionGroupId_startTime",
            "dataCollectionGroupId",
            "startTime",
        ),
        Index("DataCollection_dataCollectionPlanId", "dataCollectionPlanId"),
        Index("blSubSampleId", "blSubSampleId"),
        Index("endPositionId", "endPositionId"),
        Index("startPositionId", "startPositionId"),
    )

    dataCollectionId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    dataCollectionGroupId = Column(
        INTEGER(11), nullable=False, comment="references DataCollectionGroup table"
    )
    BLSAMPLEID = Column(INTEGER(11))
    SESSIONID = Column(INTEGER(11), server_default=text("0"))
    experimenttype = Column(String(24))
    dataCollectionNumber = Column(INTEGER(10))
    startTime = Column(DateTime, comment="Start time of the dataCollection")
    endTime = Column(DateTime, comment="end time of the dataCollection")
    runStatus = Column(String(45))
    axisStart = Column(Float)
    axisEnd = Column(Float)
    axisRange = Column(Float)
    overlap = Column(Float)
    numberOfImages = Column(INTEGER(10))
    startImageNumber = Column(INTEGER(10))
    numberOfPasses = Column(INTEGER(10))
    exposureTime = Column(Float)
    imageDirectory = Column(
        String(255),
        comment="The directory where files reside - should end with a slash",
    )
    imagePrefix = Column(String(45))
    imageSuffix = Column(String(45))
    imageContainerSubPath = Column(
        String(255),
        comment="Internal path of a HDF5 file pointing to the data for this data collection",
    )
    fileTemplate = Column(String(255))
    wavelength = Column(Float)
    resolution = Column(Float)
    detectorDistance = Column(Float)
    xBeam = Column(Float)
    yBeam = Column(Float)
    comments = Column(String(1024))
    printableForReport = Column(TINYINT(1), server_default=text("1"))
    CRYSTALCLASS = Column(String(20))
    slitGapVertical = Column(Float)
    slitGapHorizontal = Column(Float)
    transmission = Column(Float)
    synchrotronMode = Column(String(20))
    xtalSnapshotFullPath1 = Column(String(255))
    xtalSnapshotFullPath2 = Column(String(255))
    xtalSnapshotFullPath3 = Column(String(255))
    xtalSnapshotFullPath4 = Column(String(255))
    rotationAxis = Column(Enum("Omega", "Kappa", "Phi"))
    phiStart = Column(Float)
    kappaStart = Column(Float)
    omegaStart = Column(Float)
    chiStart = Column(Float)
    resolutionAtCorner = Column(Float)
    detector2Theta = Column(Float)
    DETECTORMODE = Column(String(255))
    undulatorGap1 = Column(Float)
    undulatorGap2 = Column(Float)
    undulatorGap3 = Column(Float)
    beamSizeAtSampleX = Column(Float)
    beamSizeAtSampleY = Column(Float)
    centeringMethod = Column(String(255))
    averageTemperature = Column(Float)
    ACTUALSAMPLEBARCODE = Column(String(45))
    ACTUALSAMPLESLOTINCONTAINER = Column(INTEGER(11))
    ACTUALCONTAINERBARCODE = Column(String(45))
    ACTUALCONTAINERSLOTINSC = Column(INTEGER(11))
    actualCenteringPosition = Column(String(255))
    beamShape = Column(String(45))
    POSITIONID = Column(INTEGER(11))
    detectorId = Column(INTEGER(11), comment="references Detector table")
    FOCALSPOTSIZEATSAMPLEX = Column(Float)
    POLARISATION = Column(Float)
    FOCALSPOTSIZEATSAMPLEY = Column(Float)
    APERTUREID = Column(INTEGER(11))
    screeningOrigId = Column(INTEGER(11))
    startPositionId = Column(INTEGER(11))
    endPositionId = Column(INTEGER(11))
    flux = Column(Float(asdecimal=True))
    strategySubWedgeOrigId = Column(
        INTEGER(10), comment="references ScreeningStrategySubWedge table"
    )
    blSubSampleId = Column(INTEGER(11))
    flux_end = Column(Float(asdecimal=True), comment="flux measured after the collect")
    bestWilsonPlotPath = Column(String(255))
    processedDataFile = Column(String(255))
    datFullPath = Column(String(255))
    magnification = Column(
        Float, comment="Calibrated magnification, Units: dimensionless"
    )
    totalAbsorbedDose = Column(Float, comment="Unit: e-/A^2 for EM")
    binning = Column(
        TINYINT(1),
        server_default=text("1"),
        comment="1 or 2. Number of pixels to process as 1. (Use mean value.)",
    )
    particleDiameter = Column(Float, comment="Unit: nm")
    boxSize_CTF = Column(Float, comment="Unit: pixels")
    minResolution = Column(Float, comment="Unit: A")
    minDefocus = Column(Float, comment="Unit: A")
    maxDefocus = Column(Float, comment="Unit: A")
    defocusStepSize = Column(Float, comment="Unit: A")
    amountAstigmatism = Column(Float, comment="Unit: A")
    extractSize = Column(Float, comment="Unit: pixels")
    bgRadius = Column(Float, comment="Unit: nm")
    voltage = Column(Float, comment="Unit: kV")
    objAperture = Column(Float, comment="Unit: um")
    c1aperture = Column(Float, comment="Unit: um")
    c2aperture = Column(Float, comment="Unit: um")
    c3aperture = Column(Float, comment="Unit: um")
    c1lens = Column(Float, comment="Unit: %")
    c2lens = Column(Float, comment="Unit: %")
    c3lens = Column(Float, comment="Unit: %")
    totalExposedDose = Column(Float, comment="Units: e-/A^2")
    nominalMagnification = Column(
        Float, comment="Nominal magnification: Units: dimensionless"
    )
    nominalDefocus = Column(Float, comment="Nominal defocus, Units: A")
    imageSizeX = Column(
        MEDIUMINT(8),
        comment="Image size in x, incase crop has been used, Units: pixels",
    )
    imageSizeY = Column(MEDIUMINT(8), comment="Image size in y, Units: pixels")
    pixelSizeOnImage = Column(
        Float,
        comment="Pixel size on image, calculated from magnification, duplicate? Units: um?",
    )
    phasePlate = Column(TINYINT(1), comment="Whether the phase plate was used")
    dataCollectionPlanId = Column(INTEGER(10))

    BLSubSample_ = relationship("BLSubSample", back_populates="DataCollection")
    DataCollectionGroup = relationship(
        "DataCollectionGroup", back_populates="DataCollection_"
    )
    DiffractionPlan = relationship("DiffractionPlan", back_populates="DataCollection_")
    Detector = relationship("Detector", back_populates="DataCollection_")
    MotorPosition = relationship(
        "MotorPosition", foreign_keys=[endPositionId], back_populates="DataCollection_"
    )
    MotorPosition_ = relationship(
        "MotorPosition",
        foreign_keys=[startPositionId],
        back_populates="DataCollection1",
    )
    ScreeningStrategySubWedge = relationship(
        "ScreeningStrategySubWedge", back_populates="DataCollection_"
    )
    ProcessingJob = relationship("ProcessingJob", back_populates="DataCollection_")
    Screening = relationship("Screening", back_populates="DataCollection_")
    AutoProcIntegration = relationship(
        "AutoProcIntegration", back_populates="DataCollection_"
    )
    DataCollectionFileAttachment = relationship(
        "DataCollectionFileAttachment", back_populates="DataCollection_"
    )
    EventChain = relationship("EventChain", back_populates="DataCollection_")
    GridImageMap = relationship("GridImageMap", back_populates="DataCollection_")
    Image = relationship("Image", back_populates="DataCollection_")
    Movie = relationship("Movie", back_populates="DataCollection_")
    Particle = relationship("Particle", back_populates="DataCollection_")
    ProcessingJobImageSweep = relationship(
        "ProcessingJobImageSweep", back_populates="DataCollection_"
    )
    Tomogram = relationship("Tomogram", back_populates="DataCollection_")
    DataCollectionComment = relationship(
        "DataCollectionComment", back_populates="DataCollection_"
    )
    MotionCorrection = relationship(
        "MotionCorrection", back_populates="DataCollection_"
    )
    GridInfo = relationship("GridInfo", back_populates="DataCollection_")


class DataReductionStatus(Base):
    __tablename__ = "DataReductionStatus"

    dataReductionStatusId = Column(INTEGER(11), primary_key=True)
    dataCollectionId = Column(INTEGER(11), nullable=False)
    status = Column(String(15))
    filename = Column(String(255))
    message = Column(String(255))


class Detector(Base):
    __tablename__ = "Detector"
    __table_args__ = (
        Index(
            "Detector_FKIndex1",
            "detectorType",
            "detectorManufacturer",
            "detectorModel",
            "detectorPixelSizeHorizontal",
            "detectorPixelSizeVertical",
        ),
        Index("Detector_ibuk1", "detectorSerialNumber", unique=True),
        {"comment": "Detector table is linked to a dataCollection"},
    )

    detectorId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    detectorType = Column(String(255))
    detectorManufacturer = Column(String(255))
    detectorModel = Column(String(255))
    detectorPixelSizeHorizontal = Column(Float)
    detectorPixelSizeVertical = Column(Float)
    DETECTORMAXRESOLUTION = Column(Float)
    DETECTORMINRESOLUTION = Column(Float)
    detectorSerialNumber = Column(String(30))
    detectorDistanceMin = Column(Float(asdecimal=True))
    detectorDistanceMax = Column(Float(asdecimal=True))
    trustedPixelValueRangeLower = Column(Float(asdecimal=True))
    trustedPixelValueRangeUpper = Column(Float(asdecimal=True))
    sensorThickness = Column(Float)
    overload = Column(Float)
    XGeoCorr = Column(String(255))
    YGeoCorr = Column(String(255))
    detectorMode = Column(String(255))
    density = Column(Float)
    composition = Column(String(16))
    numberOfPixelsX = Column(MEDIUMINT(9), comment="Detector number of pixels in x")
    numberOfPixelsY = Column(MEDIUMINT(9), comment="Detector number of pixels in y")
    detectorRollMin = Column(Float(asdecimal=True), comment="unit: degrees")
    detectorRollMax = Column(Float(asdecimal=True), comment="unit: degrees")
    localName = Column(String(40), comment="Colloquial name for the detector")

    DataCollection_ = relationship("DataCollection", back_populates="Detector")
    BeamLineSetup = relationship("BeamLineSetup", back_populates="Detector_")
    DiffractionPlan = relationship("DiffractionPlan", back_populates="Detector_")
    DataCollectionPlan_has_Detector = relationship(
        "DataCollectionPlanHasDetector", back_populates="Detector_"
    )


class DewarLocation(Base):
    __tablename__ = "DewarLocation"
    __table_args__ = {"comment": "ISPyB Dewar location table"}

    eventId = Column(INTEGER(10), primary_key=True)
    dewarNumber = Column(String(128), nullable=False, comment="Dewar number")
    userId = Column(String(128), comment="User who locates the dewar")
    dateTime = Column(DateTime, comment="Date and time of locatization")
    locationName = Column(String(128), comment="Location of the dewar")
    courierName = Column(
        String(128), comment="Carrier name who's shipping back the dewar"
    )
    courierTrackingNumber = Column(
        String(128), comment="Tracking number of the shippment"
    )


class DewarLocationList(Base):
    __tablename__ = "DewarLocationList"
    __table_args__ = {"comment": "List of locations for dewars"}

    locationId = Column(INTEGER(10), primary_key=True)
    locationName = Column(
        String(128), nullable=False, server_default=text("''"), comment="Location"
    )


class EMMicroscope(Base):
    __tablename__ = "EMMicroscope"

    emMicroscopeId = Column(INTEGER(11), primary_key=True)
    instrumentName = Column(String(100), nullable=False)
    voltage = Column(Float)
    CS = Column(Float)
    detectorPixelSize = Column(Float)
    C2aperture = Column(Float)
    ObjAperture = Column(Float)
    C2lens = Column(Float)


class EventType(Base):
    __tablename__ = "EventType"
    __table_args__ = (
        Index("name", "name", unique=True),
        {
            "comment": "Defines the list of event types which can occur during a data "
            "collection."
        },
    )

    eventTypeId = Column(INTEGER(11), primary_key=True)
    name = Column(String(30), nullable=False)

    Event = relationship("Event", back_populates="EventType_")


class ExperimentType(Base):
    __tablename__ = "ExperimentType"
    __table_args__ = {"comment": "A lookup table for different types of experients"}

    experimentTypeId = Column(INTEGER(10), primary_key=True)
    name = Column(String(100))
    proposalType = Column(String(10))
    active = Column(
        TINYINT(1), server_default=text("1"), comment="1=active, 0=inactive"
    )

    DiffractionPlan = relationship("DiffractionPlan", back_populates="ExperimentType_")
    DataCollectionGroup = relationship(
        "DataCollectionGroup", back_populates="ExperimentType_"
    )
    Container = relationship("Container", back_populates="ExperimentType_")


class GeometryClassname(Base):
    __tablename__ = "GeometryClassname"

    geometryClassnameId = Column(INTEGER(11), primary_key=True)
    geometryOrder = Column(INTEGER(2), nullable=False)
    geometryClassname = Column(String(45))

    SpaceGroup = relationship("SpaceGroup", back_populates="GeometryClassname_")


class ImageQualityIndicators(Base):
    __tablename__ = "ImageQualityIndicators"

    dataCollectionId = Column(INTEGER(11), primary_key=True, nullable=False)
    imageNumber = Column(MEDIUMINT(8), primary_key=True, nullable=False)
    imageId = Column(INTEGER(12))
    autoProcProgramId = Column(
        INTEGER(10), comment="Foreign key to the AutoProcProgram table"
    )
    spotTotal = Column(INTEGER(10), comment="Total number of spots")
    inResTotal = Column(
        INTEGER(10), comment="Total number of spots in resolution range"
    )
    goodBraggCandidates = Column(
        INTEGER(10), comment="Total number of Bragg diffraction spots"
    )
    iceRings = Column(INTEGER(10), comment="Number of ice rings identified")
    method1Res = Column(Float, comment="Resolution estimate 1 (see publication)")
    method2Res = Column(Float, comment="Resolution estimate 2 (see publication)")
    maxUnitCell = Column(
        Float, comment="Estimation of the largest possible unit cell edge"
    )
    pctSaturationTop50Peaks = Column(
        Float, comment="The fraction of the dynamic range being used"
    )
    inResolutionOvrlSpots = Column(INTEGER(10), comment="Number of spots overloaded")
    binPopCutOffMethod2Res = Column(
        Float, comment="Cut off used in resolution limit calculation"
    )
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")
    totalIntegratedSignal = Column(Float(asdecimal=True))
    dozor_score = Column(Float(asdecimal=True), comment="dozor_score")
    driftFactor = Column(Float, comment="EM movie drift factor")


class Imager(Base):
    __tablename__ = "Imager"

    imagerId = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), nullable=False)
    temperature = Column(Float)
    serial = Column(String(45))
    capacity = Column(SMALLINT(6))

    Container = relationship(
        "Container", foreign_keys="[Container.imagerId]", back_populates="Imager_"
    )
    Container_ = relationship(
        "Container",
        foreign_keys="[Container.requestedImagerId]",
        back_populates="Imager1",
    )
    ContainerInspection = relationship("ContainerInspection", back_populates="Imager_")


class InspectionType(Base):
    __tablename__ = "InspectionType"

    inspectionTypeId = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))

    ScheduleComponent = relationship(
        "ScheduleComponent", back_populates="InspectionType_"
    )
    ContainerInspection = relationship(
        "ContainerInspection", back_populates="InspectionType_"
    )


class IspybCrystalClass(Base):
    __tablename__ = "IspybCrystalClass"
    __table_args__ = {"comment": "ISPyB crystal class values"}

    crystalClassId = Column(INTEGER(11), primary_key=True)
    crystalClass_code = Column(String(20), nullable=False)
    crystalClass_name = Column(String(255), nullable=False)


class IspybReference(Base):
    __tablename__ = "IspybReference"

    referenceId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    referenceName = Column(String(255), comment="reference name")
    referenceUrl = Column(String(1024), comment="url of the reference")
    referenceBibtext = Column(LargeBinary, comment="bibtext value of the reference")
    beamline = Column(
        Enum("All", "ID14-4", "ID23-1", "ID23-2", "ID29", "XRF", "AllXRF", "Mesh"),
        comment="beamline involved",
    )


class LDAPSearchParameters(Base):
    __tablename__ = "LDAPSearchParameters"
    __table_args__ = {
        "comment": "All necessary parameters to run an LDAP search, except the search "
        "base"
    }

    ldapSearchParametersId = Column(INTEGER(11), primary_key=True)
    accountType = Column(
        Enum("group_member", "staff_account", "functional_account"),
        nullable=False,
        comment="The entity type returned by the search",
    )
    oneOrMany = Column(
        Enum("one", "many"), nullable=False, comment="Expected number of search results"
    )
    hostURL = Column(String(200), nullable=False, comment="URL for the LDAP host")
    attributes = Column(
        String(255), nullable=False, comment="Comma-separated list of search attributes"
    )
    accountTypeGroupName = Column(
        String(100), comment="all accounts of this type must be members of this group"
    )
    filter = Column(String(200), comment="A filter string for the search")

    LDAPSearchBase = relationship(
        "LDAPSearchBase", back_populates="LDAPSearchParameters_"
    )
    UserGroup_has_LDAPSearchParameters = relationship(
        "UserGroupHasLDAPSearchParameters", back_populates="LDAPSearchParameters_"
    )


class Laboratory(Base):
    __tablename__ = "Laboratory"

    laboratoryId = Column(INTEGER(10), primary_key=True)
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    laboratoryUUID = Column(String(45))
    name = Column(String(45))
    address = Column(String(255))
    city = Column(String(45))
    country = Column(String(45))
    url = Column(String(255))
    organization = Column(String(45))
    laboratoryPk = Column(INTEGER(10))
    postcode = Column(String(15))

    Person = relationship("Person", back_populates="Laboratory_")


class Log4Stat(Base):
    __tablename__ = "Log4Stat"

    id = Column(INTEGER(11), primary_key=True)
    priority = Column(String(15))
    LOG4JTIMESTAMP = Column(DateTime)
    msg = Column(String(255))
    detail = Column(String(255))
    value = Column(String(255))
    timestamp = Column(DateTime)


class MotorPosition(Base):
    __tablename__ = "MotorPosition"

    motorPositionId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    phiX = Column(Float(asdecimal=True))
    phiY = Column(Float(asdecimal=True))
    phiZ = Column(Float(asdecimal=True))
    sampX = Column(Float(asdecimal=True))
    sampY = Column(Float(asdecimal=True))
    omega = Column(Float(asdecimal=True))
    kappa = Column(Float(asdecimal=True))
    phi = Column(Float(asdecimal=True))
    chi = Column(Float(asdecimal=True))
    gridIndexY = Column(INTEGER(11))
    gridIndexZ = Column(INTEGER(11))

    BLSubSample_ = relationship("BLSubSample", back_populates="MotorPosition")
    DataCollection_ = relationship(
        "DataCollection",
        foreign_keys="[DataCollection.endPositionId]",
        back_populates="MotorPosition",
    )
    DataCollection1 = relationship(
        "DataCollection",
        foreign_keys="[DataCollection.startPositionId]",
        back_populates="MotorPosition_",
    )
    Image = relationship("Image", back_populates="MotorPosition_")


class PDB(Base):
    __tablename__ = "PDB"

    pdbId = Column(INTEGER(11), primary_key=True)
    name = Column(String(255))
    contents = Column(MEDIUMTEXT)
    code = Column(String(4))
    source = Column(String(30), comment="Could be e.g. AlphaFold or RoseTTAFold")

    Protein_has_PDB = relationship("ProteinHasPDB", back_populates="PDB_")


class PHPSession(Base):
    __tablename__ = "PHPSession"

    id = Column(String(50), primary_key=True)
    accessDate = Column(DateTime)
    data = Column(String(4000))


class Permission(Base):
    __tablename__ = "Permission"

    permissionId = Column(INTEGER(11), primary_key=True)
    type = Column(String(15), nullable=False)
    description = Column(String(100))

    UserGroup = relationship(
        "UserGroup", secondary="UserGroup_has_Permission", back_populates="Permission_"
    )


class PhasingAnalysis(Base):
    __tablename__ = "PhasingAnalysis"

    phasingAnalysisId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")

    ModelBuilding = relationship("ModelBuilding", back_populates="PhasingAnalysis_")
    Phasing = relationship("Phasing", back_populates="PhasingAnalysis_")
    Phasing_has_Scaling = relationship(
        "PhasingHasScaling", back_populates="PhasingAnalysis_"
    )
    PreparePhasingData = relationship(
        "PreparePhasingData", back_populates="PhasingAnalysis_"
    )
    SubstructureDetermination = relationship(
        "SubstructureDetermination", back_populates="PhasingAnalysis_"
    )


class PhasingProgramRun(Base):
    __tablename__ = "PhasingProgramRun"

    phasingProgramRunId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    phasingCommandLine = Column(String(255), comment="Command line for phasing")
    phasingPrograms = Column(String(255), comment="Phasing programs (comma separated)")
    phasingStatus = Column(TINYINT(1), comment="success (1) / fail (0)")
    phasingMessage = Column(String(255), comment="warning, error,...")
    phasingStartTime = Column(DateTime, comment="Processing start time")
    phasingEndTime = Column(DateTime, comment="Processing end time")
    phasingEnvironment = Column(String(255), comment="Cpus, Nodes,...")
    recordTimeStamp = Column(DateTime, server_default=text("current_timestamp()"))

    PhasingProgramAttachment = relationship(
        "PhasingProgramAttachment", back_populates="PhasingProgramRun_"
    )
    ModelBuilding = relationship("ModelBuilding", back_populates="PhasingProgramRun_")
    Phasing = relationship("Phasing", back_populates="PhasingProgramRun_")
    PhasingStep = relationship("PhasingStep", back_populates="PhasingProgramRun_")
    PreparePhasingData = relationship(
        "PreparePhasingData", back_populates="PhasingProgramRun_"
    )
    SubstructureDetermination = relationship(
        "SubstructureDetermination", back_populates="PhasingProgramRun_"
    )


class Position(Base):
    __tablename__ = "Position"
    __table_args__ = (
        ForeignKeyConstraint(
            ["relativePositionId"],
            ["Position.positionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Position_relativePositionfk_1",
        ),
        Index("Position_FKIndex1", "relativePositionId"),
    )

    positionId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    relativePositionId = Column(
        INTEGER(11), comment="relative position, null otherwise"
    )
    posX = Column(Float(asdecimal=True))
    posY = Column(Float(asdecimal=True))
    posZ = Column(Float(asdecimal=True))
    scale = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")
    X = Column(Float(asdecimal=True), Computed("(`posX`)", persisted=False))
    Y = Column(Float(asdecimal=True), Computed("(`posY`)", persisted=False))
    Z = Column(Float(asdecimal=True), Computed("(`posZ`)", persisted=False))

    BLSubSample_ = relationship(
        "BLSubSample",
        foreign_keys="[BLSubSample.position2Id]",
        back_populates="Position",
    )
    BLSubSample1 = relationship(
        "BLSubSample",
        foreign_keys="[BLSubSample.positionId]",
        back_populates="Position_",
    )
    Position = relationship(
        "Position", remote_side=[positionId], back_populates="Position_reverse"
    )
    Position_reverse = relationship(
        "Position", remote_side=[relativePositionId], back_populates="Position"
    )


class Positioner(Base):
    __tablename__ = "Positioner"
    __table_args__ = {
        "comment": "An arbitrary positioner and its value, could be e.g. a motor. "
        "Allows for instance to store some positions with a sample or "
        "subsample"
    }

    positionerId = Column(INTEGER(10), primary_key=True)
    positioner = Column(String(50), nullable=False)
    value = Column(Float, nullable=False)

    BLSampleImage_has_Positioner = relationship(
        "BLSampleImageHasPositioner", back_populates="Positioner_"
    )
    BLSample_has_Positioner = relationship(
        "BLSampleHasPositioner", back_populates="Positioner_"
    )
    BLSubSample_has_Positioner = relationship(
        "BLSubSampleHasPositioner", back_populates="Positioner_"
    )


class ProcessingJob(Base):
    __tablename__ = "ProcessingJob"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            name="ProcessingJob_ibfk1",
        ),
        Index("ProcessingJob_ibfk1", "dataCollectionId"),
        {"comment": "From this we get both job times and lag times"},
    )

    processingJobId = Column(INTEGER(11), primary_key=True)
    recordTimestamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="When job was submitted",
    )
    dataCollectionId = Column(INTEGER(11))
    displayName = Column(String(80), comment="xia2, fast_dp, dimple, etc")
    comments = Column(
        String(255),
        comment="For users to annotate the job and see the motivation for the job",
    )
    recipe = Column(String(50), comment="What we want to run (xia, dimple, etc).")
    automatic = Column(
        TINYINT(1),
        comment="Whether this processing job was triggered automatically or not",
    )

    AutoProcProgram_ = relationship("AutoProcProgram", back_populates="ProcessingJob")
    DataCollection_ = relationship("DataCollection", back_populates="ProcessingJob")
    ProcessingJobImageSweep = relationship(
        "ProcessingJobImageSweep", back_populates="ProcessingJob_"
    )
    ProcessingJobParameter = relationship(
        "ProcessingJobParameter", back_populates="ProcessingJob_"
    )


class ProcessingPipelineCategory(Base):
    __tablename__ = "ProcessingPipelineCategory"
    __table_args__ = {
        "comment": "A lookup table for the category of processing pipeline"
    }

    processingPipelineCategoryId = Column(INTEGER(11), primary_key=True)
    name = Column(String(20), nullable=False)

    ProcessingPipeline = relationship(
        "ProcessingPipeline", back_populates="ProcessingPipelineCategory_"
    )


class PurificationColumn(Base):
    __tablename__ = "PurificationColumn"
    __table_args__ = {
        "comment": "Size exclusion chromotography (SEC) lookup table for BioSAXS"
    }

    purificationColumnId = Column(INTEGER(10), primary_key=True)
    name = Column(String(100))
    active = Column(
        TINYINT(1), server_default=text("1"), comment="1=active, 0=inactive"
    )

    DiffractionPlan = relationship(
        "DiffractionPlan", back_populates="PurificationColumn_"
    )


t_SAFETYREQUEST = Table(
    "SAFETYREQUEST",
    metadata,
    Column("SAFETYREQUESTID", DECIMAL(10, 0)),
    Column("XMLDOCUMENTID", DECIMAL(10, 0)),
    Column("PROTEINID", DECIMAL(10, 0)),
    Column("PROJECTCODE", String(45)),
    Column("SUBMISSIONDATE", DateTime),
    Column("RESPONSE", DECIMAL(3, 0)),
    Column("REPONSEDATE", DateTime),
    Column("RESPONSEDETAILS", String(255)),
)


class SAMPLECELL(Base):
    __tablename__ = "SAMPLECELL"

    SAMPLECELLID = Column(INTEGER(11), primary_key=True)
    SAMPLEEXPOSUREUNITID = Column(INTEGER(11))
    ID = Column(String(45))
    NAME = Column(String(45))
    DIAMETER = Column(String(45))
    MATERIAL = Column(String(45))


class SAMPLEEXPOSUREUNIT(Base):
    __tablename__ = "SAMPLEEXPOSUREUNIT"

    SAMPLEEXPOSUREUNITID = Column(INTEGER(11), primary_key=True)
    ID = Column(String(45))
    PATHLENGTH = Column(String(45))
    VOLUME = Column(String(45))


class SAXSDATACOLLECTIONGROUP(Base):
    __tablename__ = "SAXSDATACOLLECTIONGROUP"

    DATACOLLECTIONGROUPID = Column(INTEGER(11), primary_key=True)
    DEFAULTDATAACQUISITIONID = Column(INTEGER(11))
    SAXSDATACOLLECTIONARRAYID = Column(INTEGER(11))


class ScanParametersService(Base):
    __tablename__ = "ScanParametersService"

    scanParametersServiceId = Column(INTEGER(10), primary_key=True)
    name = Column(String(45))
    description = Column(String(45))

    ScanParametersModel = relationship(
        "ScanParametersModel", back_populates="ScanParametersService_"
    )


class Schedule(Base):
    __tablename__ = "Schedule"

    scheduleId = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))

    ScheduleComponent = relationship("ScheduleComponent", back_populates="Schedule_")
    Container = relationship("Container", back_populates="Schedule_")


class SchemaStatus(Base):
    __tablename__ = "SchemaStatus"
    __table_args__ = (Index("scriptName", "scriptName", unique=True),)

    schemaStatusId = Column(INTEGER(11), primary_key=True)
    scriptName = Column(String(100), nullable=False)
    recordTimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    schemaStatus = Column(String(10))


class Screening(Base):
    __tablename__ = "Screening"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="Screening_fk_autoProcProgramId",
        ),
        ForeignKeyConstraint(
            ["dataCollectionGroupId"],
            ["DataCollectionGroup.dataCollectionGroupId"],
            name="Screening_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="_Screening_ibfk2",
        ),
        Index("Screening_FKIndexDiffractionPlanId", "diffractionPlanId"),
        Index("Screening_fk_autoProcProgramId", "autoProcProgramId"),
        Index("_Screening_ibfk2", "dataCollectionId"),
        Index("dcgroupId", "dataCollectionGroupId"),
    )

    screeningId = Column(INTEGER(10), primary_key=True)
    bltimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
    )
    dataCollectionId = Column(INTEGER(11))
    programVersion = Column(String(45))
    comments = Column(String(255))
    shortComments = Column(String(20))
    diffractionPlanId = Column(INTEGER(10), comment="references DiffractionPlan")
    dataCollectionGroupId = Column(INTEGER(11))
    xmlSampleInformation = Column(LONGBLOB)
    autoProcProgramId = Column(INTEGER(10))

    AutoProcProgram_ = relationship("AutoProcProgram", back_populates="Screening")
    DataCollectionGroup = relationship(
        "DataCollectionGroup", back_populates="Screening_"
    )
    DataCollection_ = relationship("DataCollection", back_populates="Screening")
    ScreeningOutput = relationship("ScreeningOutput", back_populates="Screening_")
    ScreeningInput = relationship("ScreeningInput", back_populates="Screening_")
    ScreeningRank = relationship("ScreeningRank", back_populates="Screening_")


class ScreeningOutput(Base):
    __tablename__ = "ScreeningOutput"
    __table_args__ = (
        ForeignKeyConstraint(
            ["screeningId"],
            ["Screening.screeningId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ScreeningOutput_ibfk_1",
        ),
        Index("ScreeningOutput_FKIndex1", "screeningId"),
    )

    screeningOutputId = Column(INTEGER(10), primary_key=True)
    screeningId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    mosaicityEstimated = Column(TINYINT(1), nullable=False, server_default=text("0"))
    indexingSuccess = Column(TINYINT(1), nullable=False, server_default=text("0"))
    strategySuccess = Column(TINYINT(1), nullable=False, server_default=text("0"))
    alignmentSuccess = Column(TINYINT(1), nullable=False, server_default=text("0"))
    statusDescription = Column(String(1024))
    rejectedReflections = Column(INTEGER(10))
    resolutionObtained = Column(Float)
    spotDeviationR = Column(Float)
    spotDeviationTheta = Column(Float)
    beamShiftX = Column(Float)
    beamShiftY = Column(Float)
    numSpotsFound = Column(INTEGER(10))
    numSpotsUsed = Column(INTEGER(10))
    numSpotsRejected = Column(INTEGER(10))
    mosaicity = Column(Float)
    iOverSigma = Column(Float)
    diffractionRings = Column(TINYINT(1))
    SCREENINGSUCCESS = Column(
        TINYINT(1), server_default=text("0"), comment="Column to be deleted"
    )
    rankingResolution = Column(Float(asdecimal=True))
    program = Column(String(45))
    doseTotal = Column(Float(asdecimal=True))
    totalExposureTime = Column(Float(asdecimal=True))
    totalRotationRange = Column(Float(asdecimal=True))
    totalNumberOfImages = Column(INTEGER(11))
    rFriedel = Column(Float(asdecimal=True))

    Screening_ = relationship("Screening", back_populates="ScreeningOutput")
    ScreeningStrategy = relationship(
        "ScreeningStrategy", back_populates="ScreeningOutput_"
    )
    ScreeningOutputLattice = relationship(
        "ScreeningOutputLattice", back_populates="ScreeningOutput_"
    )


class ScreeningRankSet(Base):
    __tablename__ = "ScreeningRankSet"

    screeningRankSetId = Column(INTEGER(10), primary_key=True)
    rankEngine = Column(String(255))
    rankingProjectFileName = Column(String(255))
    rankingSummaryFileName = Column(String(255))

    ScreeningRank = relationship("ScreeningRank", back_populates="ScreeningRankSet_")


class ScreeningStrategy(Base):
    __tablename__ = "ScreeningStrategy"
    __table_args__ = (
        ForeignKeyConstraint(
            ["screeningOutputId"],
            ["ScreeningOutput.screeningOutputId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ScreeningStrategy_ibfk_1",
        ),
        Index("ScreeningStrategy_FKIndex1", "screeningOutputId"),
    )

    screeningStrategyId = Column(INTEGER(10), primary_key=True)
    screeningOutputId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    anomalous = Column(TINYINT(1), nullable=False, server_default=text("0"))
    phiStart = Column(Float)
    phiEnd = Column(Float)
    rotation = Column(Float)
    exposureTime = Column(Float)
    resolution = Column(Float)
    completeness = Column(Float)
    multiplicity = Column(Float)
    program = Column(String(45))
    rankingResolution = Column(Float)
    transmission = Column(
        Float, comment="Transmission for the strategy as given by the strategy program."
    )

    ScreeningOutput_ = relationship(
        "ScreeningOutput", back_populates="ScreeningStrategy"
    )
    ScreeningStrategyWedge = relationship(
        "ScreeningStrategyWedge", back_populates="ScreeningStrategy_"
    )


class ScreeningStrategySubWedge(Base):
    __tablename__ = "ScreeningStrategySubWedge"
    __table_args__ = (
        ForeignKeyConstraint(
            ["screeningStrategyWedgeId"],
            ["ScreeningStrategyWedge.screeningStrategyWedgeId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ScreeningStrategySubWedge_FK1",
        ),
        Index("ScreeningStrategySubWedge_FK1", "screeningStrategyWedgeId"),
    )

    screeningStrategySubWedgeId = Column(
        INTEGER(10), primary_key=True, comment="Primary key"
    )
    screeningStrategyWedgeId = Column(
        INTEGER(10), comment="Foreign key to parent table"
    )
    subWedgeNumber = Column(
        INTEGER(10), comment="The number of this subwedge within the wedge"
    )
    rotationAxis = Column(String(45), comment="Angle where subwedge starts")
    axisStart = Column(Float, comment="Angle where subwedge ends")
    axisEnd = Column(Float, comment="Exposure time for subwedge")
    exposureTime = Column(Float, comment="Transmission for subwedge")
    transmission = Column(Float)
    oscillationRange = Column(Float)
    completeness = Column(Float)
    multiplicity = Column(Float)
    RESOLUTION = Column(Float)
    doseTotal = Column(Float, comment="Total dose for this subwedge")
    numberOfImages = Column(INTEGER(10), comment="Number of images for this subwedge")
    comments = Column(String(255))

    DataCollection_ = relationship(
        "DataCollection", back_populates="ScreeningStrategySubWedge"
    )
    ScreeningStrategyWedge = relationship(
        "ScreeningStrategyWedge", back_populates="ScreeningStrategySubWedge_"
    )


class ScreeningStrategyWedge(Base):
    __tablename__ = "ScreeningStrategyWedge"
    __table_args__ = (
        ForeignKeyConstraint(
            ["screeningStrategyId"],
            ["ScreeningStrategy.screeningStrategyId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ScreeningStrategyWedge_IBFK_1",
        ),
        Index("ScreeningStrategyWedge_IBFK_1", "screeningStrategyId"),
    )

    screeningStrategyWedgeId = Column(
        INTEGER(10), primary_key=True, comment="Primary key"
    )
    screeningStrategyId = Column(INTEGER(10), comment="Foreign key to parent table")
    wedgeNumber = Column(
        INTEGER(10), comment="The number of this wedge within the strategy"
    )
    resolution = Column(Float)
    completeness = Column(Float)
    multiplicity = Column(Float)
    doseTotal = Column(Float, comment="Total dose for this wedge")
    numberOfImages = Column(INTEGER(10), comment="Number of images for this wedge")
    phi = Column(Float)
    kappa = Column(Float)
    chi = Column(Float)
    comments = Column(String(255))
    wavelength = Column(Float(asdecimal=True))

    ScreeningStrategySubWedge_ = relationship(
        "ScreeningStrategySubWedge", back_populates="ScreeningStrategyWedge"
    )
    ScreeningStrategy_ = relationship(
        "ScreeningStrategy", back_populates="ScreeningStrategyWedge"
    )


class Sleeve(Base):
    __tablename__ = "Sleeve"
    __table_args__ = {
        "comment": "Registry of ice-filled sleeves used to cool plates whilst on the "
        "goniometer"
    }

    sleeveId = Column(
        TINYINT(3),
        primary_key=True,
        comment="The unique sleeve id 1...255 which also identifies its home location in the freezer",
    )
    lastMovedToFreezer = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    location = Column(
        TINYINT(3), comment="NULL == freezer, 1...255 for local storage locations"
    )
    lastMovedFromFreezer = Column(TIMESTAMP, server_default=text("current_timestamp()"))


class UserGroup(Base):
    __tablename__ = "UserGroup"
    __table_args__ = (Index("UserGroup_idx1", "name", unique=True),)

    userGroupId = Column(INTEGER(11), primary_key=True)
    name = Column(String(31), nullable=False)

    Permission_ = relationship(
        "Permission", secondary="UserGroup_has_Permission", back_populates="UserGroup"
    )
    Person = relationship(
        "Person", secondary="UserGroup_has_Person", back_populates="UserGroup_"
    )
    UserGroup_has_LDAPSearchParameters = relationship(
        "UserGroupHasLDAPSearchParameters", back_populates="UserGroup_"
    )


class Workflow(Base):
    __tablename__ = "Workflow"

    workflowId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    workflowTitle = Column(String(255))
    workflowType = Column(
        Enum(
            "Undefined",
            "BioSAXS Post Processing",
            "EnhancedCharacterisation",
            "LineScan",
            "MeshScan",
            "Dehydration",
            "KappaReorientation",
            "BurnStrategy",
            "XrayCentering",
            "DiffractionTomography",
            "TroubleShooting",
            "VisualReorientation",
            "HelicalCharacterisation",
            "GroupedProcessing",
            "MXPressE",
            "MXPressO",
            "MXPressL",
            "MXScore",
            "MXPressI",
            "MXPressM",
            "MXPressA",
        )
    )
    workflowTypeId = Column(INTEGER(11))
    comments = Column(String(1024))
    status = Column(String(255))
    resultFilePath = Column(String(255))
    logFilePath = Column(String(255))
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")
    workflowDescriptionFullPath = Column(
        String(255), comment="Full file path to a json description of the workflow"
    )

    WorkflowStep = relationship("WorkflowStep", back_populates="Workflow_")


class WorkflowType(Base):
    __tablename__ = "WorkflowType"

    workflowTypeId = Column(INTEGER(11), primary_key=True)
    workflowTypeName = Column(String(45))
    comments = Column(String(2048))
    recordTimeStamp = Column(TIMESTAMP)


class VRun(Base):
    __tablename__ = "v_run"
    __table_args__ = (Index("v_run_idx1", "startDate", "endDate"),)

    runId = Column(INTEGER(11), primary_key=True)
    run = Column(String(7), nullable=False, server_default=text("''"))
    startDate = Column(DateTime)
    endDate = Column(DateTime)


class AutoProcIntegration(Base):
    __tablename__ = "AutoProcIntegration"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="AutoProcIntegration_ibfk_2",
        ),
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="AutoProcIntegration_ibfk_1",
        ),
        Index("AutoProcIntegrationIdx1", "dataCollectionId"),
        Index("AutoProcIntegration_FKIndex1", "autoProcProgramId"),
    )

    autoProcIntegrationId = Column(
        INTEGER(10), primary_key=True, comment="Primary key (auto-incremented)"
    )
    dataCollectionId = Column(
        INTEGER(11), nullable=False, comment="DataCollection item"
    )
    autoProcProgramId = Column(INTEGER(10), comment="Related program item")
    startImageNumber = Column(INTEGER(10), comment="start image number")
    endImageNumber = Column(INTEGER(10), comment="end image number")
    refinedDetectorDistance = Column(
        Float, comment="Refined DataCollection.detectorDistance"
    )
    refinedXBeam = Column(Float, comment="Refined DataCollection.xBeam")
    refinedYBeam = Column(Float, comment="Refined DataCollection.yBeam")
    rotationAxisX = Column(Float, comment="Rotation axis")
    rotationAxisY = Column(Float, comment="Rotation axis")
    rotationAxisZ = Column(Float, comment="Rotation axis")
    beamVectorX = Column(Float, comment="Beam vector")
    beamVectorY = Column(Float, comment="Beam vector")
    beamVectorZ = Column(Float, comment="Beam vector")
    cell_a = Column(Float, comment="Unit cell")
    cell_b = Column(Float, comment="Unit cell")
    cell_c = Column(Float, comment="Unit cell")
    cell_alpha = Column(Float, comment="Unit cell")
    cell_beta = Column(Float, comment="Unit cell")
    cell_gamma = Column(Float, comment="Unit cell")
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")
    anomalous = Column(
        TINYINT(1), server_default=text("0"), comment="boolean type:0 noanoum - 1 anoum"
    )

    AutoProcProgram_ = relationship(
        "AutoProcProgram", back_populates="AutoProcIntegration"
    )
    DataCollection_ = relationship(
        "DataCollection", back_populates="AutoProcIntegration"
    )
    AutoProcScaling_has_Int = relationship(
        "AutoProcScalingHasInt", back_populates="AutoProcIntegration_"
    )
    AutoProcStatus = relationship(
        "AutoProcStatus", back_populates="AutoProcIntegration_"
    )


class AutoProcProgramAttachment(Base):
    __tablename__ = "AutoProcProgramAttachment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="AutoProcProgramAttachmentFk1",
        ),
        Index("AutoProcProgramAttachmentIdx1", "autoProcProgramId"),
    )

    autoProcProgramAttachmentId = Column(
        INTEGER(10), primary_key=True, comment="Primary key (auto-incremented)"
    )
    autoProcProgramId = Column(
        INTEGER(10), nullable=False, comment="Related autoProcProgram item"
    )
    fileType = Column(
        Enum("Log", "Result", "Graph", "Debug", "Input"),
        comment="Type of file Attachment",
    )
    fileName = Column(String(255), comment="Attachment filename")
    filePath = Column(String(255), comment="Attachment filepath to disk storage")
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")
    importanceRank = Column(
        TINYINT(3),
        comment="For the particular autoProcProgramId and fileType, indicate the importance of the attachment. Higher numbers are more important",
    )

    AutoProcProgram_ = relationship(
        "AutoProcProgram", back_populates="AutoProcProgramAttachment"
    )


class AutoProcProgramMessage(Base):
    __tablename__ = "AutoProcProgramMessage"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            name="AutoProcProgramMessage_fk1",
        ),
        Index("AutoProcProgramMessage_fk1", "autoProcProgramId"),
    )

    autoProcProgramMessageId = Column(INTEGER(10), primary_key=True)
    recordTimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    autoProcProgramId = Column(INTEGER(10))
    severity = Column(Enum("ERROR", "WARNING", "INFO"))
    message = Column(String(200))
    description = Column(Text)

    AutoProcProgram_ = relationship(
        "AutoProcProgram", back_populates="AutoProcProgramMessage"
    )


class AutoProcScaling(Base):
    __tablename__ = "AutoProcScaling"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcId"],
            ["AutoProc.autoProcId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="AutoProcScalingFk1",
        ),
        Index("AutoProcScalingFk1", "autoProcId"),
        Index("AutoProcScalingIdx1", "autoProcScalingId", "autoProcId"),
    )

    autoProcScalingId = Column(
        INTEGER(10), primary_key=True, comment="Primary key (auto-incremented)"
    )
    autoProcId = Column(
        INTEGER(10), comment="Related autoProc item (used by foreign key)"
    )
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")

    AutoProc_ = relationship("AutoProc", back_populates="AutoProcScaling")
    AutoProcScalingStatistics = relationship(
        "AutoProcScalingStatistics", back_populates="AutoProcScaling_"
    )
    AutoProcScaling_has_Int = relationship(
        "AutoProcScalingHasInt", back_populates="AutoProcScaling_"
    )
    MXMRRun = relationship("MXMRRun", back_populates="AutoProcScaling_")
    PhasingStep = relationship("PhasingStep", back_populates="AutoProcScaling_")
    Phasing_has_Scaling = relationship(
        "PhasingHasScaling", back_populates="AutoProcScaling_"
    )


class BFComponent(Base):
    __tablename__ = "BF_component"
    __table_args__ = (
        ForeignKeyConstraint(
            ["systemId"], ["BF_system.systemId"], name="bf_component_FK1"
        ),
        Index("bf_component_FK1", "systemId"),
    )

    componentId = Column(INTEGER(10), primary_key=True)
    systemId = Column(INTEGER(10))
    name = Column(String(100))
    description = Column(String(200))

    BF_system = relationship("BFSystem", back_populates="BF_component")
    BF_component_beamline = relationship(
        "BFComponentBeamline", back_populates="BF_component"
    )
    BF_subcomponent = relationship("BFSubcomponent", back_populates="BF_component")


class BFSystemBeamline(Base):
    __tablename__ = "BF_system_beamline"
    __table_args__ = (
        ForeignKeyConstraint(
            ["systemId"], ["BF_system.systemId"], name="bf_system_beamline_FK1"
        ),
        Index("bf_system_beamline_FK1", "systemId"),
    )

    system_beamlineId = Column(INTEGER(10), primary_key=True)
    systemId = Column(INTEGER(10))
    beamlineName = Column(String(20))

    BF_system = relationship("BFSystem", back_populates="BF_system_beamline")


class BLSampleImageAnalysis(Base):
    __tablename__ = "BLSampleImageAnalysis"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleImageId"],
            ["BLSampleImage.blSampleImageId"],
            name="BLSampleImageAnalysis_ibfk1",
        ),
        Index("BLSampleImageAnalysis_ibfk1", "blSampleImageId"),
    )

    blSampleImageAnalysisId = Column(INTEGER(11), primary_key=True)
    blSampleImageId = Column(INTEGER(11))
    oavSnapshotBefore = Column(String(255))
    oavSnapshotAfter = Column(String(255))
    deltaX = Column(INTEGER(11))
    deltaY = Column(INTEGER(11))
    goodnessOfFit = Column(Float)
    scaleFactor = Column(Float)
    resultCode = Column(String(15))
    matchStartTimeStamp = Column(TIMESTAMP, server_default=text("current_timestamp()"))
    matchEndTimeStamp = Column(TIMESTAMP)

    BLSampleImage_ = relationship(
        "BLSampleImage", back_populates="BLSampleImageAnalysis"
    )


class BLSampleImageAutoScoreClass(Base):
    __tablename__ = "BLSampleImageAutoScoreClass"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleImageAutoScoreSchemaId"],
            ["BLSampleImageAutoScoreSchema.blSampleImageAutoScoreSchemaId"],
            onupdate="CASCADE",
            name="BLSampleImageAutoScoreClass_fk1",
        ),
        Index("BLSampleImageAutoScoreClass_fk1", "blSampleImageAutoScoreSchemaId"),
        {"comment": "The automated scoring classes - the thing being scored"},
    )

    blSampleImageAutoScoreClassId = Column(TINYINT(3), primary_key=True)
    scoreClass = Column(
        String(15),
        nullable=False,
        comment="Thing being scored e.g. crystal, precipitant",
    )
    blSampleImageAutoScoreSchemaId = Column(TINYINT(3))

    BLSampleImageAutoScoreSchema_ = relationship(
        "BLSampleImageAutoScoreSchema", back_populates="BLSampleImageAutoScoreClass"
    )
    BLSampleImage_has_AutoScoreClass = relationship(
        "BLSampleImageHasAutoScoreClass", back_populates="BLSampleImageAutoScoreClass_"
    )


class BLSampleImageMeasurement(Base):
    __tablename__ = "BLSampleImageMeasurement"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleImageId"],
            ["BLSampleImage.blSampleImageId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSampleImageMeasurement_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["blSubSampleId"],
            ["BLSubSample.blSubSampleId"],
            name="BLSampleImageMeasurement_ibfk_2",
        ),
        Index("BLSampleImageMeasurement_ibfk_1", "blSampleImageId"),
        Index("BLSampleImageMeasurement_ibfk_2", "blSubSampleId"),
        {"comment": "For measuring crystal growth over time"},
    )

    blSampleImageMeasurementId = Column(INTEGER(11), primary_key=True)
    blSampleImageId = Column(INTEGER(11), nullable=False)
    blSubSampleId = Column(INTEGER(11))
    startPosX = Column(Float(asdecimal=True))
    startPosY = Column(Float(asdecimal=True))
    endPosX = Column(Float(asdecimal=True))
    endPosY = Column(Float(asdecimal=True))
    blTimeStamp = Column(DateTime)

    BLSampleImage_ = relationship(
        "BLSampleImage", back_populates="BLSampleImageMeasurement"
    )
    BLSubSample_ = relationship(
        "BLSubSample", back_populates="BLSampleImageMeasurement"
    )


class BLSampleImageHasPositioner(Base):
    __tablename__ = "BLSampleImage_has_Positioner"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleImageId"],
            ["BLSampleImage.blSampleImageId"],
            name="BLSampleImageHasPositioner_ibfk1",
        ),
        ForeignKeyConstraint(
            ["positionerId"],
            ["Positioner.positionerId"],
            name="BLSampleImageHasPositioner_ibfk2",
        ),
        Index("BLSampleImageHasPositioner_ibfk1", "blSampleImageId"),
        Index("BLSampleImageHasPositioner_ibfk2", "positionerId"),
        {
            "comment": "Allows a BLSampleImage to store motor positions along with the "
            "image"
        },
    )

    blSampleImageHasPositionerId = Column(INTEGER(10), primary_key=True)
    blSampleImageId = Column(INTEGER(10), nullable=False)
    positionerId = Column(INTEGER(10), nullable=False)
    value = Column(
        Float, comment="The position of this positioner for this blsampleimage"
    )

    BLSampleImage_ = relationship(
        "BLSampleImage", back_populates="BLSampleImage_has_Positioner"
    )
    Positioner_ = relationship(
        "Positioner", back_populates="BLSampleImage_has_Positioner"
    )


class BLSampleHasPositioner(Base):
    __tablename__ = "BLSample_has_Positioner"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"], ["BLSample.blSampleId"], name="BLSampleHasPositioner_ibfk1"
        ),
        ForeignKeyConstraint(
            ["positionerId"],
            ["Positioner.positionerId"],
            name="BLSampleHasPositioner_ibfk2",
        ),
        Index("BLSampleHasPositioner_ibfk1", "blSampleId"),
        Index("BLSampleHasPositioner_ibfk2", "positionerId"),
    )

    blSampleHasPositioner = Column(INTEGER(10), primary_key=True)
    blSampleId = Column(INTEGER(10), nullable=False)
    positionerId = Column(INTEGER(10), nullable=False)

    BLSample_ = relationship("BLSample", back_populates="BLSample_has_Positioner")
    Positioner_ = relationship("Positioner", back_populates="BLSample_has_Positioner")


class BLSubSampleHasPositioner(Base):
    __tablename__ = "BLSubSample_has_Positioner"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSubSampleId"],
            ["BLSubSample.blSubSampleId"],
            name="BLSubSampleHasPositioner_ibfk1",
        ),
        ForeignKeyConstraint(
            ["positionerId"],
            ["Positioner.positionerId"],
            name="BLSubSampleHasPositioner_ibfk2",
        ),
        Index("BLSubSampleHasPositioner_ibfk1", "blSubSampleId"),
        Index("BLSubSampleHasPositioner_ibfk2", "positionerId"),
    )

    blSubSampleHasPositioner = Column(INTEGER(10), primary_key=True)
    blSubSampleId = Column(INTEGER(10), nullable=False)
    positionerId = Column(INTEGER(10), nullable=False)

    BLSubSample_ = relationship(
        "BLSubSample", back_populates="BLSubSample_has_Positioner"
    )
    Positioner_ = relationship(
        "Positioner", back_populates="BLSubSample_has_Positioner"
    )


class BeamApertures(Base):
    __tablename__ = "BeamApertures"
    __table_args__ = (
        ForeignKeyConstraint(
            ["beamlineStatsId"],
            ["BeamlineStats.beamlineStatsId"],
            ondelete="CASCADE",
            name="beamapertures_FK1",
        ),
        Index("beamapertures_FK1", "beamlineStatsId"),
    )

    beamAperturesid = Column(INTEGER(11), primary_key=True)
    beamlineStatsId = Column(INTEGER(11))
    flux = Column(Float(asdecimal=True))
    x = Column(Float)
    y = Column(Float)
    apertureSize = Column(SMALLINT(5))

    BeamlineStats_ = relationship("BeamlineStats", back_populates="BeamApertures")


class BeamCentres(Base):
    __tablename__ = "BeamCentres"
    __table_args__ = (
        ForeignKeyConstraint(
            ["beamlineStatsId"],
            ["BeamlineStats.beamlineStatsId"],
            ondelete="CASCADE",
            name="beamCentres_FK1",
        ),
        Index("beamCentres_FK1", "beamlineStatsId"),
    )

    beamCentresid = Column(INTEGER(11), primary_key=True)
    beamlineStatsId = Column(INTEGER(11))
    x = Column(Float)
    y = Column(Float)
    zoom = Column(TINYINT(3))

    BeamlineStats_ = relationship("BeamlineStats", back_populates="BeamCentres")


class BeamLineSetup(Base):
    __tablename__ = "BeamLineSetup"
    __table_args__ = (
        ForeignKeyConstraint(
            ["detectorId"], ["Detector.detectorId"], name="BeamLineSetup_ibfk_1"
        ),
        Index("BeamLineSetup_ibfk_1", "detectorId"),
    )

    beamLineSetupId = Column(INTEGER(10), primary_key=True)
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    active = Column(TINYINT(1), nullable=False, server_default=text("0"))
    detectorId = Column(INTEGER(11))
    synchrotronMode = Column(String(255))
    undulatorType1 = Column(String(45))
    undulatorType2 = Column(String(45))
    undulatorType3 = Column(String(45))
    focalSpotSizeAtSample = Column(Float)
    focusingOptic = Column(String(255))
    beamDivergenceHorizontal = Column(Float)
    beamDivergenceVertical = Column(Float)
    polarisation = Column(Float)
    monochromatorType = Column(String(255))
    setupDate = Column(DateTime)
    synchrotronName = Column(String(255))
    maxExpTimePerDataCollection = Column(Float(asdecimal=True))
    maxExposureTimePerImage = Column(Float, comment="unit: seconds")
    minExposureTimePerImage = Column(Float(asdecimal=True))
    goniostatMaxOscillationSpeed = Column(Float(asdecimal=True))
    goniostatMaxOscillationWidth = Column(
        Float(asdecimal=True), comment="unit: degrees"
    )
    goniostatMinOscillationWidth = Column(Float(asdecimal=True))
    maxTransmission = Column(Float(asdecimal=True), comment="unit: percentage")
    minTransmission = Column(Float(asdecimal=True))
    CS = Column(Float, comment="Spherical Aberration, Units: mm?")
    beamlineName = Column(String(50), comment="Beamline that this setup relates to")
    beamSizeXMin = Column(Float, comment="unit: um")
    beamSizeXMax = Column(Float, comment="unit: um")
    beamSizeYMin = Column(Float, comment="unit: um")
    beamSizeYMax = Column(Float, comment="unit: um")
    energyMin = Column(Float, comment="unit: eV")
    energyMax = Column(Float, comment="unit: eV")
    omegaMin = Column(Float, comment="unit: degrees")
    omegaMax = Column(Float, comment="unit: degrees")
    kappaMin = Column(Float, comment="unit: degrees")
    kappaMax = Column(Float, comment="unit: degrees")
    phiMin = Column(Float, comment="unit: degrees")
    phiMax = Column(Float, comment="unit: degrees")
    numberOfImagesMax = Column(MEDIUMINT(8))
    numberOfImagesMin = Column(MEDIUMINT(8))
    boxSizeXMin = Column(Float(asdecimal=True), comment="For gridscans, unit: um")
    boxSizeXMax = Column(Float(asdecimal=True), comment="For gridscans, unit: um")
    boxSizeYMin = Column(Float(asdecimal=True), comment="For gridscans, unit: um")
    boxSizeYMax = Column(Float(asdecimal=True), comment="For gridscans, unit: um")
    monoBandwidthMin = Column(Float(asdecimal=True), comment="unit: percentage")
    monoBandwidthMax = Column(Float(asdecimal=True), comment="unit: percentage")
    preferredDataCentre = Column(
        String(30),
        comment="Relevant datacentre to use to process data from this beamline",
    )
    amplitudeContrast = Column(Float, comment="Needed for cryo-ET")

    Detector_ = relationship("Detector", back_populates="BeamLineSetup")
    BLSession = relationship("BLSession", back_populates="BeamLineSetup_")


class DataCollectionFileAttachment(Base):
    __tablename__ = "DataCollectionFileAttachment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="_dataCollectionFileAttachmentId_fk1",
        ),
        Index("_dataCollectionFileAttachmentId_fk1", "dataCollectionId"),
    )

    dataCollectionFileAttachmentId = Column(INTEGER(11), primary_key=True)
    dataCollectionId = Column(INTEGER(11), nullable=False)
    fileFullPath = Column(String(255), nullable=False)
    createTime = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    fileType = Column(
        Enum("snapshot", "log", "xy", "recip", "pia", "warning", "params")
    )

    DataCollection_ = relationship(
        "DataCollection", back_populates="DataCollectionFileAttachment"
    )


class EventChain(Base):
    __tablename__ = "EventChain"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="EventChain_ibfk_1",
        ),
        Index("dataCollectionId", "dataCollectionId"),
        {"comment": "Groups events together in a data collection."},
    )

    eventChainId = Column(INTEGER(11), primary_key=True)
    dataCollectionId = Column(INTEGER(11), nullable=False)
    name = Column(String(255))

    DataCollection_ = relationship("DataCollection", back_populates="EventChain")
    Event = relationship("Event", back_populates="EventChain_")


class GridImageMap(Base):
    __tablename__ = "GridImageMap"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            name="_GridImageMap_ibfk1",
        ),
        Index("_GridImageMap_ibfk1", "dataCollectionId"),
    )

    gridImageMapId = Column(INTEGER(11), primary_key=True)
    dataCollectionId = Column(INTEGER(11))
    imageNumber = Column(
        INTEGER(11), comment="Movie number, sequential 1-n in time order"
    )
    outputFileId = Column(String(80), comment="File number, file 1 may not be movie 1")
    positionX = Column(Float, comment="X position of stage, Units: um")
    positionY = Column(Float, comment="Y position of stage, Units: um")

    DataCollection_ = relationship("DataCollection", back_populates="GridImageMap")


class Image(Base):
    __tablename__ = "Image"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Image_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["motorPositionId"],
            ["MotorPosition.motorPositionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Image_ibfk_2",
        ),
        Index("Image_FKIndex1", "dataCollectionId"),
        Index("Image_FKIndex2", "imageNumber"),
        Index("Image_Index3", "fileLocation", "fileName"),
        Index("motorPositionId", "motorPositionId"),
    )

    imageId = Column(INTEGER(12), primary_key=True)
    dataCollectionId = Column(INTEGER(11), nullable=False, server_default=text("0"))
    BLTIMESTAMP = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    imageNumber = Column(INTEGER(10))
    fileName = Column(String(255))
    fileLocation = Column(String(255))
    measuredIntensity = Column(Float)
    jpegFileFullPath = Column(String(255))
    jpegThumbnailFileFullPath = Column(String(255))
    temperature = Column(Float)
    cumulativeIntensity = Column(Float)
    synchrotronCurrent = Column(Float)
    comments = Column(String(1024))
    machineMessage = Column(String(1024))
    motorPositionId = Column(INTEGER(11))

    DataCollection_ = relationship("DataCollection", back_populates="Image")
    MotorPosition_ = relationship("MotorPosition", back_populates="Image")


class LDAPSearchBase(Base):
    __tablename__ = "LDAPSearchBase"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ldapSearchParametersId"],
            ["LDAPSearchParameters.ldapSearchParametersId"],
            name="LDAPSearchBase_fk_ldapSearchParametersId",
        ),
        Index("LDAPSearchBase_fk_ldapSearchParametersId", "ldapSearchParametersId"),
        {
            "comment": "LDAP search base and the sequence number in which it should be "
            "attempted"
        },
    )

    ldapSearchBaseId = Column(INTEGER(11), primary_key=True)
    ldapSearchParametersId = Column(
        INTEGER(11),
        nullable=False,
        comment="The other LDAP search parameters to be used with this search base",
    )
    searchBase = Column(
        String(200), nullable=False, comment="Name of the object we search for"
    )
    sequenceNumber = Column(
        TINYINT(3),
        nullable=False,
        comment="The number in the sequence of searches where this search base should be attempted",
    )

    LDAPSearchParameters_ = relationship(
        "LDAPSearchParameters", back_populates="LDAPSearchBase"
    )


class Movie(Base):
    __tablename__ = "Movie"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            name="Movie_ibfk1",
        ),
        Index("Movie_ibfk1", "dataCollectionId"),
    )

    movieId = Column(INTEGER(11), primary_key=True)
    createdTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
    )
    dataCollectionId = Column(INTEGER(11))
    movieNumber = Column(MEDIUMINT(8))
    movieFullPath = Column(String(255))
    positionX = Column(Float)
    positionY = Column(Float)
    nominalDefocus = Column(Float, comment="Nominal defocus, Units: A")
    angle = Column(Float, comment="unit: degrees relative to perpendicular to beam")
    fluence = Column(
        Float,
        comment="accumulated electron fluence from start to end of acquisition of this movie (commonly, but incorrectly, referred to as ‘dose’)",
    )
    numberOfFrames = Column(
        INTEGER(11),
        comment="number of frames per movie. This should be equivalent to the number of\xa0MotionCorrectionDrift\xa0entries, but the latter is a property of data analysis, whereas the number of frames is an intrinsic property of acquisition.",
    )

    DataCollection_ = relationship("DataCollection", back_populates="Movie")
    MotionCorrection = relationship("MotionCorrection", back_populates="Movie_")
    TiltImageAlignment = relationship("TiltImageAlignment", back_populates="Movie_")


class PDBEntry(Base):
    __tablename__ = "PDBEntry"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            ondelete="CASCADE",
            name="pdbEntry_FK1",
        ),
        Index("pdbEntryIdx1", "autoProcProgramId"),
    )

    pdbEntryId = Column(INTEGER(11), primary_key=True)
    autoProcProgramId = Column(INTEGER(11), nullable=False)
    code = Column(String(4))
    cell_a = Column(Float)
    cell_b = Column(Float)
    cell_c = Column(Float)
    cell_alpha = Column(Float)
    cell_beta = Column(Float)
    cell_gamma = Column(Float)
    resolution = Column(Float)
    pdbTitle = Column(String(255))
    pdbAuthors = Column(String(600))
    pdbDate = Column(DateTime)
    pdbBeamlineName = Column(String(50))
    beamlines = Column(String(100))
    distance = Column(Float)
    autoProcCount = Column(SMALLINT(6))
    dataCollectionCount = Column(SMALLINT(6))
    beamlineMatch = Column(TINYINT(1))
    authorMatch = Column(TINYINT(1))

    AutoProcProgram_ = relationship("AutoProcProgram", back_populates="PDBEntry")
    PDBEntry_has_AutoProcProgram = relationship(
        "PDBEntryHasAutoProcProgram", back_populates="PDBEntry_"
    )


class Particle(Base):
    __tablename__ = "Particle"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Particle_FK1",
        ),
        Index("Particle_FKIND1", "dataCollectionId"),
    )

    particleId = Column(INTEGER(11), primary_key=True)
    dataCollectionId = Column(INTEGER(11), nullable=False)
    x = Column(Float)
    y = Column(Float)

    DataCollection_ = relationship("DataCollection", back_populates="Particle")


class Person(Base):
    __tablename__ = "Person"
    __table_args__ = (
        ForeignKeyConstraint(
            ["laboratoryId"], ["Laboratory.laboratoryId"], name="Person_ibfk_1"
        ),
        Index("Person_FKIndex1", "laboratoryId"),
        Index("Person_FKIndexFamilyName", "familyName"),
        Index("Person_FKIndex_Login", "login", unique=True),
        Index("siteId", "siteId"),
    )

    personId = Column(INTEGER(10), primary_key=True)
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    laboratoryId = Column(INTEGER(10))
    siteId = Column(INTEGER(11))
    personUUID = Column(String(45))
    familyName = Column(String(100))
    givenName = Column(String(45))
    title = Column(String(45))
    emailAddress = Column(String(60))
    phoneNumber = Column(String(45))
    login = Column(String(45))
    faxNumber = Column(String(45))
    cache = Column(Text)
    externalId = Column(BINARY(16))

    Laboratory_ = relationship("Laboratory", back_populates="Person")
    UserGroup_ = relationship(
        "UserGroup", secondary="UserGroup_has_Person", back_populates="Person"
    )
    Project = relationship(
        "Project", secondary="Project_has_Person", back_populates="Person_"
    )
    ContainerReport = relationship("ContainerReport", back_populates="Person_")
    DataCollectionComment = relationship(
        "DataCollectionComment", back_populates="Person_"
    )
    Pod = relationship("Pod", back_populates="Person_")
    Project_ = relationship("Project", back_populates="Person1")
    Proposal = relationship("Proposal", back_populates="Person_")
    ContainerRegistry_has_Proposal = relationship(
        "ContainerRegistryHasProposal", back_populates="Person_"
    )
    LabContact = relationship("LabContact", back_populates="Person_")
    ProposalHasPerson = relationship("ProposalHasPerson", back_populates="Person_")
    SW_onceToken = relationship("SWOnceToken", back_populates="Person_")
    BF_fault = relationship(
        "BFFault", foreign_keys="[BFFault.assigneeId]", back_populates="Person_"
    )
    BF_fault_ = relationship(
        "BFFault", foreign_keys="[BFFault.personId]", back_populates="Person1"
    )
    Session_has_Person = relationship("SessionHasPerson", back_populates="Person_")
    Shipping = relationship("Shipping", back_populates="Person_")
    CourierTermsAccepted = relationship(
        "CourierTermsAccepted", back_populates="Person_"
    )
    DewarRegistry_has_Proposal = relationship(
        "DewarRegistryHasProposal", back_populates="Person_"
    )
    Container = relationship("Container", back_populates="Person_")
    ContainerQueue = relationship("ContainerQueue", back_populates="Person_")


class PhasingProgramAttachment(Base):
    __tablename__ = "PhasingProgramAttachment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["phasingProgramRunId"],
            ["PhasingProgramRun.phasingProgramRunId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Phasing_phasingProgramAttachmentfk_1",
        ),
        Index("PhasingProgramAttachment_FKIndex1", "phasingProgramRunId"),
    )

    phasingProgramAttachmentId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    phasingProgramRunId = Column(
        INTEGER(11), nullable=False, comment="Related program item"
    )
    fileType = Column(
        Enum("Map", "Logfile", "PDB", "CSV", "INS", "RES", "TXT"), comment="file type"
    )
    fileName = Column(String(45), comment="file name")
    filePath = Column(String(255), comment="file path")
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")

    PhasingProgramRun_ = relationship(
        "PhasingProgramRun", back_populates="PhasingProgramAttachment"
    )


class ProcessingJobImageSweep(Base):
    __tablename__ = "ProcessingJobImageSweep"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            name="ProcessingJobImageSweep_ibfk2",
        ),
        ForeignKeyConstraint(
            ["processingJobId"],
            ["ProcessingJob.processingJobId"],
            name="ProcessingJobImageSweep_ibfk1",
        ),
        Index("ProcessingJobImageSweep_ibfk1", "processingJobId"),
        Index("ProcessingJobImageSweep_ibfk2", "dataCollectionId"),
        {"comment": "This allows multiple sweeps per processing job for multi-xia2"},
    )

    processingJobImageSweepId = Column(INTEGER(11), primary_key=True)
    processingJobId = Column(INTEGER(11))
    dataCollectionId = Column(INTEGER(11))
    startImage = Column(MEDIUMINT(8))
    endImage = Column(MEDIUMINT(8))

    DataCollection_ = relationship(
        "DataCollection", back_populates="ProcessingJobImageSweep"
    )
    ProcessingJob_ = relationship(
        "ProcessingJob", back_populates="ProcessingJobImageSweep"
    )


class ProcessingJobParameter(Base):
    __tablename__ = "ProcessingJobParameter"
    __table_args__ = (
        ForeignKeyConstraint(
            ["processingJobId"],
            ["ProcessingJob.processingJobId"],
            name="ProcessingJobParameter_ibfk1",
        ),
        Index("ProcessingJobParameter_ibfk1", "processingJobId"),
    )

    processingJobParameterId = Column(INTEGER(11), primary_key=True)
    processingJobId = Column(INTEGER(11))
    parameterKey = Column(String(80), comment="E.g. resolution, spacegroup, pipeline")
    parameterValue = Column(String(1024))

    ProcessingJob_ = relationship(
        "ProcessingJob", back_populates="ProcessingJobParameter"
    )


class ProcessingPipeline(Base):
    __tablename__ = "ProcessingPipeline"
    __table_args__ = (
        ForeignKeyConstraint(
            ["processingPipelineCategoryId"],
            ["ProcessingPipelineCategory.processingPipelineCategoryId"],
            name="ProcessingPipeline_fk1",
        ),
        Index("ProcessingPipeline_fk1", "processingPipelineCategoryId"),
        {
            "comment": "A lookup table for different processing pipelines and their "
            "categories"
        },
    )

    processingPipelineId = Column(INTEGER(11), primary_key=True)
    name = Column(String(20), nullable=False)
    discipline = Column(String(10), nullable=False)
    processingPipelineCategoryId = Column(INTEGER(11))
    pipelineStatus = Column(
        Enum("automatic", "optional", "deprecated"),
        comment="Is the pipeline in operation or available",
    )
    reprocessing = Column(
        TINYINT(1),
        server_default=text("1"),
        comment="Pipeline is available for re-processing",
    )

    ProcessingPipelineCategory_ = relationship(
        "ProcessingPipelineCategory", back_populates="ProcessingPipeline"
    )
    Container = relationship("Container", back_populates="ProcessingPipeline_")


class SSXDataCollection(DataCollection):
    __tablename__ = "SSXDataCollection"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="SSXDataCollection_ibfk_1",
        ),
        {"comment": "Extends DataCollection with SSX-specific fields."},
    )

    dataCollectionId = Column(
        INTEGER(11),
        primary_key=True,
        comment="Primary key is same as dataCollection (1 to 1).",
    )
    repetitionRate = Column(Float)
    energyBandwidth = Column(Float)
    monoStripe = Column(String(255))
    jetSpeed = Column(Float, comment="For jet experiments.")
    jetSize = Column(Float, comment="For jet experiments.")
    chipPattern = Column(String(255), comment="For chip experiments.")
    chipModel = Column(String(255), comment="For chip experiments.")
    reactionDuration = Column(
        Float,
        comment="When images are taken at constant time relative to reaction start.",
    )
    laserEnergy = Column(Float)
    experimentName = Column(String(255))


class ScheduleComponent(Base):
    __tablename__ = "ScheduleComponent"
    __table_args__ = (
        ForeignKeyConstraint(
            ["inspectionTypeId"],
            ["InspectionType.inspectionTypeId"],
            ondelete="CASCADE",
            name="ScheduleComponent_fk2",
        ),
        ForeignKeyConstraint(
            ["scheduleId"],
            ["Schedule.scheduleId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ScheduleComponent_fk1",
        ),
        Index("ScheduleComponent_fk2", "inspectionTypeId"),
        Index("ScheduleComponent_idx1", "scheduleId"),
    )

    scheduleComponentId = Column(INTEGER(11), primary_key=True)
    scheduleId = Column(INTEGER(11), nullable=False)
    offset_hours = Column(INTEGER(11))
    inspectionTypeId = Column(INTEGER(11))

    InspectionType_ = relationship("InspectionType", back_populates="ScheduleComponent")
    Schedule_ = relationship("Schedule", back_populates="ScheduleComponent")
    ContainerInspection = relationship(
        "ContainerInspection", back_populates="ScheduleComponent_"
    )


class ScreeningInput(Base):
    __tablename__ = "ScreeningInput"
    __table_args__ = (
        ForeignKeyConstraint(
            ["screeningId"],
            ["Screening.screeningId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ScreeningInput_ibfk_1",
        ),
        Index("ScreeningInput_FKIndex1", "screeningId"),
    )

    screeningInputId = Column(INTEGER(10), primary_key=True)
    screeningId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    beamX = Column(Float)
    beamY = Column(Float)
    rmsErrorLimits = Column(Float)
    minimumFractionIndexed = Column(Float)
    maximumFractionRejected = Column(Float)
    minimumSignalToNoise = Column(Float)
    diffractionPlanId = Column(INTEGER(10), comment="references DiffractionPlan table")
    xmlSampleInformation = Column(LONGBLOB)

    Screening_ = relationship("Screening", back_populates="ScreeningInput")


class ScreeningOutputLattice(Base):
    __tablename__ = "ScreeningOutputLattice"
    __table_args__ = (
        ForeignKeyConstraint(
            ["screeningOutputId"],
            ["ScreeningOutput.screeningOutputId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ScreeningOutputLattice_ibfk_1",
        ),
        Index("ScreeningOutputLattice_FKIndex1", "screeningOutputId"),
    )

    screeningOutputLatticeId = Column(INTEGER(10), primary_key=True)
    screeningOutputId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    bltimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
    )
    spaceGroup = Column(String(45))
    pointGroup = Column(String(45))
    bravaisLattice = Column(String(45))
    rawOrientationMatrix_a_x = Column(Float)
    rawOrientationMatrix_a_y = Column(Float)
    rawOrientationMatrix_a_z = Column(Float)
    rawOrientationMatrix_b_x = Column(Float)
    rawOrientationMatrix_b_y = Column(Float)
    rawOrientationMatrix_b_z = Column(Float)
    rawOrientationMatrix_c_x = Column(Float)
    rawOrientationMatrix_c_y = Column(Float)
    rawOrientationMatrix_c_z = Column(Float)
    unitCell_a = Column(Float)
    unitCell_b = Column(Float)
    unitCell_c = Column(Float)
    unitCell_alpha = Column(Float)
    unitCell_beta = Column(Float)
    unitCell_gamma = Column(Float)
    labelitIndexing = Column(TINYINT(1), server_default=text("0"))

    ScreeningOutput_ = relationship(
        "ScreeningOutput", back_populates="ScreeningOutputLattice"
    )


class ScreeningRank(Base):
    __tablename__ = "ScreeningRank"
    __table_args__ = (
        ForeignKeyConstraint(
            ["screeningId"],
            ["Screening.screeningId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ScreeningRank_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["screeningRankSetId"],
            ["ScreeningRankSet.screeningRankSetId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ScreeningRank_ibfk_2",
        ),
        Index("ScreeningRank_FKIndex1", "screeningId"),
        Index("ScreeningRank_FKIndex2", "screeningRankSetId"),
    )

    screeningRankId = Column(INTEGER(10), primary_key=True)
    screeningRankSetId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    screeningId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    rankValue = Column(Float)
    rankInformation = Column(String(1024))

    Screening_ = relationship("Screening", back_populates="ScreeningRank")
    ScreeningRankSet_ = relationship("ScreeningRankSet", back_populates="ScreeningRank")


class SpaceGroup(Base):
    __tablename__ = "SpaceGroup"
    __table_args__ = (
        ForeignKeyConstraint(
            ["geometryClassnameId"],
            ["GeometryClassname.geometryClassnameId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="SpaceGroup_ibfk_1",
        ),
        Index("SpaceGroup_FKShortName", "spaceGroupShortName"),
        Index("geometryClassnameId", "geometryClassnameId"),
    )

    spaceGroupId = Column(INTEGER(10), primary_key=True, comment="Primary key")
    MX_used = Column(
        TINYINT(1),
        nullable=False,
        server_default=text("0"),
        comment="1 if used in the crystal form",
    )
    spaceGroupNumber = Column(INTEGER(10), comment="ccp4 number pr IUCR")
    spaceGroupShortName = Column(String(45), comment="short name without blank")
    spaceGroupName = Column(String(45), comment="verbose name")
    bravaisLattice = Column(String(45), comment="short name")
    bravaisLatticeName = Column(String(45), comment="verbose name")
    pointGroup = Column(String(45), comment="point group")
    geometryClassnameId = Column(INTEGER(11))

    GeometryClassname_ = relationship("GeometryClassname", back_populates="SpaceGroup")
    ModelBuilding = relationship("ModelBuilding", back_populates="SpaceGroup_")
    Phasing = relationship("Phasing", back_populates="SpaceGroup_")
    PhasingStep = relationship("PhasingStep", back_populates="SpaceGroup_")
    PreparePhasingData = relationship(
        "PreparePhasingData", back_populates="SpaceGroup_"
    )
    SubstructureDetermination = relationship(
        "SubstructureDetermination", back_populates="SpaceGroup_"
    )


class Tomogram(Base):
    __tablename__ = "Tomogram"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="Tomogram_fk_autoProcProgramId",
        ),
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Tomogram_fk_dataCollectionId",
        ),
        Index("Tomogram_fk_autoProcProgramId", "autoProcProgramId"),
        Index("Tomogram_fk_dataCollectionId", "dataCollectionId"),
        {
            "comment": "For storing per-sample, per-position data analysis results "
            "(reconstruction)"
        },
    )

    tomogramId = Column(INTEGER(11), primary_key=True)
    dataCollectionId = Column(INTEGER(11), comment="FK to\xa0DataCollection\xa0table")
    autoProcProgramId = Column(
        INTEGER(10),
        comment="FK, gives processing times/status and software information",
    )
    volumeFile = Column(
        String(255),
        comment=".mrc\xa0file representing the reconstructed tomogram volume",
    )
    stackFile = Column(
        String(255),
        comment=".mrc\xa0file containing the motion corrected images ordered by angle used as input for the reconstruction",
    )
    sizeX = Column(INTEGER(11), comment="unit: pixels")
    sizeY = Column(INTEGER(11), comment="unit: pixels")
    sizeZ = Column(INTEGER(11), comment="unit: pixels")
    pixelSpacing = Column(Float, comment="Angstrom/pixel conversion factor")
    residualErrorMean = Column(Float, comment="Alignment error, unit: nm")
    residualErrorSD = Column(
        Float, comment="Standard deviation of the alignment error, unit: nm"
    )
    xAxisCorrection = Column(Float, comment="X axis angle (etomo), unit: degrees")
    tiltAngleOffset = Column(Float, comment="tilt Axis offset (etomo), unit: degrees")
    zShift = Column(Float, comment="shift to center volumen in Z (etomo)")
    fileDirectory = Column(
        String(255), comment="Directory path for files referenced by this table"
    )
    centralSliceImage = Column(String(255), comment="Tomogram central slice file")
    tomogramMovie = Column(
        String(255), comment="Movie traversing the tomogram across an axis"
    )
    xyShiftPlot = Column(String(255), comment="XY shift plot file")
    projXY = Column(String(255), comment="XY projection file")
    projXZ = Column(String(255), comment="XZ projection file")
    recordTimeStamp = Column(
        DateTime,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )

    AutoProcProgram_ = relationship("AutoProcProgram", back_populates="Tomogram")
    DataCollection_ = relationship("DataCollection", back_populates="Tomogram")
    TiltImageAlignment = relationship("TiltImageAlignment", back_populates="Tomogram_")


class UserGroupHasLDAPSearchParameters(Base):
    __tablename__ = "UserGroup_has_LDAPSearchParameters"
    __table_args__ = (
        ForeignKeyConstraint(
            ["ldapSearchParametersId"],
            ["LDAPSearchParameters.ldapSearchParametersId"],
            name="UserGroup_has_LDAPSearchParameters_fk2",
        ),
        ForeignKeyConstraint(
            ["userGroupId"],
            ["UserGroup.userGroupId"],
            name="UserGroup_has_LDAPSearchParameters_fk1",
        ),
        Index("UserGroup_has_LDAPSearchParameters_fk2", "ldapSearchParametersId"),
        {
            "comment": "Gives the LDAP search parameters needed to find a set of "
            "usergroup members"
        },
    )

    userGroupId = Column(INTEGER(11), primary_key=True, nullable=False)
    ldapSearchParametersId = Column(INTEGER(11), primary_key=True, nullable=False)
    name = Column(
        String(200),
        primary_key=True,
        nullable=False,
        comment="Name of the object we search for",
    )

    LDAPSearchParameters_ = relationship(
        "LDAPSearchParameters", back_populates="UserGroup_has_LDAPSearchParameters"
    )
    UserGroup_ = relationship(
        "UserGroup", back_populates="UserGroup_has_LDAPSearchParameters"
    )


t_UserGroup_has_Permission = Table(
    "UserGroup_has_Permission",
    metadata,
    Column("userGroupId", INTEGER(11), primary_key=True, nullable=False),
    Column("permissionId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["permissionId"],
        ["Permission.permissionId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="UserGroup_has_Permission_fk2",
    ),
    ForeignKeyConstraint(
        ["userGroupId"],
        ["UserGroup.userGroupId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="UserGroup_has_Permission_fk1",
    ),
    Index("UserGroup_has_Permission_fk2", "permissionId"),
)


class WorkflowStep(Base):
    __tablename__ = "WorkflowStep"
    __table_args__ = (
        ForeignKeyConstraint(
            ["workflowId"], ["Workflow.workflowId"], name="step_to_workflow_fk"
        ),
        Index("step_to_workflow_fk_idx", "workflowId"),
    )

    workflowStepId = Column(INTEGER(11), primary_key=True)
    workflowId = Column(INTEGER(11), nullable=False)
    type = Column(String(45))
    status = Column(String(45))
    folderPath = Column(String(1024))
    imageResultFilePath = Column(String(1024))
    htmlResultFilePath = Column(String(1024))
    resultFilePath = Column(String(1024))
    comments = Column(String(2048))
    crystalSizeX = Column(String(45))
    crystalSizeY = Column(String(45))
    crystalSizeZ = Column(String(45))
    maxDozorScore = Column(String(45))
    recordTimeStamp = Column(TIMESTAMP)

    Workflow_ = relationship("Workflow", back_populates="WorkflowStep")


class XRFFluorescenceMappingROI(Base):
    __tablename__ = "XRFFluorescenceMappingROI"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"],
            ["BLSample.blSampleId"],
            name="XRFFluorescenceMappingROI_FKblSampleId",
        ),
        Index("XRFFluorescenceMappingROI_FKblSampleId", "blSampleId"),
    )

    xrfFluorescenceMappingROIId = Column(INTEGER(11), primary_key=True)
    startEnergy = Column(Float, nullable=False)
    endEnergy = Column(Float, nullable=False)
    element = Column(String(2))
    edge = Column(
        String(15),
        comment="Edge type i.e. Ka1, could be a custom edge in case of overlap Ka1-noCa",
    )
    r = Column(TINYINT(3), comment="R colour component")
    g = Column(TINYINT(3), comment="G colour component")
    b = Column(TINYINT(3), comment="B colour component")
    blSampleId = Column(
        INTEGER(10), comment="ROIs can be created within the context of a sample"
    )
    scalar = Column(
        String(50),
        comment="For ROIs that are not an element, i.e. could be a scan counter instead",
    )

    BLSample_ = relationship("BLSample", back_populates="XRFFluorescenceMappingROI")
    XRFFluorescenceMapping = relationship(
        "XRFFluorescenceMapping", back_populates="XRFFluorescenceMappingROI_"
    )


class ZcZocaloBuffer(Base):
    __tablename__ = "zc_ZocaloBuffer"
    __table_args__ = (
        ForeignKeyConstraint(
            ["AutoProcProgramID"],
            ["AutoProcProgram.autoProcProgramId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="AutoProcProgram_fk_AutoProcProgramId",
        ),
    )

    AutoProcProgramID = Column(
        INTEGER(10),
        primary_key=True,
        nullable=False,
        comment="Reference to an existing AutoProcProgram",
    )
    UUID = Column(
        INTEGER(10),
        primary_key=True,
        nullable=False,
        comment="AutoProcProgram-specific unique identifier",
    )
    Reference = Column(
        INTEGER(10),
        comment="Context-dependent reference to primary key IDs in other ISPyB tables",
    )

    AutoProcProgram_ = relationship("AutoProcProgram", back_populates="zc_ZocaloBuffer")


class AutoProcScalingStatistics(Base):
    __tablename__ = "AutoProcScalingStatistics"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcScalingId"],
            ["AutoProcScaling.autoProcScalingId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="_AutoProcScalingStatisticsFk1",
        ),
        Index("AutoProcScalingStatistics_FKindexType", "scalingStatisticsType"),
        Index(
            "AutoProcScalingStatistics_scalingId_statisticsType",
            "autoProcScalingId",
            "scalingStatisticsType",
        ),
    )

    autoProcScalingStatisticsId = Column(
        INTEGER(10), primary_key=True, comment="Primary key (auto-incremented)"
    )
    scalingStatisticsType = Column(
        Enum("overall", "innerShell", "outerShell"),
        nullable=False,
        server_default=text("'overall'"),
        comment="Scaling statistics type",
    )
    autoProcScalingId = Column(
        INTEGER(10), comment="Related autoProcScaling item (used by foreign key)"
    )
    comments = Column(String(255), comment="Comments...")
    resolutionLimitLow = Column(Float, comment="Low resolution limit")
    resolutionLimitHigh = Column(Float, comment="High resolution limit")
    rMerge = Column(Float, comment="Rmerge")
    rMeasWithinIPlusIMinus = Column(Float, comment="Rmeas (within I+/I-)")
    rMeasAllIPlusIMinus = Column(Float, comment="Rmeas (all I+ & I-)")
    rPimWithinIPlusIMinus = Column(Float, comment="Rpim (within I+/I-) ")
    rPimAllIPlusIMinus = Column(Float, comment="Rpim (all I+ & I-)")
    fractionalPartialBias = Column(Float, comment="Fractional partial bias")
    nTotalObservations = Column(INTEGER(10), comment="Total number of observations")
    nTotalUniqueObservations = Column(INTEGER(10), comment="Total number unique")
    meanIOverSigI = Column(Float, comment="Mean((I)/sd(I))")
    completeness = Column(Float, comment="Completeness")
    multiplicity = Column(Float, comment="Multiplicity")
    anomalousCompleteness = Column(Float, comment="Anomalous completeness")
    anomalousMultiplicity = Column(Float, comment="Anomalous multiplicity")
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")
    anomalous = Column(
        TINYINT(1), server_default=text("0"), comment="boolean type:0 noanoum - 1 anoum"
    )
    ccHalf = Column(Float, comment="information from XDS")
    ccAnomalous = Column(Float)
    resIOverSigI2 = Column(Float, comment="Resolution where I/Sigma(I) equals 2")

    AutoProcScaling_ = relationship(
        "AutoProcScaling", back_populates="AutoProcScalingStatistics"
    )


class AutoProcScalingHasInt(Base):
    __tablename__ = "AutoProcScaling_has_Int"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcIntegrationId"],
            ["AutoProcIntegration.autoProcIntegrationId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="AutoProcScaling_has_IntFk2",
        ),
        ForeignKeyConstraint(
            ["autoProcScalingId"],
            ["AutoProcScaling.autoProcScalingId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="AutoProcScaling_has_IntFk1",
        ),
        Index("AutoProcScal_has_IntIdx2", "autoProcIntegrationId"),
        Index(
            "AutoProcScalingHasInt_FKIndex3",
            "autoProcScalingId",
            "autoProcIntegrationId",
        ),
    )

    autoProcScaling_has_IntId = Column(
        INTEGER(10), primary_key=True, comment="Primary key (auto-incremented)"
    )
    autoProcIntegrationId = Column(
        INTEGER(10), nullable=False, comment="AutoProcIntegration item"
    )
    autoProcScalingId = Column(INTEGER(10), comment="AutoProcScaling item")
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")

    AutoProcIntegration_ = relationship(
        "AutoProcIntegration", back_populates="AutoProcScaling_has_Int"
    )
    AutoProcScaling_ = relationship(
        "AutoProcScaling", back_populates="AutoProcScaling_has_Int"
    )


class AutoProcStatus(Base):
    __tablename__ = "AutoProcStatus"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcIntegrationId"],
            ["AutoProcIntegration.autoProcIntegrationId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="AutoProcStatus_ibfk_1",
        ),
        Index("AutoProcStatus_FKIndex1", "autoProcIntegrationId"),
        {"comment": "AutoProcStatus table is linked to AutoProcIntegration"},
    )

    autoProcStatusId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    autoProcIntegrationId = Column(INTEGER(10), nullable=False)
    step = Column(
        Enum("Indexing", "Integration", "Correction", "Scaling", "Importing"),
        nullable=False,
        comment="autoprocessing step",
    )
    status = Column(
        Enum("Launched", "Successful", "Failed"),
        nullable=False,
        comment="autoprocessing status",
    )
    bltimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
    )
    comments = Column(String(1024), comment="comments")

    AutoProcIntegration_ = relationship(
        "AutoProcIntegration", back_populates="AutoProcStatus"
    )


class BFComponentBeamline(Base):
    __tablename__ = "BF_component_beamline"
    __table_args__ = (
        ForeignKeyConstraint(
            ["componentId"],
            ["BF_component.componentId"],
            name="bf_component_beamline_FK1",
        ),
        Index("bf_component_beamline_FK1", "componentId"),
    )

    component_beamlineId = Column(INTEGER(10), primary_key=True)
    componentId = Column(INTEGER(10))
    beamlinename = Column(String(20))

    BF_component = relationship("BFComponent", back_populates="BF_component_beamline")


class BFSubcomponent(Base):
    __tablename__ = "BF_subcomponent"
    __table_args__ = (
        ForeignKeyConstraint(
            ["componentId"], ["BF_component.componentId"], name="bf_subcomponent_FK1"
        ),
        Index("bf_subcomponent_FK1", "componentId"),
    )

    subcomponentId = Column(INTEGER(10), primary_key=True)
    componentId = Column(INTEGER(10))
    name = Column(String(100))
    description = Column(String(200))

    BF_component = relationship("BFComponent", back_populates="BF_subcomponent")
    BF_subcomponent_beamline = relationship(
        "BFSubcomponentBeamline", back_populates="BF_subcomponent"
    )
    BF_fault = relationship("BFFault", back_populates="BF_subcomponent")


class BLSampleImageHasAutoScoreClass(Base):
    __tablename__ = "BLSampleImage_has_AutoScoreClass"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleImageAutoScoreClassId"],
            ["BLSampleImageAutoScoreClass.blSampleImageAutoScoreClassId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSampleImage_has_AutoScoreClass_fk2",
        ),
        ForeignKeyConstraint(
            ["blSampleImageId"],
            ["BLSampleImage.blSampleImageId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSampleImage_has_AutoScoreClass_fk1",
        ),
        Index("BLSampleImage_has_AutoScoreClass_fk2", "blSampleImageAutoScoreClassId"),
        {
            "comment": "Many-to-many relationship between drop images and thing being "
            "scored, as well as the actual probability (score) that the drop "
            "image contains that thing"
        },
    )

    blSampleImageId = Column(INTEGER(11), primary_key=True, nullable=False)
    blSampleImageAutoScoreClassId = Column(TINYINT(3), primary_key=True, nullable=False)
    probability = Column(Float)

    BLSampleImageAutoScoreClass_ = relationship(
        "BLSampleImageAutoScoreClass", back_populates="BLSampleImage_has_AutoScoreClass"
    )
    BLSampleImage_ = relationship(
        "BLSampleImage", back_populates="BLSampleImage_has_AutoScoreClass"
    )


class ContainerReport(Base):
    __tablename__ = "ContainerReport"
    __table_args__ = (
        ForeignKeyConstraint(
            ["containerRegistryId"],
            ["ContainerRegistry.containerRegistryId"],
            name="ContainerReport_ibfk1",
        ),
        ForeignKeyConstraint(
            ["personId"], ["Person.personId"], name="ContainerReport_ibfk2"
        ),
        Index("ContainerReport_ibfk1", "containerRegistryId"),
        Index("ContainerReport_ibfk2", "personId"),
    )

    containerReportId = Column(INTEGER(11), primary_key=True)
    containerRegistryId = Column(INTEGER(11))
    personId = Column(INTEGER(10), comment="Person making report")
    report = Column(Text)
    attachmentFilePath = Column(String(255))
    recordTimestamp = Column(DateTime)

    ContainerRegistry_ = relationship(
        "ContainerRegistry", back_populates="ContainerReport"
    )
    Person_ = relationship("Person", back_populates="ContainerReport")


class DataCollectionComment(Base):
    __tablename__ = "DataCollectionComment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="dataCollectionComment_fk1",
        ),
        ForeignKeyConstraint(
            ["personId"],
            ["Person.personId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="dataCollectionComment_fk2",
        ),
        Index("dataCollectionComment_fk1", "dataCollectionId"),
        Index("dataCollectionComment_fk2", "personId"),
    )

    dataCollectionCommentId = Column(INTEGER(11), primary_key=True)
    dataCollectionId = Column(INTEGER(11), nullable=False)
    personId = Column(INTEGER(10), nullable=False)
    createTime = Column(
        DateTime, nullable=False, server_default=text("current_timestamp()")
    )
    comments = Column(String(4000))
    modTime = Column(Date)

    DataCollection_ = relationship(
        "DataCollection", back_populates="DataCollectionComment"
    )
    Person_ = relationship("Person", back_populates="DataCollectionComment")


class MXMRRun(Base):
    __tablename__ = "MXMRRun"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            name="mxMRRun_FK2",
        ),
        ForeignKeyConstraint(
            ["autoProcScalingId"],
            ["AutoProcScaling.autoProcScalingId"],
            name="mxMRRun_FK1",
        ),
        Index("mxMRRun_FK1", "autoProcScalingId"),
        Index("mxMRRun_FK2", "autoProcProgramId"),
    )

    mxMRRunId = Column(INTEGER(11), primary_key=True)
    autoProcScalingId = Column(INTEGER(11), nullable=False)
    rValueStart = Column(Float)
    rValueEnd = Column(Float)
    rFreeValueStart = Column(Float)
    rFreeValueEnd = Column(Float)
    LLG = Column(Float, comment="Log Likelihood Gain")
    TFZ = Column(Float, comment="Translation Function Z-score")
    spaceGroup = Column(String(45), comment="Space group of the MR solution")
    autoProcProgramId = Column(INTEGER(11))

    AutoProcProgram_ = relationship("AutoProcProgram", back_populates="MXMRRun")
    AutoProcScaling_ = relationship("AutoProcScaling", back_populates="MXMRRun")
    MXMRRunBlob = relationship("MXMRRunBlob", back_populates="MXMRRun_")


class ModelBuilding(Base):
    __tablename__ = "ModelBuilding"
    __table_args__ = (
        ForeignKeyConstraint(
            ["phasingAnalysisId"],
            ["PhasingAnalysis.phasingAnalysisId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ModelBuilding_phasingAnalysisfk_1",
        ),
        ForeignKeyConstraint(
            ["phasingProgramRunId"],
            ["PhasingProgramRun.phasingProgramRunId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ModelBuilding_phasingProgramRunfk_1",
        ),
        ForeignKeyConstraint(
            ["spaceGroupId"],
            ["SpaceGroup.spaceGroupId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ModelBuilding_spaceGroupfk_1",
        ),
        Index("ModelBuilding_FKIndex1", "phasingAnalysisId"),
        Index("ModelBuilding_FKIndex2", "phasingProgramRunId"),
        Index("ModelBuilding_FKIndex3", "spaceGroupId"),
    )

    modelBuildingId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    phasingAnalysisId = Column(
        INTEGER(11), nullable=False, comment="Related phasing analysis item"
    )
    phasingProgramRunId = Column(
        INTEGER(11), nullable=False, comment="Related program item"
    )
    spaceGroupId = Column(INTEGER(10), comment="Related spaceGroup")
    lowRes = Column(Float(asdecimal=True))
    highRes = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")

    PhasingAnalysis_ = relationship("PhasingAnalysis", back_populates="ModelBuilding")
    PhasingProgramRun_ = relationship(
        "PhasingProgramRun", back_populates="ModelBuilding"
    )
    SpaceGroup_ = relationship("SpaceGroup", back_populates="ModelBuilding")


class MotionCorrection(Base):
    __tablename__ = "MotionCorrection"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            name="MotionCorrection_ibfk2",
        ),
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            name="_MotionCorrection_ibfk1",
        ),
        ForeignKeyConstraint(
            ["movieId"], ["Movie.movieId"], name="MotionCorrection_ibfk3"
        ),
        Index("MotionCorrection_ibfk2", "autoProcProgramId"),
        Index("MotionCorrection_ibfk3", "movieId"),
        Index("_MotionCorrection_ibfk1", "dataCollectionId"),
    )

    motionCorrectionId = Column(INTEGER(11), primary_key=True)
    dataCollectionId = Column(INTEGER(11))
    autoProcProgramId = Column(INTEGER(11))
    imageNumber = Column(SMALLINT(5), comment="Movie number, sequential in time 1-n")
    firstFrame = Column(SMALLINT(5), comment="First frame of movie used")
    lastFrame = Column(SMALLINT(5), comment="Last frame of movie used")
    dosePerFrame = Column(Float, comment="Dose per frame, Units: e-/A^2")
    doseWeight = Column(Float, comment="Dose weight, Units: dimensionless")
    totalMotion = Column(Float, comment="Total motion, Units: A")
    averageMotionPerFrame = Column(Float, comment="Average motion per frame, Units: A")
    driftPlotFullPath = Column(String(255), comment="Full path to the drift plot")
    micrographFullPath = Column(String(255), comment="Full path to the micrograph")
    micrographSnapshotFullPath = Column(
        String(255), comment="Full path to a snapshot (jpg) of the micrograph"
    )
    patchesUsedX = Column(
        MEDIUMINT(8), comment="Number of patches used in x (for motioncor2)"
    )
    patchesUsedY = Column(
        MEDIUMINT(8), comment="Number of patches used in y (for motioncor2)"
    )
    fftFullPath = Column(
        String(255), comment="Full path to the jpg image of the raw micrograph FFT"
    )
    fftCorrectedFullPath = Column(
        String(255),
        comment="Full path to the jpg image of the drift corrected micrograph FFT",
    )
    comments = Column(String(255))
    movieId = Column(INTEGER(11))

    AutoProcProgram_ = relationship(
        "AutoProcProgram", back_populates="MotionCorrection"
    )
    DataCollection_ = relationship("DataCollection", back_populates="MotionCorrection")
    Movie_ = relationship("Movie", back_populates="MotionCorrection")
    CTF = relationship("CTF", back_populates="MotionCorrection_")
    MotionCorrectionDrift = relationship(
        "MotionCorrectionDrift", back_populates="MotionCorrection_"
    )
    ParticlePicker = relationship("ParticlePicker", back_populates="MotionCorrection_")
    RelativeIceThickness = relationship(
        "RelativeIceThickness", back_populates="MotionCorrection_"
    )


class PDBEntryHasAutoProcProgram(Base):
    __tablename__ = "PDBEntry_has_AutoProcProgram"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            ondelete="CASCADE",
            name="pdbEntry_AutoProcProgram_FK2",
        ),
        ForeignKeyConstraint(
            ["pdbEntryId"],
            ["PDBEntry.pdbEntryId"],
            ondelete="CASCADE",
            name="pdbEntry_AutoProcProgram_FK1",
        ),
        Index("pdbEntry_AutoProcProgramIdx1", "pdbEntryId"),
        Index("pdbEntry_AutoProcProgramIdx2", "autoProcProgramId"),
    )

    pdbEntryHasAutoProcId = Column(INTEGER(11), primary_key=True)
    pdbEntryId = Column(INTEGER(11), nullable=False)
    autoProcProgramId = Column(INTEGER(11), nullable=False)
    distance = Column(Float)

    AutoProcProgram_ = relationship(
        "AutoProcProgram", back_populates="PDBEntry_has_AutoProcProgram"
    )
    PDBEntry_ = relationship("PDBEntry", back_populates="PDBEntry_has_AutoProcProgram")


class Phasing(Base):
    __tablename__ = "Phasing"
    __table_args__ = (
        ForeignKeyConstraint(
            ["phasingAnalysisId"],
            ["PhasingAnalysis.phasingAnalysisId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Phasing_phasingAnalysisfk_1",
        ),
        ForeignKeyConstraint(
            ["phasingProgramRunId"],
            ["PhasingProgramRun.phasingProgramRunId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Phasing_phasingProgramRunfk_1",
        ),
        ForeignKeyConstraint(
            ["spaceGroupId"],
            ["SpaceGroup.spaceGroupId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Phasing_spaceGroupfk_1",
        ),
        Index("Phasing_FKIndex1", "phasingAnalysisId"),
        Index("Phasing_FKIndex2", "phasingProgramRunId"),
        Index("Phasing_FKIndex3", "spaceGroupId"),
    )

    phasingId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    phasingAnalysisId = Column(
        INTEGER(11), nullable=False, comment="Related phasing analysis item"
    )
    phasingProgramRunId = Column(
        INTEGER(11), nullable=False, comment="Related program item"
    )
    spaceGroupId = Column(INTEGER(10), comment="Related spaceGroup")
    method = Column(
        Enum("solvent flattening", "solvent flipping", "e", "SAD", "shelxe"),
        comment="phasing method",
    )
    solventContent = Column(Float(asdecimal=True))
    enantiomorph = Column(TINYINT(1), comment="0 or 1")
    lowRes = Column(Float(asdecimal=True))
    highRes = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime, server_default=text("current_timestamp()"))

    PhasingAnalysis_ = relationship("PhasingAnalysis", back_populates="Phasing")
    PhasingProgramRun_ = relationship("PhasingProgramRun", back_populates="Phasing")
    SpaceGroup_ = relationship("SpaceGroup", back_populates="Phasing")


class PhasingStep(Base):
    __tablename__ = "PhasingStep"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcScalingId"],
            ["AutoProcScaling.autoProcScalingId"],
            name="FK_autoprocScaling",
        ),
        ForeignKeyConstraint(
            ["programRunId"],
            ["PhasingProgramRun.phasingProgramRunId"],
            name="FK_program",
        ),
        ForeignKeyConstraint(
            ["spaceGroupId"], ["SpaceGroup.spaceGroupId"], name="FK_spacegroup"
        ),
        Index("FK_autoprocScaling_id", "autoProcScalingId"),
        Index("FK_phasingAnalysis_id", "phasingAnalysisId"),
        Index("FK_programRun_id", "programRunId"),
        Index("FK_spacegroup_id", "spaceGroupId"),
    )

    phasingStepId = Column(INTEGER(10), primary_key=True)
    recordTimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    previousPhasingStepId = Column(INTEGER(10))
    programRunId = Column(INTEGER(10))
    spaceGroupId = Column(INTEGER(10))
    autoProcScalingId = Column(INTEGER(10))
    phasingAnalysisId = Column(INTEGER(10))
    phasingStepType = Column(
        Enum("PREPARE", "SUBSTRUCTUREDETERMINATION", "PHASING", "MODELBUILDING")
    )
    method = Column(String(45))
    solventContent = Column(String(45))
    enantiomorph = Column(String(45))
    lowRes = Column(String(45))
    highRes = Column(String(45))

    AutoProcScaling_ = relationship("AutoProcScaling", back_populates="PhasingStep")
    PhasingProgramRun_ = relationship("PhasingProgramRun", back_populates="PhasingStep")
    SpaceGroup_ = relationship("SpaceGroup", back_populates="PhasingStep")
    PhasingStatistics = relationship("PhasingStatistics", back_populates="PhasingStep_")


class PhasingHasScaling(Base):
    __tablename__ = "Phasing_has_Scaling"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcScalingId"],
            ["AutoProcScaling.autoProcScalingId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="PhasingHasScaling_autoProcScalingfk_1",
        ),
        ForeignKeyConstraint(
            ["phasingAnalysisId"],
            ["PhasingAnalysis.phasingAnalysisId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="PhasingHasScaling_phasingAnalysisfk_1",
        ),
        Index("PhasingHasScaling_FKIndex1", "phasingAnalysisId"),
        Index("PhasingHasScaling_FKIndex2", "autoProcScalingId"),
    )

    phasingHasScalingId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    phasingAnalysisId = Column(
        INTEGER(11), nullable=False, comment="Related phasing analysis item"
    )
    autoProcScalingId = Column(
        INTEGER(10), nullable=False, comment="Related autoProcScaling item"
    )
    datasetNumber = Column(
        INTEGER(11),
        comment="serial number of the dataset and always reserve 0 for the reference",
    )
    recordTimeStamp = Column(DateTime, server_default=text("current_timestamp()"))

    AutoProcScaling_ = relationship(
        "AutoProcScaling", back_populates="Phasing_has_Scaling"
    )
    PhasingAnalysis_ = relationship(
        "PhasingAnalysis", back_populates="Phasing_has_Scaling"
    )
    PhasingStatistics = relationship(
        "PhasingStatistics",
        foreign_keys="[PhasingStatistics.phasingHasScalingId1]",
        back_populates="Phasing_has_Scaling",
    )
    PhasingStatistics_ = relationship(
        "PhasingStatistics",
        foreign_keys="[PhasingStatistics.phasingHasScalingId2]",
        back_populates="Phasing_has_Scaling_",
    )


class Pod(Base):
    __tablename__ = "Pod"
    __table_args__ = (
        ForeignKeyConstraint(
            ["personId"],
            ["Person.personId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Pod_fk1",
        ),
        Index("Pod_fk1", "personId"),
        {"comment": "Status tracker for k8s pods launched from SynchWeb"},
    )

    podId = Column(INTEGER(10), primary_key=True)
    personId = Column(
        INTEGER(10),
        nullable=False,
        comment="Pod owner defined by the logged in SynchWeb user who requested the pod start up",
    )
    app = Column(Enum("MAXIV HDF5 Viewer", "H5Web", "JNB"), nullable=False)
    created = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    filePath = Column(
        String(255), comment="File or directory path to mount into the Pod if required"
    )
    podName = Column(String(255))
    status = Column(String(25))
    ip = Column(String(15))
    message = Column(
        Text,
        comment="Generic text field intended for storing error messages related to status field",
    )
    shutdown = Column(TIMESTAMP)

    Person_ = relationship("Person", back_populates="Pod")


class PreparePhasingData(Base):
    __tablename__ = "PreparePhasingData"
    __table_args__ = (
        ForeignKeyConstraint(
            ["phasingAnalysisId"],
            ["PhasingAnalysis.phasingAnalysisId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="PreparePhasingData_phasingAnalysisfk_1",
        ),
        ForeignKeyConstraint(
            ["phasingProgramRunId"],
            ["PhasingProgramRun.phasingProgramRunId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="PreparePhasingData_phasingProgramRunfk_1",
        ),
        ForeignKeyConstraint(
            ["spaceGroupId"],
            ["SpaceGroup.spaceGroupId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="PreparePhasingData_spaceGroupfk_1",
        ),
        Index("PreparePhasingData_FKIndex1", "phasingAnalysisId"),
        Index("PreparePhasingData_FKIndex2", "phasingProgramRunId"),
        Index("PreparePhasingData_FKIndex3", "spaceGroupId"),
    )

    preparePhasingDataId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    phasingAnalysisId = Column(
        INTEGER(11), nullable=False, comment="Related phasing analysis item"
    )
    phasingProgramRunId = Column(
        INTEGER(11), nullable=False, comment="Related program item"
    )
    spaceGroupId = Column(INTEGER(10), comment="Related spaceGroup")
    lowRes = Column(Float(asdecimal=True))
    highRes = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")

    PhasingAnalysis_ = relationship(
        "PhasingAnalysis", back_populates="PreparePhasingData"
    )
    PhasingProgramRun_ = relationship(
        "PhasingProgramRun", back_populates="PreparePhasingData"
    )
    SpaceGroup_ = relationship("SpaceGroup", back_populates="PreparePhasingData")


class Project(Base):
    __tablename__ = "Project"
    __table_args__ = (
        ForeignKeyConstraint(["personId"], ["Person.personId"], name="Project_FK1"),
        Index("Project_FK1", "personId"),
    )

    projectId = Column(INTEGER(11), primary_key=True)
    personId = Column(INTEGER(11))
    title = Column(String(200))
    acronym = Column(String(100))
    owner = Column(String(50))

    BLSample_ = relationship(
        "BLSample", secondary="Project_has_BLSample", back_populates="Project"
    )
    Person_ = relationship(
        "Person", secondary="Project_has_Person", back_populates="Project"
    )
    Person1 = relationship("Person", back_populates="Project_")
    Protein = relationship(
        "Protein", secondary="Project_has_Protein", back_populates="Project_"
    )
    BLSession = relationship(
        "BLSession", secondary="Project_has_Session", back_populates="Project_"
    )
    Shipping = relationship(
        "Shipping", secondary="Project_has_Shipping", back_populates="Project_"
    )
    XFEFluorescenceSpectrum = relationship(
        "XFEFluorescenceSpectrum",
        secondary="Project_has_XFEFSpectrum",
        back_populates="Project_",
    )
    Project_has_User = relationship("ProjectHasUser", back_populates="Project_")
    DataCollectionGroup = relationship(
        "DataCollectionGroup",
        secondary="Project_has_DCGroup",
        back_populates="Project_",
    )
    EnergyScan = relationship(
        "EnergyScan", secondary="Project_has_EnergyScan", back_populates="Project_"
    )


class Proposal(Base):
    __tablename__ = "Proposal"
    __table_args__ = (
        ForeignKeyConstraint(
            ["personId"],
            ["Person.personId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Proposal_ibfk_1",
        ),
        Index("Proposal_FKIndex1", "personId"),
        Index(
            "Proposal_FKIndexCodeNumber", "proposalCode", "proposalNumber", unique=True
        ),
    )

    proposalId = Column(INTEGER(10), primary_key=True)
    personId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    bltimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    title = Column(String(200))
    proposalCode = Column(String(45))
    proposalNumber = Column(String(45))
    proposalType = Column(String(2), comment="Proposal type: MX, BX")
    externalId = Column(BINARY(16))
    state = Column(Enum("Open", "Closed", "Cancelled"), server_default=text("'Open'"))

    Person_ = relationship("Person", back_populates="Proposal")
    BLSampleGroup = relationship("BLSampleGroup", back_populates="Proposal_")
    BLSession = relationship("BLSession", back_populates="Proposal_")
    Component = relationship("Component", back_populates="Proposal_")
    ContainerRegistry_has_Proposal = relationship(
        "ContainerRegistryHasProposal", back_populates="Proposal_"
    )
    DiffractionPlan = relationship("DiffractionPlan", back_populates="Proposal_")
    LabContact = relationship("LabContact", back_populates="Proposal_")
    ProposalHasPerson = relationship("ProposalHasPerson", back_populates="Proposal_")
    Protein = relationship("Protein", back_populates="Proposal_")
    SW_onceToken = relationship("SWOnceToken", back_populates="Proposal_")
    Screen = relationship("Screen", back_populates="Proposal_")
    DewarRegistry = relationship("DewarRegistry", back_populates="Proposal_")
    Shipping = relationship("Shipping", back_populates="Proposal_")
    CourierTermsAccepted = relationship(
        "CourierTermsAccepted", back_populates="Proposal_"
    )
    DewarRegistry_has_Proposal = relationship(
        "DewarRegistryHasProposal", back_populates="Proposal_"
    )


class SubstructureDetermination(Base):
    __tablename__ = "SubstructureDetermination"
    __table_args__ = (
        ForeignKeyConstraint(
            ["phasingAnalysisId"],
            ["PhasingAnalysis.phasingAnalysisId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="SubstructureDetermination_phasingAnalysisfk_1",
        ),
        ForeignKeyConstraint(
            ["phasingProgramRunId"],
            ["PhasingProgramRun.phasingProgramRunId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="SubstructureDetermination_phasingProgramRunfk_1",
        ),
        ForeignKeyConstraint(
            ["spaceGroupId"],
            ["SpaceGroup.spaceGroupId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="SubstructureDetermination_spaceGroupfk_1",
        ),
        Index("SubstructureDetermination_FKIndex1", "phasingAnalysisId"),
        Index("SubstructureDetermination_FKIndex2", "phasingProgramRunId"),
        Index("SubstructureDetermination_FKIndex3", "spaceGroupId"),
    )

    substructureDeterminationId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    phasingAnalysisId = Column(
        INTEGER(11), nullable=False, comment="Related phasing analysis item"
    )
    phasingProgramRunId = Column(
        INTEGER(11), nullable=False, comment="Related program item"
    )
    spaceGroupId = Column(INTEGER(10), comment="Related spaceGroup")
    method = Column(
        Enum("SAD", "MAD", "SIR", "SIRAS", "MR", "MIR", "MIRAS", "RIP", "RIPAS"),
        comment="phasing method",
    )
    lowRes = Column(Float(asdecimal=True))
    highRes = Column(Float(asdecimal=True))
    recordTimeStamp = Column(DateTime, comment="Creation or last update date/time")

    PhasingAnalysis_ = relationship(
        "PhasingAnalysis", back_populates="SubstructureDetermination"
    )
    PhasingProgramRun_ = relationship(
        "PhasingProgramRun", back_populates="SubstructureDetermination"
    )
    SpaceGroup_ = relationship("SpaceGroup", back_populates="SubstructureDetermination")


class TiltImageAlignment(Base):
    __tablename__ = "TiltImageAlignment"
    __table_args__ = (
        ForeignKeyConstraint(
            ["movieId"],
            ["Movie.movieId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="TiltImageAlignment_fk_movieId",
        ),
        ForeignKeyConstraint(
            ["tomogramId"],
            ["Tomogram.tomogramId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="TiltImageAlignment_fk_tomogramId",
        ),
        Index("TiltImageAlignment_fk_tomogramId", "tomogramId"),
        {"comment": "For storing per-movie analysis results (reconstruction)"},
    )

    movieId = Column(
        INTEGER(11), primary_key=True, nullable=False, comment="FK to\xa0Movie\xa0table"
    )
    tomogramId = Column(
        INTEGER(11),
        primary_key=True,
        nullable=False,
        comment="FK to\xa0Tomogram\xa0table; tuple (movieID, tomogramID) is unique",
    )
    defocusU = Column(Float, comment="unit: Angstroms")
    defocusV = Column(Float, comment="unit: Angstroms")
    psdFile = Column(String(255))
    resolution = Column(Float, comment="unit: Angstroms")
    fitQuality = Column(Float)
    refinedMagnification = Column(Float, comment="unitless")
    refinedTiltAngle = Column(Float, comment="units: degrees")
    refinedTiltAxis = Column(Float, comment="units: degrees")
    residualError = Column(Float, comment="Residual error, unit: nm")

    Movie_ = relationship("Movie", back_populates="TiltImageAlignment")
    Tomogram_ = relationship("Tomogram", back_populates="TiltImageAlignment")


t_UserGroup_has_Person = Table(
    "UserGroup_has_Person",
    metadata,
    Column("userGroupId", INTEGER(11), primary_key=True, nullable=False),
    Column("personId", INTEGER(10), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["personId"],
        ["Person.personId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="userGroup_has_Person_fk2",
    ),
    ForeignKeyConstraint(
        ["userGroupId"],
        ["UserGroup.userGroupId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="userGroup_has_Person_fk1",
    ),
    Index("userGroup_has_Person_fk2", "personId"),
)


class BFSubcomponentBeamline(Base):
    __tablename__ = "BF_subcomponent_beamline"
    __table_args__ = (
        ForeignKeyConstraint(
            ["subcomponentId"],
            ["BF_subcomponent.subcomponentId"],
            name="bf_subcomponent_beamline_FK1",
        ),
        Index("bf_subcomponent_beamline_FK1", "subcomponentId"),
    )

    subcomponent_beamlineId = Column(INTEGER(10), primary_key=True)
    subcomponentId = Column(INTEGER(10))
    beamlinename = Column(String(20))

    BF_subcomponent = relationship(
        "BFSubcomponent", back_populates="BF_subcomponent_beamline"
    )


class BLSampleGroup(Base):
    __tablename__ = "BLSampleGroup"
    __table_args__ = (
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="BLSampleGroup_fk_proposalId",
        ),
        Index("BLSampleGroup_fk_proposalId", "proposalId"),
    )

    blSampleGroupId = Column(INTEGER(11), primary_key=True)
    name = Column(String(100), comment="Human-readable name")
    proposalId = Column(INTEGER(10))

    Proposal_ = relationship("Proposal", back_populates="BLSampleGroup")
    BLSampleGroup_has_BLSample = relationship(
        "BLSampleGroupHasBLSample", back_populates="BLSampleGroup_"
    )


class BLSession(Base):
    __tablename__ = "BLSession"
    __table_args__ = (
        ForeignKeyConstraint(
            ["beamCalendarId"],
            ["BeamCalendar.beamCalendarId"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="BLSession_fk_beamCalendarId",
        ),
        ForeignKeyConstraint(
            ["beamLineSetupId"],
            ["BeamLineSetup.beamLineSetupId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSession_ibfk_2",
        ),
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSession_ibfk_1",
        ),
        Index("BLSession_fk_beamCalendarId", "beamCalendarId"),
        Index("Session_FKIndex2", "beamLineSetupId"),
        Index("Session_FKIndexBeamLineName", "beamLineName"),
        Index("Session_FKIndexEndDate", "endDate"),
        Index("Session_FKIndexStartDate", "startDate"),
        Index("proposalId", "proposalId", "visit_number", unique=True),
    )

    sessionId = Column(INTEGER(10), primary_key=True)
    proposalId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    bltimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    lastUpdate = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("'0000-00-00 00:00:00'"),
        comment="last update timestamp: by default the end of the session, the last collect...",
    )
    beamLineSetupId = Column(INTEGER(10))
    beamCalendarId = Column(INTEGER(10))
    startDate = Column(DateTime)
    endDate = Column(DateTime)
    beamLineName = Column(String(45))
    scheduled = Column(TINYINT(1))
    nbShifts = Column(INTEGER(10))
    comments = Column(String(2000))
    beamLineOperator = Column(String(45))
    visit_number = Column(INTEGER(10), server_default=text("0"))
    usedFlag = Column(
        TINYINT(1),
        comment="indicates if session has Datacollections or XFE or EnergyScans attached",
    )
    externalId = Column(BINARY(16))
    archived = Column(
        TINYINT(1),
        server_default=text("0"),
        comment="The data for the session is archived and no longer available on disk",
    )

    Project_ = relationship(
        "Project", secondary="Project_has_Session", back_populates="BLSession"
    )
    BeamCalendar_ = relationship("BeamCalendar", back_populates="BLSession")
    BeamLineSetup_ = relationship("BeamLineSetup", back_populates="BLSession")
    Proposal_ = relationship("Proposal", back_populates="BLSession")
    Shipping = relationship(
        "Shipping", secondary="ShippingHasSession", back_populates="BLSession_"
    )
    BF_fault = relationship("BFFault", back_populates="BLSession_")
    BLSession_has_SCPosition = relationship(
        "BLSessionHasSCPosition", back_populates="BLSession_"
    )
    BeamlineAction = relationship("BeamlineAction", back_populates="BLSession_")
    DataCollectionGroup = relationship(
        "DataCollectionGroup", back_populates="BLSession_"
    )
    EnergyScan = relationship("EnergyScan", back_populates="BLSession_")
    RobotAction = relationship("RobotAction", back_populates="BLSession_")
    SessionType = relationship("SessionType", back_populates="BLSession_")
    Session_has_Person = relationship("SessionHasPerson", back_populates="BLSession_")
    XFEFluorescenceSpectrum = relationship(
        "XFEFluorescenceSpectrum", back_populates="BLSession_"
    )
    Dewar = relationship("Dewar", back_populates="BLSession_")
    Container = relationship("Container", back_populates="BLSession_")


class CTF(Base):
    __tablename__ = "CTF"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            name="CTF_ibfk2",
        ),
        ForeignKeyConstraint(
            ["motionCorrectionId"],
            ["MotionCorrection.motionCorrectionId"],
            name="CTF_ibfk1",
        ),
        Index("CTF_ibfk1", "motionCorrectionId"),
        Index("CTF_ibfk2", "autoProcProgramId"),
    )

    ctfId = Column(INTEGER(11), primary_key=True)
    motionCorrectionId = Column(INTEGER(11))
    autoProcProgramId = Column(INTEGER(11))
    boxSizeX = Column(Float, comment="Box size in x, Units: pixels")
    boxSizeY = Column(Float, comment="Box size in y, Units: pixels")
    minResolution = Column(Float, comment="Minimum resolution for CTF, Units: A")
    maxResolution = Column(Float, comment="Units: A")
    minDefocus = Column(Float, comment="Units: A")
    maxDefocus = Column(Float, comment="Units: A")
    defocusStepSize = Column(Float, comment="Units: A")
    astigmatism = Column(Float, comment="Units: A")
    astigmatismAngle = Column(Float, comment="Units: deg?")
    estimatedResolution = Column(Float, comment="Units: A")
    estimatedDefocus = Column(Float, comment="Units: A")
    amplitudeContrast = Column(Float, comment="Units: %?")
    ccValue = Column(Float, comment="Correlation value")
    fftTheoreticalFullPath = Column(
        String(255), comment="Full path to the jpg image of the simulated FFT"
    )
    comments = Column(String(255))

    AutoProcProgram_ = relationship("AutoProcProgram", back_populates="CTF")
    MotionCorrection_ = relationship("MotionCorrection", back_populates="CTF")


class Component(Base):
    __tablename__ = "Component"
    __table_args__ = (
        ForeignKeyConstraint(
            ["componentTypeId"],
            ["ComponentType.componentTypeId"],
            name="Component_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Component_ibfk_2",
        ),
        Index("componentTypeId", "componentTypeId"),
        Index("proposalId", "proposalId"),
        {
            "comment": "Description of a component that can be used inside a crystal or a "
            "sample."
        },
    )

    componentId = Column(INTEGER(11), primary_key=True)
    componentTypeId = Column(INTEGER(11), nullable=False)
    name = Column(String(255), nullable=False)
    proposalId = Column(INTEGER(10))
    composition = Column(String(255))

    ComponentType_ = relationship("ComponentType", back_populates="Component")
    Proposal_ = relationship("Proposal", back_populates="Component")
    Event = relationship("Event", back_populates="Component_")
    SampleComposition = relationship("SampleComposition", back_populates="Component_")
    CrystalComposition = relationship("CrystalComposition", back_populates="Component_")


class ContainerRegistryHasProposal(Base):
    __tablename__ = "ContainerRegistry_has_Proposal"
    __table_args__ = (
        ForeignKeyConstraint(
            ["containerRegistryId"],
            ["ContainerRegistry.containerRegistryId"],
            name="ContainerRegistry_has_Proposal_ibfk1",
        ),
        ForeignKeyConstraint(
            ["personId"],
            ["Person.personId"],
            name="ContainerRegistry_has_Proposal_ibfk3",
        ),
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            name="ContainerRegistry_has_Proposal_ibfk2",
        ),
        Index("ContainerRegistry_has_Proposal_ibfk2", "proposalId"),
        Index("ContainerRegistry_has_Proposal_ibfk3", "personId"),
        Index("containerRegistryId", "containerRegistryId", "proposalId", unique=True),
    )

    containerRegistryHasProposalId = Column(INTEGER(11), primary_key=True)
    containerRegistryId = Column(INTEGER(11))
    proposalId = Column(INTEGER(10))
    personId = Column(INTEGER(10), comment="Person registering the container")
    recordTimestamp = Column(DateTime, server_default=text("current_timestamp()"))

    ContainerRegistry_ = relationship(
        "ContainerRegistry", back_populates="ContainerRegistry_has_Proposal"
    )
    Person_ = relationship("Person", back_populates="ContainerRegistry_has_Proposal")
    Proposal_ = relationship(
        "Proposal", back_populates="ContainerRegistry_has_Proposal"
    )


class DiffractionPlan(Base):
    __tablename__ = "DiffractionPlan"
    __table_args__ = (
        ForeignKeyConstraint(
            ["detectorId"],
            ["Detector.detectorId"],
            onupdate="CASCADE",
            name="DataCollectionPlan_ibfk3",
        ),
        ForeignKeyConstraint(
            ["experimentTypeId"],
            ["ExperimentType.experimentTypeId"],
            name="DiffractionPlan_ibfk3",
        ),
        ForeignKeyConstraint(
            ["presetForProposalId"],
            ["Proposal.proposalId"],
            name="DiffractionPlan_ibfk1",
        ),
        ForeignKeyConstraint(
            ["purificationColumnId"],
            ["PurificationColumn.purificationColumnId"],
            name="DiffractionPlan_ibfk2",
        ),
        Index("DataCollectionPlan_ibfk3", "detectorId"),
        Index("DiffractionPlan_ibfk1", "presetForProposalId"),
        Index("DiffractionPlan_ibfk2", "purificationColumnId"),
        Index("DiffractionPlan_ibfk3", "experimentTypeId"),
    )

    diffractionPlanId = Column(INTEGER(10), primary_key=True)
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    name = Column(String(20))
    experimentKind = Column(
        Enum(
            "Default",
            "MXPressE",
            "MXPressO",
            "MXPressE_SAD",
            "MXScore",
            "MXPressM",
            "MAD",
            "SAD",
            "Fixed",
            "Ligand binding",
            "Refinement",
            "OSC",
            "MAD - Inverse Beam",
            "SAD - Inverse Beam",
            "MESH",
            "XFE",
            "Stepped transmission",
            "XChem High Symmetry",
            "XChem Low Symmetry",
            "Commissioning",
        )
    )
    observedResolution = Column(Float)
    minimalResolution = Column(Float)
    exposureTime = Column(Float)
    oscillationRange = Column(Float)
    maximalResolution = Column(Float)
    screeningResolution = Column(Float)
    radiationSensitivity = Column(Float)
    anomalousScatterer = Column(String(255))
    preferredBeamSizeX = Column(Float)
    preferredBeamSizeY = Column(Float)
    preferredBeamDiameter = Column(Float)
    comments = Column(String(1024))
    DIFFRACTIONPLANUUID = Column(String(1000))
    aimedCompleteness = Column(Float(asdecimal=True))
    aimedIOverSigmaAtHighestRes = Column(Float(asdecimal=True))
    aimedMultiplicity = Column(Float(asdecimal=True))
    aimedResolution = Column(Float(asdecimal=True))
    anomalousData = Column(TINYINT(1), server_default=text("0"))
    complexity = Column(String(45))
    estimateRadiationDamage = Column(TINYINT(1), server_default=text("0"))
    forcedSpaceGroup = Column(String(45))
    requiredCompleteness = Column(Float(asdecimal=True))
    requiredMultiplicity = Column(Float(asdecimal=True))
    requiredResolution = Column(Float(asdecimal=True))
    strategyOption = Column(VARCHAR(200))
    kappaStrategyOption = Column(String(45))
    numberOfPositions = Column(INTEGER(11))
    minDimAccrossSpindleAxis = Column(
        Float(asdecimal=True), comment="minimum dimension accross the spindle axis"
    )
    maxDimAccrossSpindleAxis = Column(
        Float(asdecimal=True), comment="maximum dimension accross the spindle axis"
    )
    radiationSensitivityBeta = Column(Float(asdecimal=True))
    radiationSensitivityGamma = Column(Float(asdecimal=True))
    minOscWidth = Column(Float)
    monochromator = Column(String(8), comment="DMM or DCM")
    energy = Column(Float, comment="eV")
    transmission = Column(Float, comment="Decimal fraction in range [0,1]")
    boxSizeX = Column(Float, comment="microns")
    boxSizeY = Column(Float, comment="microns")
    kappaStart = Column(Float, comment="degrees")
    axisStart = Column(Float, comment="degrees")
    axisRange = Column(Float, comment="degrees")
    numberOfImages = Column(MEDIUMINT(9), comment="The number of images requested")
    presetForProposalId = Column(
        INTEGER(10),
        comment="Indicates this plan is available to all sessions on given proposal",
    )
    beamLineName = Column(
        String(45),
        comment="Indicates this plan is available to all sessions on given beamline",
    )
    detectorId = Column(INTEGER(11))
    distance = Column(Float(asdecimal=True))
    orientation = Column(Float(asdecimal=True))
    monoBandwidth = Column(Float(asdecimal=True))
    centringMethod = Column(Enum("xray", "loop", "diffraction", "optical"))
    userPath = Column(
        String(100),
        comment='User-specified relative "root" path inside the session directory to be used for holding collected data',
    )
    robotPlateTemperature = Column(Float, comment="units: kelvin")
    exposureTemperature = Column(Float, comment="units: kelvin")
    experimentTypeId = Column(INTEGER(10))
    purificationColumnId = Column(INTEGER(10))
    collectionMode = Column(
        Enum("auto", "manual"),
        comment="The requested collection mode, possible values are auto, manual",
    )
    priority = Column(
        INTEGER(4),
        comment="The priority of this sample relative to others in the shipment",
    )
    qMin = Column(Float, comment="minimum in qRange, unit: nm^-1, needed for SAXS")
    qMax = Column(Float, comment="maximum in qRange, unit: nm^-1, needed for SAXS")
    reductionParametersAveraging = Column(
        Enum("All", "Fastest Dimension", "1D"),
        comment="Post processing params for SAXS",
    )
    scanParameters = Column(
        LONGTEXT,
        comment="JSON serialised scan parameters, useful for parameters without designated columns",
    )

    BLSample_ = relationship("BLSample", back_populates="DiffractionPlan")
    BLSubSample_ = relationship("BLSubSample", back_populates="DiffractionPlan")
    DataCollection_ = relationship("DataCollection", back_populates="DiffractionPlan")
    Detector_ = relationship("Detector", back_populates="DiffractionPlan")
    ExperimentType_ = relationship("ExperimentType", back_populates="DiffractionPlan")
    Proposal_ = relationship("Proposal", back_populates="DiffractionPlan")
    PurificationColumn_ = relationship(
        "PurificationColumn", back_populates="DiffractionPlan"
    )
    BLSample_has_DataCollectionPlan = relationship(
        "BLSampleHasDataCollectionPlan", back_populates="DiffractionPlan_"
    )
    Crystal = relationship("Crystal", back_populates="DiffractionPlan_")
    DataCollectionPlan_has_Detector = relationship(
        "DataCollectionPlanHasDetector", back_populates="DiffractionPlan_"
    )
    ExperimentKindDetails = relationship(
        "ExperimentKindDetails", back_populates="DiffractionPlan_"
    )
    ScanParametersModel = relationship(
        "ScanParametersModel", back_populates="DiffractionPlan_"
    )
    ContainerQueueSample = relationship(
        "ContainerQueueSample", back_populates="DiffractionPlan_"
    )


class LabContact(Base):
    __tablename__ = "LabContact"
    __table_args__ = (
        ForeignKeyConstraint(
            ["personId"],
            ["Person.personId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="LabContact_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="LabContact_ibfk_2",
        ),
        Index("LabContact_FKIndex1", "proposalId"),
        Index("cardNameAndProposal", "cardName", "proposalId", unique=True),
        Index("personAndProposal", "personId", "proposalId", unique=True),
    )

    labContactId = Column(INTEGER(10), primary_key=True)
    personId = Column(INTEGER(10), nullable=False)
    cardName = Column(String(40), nullable=False)
    proposalId = Column(INTEGER(10), nullable=False)
    dewarAvgCustomsValue = Column(INTEGER(10), nullable=False, server_default=text("0"))
    dewarAvgTransportValue = Column(
        INTEGER(10), nullable=False, server_default=text("0")
    )
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    defaultCourrierCompany = Column(String(45))
    courierAccount = Column(String(45))
    billingReference = Column(String(45))

    Person_ = relationship("Person", back_populates="LabContact")
    Proposal_ = relationship("Proposal", back_populates="LabContact")
    DewarRegistry = relationship("DewarRegistry", back_populates="LabContact_")
    Shipping = relationship(
        "Shipping",
        foreign_keys="[Shipping.returnLabContactId]",
        back_populates="LabContact_",
    )
    Shipping_ = relationship(
        "Shipping",
        foreign_keys="[Shipping.sendingLabContactId]",
        back_populates="LabContact1",
    )
    DewarRegistry_has_Proposal = relationship(
        "DewarRegistryHasProposal", back_populates="LabContact_"
    )


class MXMRRunBlob(Base):
    __tablename__ = "MXMRRunBlob"
    __table_args__ = (
        ForeignKeyConstraint(
            ["mxMRRunId"], ["MXMRRun.mxMRRunId"], name="mxMRRunBlob_FK1"
        ),
        Index("mxMRRunBlob_FK1", "mxMRRunId"),
    )

    mxMRRunBlobId = Column(INTEGER(11), primary_key=True)
    mxMRRunId = Column(INTEGER(11), nullable=False)
    view1 = Column(String(255))
    view2 = Column(String(255))
    view3 = Column(String(255))
    filePath = Column(
        String(255),
        comment="File path corresponding to the filenames in the view* columns",
    )
    x = Column(Float, comment="Fractional x coordinate of blob in range [-1, 1]")
    y = Column(Float, comment="Fractional y coordinate of blob in range [-1, 1]")
    z = Column(Float, comment="Fractional z coordinate of blob in range [-1, 1]")
    height = Column(Float, comment="Blob height (sigmas)")
    occupancy = Column(Float, comment="Site occupancy factor in range [0, 1]")
    nearestAtomName = Column(String(4), comment="Name of nearest atom")
    nearestAtomChainId = Column(String(2), comment="Chain identifier of nearest atom")
    nearestAtomResName = Column(String(4), comment="Residue name of nearest atom")
    nearestAtomResSeq = Column(
        MEDIUMINT(8), comment="Residue sequence number of nearest atom"
    )
    nearestAtomDistance = Column(Float, comment="Distance in Angstrom to nearest atom")
    mapType = Column(
        Enum("anomalous", "difference"),
        comment="Type of electron density map corresponding to this blob",
    )

    MXMRRun_ = relationship("MXMRRun", back_populates="MXMRRunBlob")


class MotionCorrectionDrift(Base):
    __tablename__ = "MotionCorrectionDrift"
    __table_args__ = (
        ForeignKeyConstraint(
            ["motionCorrectionId"],
            ["MotionCorrection.motionCorrectionId"],
            name="MotionCorrectionDrift_ibfk1",
        ),
        Index("MotionCorrectionDrift_ibfk1", "motionCorrectionId"),
    )

    motionCorrectionDriftId = Column(INTEGER(11), primary_key=True)
    motionCorrectionId = Column(INTEGER(11))
    frameNumber = Column(
        SMALLINT(5), comment="Frame number of the movie these drift values relate to"
    )
    deltaX = Column(Float, comment="Drift in x, Units: A")
    deltaY = Column(Float, comment="Drift in y, Units: A")

    MotionCorrection_ = relationship(
        "MotionCorrection", back_populates="MotionCorrectionDrift"
    )


class ParticlePicker(Base):
    __tablename__ = "ParticlePicker"
    __table_args__ = (
        ForeignKeyConstraint(
            ["firstMotionCorrectionId"],
            ["MotionCorrection.motionCorrectionId"],
            onupdate="CASCADE",
            name="ParticlePicker_fk_motionCorrectionId",
        ),
        ForeignKeyConstraint(
            ["programId"],
            ["AutoProcProgram.autoProcProgramId"],
            onupdate="CASCADE",
            name="ParticlePicker_fk_programId",
        ),
        Index("ParticlePicker_fk_motionCorrectionId", "firstMotionCorrectionId"),
        Index("ParticlePicker_fk_particlePickerProgramId", "programId"),
        {"comment": "An instance of a particle picker program that was run"},
    )

    particlePickerId = Column(INTEGER(10), primary_key=True)
    programId = Column(INTEGER(10))
    firstMotionCorrectionId = Column(INTEGER(10))
    particlePickingTemplate = Column(String(255), comment="Cryolo model")
    particleDiameter = Column(Float, comment="Unit: nm")
    numberOfParticles = Column(INTEGER(10))
    summaryImageFullPath = Column(
        String(255),
        comment="Generated summary micrograph image with highlighted particles",
    )

    MotionCorrection_ = relationship(
        "MotionCorrection", back_populates="ParticlePicker"
    )
    AutoProcProgram_ = relationship("AutoProcProgram", back_populates="ParticlePicker")
    ParticleClassificationGroup = relationship(
        "ParticleClassificationGroup", back_populates="ParticlePicker_"
    )


class PhasingStatistics(Base):
    __tablename__ = "PhasingStatistics"
    __table_args__ = (
        ForeignKeyConstraint(
            ["phasingHasScalingId1"],
            ["Phasing_has_Scaling.phasingHasScalingId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="PhasingStatistics_phasingHasScalingfk_1",
        ),
        ForeignKeyConstraint(
            ["phasingHasScalingId2"],
            ["Phasing_has_Scaling.phasingHasScalingId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="PhasingStatistics_phasingHasScalingfk_2",
        ),
        ForeignKeyConstraint(
            ["phasingStepId"],
            ["PhasingStep.phasingStepId"],
            name="fk_PhasingStatistics_phasingStep",
        ),
        Index("PhasingStatistics_FKIndex1", "phasingHasScalingId1"),
        Index("PhasingStatistics_FKIndex2", "phasingHasScalingId2"),
        Index("fk_PhasingStatistics_phasingStep_idx", "phasingStepId"),
    )

    phasingStatisticsId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    phasingHasScalingId1 = Column(
        INTEGER(11), nullable=False, comment="the dataset in question"
    )
    phasingHasScalingId2 = Column(
        INTEGER(11),
        comment="if this is MIT or MAD, which scaling are being compared, null otherwise",
    )
    phasingStepId = Column(INTEGER(10))
    numberOfBins = Column(INTEGER(11), comment="the total number of bins")
    binNumber = Column(INTEGER(11), comment="binNumber, 999 for overall")
    lowRes = Column(
        Float(asdecimal=True), comment="low resolution cutoff of this binfloat"
    )
    highRes = Column(
        Float(asdecimal=True), comment="high resolution cutoff of this binfloat"
    )
    metric = Column(
        Enum(
            "Rcullis",
            "Average Fragment Length",
            "Chain Count",
            "Residues Count",
            "CC",
            "PhasingPower",
            "FOM",
            '<d"/sig>',
            "Best CC",
            "CC(1/2)",
            "Weak CC",
            "CFOM",
            "Pseudo_free_CC",
            "CC of partial model",
        ),
        comment="metric",
    )
    statisticsValue = Column(Float(asdecimal=True), comment="the statistics value")
    nReflections = Column(INTEGER(11))
    recordTimeStamp = Column(DateTime, server_default=text("current_timestamp()"))

    Phasing_has_Scaling = relationship(
        "PhasingHasScaling",
        foreign_keys=[phasingHasScalingId1],
        back_populates="PhasingStatistics",
    )
    Phasing_has_Scaling_ = relationship(
        "PhasingHasScaling",
        foreign_keys=[phasingHasScalingId2],
        back_populates="PhasingStatistics_",
    )
    PhasingStep_ = relationship("PhasingStep", back_populates="PhasingStatistics")


t_Project_has_BLSample = Table(
    "Project_has_BLSample",
    metadata,
    Column("projectId", INTEGER(11), primary_key=True, nullable=False),
    Column("blSampleId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["blSampleId"],
        ["BLSample.blSampleId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="Project_has_BLSample_FK2",
    ),
    ForeignKeyConstraint(
        ["projectId"],
        ["Project.projectId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="Project_has_BLSample_FK1",
    ),
    Index("Project_has_BLSample_FK2", "blSampleId"),
)


t_Project_has_Person = Table(
    "Project_has_Person",
    metadata,
    Column("projectId", INTEGER(11), primary_key=True, nullable=False),
    Column("personId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["personId"],
        ["Person.personId"],
        ondelete="CASCADE",
        name="project_has_person_FK2",
    ),
    ForeignKeyConstraint(
        ["projectId"],
        ["Project.projectId"],
        ondelete="CASCADE",
        name="project_has_person_FK1",
    ),
    Index("project_has_person_FK2", "personId"),
)


class ProjectHasUser(Base):
    __tablename__ = "Project_has_User"
    __table_args__ = (
        ForeignKeyConstraint(
            ["projectid"], ["Project.projectId"], name="Project_Has_user_FK1"
        ),
        Index("Project_Has_user_FK1", "projectid"),
    )

    projecthasuserid = Column(INTEGER(11), primary_key=True)
    projectid = Column(INTEGER(11), nullable=False)
    username = Column(String(15))

    Project_ = relationship("Project", back_populates="Project_has_User")


class ProposalHasPerson(Base):
    __tablename__ = "ProposalHasPerson"
    __table_args__ = (
        ForeignKeyConstraint(
            ["personId"], ["Person.personId"], name="fk_ProposalHasPerson_Personal"
        ),
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            name="fk_ProposalHasPerson_Proposal",
        ),
        Index("fk_ProposalHasPerson_Personal", "personId"),
        Index("fk_ProposalHasPerson_Proposal", "proposalId"),
    )

    proposalHasPersonId = Column(INTEGER(10), primary_key=True)
    proposalId = Column(INTEGER(10), nullable=False)
    personId = Column(INTEGER(10), nullable=False)
    role = Column(
        Enum(
            "Co-Investigator",
            "Principal Investigator",
            "Alternate Contact",
            "ERA Admin",
            "Associate",
        )
    )

    Person_ = relationship("Person", back_populates="ProposalHasPerson")
    Proposal_ = relationship("Proposal", back_populates="ProposalHasPerson")


class Protein(Base):
    __tablename__ = "Protein"
    __table_args__ = (
        ForeignKeyConstraint(
            ["componentTypeId"],
            ["ComponentType.componentTypeId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="protein_fk3",
        ),
        ForeignKeyConstraint(
            ["concentrationTypeId"],
            ["ConcentrationType.concentrationTypeId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="protein_fk4",
        ),
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Protein_ibfk_1",
        ),
        Index("ProteinAcronym_Index", "proposalId", "acronym"),
        Index("Protein_FKIndex2", "personId"),
        Index("Protein_Index2", "acronym"),
        Index("protein_fk3", "componentTypeId"),
        Index("protein_fk4", "concentrationTypeId"),
    )

    proteinId = Column(INTEGER(10), primary_key=True)
    proposalId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    hazardGroup = Column(
        TINYINT(3),
        nullable=False,
        server_default=text("1"),
        comment="A.k.a. risk group",
    )
    containmentLevel = Column(
        TINYINT(3),
        nullable=False,
        server_default=text("1"),
        comment="A.k.a. biosafety level, which indicates the level of containment required",
    )
    bltimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    name = Column(String(255))
    acronym = Column(String(45))
    description = Column(
        Text, comment="A description/summary using words and sentences"
    )
    safetyLevel = Column(Enum("GREEN", "YELLOW", "RED"))
    molecularMass = Column(Float(asdecimal=True))
    proteinType = Column(String(45))
    personId = Column(INTEGER(10))
    isCreatedBySampleSheet = Column(TINYINT(1), server_default=text("0"))
    sequence = Column(Text)
    MOD_ID = Column(String(20))
    componentTypeId = Column(INTEGER(11))
    concentrationTypeId = Column(INTEGER(11))
    global_ = Column("global", TINYINT(1), server_default=text("0"))
    externalId = Column(BINARY(16))
    density = Column(Float)
    abundance = Column(Float, comment="Deprecated")
    isotropy = Column(Enum("isotropic", "anisotropic"))

    Project_ = relationship(
        "Project", secondary="Project_has_Protein", back_populates="Protein"
    )
    ComponentType_ = relationship("ComponentType", back_populates="Protein")
    ConcentrationType_ = relationship("ConcentrationType", back_populates="Protein")
    Proposal_ = relationship("Proposal", back_populates="Protein")
    ComponentSubType_ = relationship(
        "ComponentSubType", secondary="Component_has_SubType", back_populates="Protein"
    )
    ComponentLattice = relationship("ComponentLattice", back_populates="Protein_")
    Crystal = relationship("Crystal", back_populates="Protein_")
    Protein_has_PDB = relationship("ProteinHasPDB", back_populates="Protein_")
    BLSampleType_has_Component = relationship(
        "BLSampleTypeHasComponent", back_populates="Protein_"
    )
    ScreenComponent = relationship("ScreenComponent", back_populates="Protein_")


class RelativeIceThickness(Base):
    __tablename__ = "RelativeIceThickness"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            onupdate="CASCADE",
            name="RelativeIceThickness_fk_programId",
        ),
        ForeignKeyConstraint(
            ["motionCorrectionId"],
            ["MotionCorrection.motionCorrectionId"],
            onupdate="CASCADE",
            name="RelativeIceThickness_fk_motionCorrectionId",
        ),
        Index("RelativeIceThickness_fk_motionCorrectionId", "motionCorrectionId"),
        Index("RelativeIceThickness_fk_programId", "autoProcProgramId"),
    )

    relativeIceThicknessId = Column(INTEGER(11), primary_key=True)
    motionCorrectionId = Column(INTEGER(11))
    autoProcProgramId = Column(INTEGER(11))
    minimum = Column(Float, comment="Minimum relative ice thickness, Unitless")
    q1 = Column(Float, comment="Quartile 1, unitless")
    median = Column(Float, comment="Median relative ice thickness, Unitless")
    q3 = Column(Float, comment="Quartile 3, unitless")
    maximum = Column(Float, comment="Minimum relative ice thickness, Unitless")

    AutoProcProgram_ = relationship(
        "AutoProcProgram", back_populates="RelativeIceThickness"
    )
    MotionCorrection_ = relationship(
        "MotionCorrection", back_populates="RelativeIceThickness"
    )


class SWOnceToken(Base):
    __tablename__ = "SW_onceToken"
    __table_args__ = (
        ForeignKeyConstraint(
            ["personId"], ["Person.personId"], name="SW_onceToken_fk1"
        ),
        ForeignKeyConstraint(
            ["proposalId"], ["Proposal.proposalId"], name="SW_onceToken_fk2"
        ),
        Index("SW_onceToken_fk1", "personId"),
        Index("SW_onceToken_fk2", "proposalId"),
        Index("SW_onceToken_recordTimeStamp_idx", "recordTimeStamp"),
        {
            "comment": "One-time use tokens needed for token auth in order to grant "
            "access to file downloads and webcams (and some images)"
        },
    )

    onceTokenId = Column(INTEGER(11), primary_key=True)
    recordTimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    token = Column(String(128))
    personId = Column(INTEGER(10))
    proposalId = Column(INTEGER(10))
    validity = Column(String(200))

    Person_ = relationship("Person", back_populates="SW_onceToken")
    Proposal_ = relationship("Proposal", back_populates="SW_onceToken")


class Screen(Base):
    __tablename__ = "Screen"
    __table_args__ = (
        ForeignKeyConstraint(
            ["proposalId"], ["Proposal.proposalId"], name="Screen_fk1"
        ),
        Index("Screen_fk1", "proposalId"),
    )

    screenId = Column(INTEGER(11), primary_key=True)
    name = Column(String(45))
    proposalId = Column(INTEGER(10))
    global_ = Column("global", TINYINT(1))

    Proposal_ = relationship("Proposal", back_populates="Screen")
    ScreenComponentGroup = relationship(
        "ScreenComponentGroup", back_populates="Screen_"
    )
    Container = relationship("Container", back_populates="Screen_")


class BFFault(Base):
    __tablename__ = "BF_fault"
    __table_args__ = (
        ForeignKeyConstraint(["assigneeId"], ["Person.personId"], name="bf_fault_FK4"),
        ForeignKeyConstraint(["personId"], ["Person.personId"], name="bf_fault_FK3"),
        ForeignKeyConstraint(
            ["sessionId"], ["BLSession.sessionId"], name="bf_fault_FK1"
        ),
        ForeignKeyConstraint(
            ["subcomponentId"], ["BF_subcomponent.subcomponentId"], name="bf_fault_FK2"
        ),
        Index("bf_fault_FK1", "sessionId"),
        Index("bf_fault_FK2", "subcomponentId"),
        Index("bf_fault_FK3", "personId"),
        Index("bf_fault_FK4", "assigneeId"),
    )

    faultId = Column(INTEGER(10), primary_key=True)
    sessionId = Column(INTEGER(10), nullable=False)
    owner = Column(String(50))
    subcomponentId = Column(INTEGER(10))
    starttime = Column(DateTime)
    endtime = Column(DateTime)
    beamtimelost = Column(TINYINT(1))
    beamtimelost_starttime = Column(DateTime)
    beamtimelost_endtime = Column(DateTime)
    title = Column(String(200))
    description = Column(Text)
    resolved = Column(TINYINT(1))
    resolution = Column(Text)
    attachment = Column(String(200))
    eLogId = Column(INTEGER(11))
    assignee = Column(String(50))
    personId = Column(INTEGER(10))
    assigneeId = Column(INTEGER(10))

    Person_ = relationship(
        "Person", foreign_keys=[assigneeId], back_populates="BF_fault"
    )
    Person1 = relationship(
        "Person", foreign_keys=[personId], back_populates="BF_fault_"
    )
    BLSession_ = relationship("BLSession", back_populates="BF_fault")
    BF_subcomponent = relationship("BFSubcomponent", back_populates="BF_fault")


class BLSampleGroupHasBLSample(Base):
    __tablename__ = "BLSampleGroup_has_BLSample"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleGroupId"],
            ["BLSampleGroup.blSampleGroupId"],
            name="BLSampleGroup_has_BLSample_ibfk1",
        ),
        ForeignKeyConstraint(
            ["blSampleId"],
            ["BLSample.blSampleId"],
            name="BLSampleGroup_has_BLSample_ibfk2",
        ),
        ForeignKeyConstraint(
            ["blSampleTypeId"],
            ["BLSampleType.blSampleTypeId"],
            name="BLSampleGroup_has_BLSample_ibfk3",
        ),
        Index("BLSampleGroup_has_BLSample_ibfk2", "blSampleId"),
        Index("BLSampleGroup_has_BLSample_ibfk3", "blSampleTypeId"),
    )

    blSampleGroupId = Column(INTEGER(11), primary_key=True, nullable=False)
    blSampleId = Column(INTEGER(11), primary_key=True, nullable=False)
    groupOrder = Column(MEDIUMINT(9))
    type = Column(Enum("background", "container", "sample", "calibrant", "capillary"))
    blSampleTypeId = Column(INTEGER(10))

    BLSampleGroup_ = relationship(
        "BLSampleGroup", back_populates="BLSampleGroup_has_BLSample"
    )
    BLSample_ = relationship("BLSample", back_populates="BLSampleGroup_has_BLSample")
    BLSampleType_ = relationship(
        "BLSampleType", back_populates="BLSampleGroup_has_BLSample"
    )


class BLSampleHasDataCollectionPlan(Base):
    __tablename__ = "BLSample_has_DataCollectionPlan"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"],
            ["BLSample.blSampleId"],
            name="BLSample_has_DataCollectionPlan_ibfk1",
        ),
        ForeignKeyConstraint(
            ["dataCollectionPlanId"],
            ["DiffractionPlan.diffractionPlanId"],
            name="BLSample_has_DataCollectionPlan_ibfk2",
        ),
        Index("BLSample_has_DataCollectionPlan_ibfk2", "dataCollectionPlanId"),
    )

    blSampleId = Column(INTEGER(11), primary_key=True, nullable=False)
    dataCollectionPlanId = Column(INTEGER(11), primary_key=True, nullable=False)
    planOrder = Column(SMALLINT(5))

    BLSample_ = relationship(
        "BLSample", back_populates="BLSample_has_DataCollectionPlan"
    )
    DiffractionPlan_ = relationship(
        "DiffractionPlan", back_populates="BLSample_has_DataCollectionPlan"
    )


class BLSessionHasSCPosition(Base):
    __tablename__ = "BLSession_has_SCPosition"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blsessionid"],
            ["BLSession.sessionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="blsession_has_scposition_FK1",
        ),
        Index("blsession_has_scposition_FK1", "blsessionid"),
    )

    blsessionhasscpositionid = Column(INTEGER(11), primary_key=True)
    blsessionid = Column(INTEGER(11), nullable=False)
    scContainer = Column(
        SMALLINT(5), comment="Position of container within sample changer"
    )
    containerPosition = Column(
        SMALLINT(5), comment="Position of sample within container"
    )

    BLSession_ = relationship("BLSession", back_populates="BLSession_has_SCPosition")


class BeamlineAction(Base):
    __tablename__ = "BeamlineAction"
    __table_args__ = (
        ForeignKeyConstraint(
            ["sessionId"], ["BLSession.sessionId"], name="BeamlineAction_ibfk1"
        ),
        Index("BeamlineAction_ibfk1", "sessionId"),
    )

    beamlineActionId = Column(INTEGER(11), primary_key=True)
    startTimestamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
    )
    endTimestamp = Column(
        TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'")
    )
    sessionId = Column(INTEGER(11))
    message = Column(String(255))
    parameter = Column(String(50))
    value = Column(String(30))
    loglevel = Column(Enum("DEBUG", "CRITICAL", "INFO"))
    status = Column(
        Enum("PAUSED", "RUNNING", "TERMINATED", "COMPLETE", "ERROR", "EPICSFAIL")
    )

    BLSession_ = relationship("BLSession", back_populates="BeamlineAction")


class ComponentLattice(Base):
    __tablename__ = "ComponentLattice"
    __table_args__ = (
        ForeignKeyConstraint(
            ["componentId"], ["Protein.proteinId"], name="ComponentLattice_ibfk1"
        ),
        Index("ComponentLattice_ibfk1", "componentId"),
    )

    componentLatticeId = Column(INTEGER(11), primary_key=True)
    componentId = Column(INTEGER(10))
    spaceGroup = Column(String(20))
    cell_a = Column(Float(asdecimal=True))
    cell_b = Column(Float(asdecimal=True))
    cell_c = Column(Float(asdecimal=True))
    cell_alpha = Column(Float(asdecimal=True))
    cell_beta = Column(Float(asdecimal=True))
    cell_gamma = Column(Float(asdecimal=True))

    Protein_ = relationship("Protein", back_populates="ComponentLattice")


t_Component_has_SubType = Table(
    "Component_has_SubType",
    metadata,
    Column("componentId", INTEGER(10), primary_key=True, nullable=False),
    Column("componentSubTypeId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["componentId"],
        ["Protein.proteinId"],
        ondelete="CASCADE",
        name="component_has_SubType_fk1",
    ),
    ForeignKeyConstraint(
        ["componentSubTypeId"],
        ["ComponentSubType.componentSubTypeId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="component_has_SubType_fk2",
    ),
    Index("component_has_SubType_fk2", "componentSubTypeId"),
)


class Crystal(Base):
    __tablename__ = "Crystal"
    __table_args__ = (
        ForeignKeyConstraint(
            ["diffractionPlanId"],
            ["DiffractionPlan.diffractionPlanId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Crystal_ibfk_2",
        ),
        ForeignKeyConstraint(
            ["proteinId"],
            ["Protein.proteinId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Crystal_ibfk_1",
        ),
        Index("Crystal_FKIndex1", "proteinId"),
        Index("Crystal_FKIndex2", "diffractionPlanId"),
    )

    crystalId = Column(INTEGER(10), primary_key=True)
    proteinId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    diffractionPlanId = Column(INTEGER(10))
    crystalUUID = Column(String(45))
    name = Column(String(255))
    spaceGroup = Column(String(20))
    morphology = Column(String(255))
    color = Column(String(45))
    size_X = Column(Float(asdecimal=True))
    size_Y = Column(Float(asdecimal=True))
    size_Z = Column(Float(asdecimal=True))
    cell_a = Column(Float(asdecimal=True))
    cell_b = Column(Float(asdecimal=True))
    cell_c = Column(Float(asdecimal=True))
    cell_alpha = Column(Float(asdecimal=True))
    cell_beta = Column(Float(asdecimal=True))
    cell_gamma = Column(Float(asdecimal=True))
    comments = Column(String(255))
    pdbFileName = Column(String(255), comment="pdb file name")
    pdbFilePath = Column(String(1024), comment="pdb file path")
    abundance = Column(Float)
    theoreticalDensity = Column(Float)

    BLSample_ = relationship("BLSample", back_populates="Crystal")
    DiffractionPlan_ = relationship("DiffractionPlan", back_populates="Crystal")
    Protein_ = relationship("Protein", back_populates="Crystal")
    BLSampleType_has_Component = relationship(
        "BLSampleTypeHasComponent", back_populates="Crystal_"
    )
    CrystalComposition = relationship("CrystalComposition", back_populates="Crystal_")
    Crystal_has_UUID = relationship("CrystalHasUUID", back_populates="Crystal_")


class DataCollectionGroup(Base):
    __tablename__ = "DataCollectionGroup"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"],
            ["BLSample.blSampleId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="DataCollectionGroup_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["experimentTypeId"],
            ["ExperimentType.experimentTypeId"],
            name="DataCollectionGroup_ibfk_4",
        ),
        ForeignKeyConstraint(
            ["sessionId"],
            ["BLSession.sessionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="DataCollectionGroup_ibfk_2",
        ),
        Index("DataCollectionGroup_FKIndex1", "blSampleId"),
        Index("DataCollectionGroup_FKIndex2", "sessionId"),
        Index("DataCollectionGroup_ibfk_4", "experimentTypeId"),
        {"comment": "a dataCollectionGroup is a group of dataCollection for a spe"},
    )

    dataCollectionGroupId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    sessionId = Column(INTEGER(10), nullable=False, comment="references Session table")
    comments = Column(String(1024), comment="comments")
    blSampleId = Column(INTEGER(10), comment="references BLSample table")
    experimentType = Column(
        Enum(
            "SAD",
            "SAD - Inverse Beam",
            "OSC",
            "Collect - Multiwedge",
            "MAD",
            "Helical",
            "Multi-positional",
            "Mesh",
            "Burn",
            "MAD - Inverse Beam",
            "Characterization",
            "Dehydration",
            "tomo",
            "experiment",
            "EM",
            "PDF",
            "PDF+Bragg",
            "Bragg",
            "single particle",
            "Serial Fixed",
            "Serial Jet",
            "Standard",
            "Time Resolved",
            "Diamond Anvil High Pressure",
            "Custom",
            "XRF map",
            "Energy scan",
            "XRF spectrum",
            "XRF map xas",
            "Mesh3D",
            "Screening",
        ),
        comment="Standard: Routine structure determination experiment. Time Resolved: Investigate the change of a system over time. Custom: Special or non-standard data collection.",
    )
    startTime = Column(DateTime, comment="Start time of the dataCollectionGroup")
    endTime = Column(DateTime, comment="end time of the dataCollectionGroup")
    crystalClass = Column(String(20), comment="Crystal Class for industrials users")
    detectorMode = Column(String(255), comment="Detector mode")
    actualSampleBarcode = Column(String(45), comment="Actual sample barcode")
    actualSampleSlotInContainer = Column(
        INTEGER(10), comment="Actual sample slot number in container"
    )
    actualContainerBarcode = Column(String(45), comment="Actual container barcode")
    actualContainerSlotInSC = Column(
        INTEGER(10), comment="Actual container slot number in sample changer"
    )
    xtalSnapshotFullPath = Column(String(255))
    scanParameters = Column(LONGTEXT)
    experimentTypeId = Column(INTEGER(10))

    DataCollection_ = relationship(
        "DataCollection", back_populates="DataCollectionGroup"
    )
    Screening_ = relationship("Screening", back_populates="DataCollectionGroup")
    BLSample_ = relationship("BLSample", back_populates="DataCollectionGroup")
    ExperimentType_ = relationship(
        "ExperimentType", back_populates="DataCollectionGroup"
    )
    BLSession_ = relationship("BLSession", back_populates="DataCollectionGroup")
    Project_ = relationship(
        "Project", secondary="Project_has_DCGroup", back_populates="DataCollectionGroup"
    )
    GridInfo = relationship("GridInfo", back_populates="DataCollectionGroup_")
    XrayCentring = relationship("XrayCentring", back_populates="DataCollectionGroup_")


class DataCollectionPlanHasDetector(Base):
    __tablename__ = "DataCollectionPlan_has_Detector"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionPlanId"],
            ["DiffractionPlan.diffractionPlanId"],
            name="DataCollectionPlan_has_Detector_ibfk1",
        ),
        ForeignKeyConstraint(
            ["detectorId"],
            ["Detector.detectorId"],
            name="DataCollectionPlan_has_Detector_ibfk2",
        ),
        Index("DataCollectionPlan_has_Detector_ibfk2", "detectorId"),
        Index(
            "dataCollectionPlanId", "dataCollectionPlanId", "detectorId", unique=True
        ),
    )

    dataCollectionPlanHasDetectorId = Column(INTEGER(11), primary_key=True)
    dataCollectionPlanId = Column(INTEGER(11), nullable=False)
    detectorId = Column(INTEGER(11), nullable=False)
    exposureTime = Column(Float(asdecimal=True))
    distance = Column(Float(asdecimal=True))
    roll = Column(Float(asdecimal=True))

    DiffractionPlan_ = relationship(
        "DiffractionPlan", back_populates="DataCollectionPlan_has_Detector"
    )
    Detector_ = relationship(
        "Detector", back_populates="DataCollectionPlan_has_Detector"
    )


class DewarRegistry(Base):
    __tablename__ = "DewarRegistry"
    __table_args__ = (
        ForeignKeyConstraint(
            ["labContactId"],
            ["LabContact.labContactId"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="DewarRegistry_ibfk_2",
        ),
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            onupdate="CASCADE",
            name="DewarRegistry_ibfk_1",
        ),
        Index("DewarRegistry_ibfk_1", "proposalId"),
        Index("DewarRegistry_ibfk_2", "labContactId"),
        Index("facilityCode", "facilityCode", unique=True),
    )

    dewarRegistryId = Column(INTEGER(11), primary_key=True)
    facilityCode = Column(String(20), nullable=False)
    bltimestamp = Column(
        DateTime, nullable=False, server_default=text("current_timestamp()")
    )
    proposalId = Column(INTEGER(11))
    labContactId = Column(INTEGER(11))
    purchaseDate = Column(DateTime)

    LabContact_ = relationship("LabContact", back_populates="DewarRegistry")
    Proposal_ = relationship("Proposal", back_populates="DewarRegistry")
    DewarRegistry_has_Proposal = relationship(
        "DewarRegistryHasProposal", back_populates="DewarRegistry_"
    )
    DewarReport = relationship("DewarReport", back_populates="DewarRegistry_")


class EnergyScan(Base):
    __tablename__ = "EnergyScan"
    __table_args__ = (
        ForeignKeyConstraint(["blSampleId"], ["BLSample.blSampleId"], name="ES_ibfk_2"),
        ForeignKeyConstraint(
            ["blSubSampleId"], ["BLSubSample.blSubSampleId"], name="ES_ibfk_3"
        ),
        ForeignKeyConstraint(
            ["sessionId"],
            ["BLSession.sessionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ES_ibfk_1",
        ),
        Index("ES_ibfk_2", "blSampleId"),
        Index("ES_ibfk_3", "blSubSampleId"),
        Index("EnergyScan_FKIndex2", "sessionId"),
    )

    energyScanId = Column(INTEGER(10), primary_key=True)
    sessionId = Column(INTEGER(10), nullable=False)
    blSampleId = Column(INTEGER(10))
    fluorescenceDetector = Column(String(255))
    scanFileFullPath = Column(String(255))
    jpegChoochFileFullPath = Column(String(255))
    element = Column(String(45))
    startEnergy = Column(Float)
    endEnergy = Column(Float)
    transmissionFactor = Column(Float)
    exposureTime = Column(Float)
    axisPosition = Column(Float)
    synchrotronCurrent = Column(Float)
    temperature = Column(Float)
    peakEnergy = Column(Float)
    peakFPrime = Column(Float)
    peakFDoublePrime = Column(Float)
    inflectionEnergy = Column(Float)
    inflectionFPrime = Column(Float)
    inflectionFDoublePrime = Column(Float)
    xrayDose = Column(Float)
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    edgeEnergy = Column(String(255))
    filename = Column(String(255))
    beamSizeVertical = Column(Float)
    beamSizeHorizontal = Column(Float)
    choochFileFullPath = Column(String(255))
    crystalClass = Column(String(20))
    comments = Column(String(1024))
    flux = Column(Float(asdecimal=True), comment="flux measured before the energyScan")
    flux_end = Column(
        Float(asdecimal=True), comment="flux measured after the energyScan"
    )
    workingDirectory = Column(String(45))
    blSubSampleId = Column(INTEGER(11))

    BLSample_ = relationship("BLSample", back_populates="EnergyScan")
    BLSubSample_ = relationship("BLSubSample", back_populates="EnergyScan")
    BLSession_ = relationship("BLSession", back_populates="EnergyScan")
    Project_ = relationship(
        "Project", secondary="Project_has_EnergyScan", back_populates="EnergyScan"
    )
    BLSample_has_EnergyScan = relationship(
        "BLSampleHasEnergyScan", back_populates="EnergyScan_"
    )


class Event(Base):
    __tablename__ = "Event"
    __table_args__ = (
        ForeignKeyConstraint(
            ["componentId"], ["Component.componentId"], name="Event_ibfk_2"
        ),
        ForeignKeyConstraint(
            ["eventChainId"],
            ["EventChain.eventChainId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Event_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["eventTypeId"], ["EventType.eventTypeId"], name="Event_ibfk_3"
        ),
        Index("componentId", "componentId"),
        Index("eventChainId", "eventChainId"),
        Index("eventTypeId", "eventTypeId"),
        {
            "comment": "Describes an event that occurred during a data collection and "
            "should be taken into account for data analysis. Can optionally be "
            "repeated at a specified frequency."
        },
    )

    eventId = Column(INTEGER(11), primary_key=True)
    eventChainId = Column(INTEGER(11), nullable=False)
    eventTypeId = Column(INTEGER(11), nullable=False)
    offset = Column(
        Float,
        nullable=False,
        comment="Start of the event relative to data collection start time in seconds.",
    )
    componentId = Column(INTEGER(11))
    name = Column(String(255))
    duration = Column(Float, comment="Duration of the event if applicable.")
    period = Column(Float, comment="Repetition period if applicable in seconds.")
    repetition = Column(Float, comment="Number of repetitions if applicable.")

    Component_ = relationship("Component", back_populates="Event")
    EventChain_ = relationship("EventChain", back_populates="Event")
    EventType_ = relationship("EventType", back_populates="Event")


class ExperimentKindDetails(Base):
    __tablename__ = "ExperimentKindDetails"
    __table_args__ = (
        ForeignKeyConstraint(
            ["diffractionPlanId"],
            ["DiffractionPlan.diffractionPlanId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="EKD_ibfk_1",
        ),
        Index("ExperimentKindDetails_FKIndex1", "diffractionPlanId"),
    )

    experimentKindId = Column(INTEGER(10), primary_key=True)
    diffractionPlanId = Column(INTEGER(10), nullable=False)
    exposureIndex = Column(INTEGER(10))
    dataCollectionType = Column(String(45))
    dataCollectionKind = Column(String(45))
    wedgeValue = Column(Float)

    DiffractionPlan_ = relationship(
        "DiffractionPlan", back_populates="ExperimentKindDetails"
    )


class ParticleClassificationGroup(Base):
    __tablename__ = "ParticleClassificationGroup"
    __table_args__ = (
        ForeignKeyConstraint(
            ["particlePickerId"],
            ["ParticlePicker.particlePickerId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ParticleClassificationGroup_fk_particlePickerId",
        ),
        ForeignKeyConstraint(
            ["programId"],
            ["AutoProcProgram.autoProcProgramId"],
            onupdate="CASCADE",
            name="ParticleClassificationGroup_fk_programId",
        ),
        Index("ParticleClassificationGroup_fk_particlePickerId", "particlePickerId"),
        Index("ParticleClassificationGroup_fk_programId", "programId"),
    )

    particleClassificationGroupId = Column(INTEGER(10), primary_key=True)
    particlePickerId = Column(INTEGER(10))
    programId = Column(INTEGER(10))
    type = Column(
        Enum("2D", "3D"), comment="Indicates the type of particle classification"
    )
    batchNumber = Column(INTEGER(10), comment="Corresponding to batch number")
    numberOfParticlesPerBatch = Column(
        INTEGER(10), comment="total number of particles per batch (a large integer)"
    )
    numberOfClassesPerBatch = Column(INTEGER(10))
    symmetry = Column(String(20))

    ParticlePicker_ = relationship(
        "ParticlePicker", back_populates="ParticleClassificationGroup"
    )
    AutoProcProgram_ = relationship(
        "AutoProcProgram", back_populates="ParticleClassificationGroup"
    )
    ParticleClassification = relationship(
        "ParticleClassification", back_populates="ParticleClassificationGroup_"
    )


t_Project_has_Protein = Table(
    "Project_has_Protein",
    metadata,
    Column("projectId", INTEGER(11), primary_key=True, nullable=False),
    Column("proteinId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["projectId"],
        ["Project.projectId"],
        ondelete="CASCADE",
        name="project_has_protein_FK1",
    ),
    ForeignKeyConstraint(
        ["proteinId"],
        ["Protein.proteinId"],
        ondelete="CASCADE",
        name="project_has_protein_FK2",
    ),
    Index("project_has_protein_FK2", "proteinId"),
)


t_Project_has_Session = Table(
    "Project_has_Session",
    metadata,
    Column("projectId", INTEGER(11), primary_key=True, nullable=False),
    Column("sessionId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["projectId"],
        ["Project.projectId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="project_has_session_FK1",
    ),
    ForeignKeyConstraint(
        ["sessionId"],
        ["BLSession.sessionId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="project_has_session_FK2",
    ),
    Index("project_has_session_FK2", "sessionId"),
)


class ProteinHasPDB(Base):
    __tablename__ = "Protein_has_PDB"
    __table_args__ = (
        ForeignKeyConstraint(["pdbid"], ["PDB.pdbId"], name="Protein_Has_PDB_fk2"),
        ForeignKeyConstraint(
            ["proteinid"], ["Protein.proteinId"], name="Protein_Has_PDB_fk1"
        ),
        Index("Protein_Has_PDB_fk1", "proteinid"),
        Index("Protein_Has_PDB_fk2", "pdbid"),
    )

    proteinhaspdbid = Column(INTEGER(11), primary_key=True)
    proteinid = Column(INTEGER(11), nullable=False)
    pdbid = Column(INTEGER(11), nullable=False)

    PDB_ = relationship("PDB", back_populates="Protein_has_PDB")
    Protein_ = relationship("Protein", back_populates="Protein_has_PDB")


class RobotAction(Base):
    __tablename__ = "RobotAction"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blsampleId"], ["BLSample.blSampleId"], name="RobotAction_FK2"
        ),
        ForeignKeyConstraint(
            ["blsessionId"], ["BLSession.sessionId"], name="RobotAction_FK1"
        ),
        Index("RobotAction_FK1", "blsessionId"),
        Index("RobotAction_FK2", "blsampleId"),
        {"comment": "Robot actions as reported by GDA"},
    )

    robotActionId = Column(INTEGER(11), primary_key=True)
    blsessionId = Column(INTEGER(11), nullable=False)
    startTimestamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp() ON UPDATE current_timestamp()"),
    )
    endTimestamp = Column(
        TIMESTAMP, nullable=False, server_default=text("'0000-00-00 00:00:00'")
    )
    blsampleId = Column(INTEGER(11))
    actionType = Column(
        Enum("LOAD", "UNLOAD", "DISPOSE", "STORE", "WASH", "ANNEAL", "MOSAIC")
    )
    status = Column(
        Enum("SUCCESS", "ERROR", "CRITICAL", "WARNING", "EPICSFAIL", "COMMANDNOTSENT")
    )
    message = Column(String(255))
    containerLocation = Column(SMALLINT(6))
    dewarLocation = Column(SMALLINT(6))
    sampleBarcode = Column(String(45))
    xtalSnapshotBefore = Column(String(255))
    xtalSnapshotAfter = Column(String(255))

    BLSample_ = relationship("BLSample", back_populates="RobotAction")
    BLSession_ = relationship("BLSession", back_populates="RobotAction")


class SampleComposition(Base):
    __tablename__ = "SampleComposition"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"], ["BLSample.blSampleId"], name="SampleComposition_ibfk_2"
        ),
        ForeignKeyConstraint(
            ["componentId"], ["Component.componentId"], name="SampleComposition_ibfk_1"
        ),
        ForeignKeyConstraint(
            ["concentrationTypeId"],
            ["ConcentrationType.concentrationTypeId"],
            name="SampleComposition_ibfk_3",
        ),
        Index("blSampleId", "blSampleId"),
        Index("componentId", "componentId"),
        Index("concentrationTypeId", "concentrationTypeId"),
        {
            "comment": "Links a sample to its components with a specified abundance or "
            "ratio."
        },
    )

    sampleCompositionId = Column(INTEGER(11), primary_key=True)
    componentId = Column(INTEGER(11), nullable=False)
    blSampleId = Column(INTEGER(11), nullable=False)
    concentrationTypeId = Column(INTEGER(11))
    abundance = Column(
        Float,
        comment="Abundance or concentration in the unit defined by concentrationTypeId.",
    )
    ratio = Column(Float)
    pH = Column(Float)

    BLSample_ = relationship("BLSample", back_populates="SampleComposition")
    Component_ = relationship("Component", back_populates="SampleComposition")
    ConcentrationType_ = relationship(
        "ConcentrationType", back_populates="SampleComposition"
    )


class ScanParametersModel(Base):
    __tablename__ = "ScanParametersModel"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionPlanId"],
            ["DiffractionPlan.diffractionPlanId"],
            onupdate="CASCADE",
            name="PDF_Model_ibfk2",
        ),
        ForeignKeyConstraint(
            ["scanParametersServiceId"],
            ["ScanParametersService.scanParametersServiceId"],
            onupdate="CASCADE",
            name="PDF_Model_ibfk1",
        ),
        Index("PDF_Model_ibfk1", "scanParametersServiceId"),
        Index("PDF_Model_ibfk2", "dataCollectionPlanId"),
    )

    scanParametersModelId = Column(INTEGER(11), primary_key=True)
    scanParametersServiceId = Column(INTEGER(10))
    dataCollectionPlanId = Column(INTEGER(11))
    sequenceNumber = Column(TINYINT(3))
    start = Column(Float(asdecimal=True))
    stop = Column(Float(asdecimal=True))
    step = Column(Float(asdecimal=True))
    array = Column(Text)
    duration = Column(MEDIUMINT(8), comment="Duration for parameter change in seconds")

    DiffractionPlan_ = relationship(
        "DiffractionPlan", back_populates="ScanParametersModel"
    )
    ScanParametersService_ = relationship(
        "ScanParametersService", back_populates="ScanParametersModel"
    )


class ScreenComponentGroup(Base):
    __tablename__ = "ScreenComponentGroup"
    __table_args__ = (
        ForeignKeyConstraint(
            ["screenId"], ["Screen.screenId"], name="ScreenComponentGroup_fk1"
        ),
        Index("ScreenComponentGroup_fk1", "screenId"),
    )

    screenComponentGroupId = Column(INTEGER(11), primary_key=True)
    screenId = Column(INTEGER(11), nullable=False)
    position = Column(SMALLINT(6))

    BLSample_ = relationship("BLSample", back_populates="ScreenComponentGroup")
    Screen_ = relationship("Screen", back_populates="ScreenComponentGroup")
    ScreenComponent = relationship(
        "ScreenComponent", back_populates="ScreenComponentGroup_"
    )


class SessionType(Base):
    __tablename__ = "SessionType"
    __table_args__ = (
        ForeignKeyConstraint(
            ["sessionId"],
            ["BLSession.sessionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="SessionType_ibfk_1",
        ),
        Index("SessionType_FKIndex1", "sessionId"),
    )

    sessionTypeId = Column(INTEGER(10), primary_key=True)
    sessionId = Column(INTEGER(10), nullable=False)
    typeName = Column(String(31), nullable=False)

    BLSession_ = relationship("BLSession", back_populates="SessionType")


class SessionHasPerson(Base):
    __tablename__ = "Session_has_Person"
    __table_args__ = (
        ForeignKeyConstraint(
            ["personId"],
            ["Person.personId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Session_has_Person_ibfk_2",
        ),
        ForeignKeyConstraint(
            ["sessionId"],
            ["BLSession.sessionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Session_has_Person_ibfk_1",
        ),
        Index("Session_has_Person_FKIndex2", "personId"),
    )

    sessionId = Column(
        INTEGER(10), primary_key=True, nullable=False, server_default=text("0")
    )
    personId = Column(
        INTEGER(10), primary_key=True, nullable=False, server_default=text("0")
    )
    role = Column(
        Enum(
            "Local Contact",
            "Local Contact 2",
            "Staff",
            "Team Leader",
            "Co-Investigator",
            "Principal Investigator",
            "Alternate Contact",
            "Data Access",
            "Team Member",
            "ERA Admin",
            "Associate",
        )
    )
    remote = Column(TINYINT(1), server_default=text("0"))

    Person_ = relationship("Person", back_populates="Session_has_Person")
    BLSession_ = relationship("BLSession", back_populates="Session_has_Person")


class Shipping(Base):
    __tablename__ = "Shipping"
    __table_args__ = (
        ForeignKeyConstraint(
            ["deliveryAgent_flightCodePersonId"],
            ["Person.personId"],
            name="Shipping_ibfk_4",
        ),
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Shipping_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["returnLabContactId"],
            ["LabContact.labContactId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Shipping_ibfk_3",
        ),
        ForeignKeyConstraint(
            ["sendingLabContactId"],
            ["LabContact.labContactId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Shipping_ibfk_2",
        ),
        Index("Shipping_FKIndex1", "proposalId"),
        Index("Shipping_FKIndex2", "sendingLabContactId"),
        Index("Shipping_FKIndex3", "returnLabContactId"),
        Index("Shipping_FKIndexCreationDate", "creationDate"),
        Index("Shipping_FKIndexName", "shippingName"),
        Index("Shipping_FKIndexStatus", "shippingStatus"),
        Index("Shipping_ibfk_4", "deliveryAgent_flightCodePersonId"),
        Index("laboratoryId", "laboratoryId"),
    )

    shippingId = Column(INTEGER(10), primary_key=True)
    proposalId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    shippingName = Column(String(45))
    deliveryAgent_agentName = Column(String(45))
    deliveryAgent_shippingDate = Column(Date)
    deliveryAgent_deliveryDate = Column(Date)
    deliveryAgent_agentCode = Column(String(45))
    deliveryAgent_flightCode = Column(String(45))
    shippingStatus = Column(String(45))
    bltimeStamp = Column(DateTime)
    laboratoryId = Column(INTEGER(10))
    isStorageShipping = Column(TINYINT(1), server_default=text("0"))
    creationDate = Column(DateTime)
    comments = Column(String(1000))
    sendingLabContactId = Column(INTEGER(10))
    returnLabContactId = Column(INTEGER(10))
    returnCourier = Column(String(45))
    dateOfShippingToUser = Column(DateTime)
    shippingType = Column(String(45))
    SAFETYLEVEL = Column(String(8))
    deliveryAgent_flightCodeTimestamp = Column(
        TIMESTAMP, comment="Date flight code created, if automatic"
    )
    deliveryAgent_label = Column(Text, comment="Base64 encoded pdf of airway label")
    readyByTime = Column(Time, comment="Time shipment will be ready")
    closeTime = Column(Time, comment="Time after which shipment cannot be picked up")
    physicalLocation = Column(
        String(50), comment="Where shipment can be picked up from: i.e. Stores"
    )
    deliveryAgent_pickupConfirmationTimestamp = Column(
        TIMESTAMP, comment="Date picked confirmed"
    )
    deliveryAgent_pickupConfirmation = Column(
        String(10), comment="Confirmation number of requested pickup"
    )
    deliveryAgent_readyByTime = Column(Time, comment="Confirmed ready-by time")
    deliveryAgent_callinTime = Column(Time, comment="Confirmed courier call-in time")
    deliveryAgent_productcode = Column(
        String(10), comment="A code that identifies which shipment service was used"
    )
    deliveryAgent_flightCodePersonId = Column(
        INTEGER(10), comment="The person who created the AWB (for auditing)"
    )
    extra = Column(
        LONGTEXT,
        comment="JSON column for facility-specific or hard-to-define attributes",
    )

    Project_ = relationship(
        "Project", secondary="Project_has_Shipping", back_populates="Shipping"
    )
    BLSession_ = relationship(
        "BLSession", secondary="ShippingHasSession", back_populates="Shipping"
    )
    Person_ = relationship("Person", back_populates="Shipping")
    Proposal_ = relationship("Proposal", back_populates="Shipping")
    LabContact_ = relationship(
        "LabContact", foreign_keys=[returnLabContactId], back_populates="Shipping"
    )
    LabContact1 = relationship(
        "LabContact", foreign_keys=[sendingLabContactId], back_populates="Shipping_"
    )
    CourierTermsAccepted = relationship(
        "CourierTermsAccepted", back_populates="Shipping_"
    )
    Dewar = relationship("Dewar", back_populates="Shipping_")


class XFEFluorescenceSpectrum(Base):
    __tablename__ = "XFEFluorescenceSpectrum"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"],
            ["BLSample.blSampleId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="XFE_ibfk_2",
        ),
        ForeignKeyConstraint(
            ["blSubSampleId"], ["BLSubSample.blSubSampleId"], name="XFE_ibfk_3"
        ),
        ForeignKeyConstraint(
            ["sessionId"],
            ["BLSession.sessionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="XFE_ibfk_1",
        ),
        Index("XFEFluorescnceSpectrum_FKIndex1", "blSampleId"),
        Index("XFEFluorescnceSpectrum_FKIndex2", "sessionId"),
        Index("XFE_ibfk_3", "blSubSampleId"),
    )

    xfeFluorescenceSpectrumId = Column(INTEGER(10), primary_key=True)
    sessionId = Column(INTEGER(10), nullable=False)
    blSampleId = Column(INTEGER(10))
    jpegScanFileFullPath = Column(String(255))
    startTime = Column(DateTime)
    endTime = Column(DateTime)
    filename = Column(String(255))
    exposureTime = Column(Float)
    axisPosition = Column(Float)
    beamTransmission = Column(Float)
    annotatedPymcaXfeSpectrum = Column(String(255))
    fittedDataFileFullPath = Column(String(255))
    scanFileFullPath = Column(String(255))
    energy = Column(Float)
    beamSizeVertical = Column(Float)
    beamSizeHorizontal = Column(Float)
    crystalClass = Column(String(20))
    comments = Column(String(1024))
    blSubSampleId = Column(INTEGER(11))
    flux = Column(Float(asdecimal=True), comment="flux measured before the xrfSpectra")
    flux_end = Column(
        Float(asdecimal=True), comment="flux measured after the xrfSpectra"
    )
    workingDirectory = Column(String(512))

    Project_ = relationship(
        "Project",
        secondary="Project_has_XFEFSpectrum",
        back_populates="XFEFluorescenceSpectrum",
    )
    BLSample_ = relationship("BLSample", back_populates="XFEFluorescenceSpectrum")
    BLSubSample_ = relationship("BLSubSample", back_populates="XFEFluorescenceSpectrum")
    BLSession_ = relationship("BLSession", back_populates="XFEFluorescenceSpectrum")


class BLSampleTypeHasComponent(Base):
    __tablename__ = "BLSampleType_has_Component"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleTypeId"],
            ["Crystal.crystalId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="blSampleType_has_Component_fk1",
        ),
        ForeignKeyConstraint(
            ["componentId"],
            ["Protein.proteinId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="blSampleType_has_Component_fk2",
        ),
        Index("blSampleType_has_Component_fk2", "componentId"),
    )

    blSampleTypeId = Column(INTEGER(10), primary_key=True, nullable=False)
    componentId = Column(INTEGER(10), primary_key=True, nullable=False)
    abundance = Column(Float)

    Crystal_ = relationship("Crystal", back_populates="BLSampleType_has_Component")
    Protein_ = relationship("Protein", back_populates="BLSampleType_has_Component")


class BLSampleHasEnergyScan(Base):
    __tablename__ = "BLSample_has_EnergyScan"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"],
            ["BLSample.blSampleId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSample_has_EnergyScan_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["energyScanId"],
            ["EnergyScan.energyScanId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="BLSample_has_EnergyScan_ibfk_2",
        ),
        Index("BLSample_has_EnergyScan_FKIndex1", "blSampleId"),
        Index("BLSample_has_EnergyScan_FKIndex2", "energyScanId"),
    )

    blSampleId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    energyScanId = Column(INTEGER(10), nullable=False, server_default=text("0"))
    blSampleHasEnergyScanId = Column(INTEGER(10), primary_key=True)

    BLSample_ = relationship("BLSample", back_populates="BLSample_has_EnergyScan")
    EnergyScan_ = relationship("EnergyScan", back_populates="BLSample_has_EnergyScan")


class CourierTermsAccepted(Base):
    __tablename__ = "CourierTermsAccepted"
    __table_args__ = (
        ForeignKeyConstraint(
            ["personId"], ["Person.personId"], name="CourierTermsAccepted_ibfk_2"
        ),
        ForeignKeyConstraint(
            ["proposalId"], ["Proposal.proposalId"], name="CourierTermsAccepted_ibfk_1"
        ),
        ForeignKeyConstraint(
            ["shippingId"],
            ["Shipping.shippingId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="CourierTermsAccepted_ibfk_3",
        ),
        Index("CourierTermsAccepted_ibfk_1", "proposalId"),
        Index("CourierTermsAccepted_ibfk_2", "personId"),
        Index("CourierTermsAccepted_ibfk_3", "shippingId"),
        {"comment": "Records acceptances of the courier T and C"},
    )

    courierTermsAcceptedId = Column(INTEGER(10), primary_key=True)
    proposalId = Column(INTEGER(10), nullable=False)
    personId = Column(INTEGER(10), nullable=False)
    shippingName = Column(String(100))
    timestamp = Column(DateTime, server_default=text("current_timestamp()"))
    shippingId = Column(INTEGER(11))

    Person_ = relationship("Person", back_populates="CourierTermsAccepted")
    Proposal_ = relationship("Proposal", back_populates="CourierTermsAccepted")
    Shipping_ = relationship("Shipping", back_populates="CourierTermsAccepted")


class CrystalComposition(Base):
    __tablename__ = "CrystalComposition"
    __table_args__ = (
        ForeignKeyConstraint(
            ["componentId"], ["Component.componentId"], name="CrystalComposition_ibfk_1"
        ),
        ForeignKeyConstraint(
            ["concentrationTypeId"],
            ["ConcentrationType.concentrationTypeId"],
            name="CrystalComposition_ibfk_3",
        ),
        ForeignKeyConstraint(
            ["crystalId"], ["Crystal.crystalId"], name="CrystalComposition_ibfk_2"
        ),
        Index("componentId", "componentId"),
        Index("concentrationTypeId", "concentrationTypeId"),
        Index("crystalId", "crystalId"),
        {
            "comment": "Links a crystal to its components with a specified abundance or "
            "ratio."
        },
    )

    crystalCompositionId = Column(INTEGER(11), primary_key=True)
    componentId = Column(INTEGER(11), nullable=False)
    crystalId = Column(INTEGER(11), nullable=False)
    concentrationTypeId = Column(INTEGER(10))
    abundance = Column(
        Float,
        comment="Abundance or concentration in the unit defined by concentrationTypeId.",
    )
    ratio = Column(Float)
    pH = Column(Float)

    Component_ = relationship("Component", back_populates="CrystalComposition")
    ConcentrationType_ = relationship(
        "ConcentrationType", back_populates="CrystalComposition"
    )
    Crystal_ = relationship("Crystal", back_populates="CrystalComposition")


class CrystalHasUUID(Base):
    __tablename__ = "Crystal_has_UUID"
    __table_args__ = (
        ForeignKeyConstraint(
            ["crystalId"],
            ["Crystal.crystalId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ibfk_1",
        ),
        Index("Crystal_has_UUID_FKIndex1", "crystalId"),
        Index("Crystal_has_UUID_FKIndex2", "UUID"),
    )

    crystal_has_UUID_Id = Column(INTEGER(10), primary_key=True)
    crystalId = Column(INTEGER(10), nullable=False)
    UUID = Column(String(45))
    imageURL = Column(String(255))

    Crystal_ = relationship("Crystal", back_populates="Crystal_has_UUID")


class Dewar(Base):
    __tablename__ = "Dewar"
    __table_args__ = (
        ForeignKeyConstraint(
            ["firstExperimentId"],
            ["BLSession.sessionId"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="Dewar_fk_firstExperimentId",
        ),
        ForeignKeyConstraint(
            ["shippingId"],
            ["Shipping.shippingId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Dewar_ibfk_1",
        ),
        Index("Dewar_FKIndex1", "shippingId"),
        Index("Dewar_FKIndex2", "firstExperimentId"),
        Index("Dewar_FKIndexCode", "code"),
        Index("Dewar_FKIndexStatus", "dewarStatus"),
        Index("barCode", "barCode", unique=True),
    )

    dewarId = Column(INTEGER(10), primary_key=True)
    type = Column(
        Enum("Dewar", "Toolbox", "Parcel"),
        nullable=False,
        server_default=text("'Dewar'"),
    )
    shippingId = Column(INTEGER(10))
    code = Column(String(45))
    comments = Column(TINYTEXT)
    storageLocation = Column(String(45))
    dewarStatus = Column(String(45))
    bltimeStamp = Column(DateTime)
    isStorageDewar = Column(TINYINT(1), server_default=text("0"))
    barCode = Column(String(45))
    firstExperimentId = Column(INTEGER(10))
    customsValue = Column(INTEGER(11))
    transportValue = Column(INTEGER(11))
    trackingNumberToSynchrotron = Column(String(30))
    trackingNumberFromSynchrotron = Column(String(30))
    facilityCode = Column(String(20))
    weight = Column(Float, comment="dewar weight in kg")
    deliveryAgent_barcode = Column(
        String(30), comment="Courier piece barcode (not the airway bill)"
    )

    BLSession_ = relationship("BLSession", back_populates="Dewar")
    Shipping_ = relationship("Shipping", back_populates="Dewar")
    Container = relationship(
        "Container", foreign_keys="[Container.currentDewarId]", back_populates="Dewar_"
    )
    Container_ = relationship(
        "Container", foreign_keys="[Container.dewarId]", back_populates="Dewar1"
    )
    DewarTransportHistory = relationship(
        "DewarTransportHistory", back_populates="Dewar_"
    )
    ContainerHistory = relationship("ContainerHistory", back_populates="Dewar_")


class DewarRegistryHasProposal(Base):
    __tablename__ = "DewarRegistry_has_Proposal"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dewarRegistryId"],
            ["DewarRegistry.dewarRegistryId"],
            name="DewarRegistry_has_Proposal_ibfk1",
        ),
        ForeignKeyConstraint(
            ["labContactId"],
            ["LabContact.labContactId"],
            onupdate="CASCADE",
            name="DewarRegistry_has_Proposal_ibfk4",
        ),
        ForeignKeyConstraint(
            ["personId"], ["Person.personId"], name="DewarRegistry_has_Proposal_ibfk3"
        ),
        ForeignKeyConstraint(
            ["proposalId"],
            ["Proposal.proposalId"],
            name="DewarRegistry_has_Proposal_ibfk2",
        ),
        Index("DewarRegistry_has_Proposal_ibfk2", "proposalId"),
        Index("DewarRegistry_has_Proposal_ibfk3", "personId"),
        Index("DewarRegistry_has_Proposal_ibfk4", "labContactId"),
        Index("dewarRegistryId", "dewarRegistryId", "proposalId", unique=True),
    )

    dewarRegistryHasProposalId = Column(INTEGER(11), primary_key=True)
    dewarRegistryId = Column(INTEGER(11))
    proposalId = Column(INTEGER(10))
    personId = Column(INTEGER(10), comment="Person registering the dewar")
    recordTimestamp = Column(DateTime, server_default=text("current_timestamp()"))
    labContactId = Column(INTEGER(11), comment="Owner of the dewar")

    DewarRegistry_ = relationship(
        "DewarRegistry", back_populates="DewarRegistry_has_Proposal"
    )
    LabContact_ = relationship(
        "LabContact", back_populates="DewarRegistry_has_Proposal"
    )
    Person_ = relationship("Person", back_populates="DewarRegistry_has_Proposal")
    Proposal_ = relationship("Proposal", back_populates="DewarRegistry_has_Proposal")


class DewarReport(Base):
    __tablename__ = "DewarReport"
    __table_args__ = (
        ForeignKeyConstraint(
            ["facilityCode"],
            ["DewarRegistry.facilityCode"],
            ondelete="CASCADE",
            name="DewarReport_ibfk_1",
        ),
        Index("DewarReportIdx1", "facilityCode"),
    )

    dewarReportId = Column(INTEGER(11), primary_key=True)
    facilityCode = Column(String(20), nullable=False)
    bltimestamp = Column(
        DateTime, nullable=False, server_default=text("current_timestamp()")
    )
    report = Column(Text)
    attachment = Column(String(255))

    DewarRegistry_ = relationship("DewarRegistry", back_populates="DewarReport")


class GridInfo(Base):
    __tablename__ = "GridInfo"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionGroupId"],
            ["DataCollectionGroup.dataCollectionGroupId"],
            name="GridInfo_ibfk_2",
        ),
        ForeignKeyConstraint(
            ["dataCollectionId"],
            ["DataCollection.dataCollectionId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="GridInfo_fk_dataCollectionId",
        ),
        Index("GridInfo_fk_dataCollectionId", "dataCollectionId"),
        Index("GridInfo_ibfk_2", "dataCollectionGroupId"),
        Index("workflowMeshId", "workflowMeshId"),
    )

    gridInfoId = Column(
        INTEGER(11), primary_key=True, comment="Primary key (auto-incremented)"
    )
    recordTimeStamp = Column(
        TIMESTAMP,
        nullable=False,
        server_default=text("current_timestamp()"),
        comment="Creation or last update date/time",
    )
    xOffset = Column(Float(asdecimal=True))
    yOffset = Column(Float(asdecimal=True))
    dx_mm = Column(Float(asdecimal=True))
    dy_mm = Column(Float(asdecimal=True))
    steps_x = Column(Float(asdecimal=True))
    steps_y = Column(Float(asdecimal=True))
    meshAngle = Column(Float(asdecimal=True))
    workflowMeshId = Column(INTEGER(11))
    orientation = Column(
        Enum("vertical", "horizontal"), server_default=text("'horizontal'")
    )
    dataCollectionGroupId = Column(INTEGER(11))
    pixelsPerMicronX = Column(Float)
    pixelsPerMicronY = Column(Float)
    snapshot_offsetXPixel = Column(Float)
    snapshot_offsetYPixel = Column(Float)
    snaked = Column(
        TINYINT(1),
        server_default=text("0"),
        comment="True: The images associated with the DCG were collected in a snaked pattern",
    )
    dataCollectionId = Column(INTEGER(11))
    patchesX = Column(
        INTEGER(10),
        server_default=text("1"),
        comment="Number of patches the grid is made up of in the X direction",
    )
    patchesY = Column(
        INTEGER(10),
        server_default=text("1"),
        comment="Number of patches the grid is made up of in the Y direction",
    )

    DataCollectionGroup_ = relationship(
        "DataCollectionGroup", back_populates="GridInfo"
    )
    DataCollection_ = relationship("DataCollection", back_populates="GridInfo")
    XRFFluorescenceMapping = relationship(
        "XRFFluorescenceMapping", back_populates="GridInfo_"
    )
    XrayCentringResult = relationship("XrayCentringResult", back_populates="GridInfo_")


class ParticleClassification(Base):
    __tablename__ = "ParticleClassification"
    __table_args__ = (
        ForeignKeyConstraint(
            ["particleClassificationGroupId"],
            ["ParticleClassificationGroup.particleClassificationGroupId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ParticleClassification_fk_particleClassificationGroupId",
        ),
        Index(
            "ParticleClassification_fk_particleClassificationGroupId",
            "particleClassificationGroupId",
        ),
        {"comment": "Results of 2D or 2D classification"},
    )

    particleClassificationId = Column(INTEGER(10), primary_key=True)
    classNumber = Column(
        INTEGER(10), comment="Identified of the class. A unique ID given by Relion"
    )
    classImageFullPath = Column(String(255), comment="The PNG of the class")
    particlesPerClass = Column(
        INTEGER(10),
        comment="Number of particles within the selected class, can then be used together with the total number above to calculate the percentage",
    )
    rotationAccuracy = Column(Float, comment="???")
    translationAccuracy = Column(Float, comment="Unit: Angstroms")
    estimatedResolution = Column(Float, comment="???, Unit: Angstroms")
    overallFourierCompleteness = Column(Float)
    particleClassificationGroupId = Column(INTEGER(10))
    classDistribution = Column(
        Float,
        comment="Provides a figure of merit for the class, higher number is better",
    )
    selected = Column(
        TINYINT(1),
        server_default=text("0"),
        comment="Indicates whether the group is selected for processing or not.",
    )

    CryoemInitialModel_ = relationship(
        "CryoemInitialModel",
        secondary="ParticleClassification_has_CryoemInitialModel",
        back_populates="ParticleClassification",
    )
    ParticleClassificationGroup_ = relationship(
        "ParticleClassificationGroup", back_populates="ParticleClassification"
    )
    BFactorFit = relationship("BFactorFit", back_populates="ParticleClassification_")


t_Project_has_DCGroup = Table(
    "Project_has_DCGroup",
    metadata,
    Column("projectId", INTEGER(11), primary_key=True, nullable=False),
    Column("dataCollectionGroupId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["dataCollectionGroupId"],
        ["DataCollectionGroup.dataCollectionGroupId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="Project_has_DCGroup_FK2",
    ),
    ForeignKeyConstraint(
        ["projectId"],
        ["Project.projectId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="Project_has_DCGroup_FK1",
    ),
    Index("Project_has_DCGroup_FK2", "dataCollectionGroupId"),
)


t_Project_has_EnergyScan = Table(
    "Project_has_EnergyScan",
    metadata,
    Column("projectId", INTEGER(11), primary_key=True, nullable=False),
    Column("energyScanId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["energyScanId"],
        ["EnergyScan.energyScanId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="project_has_energyscan_FK2",
    ),
    ForeignKeyConstraint(
        ["projectId"],
        ["Project.projectId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="project_has_energyscan_FK1",
    ),
    Index("project_has_energyscan_FK2", "energyScanId"),
)


t_Project_has_Shipping = Table(
    "Project_has_Shipping",
    metadata,
    Column("projectId", INTEGER(11), primary_key=True, nullable=False),
    Column("shippingId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["projectId"],
        ["Project.projectId"],
        ondelete="CASCADE",
        name="project_has_shipping_FK1",
    ),
    ForeignKeyConstraint(
        ["shippingId"],
        ["Shipping.shippingId"],
        ondelete="CASCADE",
        name="project_has_shipping_FK2",
    ),
    Index("project_has_shipping_FK2", "shippingId"),
)


t_Project_has_XFEFSpectrum = Table(
    "Project_has_XFEFSpectrum",
    metadata,
    Column("projectId", INTEGER(11), primary_key=True, nullable=False),
    Column("xfeFluorescenceSpectrumId", INTEGER(11), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["projectId"],
        ["Project.projectId"],
        ondelete="CASCADE",
        name="project_has_xfefspectrum_FK1",
    ),
    ForeignKeyConstraint(
        ["xfeFluorescenceSpectrumId"],
        ["XFEFluorescenceSpectrum.xfeFluorescenceSpectrumId"],
        ondelete="CASCADE",
        name="project_has_xfefspectrum_FK2",
    ),
    Index("project_has_xfefspectrum_FK2", "xfeFluorescenceSpectrumId"),
)


class ScreenComponent(Base):
    __tablename__ = "ScreenComponent"
    __table_args__ = (
        ForeignKeyConstraint(
            ["componentId"], ["Protein.proteinId"], name="ScreenComponent_fk2"
        ),
        ForeignKeyConstraint(
            ["screenComponentGroupId"],
            ["ScreenComponentGroup.screenComponentGroupId"],
            name="ScreenComponent_fk1",
        ),
        Index("ScreenComponent_fk1", "screenComponentGroupId"),
        Index("ScreenComponent_fk2", "componentId"),
    )

    screenComponentId = Column(INTEGER(11), primary_key=True)
    screenComponentGroupId = Column(INTEGER(11), nullable=False)
    componentId = Column(INTEGER(11))
    concentration = Column(Float)
    pH = Column(Float)

    Protein_ = relationship("Protein", back_populates="ScreenComponent")
    ScreenComponentGroup_ = relationship(
        "ScreenComponentGroup", back_populates="ScreenComponent"
    )


t_ShippingHasSession = Table(
    "ShippingHasSession",
    metadata,
    Column("shippingId", INTEGER(10), primary_key=True, nullable=False),
    Column("sessionId", INTEGER(10), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["sessionId"],
        ["BLSession.sessionId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="ShippingHasSession_ibfk_2",
    ),
    ForeignKeyConstraint(
        ["shippingId"],
        ["Shipping.shippingId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="ShippingHasSession_ibfk_1",
    ),
    Index("ShippingHasSession_FKIndex2", "sessionId"),
)


class XrayCentring(Base):
    __tablename__ = "XrayCentring"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dataCollectionGroupId"],
            ["DataCollectionGroup.dataCollectionGroupId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="XrayCentring_ibfk_1",
        ),
        Index("dataCollectionGroupId", "dataCollectionGroupId"),
        {"comment": "Xray Centring analysis associated with one or more grid scans."},
    )

    xrayCentringId = Column(INTEGER(11), primary_key=True)
    dataCollectionGroupId = Column(
        INTEGER(11), nullable=False, comment="references DataCollectionGroup table"
    )
    status = Column(Enum("success", "failed", "pending"))
    xrayCentringType = Column(Enum("2d", "3d"))

    DataCollectionGroup_ = relationship(
        "DataCollectionGroup", back_populates="XrayCentring"
    )


class BFactorFit(Base):
    __tablename__ = "BFactorFit"
    __table_args__ = (
        ForeignKeyConstraint(
            ["particleClassificationId"],
            ["ParticleClassification.particleClassificationId"],
            name="BFactorFit_fk_particleClassificationId",
        ),
        Index("BFactorFit_fk_particleClassificationId", "particleClassificationId"),
        {
            "comment": "CryoEM reconstruction resolution as a function of the number of "
            "particles for the creation of a Rosenthal-Henderson plot and the "
            "calculation of B-factors"
        },
    )

    bFactorFitId = Column(INTEGER(11), primary_key=True)
    particleClassificationId = Column(INTEGER(11), nullable=False)
    resolution = Column(
        Float, comment="Resolution of a refined map using a given number of particles"
    )
    numberOfParticles = Column(
        INTEGER(10), comment="Number of particles used in refinement"
    )
    particleBatchSize = Column(
        INTEGER(10),
        comment="Number of particles in the batch that the B-factor analysis was performed on",
    )

    ParticleClassification_ = relationship(
        "ParticleClassification", back_populates="BFactorFit"
    )


class Container(Base):
    __tablename__ = "Container"
    __table_args__ = (
        ForeignKeyConstraint(
            ["containerRegistryId"],
            ["ContainerRegistry.containerRegistryId"],
            name="Container_ibfk8",
        ),
        ForeignKeyConstraint(
            ["containerTypeId"],
            ["ContainerType.containerTypeId"],
            name="Container_ibfk10",
        ),
        ForeignKeyConstraint(
            ["currentDewarId"], ["Dewar.dewarId"], name="Container_fk_currentDewarId"
        ),
        ForeignKeyConstraint(
            ["dewarId"],
            ["Dewar.dewarId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="Container_ibfk_1",
        ),
        ForeignKeyConstraint(
            ["experimentTypeId"],
            ["ExperimentType.experimentTypeId"],
            name="Container_fk_experimentTypeId",
        ),
        ForeignKeyConstraint(["imagerId"], ["Imager.imagerId"], name="Container_ibfk4"),
        ForeignKeyConstraint(["ownerId"], ["Person.personId"], name="Container_ibfk5"),
        ForeignKeyConstraint(
            ["parentContainerId"],
            ["Container.containerId"],
            name="Container_fk_parentContainerId",
        ),
        ForeignKeyConstraint(
            ["priorityPipelineId"],
            ["ProcessingPipeline.processingPipelineId"],
            name="Container_ibfk9",
        ),
        ForeignKeyConstraint(
            ["requestedImagerId"], ["Imager.imagerId"], name="Container_ibfk7"
        ),
        ForeignKeyConstraint(
            ["scheduleId"], ["Schedule.scheduleId"], name="Container_ibfk3"
        ),
        ForeignKeyConstraint(["screenId"], ["Screen.screenId"], name="Container_ibfk2"),
        ForeignKeyConstraint(
            ["sessionId"],
            ["BLSession.sessionId"],
            ondelete="SET NULL",
            onupdate="CASCADE",
            name="Container_ibfk6",
        ),
        Index("Container_FKIndex", "beamlineLocation"),
        Index("Container_FKIndex1", "dewarId"),
        Index("Container_FKIndexStatus", "containerStatus"),
        Index("Container_UNIndex1", "barcode", unique=True),
        Index("Container_fk_currentDewarId", "currentDewarId"),
        Index("Container_fk_experimentTypeId", "experimentTypeId"),
        Index("Container_fk_parentContainerId", "parentContainerId"),
        Index("Container_ibfk10", "containerTypeId"),
        Index("Container_ibfk2", "screenId"),
        Index("Container_ibfk3", "scheduleId"),
        Index("Container_ibfk4", "imagerId"),
        Index("Container_ibfk5", "ownerId"),
        Index("Container_ibfk6", "sessionId"),
        Index("Container_ibfk7", "requestedImagerId"),
        Index("Container_ibfk8", "containerRegistryId"),
        Index("Container_ibfk9", "priorityPipelineId"),
    )

    containerId = Column(INTEGER(10), primary_key=True)
    dewarId = Column(INTEGER(10))
    code = Column(String(45))
    containerType = Column(String(20))
    capacity = Column(INTEGER(10))
    sampleChangerLocation = Column(String(20))
    containerStatus = Column(String(45))
    bltimeStamp = Column(DateTime)
    beamlineLocation = Column(String(20))
    screenId = Column(INTEGER(11))
    scheduleId = Column(INTEGER(11))
    barcode = Column(String(45))
    imagerId = Column(INTEGER(11))
    sessionId = Column(INTEGER(10))
    ownerId = Column(INTEGER(10))
    requestedImagerId = Column(INTEGER(11))
    requestedReturn = Column(
        TINYINT(1),
        server_default=text("0"),
        comment="True for requesting return, False means container will be disposed",
    )
    comments = Column(String(255))
    experimentType = Column(String(20))
    storageTemperature = Column(Float, comment="NULL=ambient")
    containerRegistryId = Column(INTEGER(11))
    scLocationUpdated = Column(DateTime)
    priorityPipelineId = Column(
        INTEGER(11),
        server_default=text("6"),
        comment="Processing pipeline to prioritise, defaults to 6 which is xia2/DIALS",
    )
    experimentTypeId = Column(INTEGER(10))
    containerTypeId = Column(INTEGER(10))
    currentDewarId = Column(
        INTEGER(10),
        comment="The dewar with which the container is currently associated",
    )
    parentContainerId = Column(INTEGER(10))

    BLSample_ = relationship("BLSample", back_populates="Container")
    ContainerRegistry_ = relationship("ContainerRegistry", back_populates="Container")
    ContainerType_ = relationship("ContainerType", back_populates="Container")
    Dewar_ = relationship(
        "Dewar", foreign_keys=[currentDewarId], back_populates="Container"
    )
    Dewar1 = relationship("Dewar", foreign_keys=[dewarId], back_populates="Container_")
    ExperimentType_ = relationship("ExperimentType", back_populates="Container")
    Imager_ = relationship(
        "Imager", foreign_keys=[imagerId], back_populates="Container"
    )
    Person_ = relationship("Person", back_populates="Container")
    Container = relationship(
        "Container", remote_side=[containerId], back_populates="Container_reverse"
    )
    Container_reverse = relationship(
        "Container", remote_side=[parentContainerId], back_populates="Container"
    )
    ProcessingPipeline_ = relationship("ProcessingPipeline", back_populates="Container")
    Imager1 = relationship(
        "Imager", foreign_keys=[requestedImagerId], back_populates="Container_"
    )
    Schedule_ = relationship("Schedule", back_populates="Container")
    Screen_ = relationship("Screen", back_populates="Container")
    BLSession_ = relationship("BLSession", back_populates="Container")
    BF_automationFault = relationship("BFAutomationFault", back_populates="Container_")
    ContainerHistory = relationship("ContainerHistory", back_populates="Container_")
    ContainerInspection = relationship(
        "ContainerInspection", back_populates="Container_"
    )
    ContainerQueue = relationship("ContainerQueue", back_populates="Container_")


class DewarTransportHistory(Base):
    __tablename__ = "DewarTransportHistory"
    __table_args__ = (
        ForeignKeyConstraint(
            ["dewarId"],
            ["Dewar.dewarId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="DewarTransportHistory_ibfk_1",
        ),
        Index("DewarTransportHistory_FKIndex1", "dewarId"),
    )

    DewarTransportHistoryId = Column(INTEGER(10), primary_key=True)
    dewarStatus = Column(String(45), nullable=False)
    storageLocation = Column(String(45), nullable=False)
    arrivalDate = Column(DateTime, nullable=False)
    dewarId = Column(INTEGER(10))

    Dewar_ = relationship("Dewar", back_populates="DewarTransportHistory")


t_ParticleClassification_has_CryoemInitialModel = Table(
    "ParticleClassification_has_CryoemInitialModel",
    metadata,
    Column("particleClassificationId", INTEGER(10), primary_key=True, nullable=False),
    Column("cryoemInitialModelId", INTEGER(10), primary_key=True, nullable=False),
    ForeignKeyConstraint(
        ["cryoemInitialModelId"],
        ["CryoemInitialModel.cryoemInitialModelId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="ParticleClassification_has_InitialModel_fk2",
    ),
    ForeignKeyConstraint(
        ["particleClassificationId"],
        ["ParticleClassification.particleClassificationId"],
        ondelete="CASCADE",
        onupdate="CASCADE",
        name="ParticleClassification_has_CryoemInitialModel_fk1",
    ),
    Index("ParticleClassification_has_InitialModel_fk2", "cryoemInitialModelId"),
)


class XRFFluorescenceMapping(Base):
    __tablename__ = "XRFFluorescenceMapping"
    __table_args__ = (
        ForeignKeyConstraint(
            ["autoProcProgramId"],
            ["AutoProcProgram.autoProcProgramId"],
            name="XRFFluorescenceMapping_ibfk3",
        ),
        ForeignKeyConstraint(
            ["gridInfoId"], ["GridInfo.gridInfoId"], name="XRFFluorescenceMapping_ibfk2"
        ),
        ForeignKeyConstraint(
            ["xrfFluorescenceMappingROIId"],
            ["XRFFluorescenceMappingROI.xrfFluorescenceMappingROIId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="XRFFluorescenceMapping_ibfk1",
        ),
        Index("XRFFluorescenceMapping_ibfk1", "xrfFluorescenceMappingROIId"),
        Index("XRFFluorescenceMapping_ibfk2", "gridInfoId"),
        Index("XRFFluorescenceMapping_ibfk3", "autoProcProgramId"),
        {
            "comment": "An XRF map generated from an XRF Mapping ROI based on data from a "
            "gridscan of a sample"
        },
    )

    xrfFluorescenceMappingId = Column(INTEGER(11), primary_key=True)
    xrfFluorescenceMappingROIId = Column(INTEGER(11), nullable=False)
    gridInfoId = Column(INTEGER(11), nullable=False)
    dataFormat = Column(
        String(15),
        nullable=False,
        comment="Description of format and any compression, i.e. json+gzip for gzipped json",
    )
    data = Column(LONGBLOB, nullable=False, comment="The actual data")
    opacity = Column(
        Float, nullable=False, server_default=text("1"), comment="Display opacity"
    )
    points = Column(
        INTEGER(11), comment="The number of points available, for realtime feedback"
    )
    colourMap = Column(String(20), comment="Colour map for displaying the data")
    min = Column(INTEGER(3), comment="Min value in the data for histogramming")
    max = Column(INTEGER(3), comment="Max value in the data for histogramming")
    autoProcProgramId = Column(INTEGER(10), comment="Related autoproc programid")

    AutoProcProgram_ = relationship(
        "AutoProcProgram", back_populates="XRFFluorescenceMapping"
    )
    GridInfo_ = relationship("GridInfo", back_populates="XRFFluorescenceMapping")
    XRFFluorescenceMappingROI_ = relationship(
        "XRFFluorescenceMappingROI", back_populates="XRFFluorescenceMapping"
    )
    XFEFluorescenceComposite = relationship(
        "XFEFluorescenceComposite",
        foreign_keys="[XFEFluorescenceComposite.b]",
        back_populates="XRFFluorescenceMapping_",
    )
    XFEFluorescenceComposite_ = relationship(
        "XFEFluorescenceComposite",
        foreign_keys="[XFEFluorescenceComposite.g]",
        back_populates="XRFFluorescenceMapping1",
    )
    XFEFluorescenceComposite1 = relationship(
        "XFEFluorescenceComposite",
        foreign_keys="[XFEFluorescenceComposite.r]",
        back_populates="XRFFluorescenceMapping2",
    )


class XrayCentringResult(Base):
    __tablename__ = "XrayCentringResult"
    __table_args__ = (
        ForeignKeyConstraint(
            ["gridInfoId"],
            ["GridInfo.gridInfoId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="XrayCentringResult_ibfk_1",
        ),
        Index("XrayCenteringResult_ibfk_1", "gridInfoId"),
    )

    xrayCentringResultId = Column(INTEGER(11), primary_key=True)
    gridInfoId = Column(INTEGER(11), nullable=False)
    status = Column(
        Enum("success", "failure", "pending"),
        nullable=False,
        server_default=text("'pending'"),
    )
    method = Column(String(15), comment="Type of X-ray centering calculation")
    x = Column(
        Float,
        comment="position in number of boxes in direction of the fast scan within GridInfo grid",
    )
    y = Column(
        Float,
        comment="position in number of boxes in direction of the slow scan within GridInfo grid",
    )

    GridInfo_ = relationship("GridInfo", back_populates="XrayCentringResult")


class BFAutomationFault(Base):
    __tablename__ = "BF_automationFault"
    __table_args__ = (
        ForeignKeyConstraint(
            ["automationErrorId"],
            ["BF_automationError.automationErrorId"],
            name="BF_automationFault_ibfk1",
        ),
        ForeignKeyConstraint(
            ["containerId"], ["Container.containerId"], name="BF_automationFault_ibfk2"
        ),
        Index("BF_automationFault_ibfk1", "automationErrorId"),
        Index("BF_automationFault_ibfk2", "containerId"),
    )

    automationFaultId = Column(INTEGER(10), primary_key=True)
    faultTimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    automationErrorId = Column(INTEGER(10))
    containerId = Column(INTEGER(10))
    severity = Column(Enum("1", "2", "3"))
    stacktrace = Column(Text)
    resolved = Column(TINYINT(1))

    BF_automationError = relationship(
        "BFAutomationError", back_populates="BF_automationFault"
    )
    Container_ = relationship("Container", back_populates="BF_automationFault")


class ContainerHistory(Base):
    __tablename__ = "ContainerHistory"
    __table_args__ = (
        ForeignKeyConstraint(
            ["containerId"],
            ["Container.containerId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ContainerHistory_ibfk1",
        ),
        ForeignKeyConstraint(
            ["currentDewarId"], ["Dewar.dewarId"], name="ContainerHistory_fk_dewarId"
        ),
        Index("ContainerHistory_fk_dewarId", "currentDewarId"),
        Index("ContainerHistory_ibfk1", "containerId"),
    )

    containerHistoryId = Column(INTEGER(11), primary_key=True)
    blTimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    containerId = Column(INTEGER(10))
    location = Column(String(45))
    status = Column(String(45))
    beamlineName = Column(String(20))
    currentDewarId = Column(
        INTEGER(10),
        comment="The dewar with which the container was associated at the creation of this row",
    )

    Container_ = relationship("Container", back_populates="ContainerHistory")
    Dewar_ = relationship("Dewar", back_populates="ContainerHistory")


class ContainerInspection(Base):
    __tablename__ = "ContainerInspection"
    __table_args__ = (
        ForeignKeyConstraint(
            ["containerId"],
            ["Container.containerId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ContainerInspection_fk1",
        ),
        ForeignKeyConstraint(
            ["imagerId"], ["Imager.imagerId"], name="ContainerInspection_fk3"
        ),
        ForeignKeyConstraint(
            ["inspectionTypeId"],
            ["InspectionType.inspectionTypeId"],
            name="ContainerInspection_fk2",
        ),
        ForeignKeyConstraint(
            ["scheduleComponentid"],
            ["ScheduleComponent.scheduleComponentId"],
            name="ContainerInspection_fk4",
        ),
        Index("ContainerInspection_fk4", "scheduleComponentid"),
        Index("ContainerInspection_idx2", "inspectionTypeId"),
        Index("ContainerInspection_idx3", "imagerId"),
        Index(
            "ContainerInspection_idx4",
            "containerId",
            "scheduleComponentid",
            "state",
            "manual",
        ),
    )

    containerInspectionId = Column(INTEGER(11), primary_key=True)
    containerId = Column(INTEGER(11), nullable=False)
    inspectionTypeId = Column(INTEGER(11), nullable=False)
    imagerId = Column(INTEGER(11))
    temperature = Column(Float)
    blTimeStamp = Column(DateTime)
    scheduleComponentid = Column(INTEGER(11))
    state = Column(String(20))
    priority = Column(SMALLINT(6))
    manual = Column(TINYINT(1))
    scheduledTimeStamp = Column(DateTime)
    completedTimeStamp = Column(DateTime)

    BLSampleImage_ = relationship("BLSampleImage", back_populates="ContainerInspection")
    Container_ = relationship("Container", back_populates="ContainerInspection")
    Imager_ = relationship("Imager", back_populates="ContainerInspection")
    InspectionType_ = relationship(
        "InspectionType", back_populates="ContainerInspection"
    )
    ScheduleComponent_ = relationship(
        "ScheduleComponent", back_populates="ContainerInspection"
    )


class ContainerQueue(Base):
    __tablename__ = "ContainerQueue"
    __table_args__ = (
        ForeignKeyConstraint(
            ["containerId"],
            ["Container.containerId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ContainerQueue_ibfk1",
        ),
        ForeignKeyConstraint(
            ["personId"],
            ["Person.personId"],
            onupdate="CASCADE",
            name="ContainerQueue_ibfk2",
        ),
        Index("ContainerQueue_ibfk1", "containerId"),
        Index("ContainerQueue_ibfk2", "personId"),
    )

    containerQueueId = Column(INTEGER(11), primary_key=True)
    createdTimeStamp = Column(
        TIMESTAMP, nullable=False, server_default=text("current_timestamp()")
    )
    containerId = Column(INTEGER(10))
    personId = Column(INTEGER(10))
    completedTimeStamp = Column(TIMESTAMP)

    Container_ = relationship("Container", back_populates="ContainerQueue")
    Person_ = relationship("Person", back_populates="ContainerQueue")
    ContainerQueueSample = relationship(
        "ContainerQueueSample", back_populates="ContainerQueue_"
    )


class XFEFluorescenceComposite(Base):
    __tablename__ = "XFEFluorescenceComposite"
    __table_args__ = (
        ForeignKeyConstraint(
            ["b"],
            ["XRFFluorescenceMapping.xrfFluorescenceMappingId"],
            name="XFEFluorescenceComposite_ibfk3",
        ),
        ForeignKeyConstraint(
            ["g"],
            ["XRFFluorescenceMapping.xrfFluorescenceMappingId"],
            name="XFEFluorescenceComposite_ibfk2",
        ),
        ForeignKeyConstraint(
            ["r"],
            ["XRFFluorescenceMapping.xrfFluorescenceMappingId"],
            name="XFEFluorescenceComposite_ibfk1",
        ),
        Index("XFEFluorescenceComposite_ibfk1", "r"),
        Index("XFEFluorescenceComposite_ibfk2", "g"),
        Index("XFEFluorescenceComposite_ibfk3", "b"),
        {
            "comment": "A composite XRF map composed of three XRFFluorescenceMapping "
            "entries creating r, g, b layers"
        },
    )

    xfeFluorescenceCompositeId = Column(INTEGER(10), primary_key=True)
    r = Column(INTEGER(10), nullable=False, comment="Red layer")
    g = Column(INTEGER(10), nullable=False, comment="Green layer")
    b = Column(INTEGER(10), nullable=False, comment="Blue layer")
    rOpacity = Column(
        Float, nullable=False, server_default=text("1"), comment="Red layer opacity"
    )
    bOpacity = Column(
        Float, nullable=False, server_default=text("1"), comment="Red layer opacity"
    )
    gOpacity = Column(
        Float, nullable=False, server_default=text("1"), comment="Red layer opacity"
    )
    opacity = Column(
        Float, nullable=False, server_default=text("1"), comment="Total map opacity"
    )

    XRFFluorescenceMapping_ = relationship(
        "XRFFluorescenceMapping",
        foreign_keys=[b],
        back_populates="XFEFluorescenceComposite",
    )
    XRFFluorescenceMapping1 = relationship(
        "XRFFluorescenceMapping",
        foreign_keys=[g],
        back_populates="XFEFluorescenceComposite_",
    )
    XRFFluorescenceMapping2 = relationship(
        "XRFFluorescenceMapping",
        foreign_keys=[r],
        back_populates="XFEFluorescenceComposite1",
    )


class ContainerQueueSample(Base):
    __tablename__ = "ContainerQueueSample"
    __table_args__ = (
        ForeignKeyConstraint(
            ["blSampleId"],
            ["BLSample.blSampleId"],
            name="ContainerQueueSample_blSampleId",
        ),
        ForeignKeyConstraint(
            ["blSubSampleId"],
            ["BLSubSample.blSubSampleId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ContainerQueueSample_ibfk2",
        ),
        ForeignKeyConstraint(
            ["containerQueueId"],
            ["ContainerQueue.containerQueueId"],
            ondelete="CASCADE",
            onupdate="CASCADE",
            name="ContainerQueueSample_ibfk1",
        ),
        ForeignKeyConstraint(
            ["dataCollectionPlanId"],
            ["DiffractionPlan.diffractionPlanId"],
            name="ContainerQueueSample_dataCollectionPlanId",
        ),
        Index("ContainerQueueSample_blSampleId", "blSampleId"),
        Index("ContainerQueueSample_dataCollectionPlanId", "dataCollectionPlanId"),
        Index("ContainerQueueSample_ibfk1", "containerQueueId"),
        Index("ContainerQueueSample_ibfk2", "blSubSampleId"),
    )

    containerQueueSampleId = Column(INTEGER(11), primary_key=True)
    containerQueueId = Column(INTEGER(11))
    blSubSampleId = Column(INTEGER(11))
    status = Column(
        String(20),
        comment="The status of the queued item, i.e. skipped, reinspect. Completed / failed should be inferred from related DataCollection",
    )
    startTime = Column(DateTime, comment="Start time of processing the queue item")
    endTime = Column(DateTime, comment="End time of processing the queue item")
    dataCollectionPlanId = Column(INTEGER(10))
    blSampleId = Column(INTEGER(10))

    BLSample_ = relationship("BLSample", back_populates="ContainerQueueSample")
    BLSubSample_ = relationship("BLSubSample", back_populates="ContainerQueueSample")
    ContainerQueue_ = relationship(
        "ContainerQueue", back_populates="ContainerQueueSample"
    )
    DiffractionPlan_ = relationship(
        "DiffractionPlan", back_populates="ContainerQueueSample"
    )
