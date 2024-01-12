from typing import Any

import pandas as pd
from torch.utils.data import DataLoader
from langchain.schema.retriever import BaseRetriever

from antimatter import errors
from antimatter.datatype.datatypes import Datatype
from antimatter.fieldtype.infer import infer_fieldtype


def infer_datatype(data: Any) -> Datatype:
    """
    Convenience handler for inferring the Datatype from an instance of a data
    object. Supported data types include string value, dictionary, list of
    dictionaries, pandas DataFrame, pytorch DataLoader, and langchain Retriever

    :param data: Instance of a data object to get the Datatype for.
    :return: The Datatype whose handler can work with the provided data instance.
    """
    if isinstance(data, dict):
        return Datatype.Dict
    elif isinstance(data, list):
        return Datatype.DictList
    elif isinstance(data, pd.DataFrame):
        return Datatype.PandasDataframe
    elif isinstance(data, DataLoader):
        return Datatype.PytorchDataLoader
    elif isinstance(data, BaseRetriever):
        return Datatype.LangchainRetriever
    else:
        try:
            # Use `infer_fieldtype` to check if it's a supported scalar value by 
            # inferring the FieldType. If not inferred, DataFormatError is raised.
            infer_fieldtype(data)
            return Datatype.Scalar
        except errors.DataFormatError:
            return Datatype.Unknown