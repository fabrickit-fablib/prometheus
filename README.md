# prometheus

## Overview
This is prometheus of fablib.

## Design
```
# exporter         scrap/1m, 7days  scrap/10m, 1mounth   scrap/1d, 1year, ...
|node-exporter|  -> |prometheus| --> |prometheus| -->
|node-exporter|  ->      ↑      ＼／      ↑
|node-exporter|  ->      ↓      ／＼      ↓
|node-exporter|  -> |prometheus| --> |prometheus| -->
```


prometheus


## License
This is licensed under the MIT. See the [LICENSE](./LICENSE) file for details.
