# Model Schema

## Packages

| Name | Description |
|:---- |:-----------|
| birdData | Reporting Rates of Australian Birds (v0.91, 2021-09-14) |

## Entities

| Name | Description | Package |
|:---- |:-----------|:-------|
| species | Reporting Counts and Rates by Species | birdData |

## Attributes

### Entity: birdData_species

Reporting Counts and Rates by Species

| Name | Label | Description | Data Type | ID Attribute |
|:---- |:-----|:-----------|:---------|:------------|
| birdID | BirdID | Species Identifier | string | True |
| commonName | Common Name | Commonly used name for a species | string | False |
| scientificName | Scientific Name | Scientific name for a species | string | False |
| count | Count | - | int | False |
| reportingRate | Reporting Rate | Percent reported | decimal | False |
