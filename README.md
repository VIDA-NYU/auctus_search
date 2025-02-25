<div align="center">
   <h1>Auctus Search</h1>
   <h3>Discover and Load Datasets in your Notebook</h3>
    <p><i>with ease-of-use</i></p>
   <p>
      <img src="https://img.shields.io/static/v1?label=Python&message=3.9%2B&color=3776AB&style=for-the-badge&logo=python&logoColor=white" alt="Python 3.9+">
      <img src="https://img.shields.io/badge/Skrub-FF9800?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Skrub">
      <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
      <img src="https://img.shields.io/badge/Version-0.1.0-red?style=for-the-badge" alt="Version">
      <img src="https://img.shields.io/badge/status-unstable-orange?style=for-the-badge" alt="Unstable">
   </p>
   <p>Search for datasets using Auctus and integrate them seamlessly into your Notebook exploration!</p>
</div>

---

![Auctus Search Cover](public/resources/auctus_search_main_cover.png)

> [!NOTE]
> [Marimo](https://github.com/marimo-team/marimo) is not yet supported/nor-tested but is in discussion for future
> releases.

## 🌆 Auctus Search –– In a Nutshell

`Auctus Search` is a lightweight library that connects to the
[Auctus](https://github.com/VIDA-NYU/auctus) [API](https://docs.auctus.vida-nyu.org/rest/),
allowing easy **search**, **filtering**, and **loading** of datasets.

It offers an easy way to find datasets `.search_datasets(search_query="Taxis")`, 
preview them interactively `.display()`, optionally filter them `.with_types(["spatial"])` or `.with_score_greater_than(20)` to name a few,
and integrate them into your notebook workflow
as `pandas.DataFrame` or `geopandas.GeoDataFrame` objects, `.load_selected_dataset()`.

For developers, it also allows you to integrate it all into your project, have a look at the `Auctus Search Mixin`
in the [OSMNxMapping](https://github.com/VIDA-NYU/OSMNXMapping) – It is fully integrated for the user to benefits from
the `Auctus Search` capabilities and most importantly the great `Auctus API` as a whole.

> [!WARNING]
> This library is currently in an **unstable** state and under active development.
> Expect changes and new features very frequently.


See further notebook-based examples in the `examples/` directory. 📓

---

## 🥐 Installation

We *highly* recommend using `uv` for installation from source to avoid the hassle of `Conda` or other package managers.
It is also the fastest known to date on the OSS market and manages dependencies seamlessly without manual environment
activation (Biggest flex!). If you do not want to use `uv`, there are no issues, but we will cover it in the upcoming
section; but in the *incoming* documentation.

First, ensure `uv` is installed on your machine by
following [these instructions](https://docs.astral.sh/uv/getting-started/installation/).

### Prerequisites

- Install `uv` as described above.
- Clone `Auctus Search` (required for alpha development) into your desired directory. Use:
  ```bash
  git clone git@github.com:VIDA-NYU/auctus_search.git
  ```
  This step ensures `pyproject.toml` builds `auctus_search` from source during installation, though we plan for
  `auctus_search` to become a PyPi package (`uv add auctus_search` or `pip install auctus_search`) in future releases.

### Steps

1. Jump into the `Auctus Search` repository:
   ```bash
   cd auctus_search
   ```
2. Lock and sync dependencies with `uv`:
   ```bash
   uv lock
   uv sync
   ```
3. (Recommended) Install Jupyter extensions for interactive features requiring Jupyter widgets:
   ```bash
   uv run jupyter labextension install @jupyter-widgets/jupyterlab-manager
   ```
4. Launch Jupyter Lab to explore `Auctus Search` (Way faster than running Jupyter without `uv`):
   ```bash
   uv run --with jupyter jupyter lab
   ```

> [!NOTE]  
> Future versions will simplify this process: `auctus_search` will move to PyPi, removing the need for manual cloning,
> and Jupyter extensions will auto-install via `pyproject.toml` configuration.

Voila 🥐! You’re all set to explore `Auctus Search` in Jupyter Lab.

---

# Getting Started!

Below is a concise, step-by-step example of how to use the `Auctus Search` library in a Jupyter notebook.

### **Cell 1: Import the Library**

```python
from auctus_search import

AuctusSearch  # This imports the main `AuctusSearch` class, which provides all the functionality we'll use.
```

### **Cell 2: Initialise An AuctusSearch Instance**

```python
search = AuctusSearch()  # Create an instance of `AuctusSearch` to start searching for datasets. This object will handle all interactions with the Auctus API and dataset management.
```

### **Cell 3: Search for Datasets**

```python
collection = search.search_datasets(search_query="Taxis", display_initial_results=True)

# Search for datasets related to "Taxis" (very broad right!). The `search_datasets` method queries the Auctus API and returns a
# `DatasetCollection`. Setting `display_initial_results=True` shows the initial results interactively in the notebook,
# allowing you to see available datasets right away.

# More parameters such as page and size for pagination are available, but we'll stick to the defaults for now. Readers are instructed to check the API below for more details.
```

### **Cell 4: Filter the Dataset Collection**

```python
filtered_collection = (
    collection
    .with_types(
        ["spatial"])  # Refine the search results to only include datasets that at least have a spatial component.
    .with_number_of_rows_greater_than(100000)
    # Refine further to – after the with_types– only include datasets with more than 100,000 rows.
)
```

### **Cell 5: Display Filtered Datasets Interactively**

```python
filtered_collection.display()

# Display the filtered datasets in an interactive grid. Each dataset is shown as a card with details like name, source,
# and size. You can click "Select This Dataset" on any card to choose one for further use.
```

### **Cell 6: Load the Selected Dataset**

```python
dataset = search.load_selected_dataset()

# After selecting a dataset in the previous step, this loads it into memory as a `pandas.DataFrame` (or
# `geopandas.GeoDataFrame` if spatial). By default, it also displays an interactive table preview of the dataset.
```

Are you coping with the idea of Auctus Search a lightweight jupyter-focussed wrapper around the Auctus API?

Want more filtering actions? Have more advanced usage? Check the API below for more details on how to filter datasets.

Enjoy! 🥐

---

## 🗺️ Roadmap / Future Work

1) From labs to more general communities, we want to advance `Auctus Search` by attaining large unit-test coverage,
   integrating routines via `G.Actions`, and producing thorough documentation for users all around.

2) It would be very interesting to explore interfacing the whole management of the `Auctus API` so that we could add any alternative to
   Auctus to have a pretty large library being able to target multiple dataset collection APIs. Such as: https://lil.law.harvard.edu/blog/2025/02/06/announcing-data-gov-archive/

We are also looking forward to seeing more examples in the `examples/` directory; Yet in the meantime,
we are happy to welcome you to contribute to the library 🎄

---

## 🌁 API

The `Auctus Search` API is split into two main parts: the `AuctusSearch` class for searching and loading, and the
`AuctusDatasetCollection` class for filtering and displaying results. Here's the rundown:

### AuctusSearch

Your main entry point for searching and loading datasets.

<details>
<summary><code>search_datasets(search_query, page=1, size=10, display_initial_results=False)</code></summary>

- **Purpose**: Searches the Auctus API for datasets matching your query.
- **Parameters**:
    - `search_query` (str or list): Search term(s) (e.g., "Taxis" or ["Taxis", "NYC"] –– Could be "Taxis NYC" too).
    - `page` (int, default=1): Page number of results. It is used for pagination. It also depends on the number of
      results per page and parameter `size`. If you put a high number into `size`, you will have fewer pages, and
      vice-versa, if you have a low number in `size`, you will have more pages.
    - `size` (int, default=10): Number of results per page.
    - `display_initial_results` (bool, default=False): If True, shows initial results in a Jupyter notebook cell.
- **Returns**: An `AuctusDatasetCollection` object containing the search results.
- **Example**:
  ```python
  from auctus_search import AuctusSearch
  search = AuctusSearch()
  collection = search.search_datasets(search_query="Taxis", page=1, size=100)  # This will show all Taxis data Auctus has without pagination but could take more time / while having a long scroll. If you do not like that, lower the number and play with the page parameter.
  ```

</details>

<details>
<summary><code>load_selected_dataset(display_table=True)</code></summary>

- **Purpose**: Downloads and loads the dataset you selected from the collection (i.e., after having clicked on
  `Select This Dataset`).
- **Parameters**:
    - `display_table` (bool, default=True): If True, shows a preview table using `Skrub`.
- **Returns**: A `pandas.DataFrame` or `geopandas.GeoDataFrame` (currently supports CSV; more formats coming soon!).
- **Raises**: `ValueError` if no dataset is selected.
- **Example**:
  ```python
  dataset = search.load_selected_dataset()  # Make sure to have selected a dataset before running this line otherwise it'll simply raise a ValueError.
  ```

</details>

<details>
<summary><code>interactive_table_display(dataframe, n_rows=10, order_by=None, title="Table Report", column_filters=None, verbose=1)</code></summary>

- **Purpose**: Displays an interactive table of your loaded dataset in Jupyter.
- **Parameters**:
    - `dataframe` (pandas.DataFrame or geopandas.GeoDataFrame): The dataset to display.
    - `n_rows` (int, default=10): Number of rows to show.
    - `order_by` (str or list, optional): Column(s) to sort by.
    - `title` (str, optional): Table title.
    - `column_filters` (dict, optional): Filters for columns (e.g., `{"city": {"eq": "NYC"}}`).
    - `verbose` (int, default=1): Verbosity level.
- **Returns**: Displays the table (no return value).
- **Example**:
  ```python
  search.interactive_table_display(dataset, n_rows=5, title="Taxis Data")
  ```

</details>

---

### AuctusDatasetCollection

A helper class to filter and explore the datasets returned from a search. It works by chaining filter methods together,
which is a very nice way to filter while in a Jupyter notebook rather than using only parameters, which could get very
messy 🙃.

<details>
<summary>Filtering Methods</summary>

- **`with_types(types)`**
    - **Purpose**: Filters datasets by dataset types. Available types are "spatial", "temporal", "numerical", "
      categorical".
    - **Parameters**:
        - `types` (list): List of desired types, e.g., `["spatial", "temporal"]`.
    - **Returns**: A new `AuctusDatasetCollection`.
    - **Example**:
      ```python
      filtered = collection.with_types(["spatial"])
      ```

- **`with_number_of_rows_greater_than(min_rows)`**
    - **Purpose**: Keeps datasets with more than `min_rows` rows.
    - **Parameters**:
        - `min_rows` (int): Minimum number of rows.
    - **Returns**: A new `AuctusDatasetCollection`.
    - **Example**:
      ```python
      filtered = collection.with_number_of_rows_greater_than(500)
      ```

- **`with_number_of_rows_less_than(max_rows)`**
    - **Purpose**: Keeps datasets with fewer than `max_rows` rows.
    - **Parameters**:
        - `max_rows` (int): Maximum number of rows.
    - **Returns**: A new `AuctusDatasetCollection`.

- **`with_number_of_rows_between(min_rows, max_rows)`**
    - **Purpose**: Filters datasets with rows between `min_rows` and `max_rows`.
    - **Parameters**:
        - `min_rows` (int): Minimum number of rows.
        - `max_rows` (int): Maximum number of rows.
    - **Returns**: A new `AuctusDatasetCollection`.

- **`with_number_of_columns_greater_than(min_columns)`**
    - **Purpose**: Keeps datasets with more than `min_columns` columns.
    - **Parameters**:
        - `min_columns` (int): Minimum number of columns.
    - **Returns**: A new `AuctusDatasetCollection`.

- **`with_number_of_columns_less_than(max_columns)`**
    - **Purpose**: Keeps datasets with fewer than `max_columns` columns.
    - **Parameters**:
        - `max_columns` (int): Maximum number of columns.
    - **Returns**: A new `AuctusDatasetCollection`.

- **`with_number_of_columns_between(min_columns, max_columns)`**
    - **Purpose**: Filters datasets with columns between `min_columns` and `max_columns`.
    - **Parameters**:
        - `min_columns` (int): Minimum number of columns.
        - `max_columns` (int): Maximum number of columns.
    - **Returns**: A new `AuctusDatasetCollection`.

- **`with_score_greater_than(min_score)`**
    - **Purpose**: Keeps datasets with a relevancy score above `min_score`.
    - **Parameters**:
        - `min_score` (int or float): Minimum score.
    - **Returns**: A new `AuctusDatasetCollection`.
    - **Example**:
      ```python
      filtered = collection.with_score_greater_than(20)
      ```

- **`with_score_less_than(max_score)`**
    - **Purpose**: Keeps datasets with a score below `max_score`. There is not much value to this method as the score is
      a relevancy score, and higher is better; yet it offers flexibility.
    - **Parameters**:
        - `max_score` (int or float): Maximum score.
    - **Returns**: A new `AuctusDatasetCollection`.

- **`with_score_between(min_score, max_score)`**
    - **Purpose**: Filters datasets with scores between `min_score` and `max_score`.
    - **Parameters**:
        - `min_score` (int or float): Minimum score.
        - `max_score` (int or float): Maximum score.
    - **Returns**: A new `AuctusDatasetCollection`.

</details>

<details>
<summary><code>preview()</code></summary>

- **Purpose**: Prints a summary of the dataset collection (search query, filters, and count).
- **Returns**: None (prints to console).
- **Example**:
  ```python
  filtered.preview()
  ```

</details>

<details>
<summary><code>display()</code></summary>

- **Purpose**: Shows an interactive grid of dataset cards in Jupyter for you to select one.
- **Returns**: None (displays in notebook).
- **Example**:
  ```python
  filtered.display()
  ```

</details>


---

## 📓 Examples

Check out the `examples/` directory in the [Auctus Search repo](https://github.com/VIDA-NYU/auctus_search) for more
detailed Jupyter notebook examples.

---

## Licence

`Auctus Search` is released under the [MIT Licence](./LICENCE).
