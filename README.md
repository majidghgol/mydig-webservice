# mydig-webservice

## Configuration File

### Fields

| Attribute     | Possible Values | Explanation  |
| ------------- |---------------| -----|
| name          | alphanumeric and underscore | the name of a field, cannot be changed |
| description   | text          |   A description of the field |
| screen_label  | text        | The text to display the field in DIG |
| screen_label_plural | text | Label when a field contains multiple values |
| icon | see below | The icon to decorate the field in DIG |
| color | see below | The color used to display the field in DIG |
| show_as_link | entity, text, no | Specifies the appearance of the field |
| show_in_facets | false, true | When true, the field appears in the facets section |
| show_in_result | title, description, detail, header, no | Where the field appears in the results page |
| show_in_search | false, true | When true, the field appears in the query form |
| glossaries | array of glossary names | The names of glossaries used to extrace values for the field |
| search_importance | Integer, range(1, 10) | High numbers make results matching in a field push documents up in the ranking |
| type | date, email, hyphenated, image, location, phone, string, username | affect appearance as well as search behavior |
| use_in_network_search | false, true | support network creation using the values from a field |
