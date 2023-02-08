# Model Schema

## Packages

| Name | Description | Parent |
|:---- |:-----------|:------|
| birdData | Reporting Rates of Australian Bird Species (v1.0.0, 2021-11-12) | - |

## Entities

| Name | Description | Package |
|:---- |:-----------|:-------|
| template | lookup table attribute template | birdData |
| wings | reference for wing characteristics | birdData |
| colors | reference for colors and patterns | birdData |
| conservationStatus | reference for conservation status | birdData |
| states | Australian States and Territories | birdData |
| species | Reporting Counts and Rates by Species | birdData |

## Attributes

### Entity: birdData_template

lookup table attribute template

| Name | Label | Description | Data Type |
|:---- |:-----|:-----------|:---------|
| value&#8251; | - | The information contained in a data field. It may represent a numeric quantity, a textual characterization, a date or time measurement, or some other state, depending on the nature of the attribute. | string |
| description | - | A written or verbal account, representation, statement, or explanation of something | text |
| codesystem | - | A systematized collection of concepts that define corresponding codes. | string |
| code | - | A symbol or combination of symbols which is assigned to the members of a collection. | string |
| iri | - | A unique symbol that establishes identity of the resource. | hyperlink |

### Entity: birdData_states

Australian States and Territories

| Name | Label | Description | Data Type |
|:---- |:-----|:-----------|:---------|
| code&#8251; | code | state code | string |
| category | category | state type (state or territory) | string |
| name | name | state name | string |

### Entity: birdData_species

Reporting Counts and Rates by Species

| Name | Label | Description | Data Type |
|:---- |:-----|:-----------|:---------|
| birdID&#8251; | BirdID | Species Identifier | string |
| commonName | Common Name | Commonly used name for a species | string |
| scientificName | Scientific Name | Scientific name for a species | string |
| count | Count | - | int |
| reportingRate | Reporting Rate | Percent reported | decimal |
| primaryReportingTerritories | Primary Reporting Territories | - | mref |

Note: The symbol &#8251; denotes attributes that are primary keys

