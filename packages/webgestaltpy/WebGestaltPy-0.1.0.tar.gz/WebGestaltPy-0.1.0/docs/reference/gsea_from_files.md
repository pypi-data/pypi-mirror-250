# `gsea_from_files`
Run single-omic GSEA with files at provided paths.

## Parameters
- `gmt` - `String` of the path to the gmt file of interest
- `rank` - `String` of the path to the rank file of interest. Tab separated.

## Returns

Returns a [`PyResult<Vec<GSEAResultWrapper>>`] containing the GSEA results for every set.

## Panics

Panics if the GMT or the rank file is malformed or not at specified path.

