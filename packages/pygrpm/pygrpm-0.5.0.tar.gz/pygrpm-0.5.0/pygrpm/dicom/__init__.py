"""DICOM related stuff."""
from . import sr
from .reader import DicomReader, DicomSeries, DicomStudy
from .utils import VR

__all__ = ["sr", "DicomReader", "DicomStudy", "DicomSeries", "VR"]
