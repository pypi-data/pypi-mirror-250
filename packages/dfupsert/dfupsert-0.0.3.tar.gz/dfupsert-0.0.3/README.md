
# dfupsert

## Overview
`dfupsert` is an efficient Python package designed for synchronizing pandas DataFrames with databases using upsert operations (insert or update). It works seamlessly with SQLAlchemy's well-defined table mappings, facilitating a smooth integration between pandas and various databases.

## Features
- **Streamlined Upsert Operations**: Facilitates upserts directly from pandas DataFrames to database tables using SQLAlchemy mappings.
- **Wide Database Compatibility**: Built on top of SQLAlchemy, it supports a diverse range of database systems.
- **Efficient Handling of Large DataSets**: Implements chunk-based data processing for optimized performance with large data volumes.
- **Customizable and User-Friendly**: Offers flexibility in connection types, table mappings, and chunk sizes to accommodate different use cases.

## Installation
Install `dfupsert` using pip:
```bash
pip install dfupsert
```

## Usage

```python
from dfupsert import upsert
from pandas import DataFrame
from sqlalchemy import create_engine
from your_application.model import YourTableClass  # Import your SQLAlchemy table class

# Example DataFrame
data = {'column1': [1, 2], 'column2': [3, 4]}
df = DataFrame(data)

# Establish a database connection using SQLAlchemy
engine = create_engine('your-database-connection-string')

# Upsert DataFrame into the database table
upsert(df=df, con=engine, table=YourTableClass, chunksize=1000)
```

## Requirements
- Python 3.x
- pandas
- SQLAlchemy

## Contributing
We welcome contributions to the `dfupsert`[github project](https://github.com/TommyLeung-gj/dfupsert).
## License
`dfupsert` is available under the MIT License. See the [MIT](https://choosealicense.com/licenses/mit/) or [LICENSE](LICENSE) file for more details.

## Support
For questions and support, please open an issue in the project's GitHub issue tracker.
