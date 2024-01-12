# `ora_from_files`
Run a single-omic ORA with files at the provided paths.

## Parameters
- `gmt` - `String` of the path to the gmt file of interest
- `rank` - `String` of the path to the rank file of interest. Tab separated.

## Returns

Returns a [`PyResult<Vec<GSEAResultWrapper>>`] containing the GSEA results for every set.

## Panics

Panics if the any file is malformed or not at specified path.

## Example

```python
import webgestaltpy

res = webgestaltpy.ora_from_files("kegg.gmt", "gene_list.txt", "reference.txt")

print(res[0:2])
```

**Output**

```
[
    {
      'set': 'hsa00010',
      'p': 0.7560574551180973,
      'fdr': 1,
      'overlap': 2,
      'expected': 2.6840874707743088,
      'enrichment_ratio': 0.7451321992211519
    },
    {
      'set': 'hsa00020',
      'p': 0.7019892669020903,
      'fdr': 0.9981116297866582,
      'overlap': 1,
      'expected': 1.1841562371063128,
      'enrichment_ratio': 0.8444831591173054
    }
  ]
```


