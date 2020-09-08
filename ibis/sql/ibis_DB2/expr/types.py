import ibis.expr.types as tp


class CLOBValue(tp.StringValue):
    pass  # noqa: E701,E302


class CLOBScalar(tp.StringScalar, CLOBValue):
    pass  # noqa: E701,E302


class CLOBColumn(tp.StringColumn, CLOBValue):
    pass  # noqa: E701,E302


class BLOBValue(tp.StringValue):
    pass  # noqa: E701,E302


class BLOBScalar(tp.StringScalar, BLOBValue):
    pass  # noqa: E701,E302


class BLOBColumn(tp.StringColumn, BLOBValue):
    pass  # noqa: E701,E302


class DBCLOBValue(tp.BinaryValue):
    pass  # noqa: E701,E302


class DBCLOBScalar(tp.BinaryScalar, DBCLOBValue):
    pass  # noqa: E701,E302


class DBCLOBColumn(tp.BinaryColumn, DBCLOBValue):
    pass  # noqa: E701,E302


# --------------Graphic-----------------------------


class GRAPHICValue(tp.StringValue):
    pass  # noqa: E701,E302


class GRAPHICScalar(tp.StringScalar, GRAPHICValue):
    pass  # noqa: E701,E302


class GRAPHICColumn(tp.StringColumn, GRAPHICValue):
    pass  # noqa: E701,E302


# --------------Vargraphic-----------------------------


class VARGRAPHICValue(tp.StringValue):
    pass  # noqa: E701,E302


class VARGRAPHICScalar(tp.StringScalar, VARGRAPHICValue):
    pass  # noqa: E701,E302


class VARGRAPHICColumn(tp.StringColumn, VARGRAPHICValue):
    pass  # noqa: E701,E302


# ---------------Binary Integer----------------------------


class SMALLINTValue(tp.NumericValue):
    pass  # noqa: E701,E302


class SMALLINTScalar(tp.NumericScalar, SMALLINTValue):
    pass  # noqa: E701,E302


class SMALLINTColumn(tp.NumericColumn, SMALLINTValue):
    pass  # noqa: E701,E302


class INTEGERValue(tp.NumericValue):
    pass  # noqa: E701,E302


class INTEGERScalar(tp.NumericScalar, INTEGERValue):
    pass  # noqa: E701,E302


class INTEGERColumn(tp.NumericColumn, INTEGERValue):
    pass  # noqa: E701,E302


class BIGINTValue(tp.NumericValue):
    pass  # noqa: E701,E302


class BIGINTScalar(tp.NumericScalar, BIGINTValue):
    pass  # noqa: E701,E302


class BIGINTColumn(tp.NumericColumn, BIGINTValue):
    pass  # noqa: E701,E302


# -------------Floating points------------------------------


class REALValue(tp.NumericValue):
    pass  # noqa: E701,E302


class REALScalar(tp.NumericScalar, REALValue):
    pass  # noqa: E701,E302


class REALColumn(tp.NumericColumn, REALValue):
    pass  # noqa: E701,E302
