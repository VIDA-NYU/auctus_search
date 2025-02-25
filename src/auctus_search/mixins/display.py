from typing import Dict, List, Optional, Union

import geopandas
import pandas
from IPython.display import display, HTML
from skrub import TableReport

from auctus_search.mixins.search import AuctusSearchMixin

from beartype import beartype


@beartype
class AuctusSearchDisplayMixin:
    @beartype
    def interactive_table_display(
        self: "AuctusSearchMixin",
        dataframe: Union[pandas.DataFrame, geopandas.GeoDataFrame],
        n_rows: int = 10,
        order_by: Optional[Union[str, List[str]]] = None,
        title: Optional[str] = "Table Report",
        column_filters: Optional[Dict[str, Dict[str, Union[str, List[str]]]]] = None,
        verbose: int = 1,
    ) -> None:
        if dataframe is not None and 0 < n_rows < len(dataframe):
            report = TableReport(
                dataframe=dataframe,
                n_rows=n_rows,
                order_by=order_by,
                title=title,
                column_filters=column_filters,
                verbose=verbose,
            )
            display(HTML(report.html()))
