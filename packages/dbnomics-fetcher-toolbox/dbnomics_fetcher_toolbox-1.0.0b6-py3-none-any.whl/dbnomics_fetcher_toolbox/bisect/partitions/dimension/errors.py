from dbnomics_fetcher_toolbox.bisect.errors import BisectionError


class BisectDimensionNotFound(BisectionError):
    def __init__(self, code: "BisectDimensionCode", *, dimensions: list["BisectDimension"]) -> None:
        msg = f"Dimension {code!r} not found"
        super().__init__(msg=msg)
        self.code = code
        self.dimensions = dimensions


class NoBisectDimension(BisectionError):
    def __init__(self) -> None:
        msg = "Can't bisect an empty dimension list"
        super().__init__(msg=msg)


class NoBisectableDimension(BisectionError):
    def __init__(self, *, dimensions: list["BisectDimension"]) -> None:
        msg = "All dimensions have one value, can't bisect"
        super().__init__(msg=msg)
        self.dimensions = dimensions
