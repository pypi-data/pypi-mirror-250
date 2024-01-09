import io
import os
from typing import Optional, Union

import pandas as pd
from pandas import DataFrame

from lumipy.lumiflex import DType
from lumipy.provider.base_provider import BaseProvider
from lumipy.provider.context import Context
from lumipy.provider.metadata import ColumnMeta, ParamMeta
from ..common import infer_datatype, df_summary_str, clean_colname


class PandasProvider(BaseProvider):
    """Provides rows of data from a Pandas DataFrame.

    """

    def __init__(
            self,
            source: Union[DataFrame, str, os.PathLike, io.IOBase],
            name: str,
            name_root: Optional[str] = 'Pandas',
            description: Optional[str] = None,
            **kwargs
    ):
        """Constructor of the PandasProvider class.

        Args:
            source (Union[DataFrame, str, os.PathLike, io.IOBase]): the dataframe or pd.read_csv-compatible source to
            serve data from. Datetime-valued columns must be timezone-aware.
            See https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
            name (str): name to give the provider. The name will be appended to name_root ('Pandas') by default to
            create the full name 'Pandas.(name)' unless the name root is overridden by supplying a value.
            name_root (Optional[str]): optional name_root value. Will override 'Pandas' if not supplied.
            description (Optional[str]): optional description string of the provider.

        Keyword Args:
            keyword args are passed down to pandas read_csv if source is not a DataFrame

        """

        if name_root:
            name = f'{name_root}.{name}'

        if isinstance(source, DataFrame):
            df = source
        else:
            df = pd.read_csv(source, **kwargs)

        self.df = df.rename({c: clean_colname(c) for c in df.columns}, axis=1)

        cols = [ColumnMeta(c, infer_datatype(self.df[c])) for c in self.df.columns]
        params = [ParamMeta(
            "UsePandasFilter",
            DType.Boolean,
            "Whether to apply a filter within the pandas provider.",
            default_value=True
        )]

        if description is None:
            description = 'A provider that serves data from a pandas dataframe.'

        super().__init__(name, cols, params, description=description + df_summary_str(self.df))

    def get_data(self, context: Context) -> DataFrame:
        if context.get('UsePandasFilter'):
            return context.pandas.apply(self.df)
        return self.df
