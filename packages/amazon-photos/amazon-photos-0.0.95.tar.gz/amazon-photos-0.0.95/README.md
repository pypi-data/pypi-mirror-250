# Amazon Photos API

## Table of Contents

<!-- TOC -->

* [Installation](#installation)
* [Setup](#setup)
* [Examples](#examples)
* [Search](#search)
* [Nodes](#nodes)
    * [Restrictions](#restrictions)
    * [Range Queries](#range-queries)
* [Notes](#notes)
    * [Known File Types](#known-file-types)
* [Custom Image Labeling (Optional)](#custom-image-labeling-optional)

<!-- TOC -->

> It is recommended to use this API in a [Jupyter Notebook](https://jupyter.org/install), as the results from most
> endpoints
> are a [DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html#pandas.DataFrame)
> which can be neatly displayed and efficiently manipulated with vectorized ops. This becomes
> increasingly important if you have "large" amounts of data (e.g. >1 million photos/videos).

## Installation

```bash
pip install amazon-photos -U
```

### Output Examples

`ap.db`

|   | dateTimeDigitized        | id                     | name              | ... | model             | apertureValue | focalLength | width | height |   size |
|--:|:-------------------------|:-----------------------|:------------------|:----|:------------------|:--------------|:------------|------:|-------:|-------:|
| 0 | 2019-07-06T18:22:00.000Z | HeMReF-vvJiTTkdPIeWuoP | 1694252973839.png | ... | iPhone XS         | 54823/32325   | 17/4        |  3024 |   4032 | 432777 |
| 1 | 2023-01-18T09:36:22.000Z | z_HiIvASAKqWmdrkjWiqMZ | 1692626817154.jpg | ... | iPhone XS         | 54823/32325   | 17/4        |  3024 |   4032 | 234257 |
| 2 | 2022-08-14T14:13:21.000Z | LKXEZbqoVrhrOYBezisGEQ | 1798219686789.jpg | ... | iPhone 11 Pro Max | 54823/32325   | 17/4        |  3024 |   4032 | 423987 |
| 3 | 2020-06-28T19:32:30.000Z | EPUeciHtfKkGiYkfUyEuMa | 1593482220567.jpg | ... | iPhone XS         | 54823/32325   | 17/4        |  3024 |   4032 | 898957 |
| 4 | 2021-07-07T17:12:55.000Z | fdfKzRJbEyoVeGcfCoJgE- | 1592299282720.png | ... | iPhone XR         | 54823/32325   | 17/4        |  3024 |   4032 | 432556 |
| 5 | 2021-08-18T18:32:41.000Z | crskJSmKPFRhxbpfkivyLm | 1592902159105.png | ... | iPhone XR         | 54823/32325   | 17/4        |  3024 |   4032 | 123123 |
| 6 | 2023-08-23T19:12:21.000Z | qkBFUlyIdkUwVVSaVWWKEF | 1598138358650.png | ... | iPhone 11         | 54823/32325   | 17/4        |  3024 |   4032 | 437887 |
| 7 | 2021-06-19T17:14:13.000Z | TXKMKC-mHvSUrtRfwmtyDe | 1622199863606.jpg | ... | iPhone 12 Pro     | 14447/10653   | 21/5        |  1536 |   2048 | 758432 |
| 8 | 2023-02-15T22:45:40.000Z | FRDvvjcZdpFWiwrIZfTNHO | 1581874518054.jpg | ... | iPhone 8 Plus     | 54823/32325   | 399/100     |  1348 |   2049 | 862883 |

`ap.print_tree()`

```text
~ 
├── Documents 
├── Pictures 
│   ├── iPhone 
│   └── Web 
│       ├── foo 
│       └── bar
├── Videos 
└── Backup 
    ├── LAPTOP-XYZ 
    │   └── Desktop 
    └── DESKTOP-IJK 
        └── Desktop
```

## Setup

> [Update] Jan 04 2024: To avoid confusion, setting env vars is no longer supported. One must pass cookies directly as
> shown below.

Log in to Amazon Photos and copy the following cookies:

- `session-id`
- `ubid`*
- `at`*

### Canada/Europe

where `xx` is the TLD (top-level domain)

- `ubid-acbxx`
- `at-acbxx`

### United States

- `ubid_main`
- `at_main`

E.g.

```python
from amazon_photos import AmazonPhotos

ap = AmazonPhotos(
    ## US
    # cookies={
    #     'ubid_main': ...,
    #     'at_main': ...,
    #     'session-id': ...,
    # },

    ## Canada
    # cookies={
    #     'ubid-acbca': ...,
    #     'at-acbca': ...,
    #     'session-id': ...,
    # }

    ## Italy
    # cookies={
    #     'ubid-acbit': ...,
    #     'at-acbit': ...,
    #     'session-id': ...,
    # }
)
```

## Examples

> A database named `ap.parquet` will be created during the initial setup. This is mainly used to reduce upload conflicts
> by checking your local file(s) md5 against the database before sending the request.

```python
from amazon_photos import AmazonPhotos

ap = AmazonPhotos(
    # see cookie examples above
    cookies={...},
    # optionally cache all intermediate JSON responses
    tmp='tmp',
    # pandas options
    dtype_backend='pyarrow',
    engine='pyarrow',
)

# get current usage stats
ap.usage()

# get entire Amazon Photos library
nodes = ap.query("type:(PHOTOS OR VIDEOS)")

# query Amazon Photos library with more filters applied
nodes = ap.query("type:(PHOTOS OR VIDEOS) AND things:(plant AND beach OR moon) AND timeYear:(2023) AND timeMonth:(8) AND timeDay:(14) AND location:(CAN#BC#Vancouver)")

# sample first 10 nodes
node_ids = nodes.id[:10]

# move a batch of images/videos to the trash bin
ap.trash(node_ids)

# get trash bin contents
ap.trashed()

# permanently delete a batch of images/videos
ap.delete(node_ids)

# restore a batch of images/videos from the trash bin
ap.restore(node_ids)

# upload media (preserves local directory structure and copies to Amazon Photos root directory)
ap.upload('path/to/files')

# download a batch of images/videos
ap.download(node_ids)

# convenience method to get photos only
ap.photos()

# convenience method to get videos only
ap.videos()

# get all identifiers calculated by Amazon.
ap.aggregations(category="all")

# get specific identifiers calculated by Amazon.
ap.aggregations(category="location")
```

## Search

*Undocumented API, current endpoints valid Dec 2023.*

For valid **location** and **people** IDs, see the results from the `aggregations()` method.

| name            | type | description                                                                                                                                                                                                                                               |
|:----------------|:-----|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ContentType     | str  | `"JSON"`                                                                                                                                                                                                                                                  |
| _               | int  | `1690059771064`                                                                                                                                                                                                                                           |
| asset           | str  | `"ALL"`<br/>`"MOBILE"`<br/>`"NONE`<br/>`"DESKTOP"`<br/><br/>default: `"ALL"`                                                                                                                                                                              |
| filters         | str  | `"type:(PHOTOS OR VIDEOS) AND things:(plant AND beach OR moon) AND timeYear:(2019) AND timeMonth:(7) AND location:(CAN#BC#Vancouver) AND people:(CyChdySYdfj7DHsjdSHdy)"`<br/><br/>default: `"type:(PHOTOS OR VIDEOS)"`                                   |
| groupByForTime  | str  | `"day"`<br/>`"month"`<br/>`"year"`                                                                                                                                                                                                                        |
| limit           | int  | `200`                                                                                                                                                                                                                                                     |
| lowResThumbnail | str  | `"true"`<br/>`"false"`<br/><br/>default: `"true"`                                                                                                                                                                                                         |
| resourceVersion | str  | `"V2"`                                                                                                                                                                                                                                                    |
| searchContext   | str  | `"customer"`<br/>`"all"`<br/>`"unknown"`<br/>`"family"`<br/>`"groups"`<br/><br/>default: `"customer"`                                                                                                                                                     |
| sort            | str  | `"['contentProperties.contentDate DESC']"`<br/>`"['contentProperties.contentDate ASC']"`<br/>`"['createdDate DESC']"`<br/>`"['createdDate ASC']"`<br/>`"['name DESC']"`<br/>`"['name ASC']"`<br/><br/>default: `"['contentProperties.contentDate DESC']"` |
| tempLink        | str  | `"false"`<br/>`"true"`<br/><br/>default: `"false"`                                                                                                                                                                                                        |             |

## Nodes

*Docs last updated in 2015*

| FieldName                     | FieldType                | Sort Allowed | Notes                                                                                                                                                                                                                                       |
|-------------------------------|--------------------------|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| isRoot                        | Boolean                  |              | Only lower case `"true"` is supported.                                                                                                                                                                                                      |
| name                          | String                   | Yes          | This field does an exact match on the name and prefix query. Consider `node1{ "name" : "sample" }` `node2 { "name" : "sample1" }` Query filter<br>`name:sample` will return node1<br>`name:sample*` will return node1 and node2             |
| kind                          | String                   | Yes          | To search for all the nodes which contains kind as FILE `kind:FILE`                                                                                                                                                                         |
| modifiedDate                  | Date (in ISO8601 Format) | Yes          | To Search for all the nodes which has modified from time `modifiedDate:{"2014-12-31T23:59:59.000Z" TO *]`                                                                                                                                   |
| createdDate                   | Date (in ISO8601 Format) | Yes          | To Search for all the nodes created on  `createdDate:2014-12-31T23:59:59.000Z`                                                                                                                                                              |
| labels                        | String Array             |              | Only Equality can be tested with arrays.<br>if labels contains `["name", "test", "sample"]`.<br>Label can be searched for name or combination of values.<br>To get all the labels which contain name and test<br>`labels: (name AND test)`  |
| description                   | String                   |              | To Search all the nodes for description with value 'test'<br>`description:test`                                                                                                                                                             |
| parents                       | String Array             |              | Only Equality can be tested with arrays.<br>if parents contains `["id1", "id2", "id3"]`.<br>Parent can be searched for name or combination of values.<br>To get all the parents which contains id1 and id2<br>`parents:id1 AND parents:id2` |
| status                        | String                   | Yes          | For searching nodes with AVAILABLE status.<br>`status:AVAILABLE`                                                                                                                                                                            |
| contentProperties.size        | Long                     | Yes          |                                                                                                                                                                                                                                             |
| contentProperties.contentType | String                   | Yes          | If prefix query, only the major content-type (e.g. `image*`, `video*`, etc.) is supported as a prefix.                                                                                                                                      |
| contentProperties.md5         | String                   |              |                                                                                                                                                                                                                                             |
| contentProperties.contentDate | Date (in ISO8601 Format) | Yes          | RangeQueries and equals queries can be used with this field                                                                                                                                                                                 |
| contentProperties.extension   | String                   | Yes          |                                                                                                                                                                                                                                             |

### Restrictions

> Max # of Filter Parameters Allowed is 8

| Filter Type | Filters                                                                               |
|:------------|:--------------------------------------------------------------------------------------|
| Equality    | createdDate, description, isRoot, kind, labels, modifiedDate, name, parentIds, status |
| Range       | contentProperties.contentDate, createdDate, modifiedDate                              |
| Prefix      | contentProperties.contentType, name                                                   |

### Range Queries

| Operation            | Syntax                                                           |
|----------------------|------------------------------------------------------------------|
| GreaterThan          | `{"valueToBeTested" TO *}`                                       |
| GreaterThan or Equal | `["ValueToBeTested" TO *]`                                       |
| LessThan             | `{* TO "ValueToBeTested"}`                                       |
| LessThan or Equal    | `{* TO "ValueToBeTested"]`                                       |
| Between              | `["ValueToBeTested_LowerBound" TO "ValueToBeTested_UpperBound"]` |

## Notes

#### `https://www.amazon.ca/drive/v1/batchLink`

- This endpoint is called when downloading a batch of photos/videos in the web interface. It then returns a URL to
  download a zip file, then makes a request to that url to download the content.
  When making a request to download data for 1200 nodes (max batch size), it turns out to be much slower (~2.5 minutes)
  than asynchronously downloading 1200 photos/videos individually (~1 minute).

### Known File Types

| Extension | Category |
|-----------|----------|
| \.pdf     | pdf      |
| \.doc     | doc      |
| \.docx    | doc      |
| \.docm    | doc      |
| \.dot     | doc      |
| \.dotx    | doc      |
| \.dotm    | doc      |
| \.asd     | doc      |
| \.cnv     | doc      |
| \.mp3     | mp3      |
| \.m4a     | mp3      |
| \.m4b     | mp3      |
| \.m4p     | mp3      |
| \.wav     | mp3      |
| \.aac     | mp3      |
| \.aif     | mp3      |
| \.mpa     | mp3      |
| \.wma     | mp3      |
| \.flac    | mp3      |
| \.mid     | mp3      |
| \.ogg     | mp3      |
| \.xls     | xls      |
| \.xlm     | xls      |
| \.xll     | xls      |
| \.xlc     | xls      |
| \.xar     | xls      |
| \.xla     | xls      |
| \.xlb     | xls      |
| \.xlsb    | xls      |
| \.xlsm    | xls      |
| \.xlsx    | xls      |
| \.xlt     | xls      |
| \.xltm    | xls      |
| \.xltx    | xls      |
| \.xlw     | xls      |
| \.ppt     | ppt      |
| \.pptx    | ppt      |
| \.ppa     | ppt      |
| \.ppam    | ppt      |
| \.pptm    | ppt      |
| \.pps     | ppt      |
| \.ppsm    | ppt      |
| \.ppsx    | ppt      |
| \.pot     | ppt      |
| \.potm    | ppt      |
| \.potx    | ppt      |
| \.sldm    | ppt      |
| \.sldx    | ppt      |
| \.txt     | txt      |
| \.text    | txt      |
| \.rtf     | txt      |
| \.xml     | markup   |
| \.htm     | markup   |
| \.html    | markup   |
| \.zip     | zip      |
| \.rar     | zip      |
| \.7z      | zip      |
| \.jpg     | img      |
| \.jpeg    | img      |
| \.png     | img      |
| \.bmp     | img      |
| \.gif     | img      |
| \.tif     | img      |
| \.svg     | img      |
| \.mp4     | vid      |
| \.m4v     | vid      |
| \.qt      | vid      |
| \.mov     | vid      |
| \.mpg     | vid      |
| \.mpeg    | vid      |
| \.3g2     | vid      |
| \.3gp     | vid      |
| \.flv     | vid      |
| \.f4v     | vid      |
| \.asf     | vid      |
| \.avi     | vid      |
| \.wmv     | vid      |
| \.swf     | exe      |
| \.exe     | exe      |
| \.dll     | exe      |
| \.ax      | exe      |
| \.ocx     | exe      |
| \.rpm     | exe      |

## Custom Image Labeling (Optional)

Categorize your images into folders using computer vision models.

```bash
pip install amazon-photos[extras] -U
```

See the [Model List](https://www.hobenshield.com/stats/bench/index.html) for a list of all available models.

### Sample Models

**Very Large**

```
eva02_base_patch14_448.mim_in22k_ft_in22k_in1k
```

**Large**

```
eva02_large_patch14_448.mim_m38m_ft_in22k_in1k
```

**Medium**

```
eva02_small_patch14_336.mim_in22k_ft_in1k
vit_base_patch16_clip_384.laion2b_ft_in12k_in1k
vit_base_patch16_clip_384.openai_ft_in12k_in1k
caformer_m36.sail_in22k_ft_in1k_384
```

**Small**

```
eva02_tiny_patch14_336.mim_in22k_ft_in1k
tiny_vit_5m_224.dist_in22k_ft_in1k
edgenext_small.usi_in1k
xcit_tiny_12_p8_384.fb_dist_in1k
```

```python
run(
    'eva02_base_patch14_448.mim_in22k_ft_in22k_in1k',
    path_in='images',
    path_out='labeled',
    thresh=0.0,  # threshold for predictions, 0.9 means you want very confident predictions only
    topk=5,
    # window of predictions to check if using exclude or restrict, if set to 1, only the top prediction will be checked
    exclude=lambda x: re.search('boat|ocean', x, flags=re.I),
    # function to exclude classification of these predicted labels
    restrict=lambda x: re.search('sand|beach|sunset', x, flags=re.I),
    # function to restrict classification to only these predicted labels
    dataloader_options={
        'batch_size': 4,  # *** adjust ***
        'shuffle': False,
        'num_workers': psutil.cpu_count(logical=False),  # *** adjust ***
        'pin_memory': True,
    },
    accumulate=False,
    # accumulate results in path_out, if False, everything in path_out will be deleted before running again
    device='cuda',
    naming_style='name',  # use human-readable label names, optionally use the label index or synset
    debug=0,
)
```
