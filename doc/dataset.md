# row, col access

## Examples
   
   example | description
   --- | ---
   a['col']              | select col from a
   a['col1', 'col2', 'col3'] | select col1, col2, col3 from a
   a['col'][0]           | first row of select col from a
   a[col] | top        | top from a[col]
   a[col][10/31/2021]  | range for 10/31/2021 (all values that date)
   a[col][1d]          | past 1d from a[col]
   a[col='col', row='10/31/2021']  | alternate syntax
   a[1d]               | when using duration, time, or integers, row is assumed if not specified
   a[row=1d]           | formal syntax
   a{1d}               | maybe use {} for row-based query?
   a.col1              | alternate syntax
   a.col1[1d]          | good for single column
   a['col1', 'col2' > 0, 'col3']
   a[col1:, col2:, col3: ]  | uses table metadata and bypasses string lookups
   a[col1:, col2: > 10, col3: ]  | uses table metadata and bypasses string lookups

