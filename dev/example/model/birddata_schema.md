# Model Schema

## Packages

| Name | Description |
|:---- |:-----------|
| data | Parent Package Test (v0.0.9000, 2021-09-20) |

## Entities

| Name | Description | Package |
|:---- |:-----------|:-------|
| species | Reporting Counts and Rates by Species | data |
| states | Australian States and Codes | data |

## Attributes

### Entity: data_species

Reporting Counts and Rates by Species

| Name | Label | Description | Data Type | ID Attribute |
|:---- |:-----|:-----------|:---------|:------------|
| birdID | BirdID | Species Identifier | string | True |
| commonName | Common Name | Commonly used name for a species | string | False |
| scientificName | Scientific Name | Scientific name for a species | string | False |
| count | Count | - | int | False |
| reportingRate | Reporting Rate | Percent reported | decimal | False |

### Entity: data_states

Australian States and Codes

| Name | Label | Description | Data Type | ID Attribute |
|:---- |:-----|:-----------|:---------|:------------|
| code | - | - | string | True |
| category | - | - | string | False |
| name | - | - | string | False |
