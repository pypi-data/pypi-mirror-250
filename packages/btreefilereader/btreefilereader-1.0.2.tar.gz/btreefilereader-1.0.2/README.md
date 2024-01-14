# btreefilereader

BTreeFileReader is a Python library for reading txt files containing all Brazil financial market data. The txt files are available on the B3 S.A. website.

This README contains two main sections, the first dedicated to users and the second dedicated to developers who want to contribute to the project.


## Users:

### Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install btreefilereader.

```bash
pip install btreefilereader
```

### Usage

#### 1. Reading txt file
---

To reader the txt file just need to call the `file_reader_txt()` funcion and set the path appropriately.

  * **If just one file:**

    ```python
    from btreefilereader.core.reader_txt import file_reader_txt
    
    df = file_reader_txt('/path/to/file/file.txt')
    ```
  
  * **If more than one:**
  
    ```python
    from btreefilereader.core.reader_txt import file_reader_txt
    
    df = file_reader_txt('/path/to/file/*')
    ```
  
  The `df` object is a concatenated dataframe if there is more than one file to read.

#### 2. Filtering dataframe
---

To filter the dataframe by stock_id just need to set the dataframe and the stock id in a list object.

  *
    ```python
    from btreefilereader.ByBTree.filter_by import FilterDataframes
    
    filter_df = FilterDataframes()
    stocks = filter_df.by_stock_id(dataframe=df, stock_ids=['ABEV3', 'MODL11'])
    ```

For example, the `stocks` object receives a dictionary with the stocks as a keys. So, I can get the ABEV3 stock_id and get the open_price:

  *
    ```python
    abev3 = stocks.get('ABEV3')
    print(abev3.open_price)
    ```

The result is a list with the open prices from dataframe by stock id.

  **Terminal**
   ```bash
  [15.4, 16.01, 16.3, 16.57, 16.54, 16.2, 16.4, 17.02, 17.24, 17.57, 17.7, 17.68, 17.9, 17.93, 17.89, 17.6, 17.2, 17.1, 18.02, 17.97, 18.0, 17.54, 18.07, 18.38, 18.44, 18.19, 18.65, 18.25, 18.78, 18.86, 18.36, 18.58, 18.5, 18.19, 18.31, 18.24, 18.24, 18.3, 18.42, 18.43, 18.14, 17.14, 16.72, 16.37, 16.59, 16.69, 17.2, 16.98, 16.92, 16.66, 16.8, 17.27, 17.16, 16.89, 16.7, 16.65, 16.64, 16.8, 16.54, 16.87, 16.87, 17.0, 16.87, 16.95, 17.37, 17.44, 17.21, 17.7, 17.51, 17.06, 17.2, 17.38, 17.69, 17.2, 17.08, 17.56, 17.7, 17.63, 18.2, 18.3, 18.38, 18.26, 18.03, 17.7, 18.2, 17.8, 17.75, 17.5, 17.0, 17.06, 16.72, 16.5, 16.54, 16.59, 16.7, 17.17, 17.18, 17.26, 17.1, 17.29, 17.32, 17.22, 17.39, 17.6, 17.49, 17.39, 17.6, 17.7, 17.61, 17.68, 17.72, 17.7, 17.86, 17.61, 17.85, 18.05, 18.28, 18.44, 18.33, 18.19, 17.97, 18.16, 18.1, 17.8, 18.02, 18.95, 18.97, 19.04, 18.95, 19.07, 18.7, 18.4, 18.25, 18.14, 18.03, 18.23, 18.07, 18.0, 18.19, 19.0, 19.49, 19.8, 20.32, 20.31, 20.16, 20.41, 20.15, 20.17, 20.19, 20.05, 20.17, 19.77, 19.32, 19.3, 19.06, 18.92, 19.0, 19.05, 19.15, 18.92, 18.29, 18.46, 18.16, 18.01, 18.07, 18.62, 18.72, 18.34, 18.74, 18.9, 18.83, 18.79, 18.87, 18.9, 19.1, 19.35, 19.06, 19.03, 19.36, 19.48, 19.43, 19.24, 19.47, 19.25, 19.57, 19.56, 19.53, 19.3, 19.21, 18.8, 18.59, 19.21, 18.84, 18.7, 18.62, 18.54, 18.69, 18.72, 19.05, 18.94, 18.83, 18.6, 18.87, 18.75, 18.72, 17.9, 17.79, 17.53, 17.61, 17.47, 17.45, 17.35, 17.59, 17.6, 17.59, 17.45, 17.28, 17.4, 17.37, 17.37, 17.59, 17.61, 17.83, 18.02, 18.19, 18.11, 17.95, 17.96, 18.1, 18.05, 18.1, 18.0, 18.28, 18.21, 18.45, 18.39, 18.46, 18.47, 18.8, 19.02, 19.15, 18.96, 19.09, 18.62, 19.01, 18.96, 19.25, 19.2]
  ```

## For Devs:


## License

[MIT](https://choosealicense.com/licenses/mit/)
