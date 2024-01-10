# promsoft_weight_calc_interface
Interface for weight_calc microservice.

Usage:
```
from promsoft_weight_calc_interface import Entry, ComplEntry

my_entry = Entry(id=10004, cnt=2)
print(f"Entry as dict: {my_entry.dict()}")

my_compl_entry = ComplEntry(items=[Entry(id=10004, cnt=2), Entry(id=10005, cnt=2)], return_sizes_goods=True)
print(f"ComplEntry as dict: {my_compl_entry.dict()}")

```