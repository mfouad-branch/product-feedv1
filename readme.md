# Link Creator 

### Dependencies
1. Python 3.5+ 

### How to run:
1. fill out variables in the settings.json file
2. add a csv to parse in the input folder `/input`
3. excute script `python main.py` | `./main.py` etc. 

### How it works:

Take the values from the old `LINK_COL_NAME_TO_REPLACE` column name and replace it with a branch link. 

To build the branch link we will use the `active_template` (which translates to a file name in the `templates` folder 
**without the file extension**). These values will be appended to the link as link data/query params

#### Files

`settings.json` should contain these variables:

```javascript

{
  "input_folder":"input", // folder where the input file lives (relative path) (should not need to be changed)
  "templates_folder":"templates", //folder where default templates live (should not need to be changed)
  "input_file": "input.csv", // csv file to parse
  "output_file": "output.txt", // the output file
  "csv_deliminator": ",", // what to delimatine csv on 
  "base_url": "", // base url for all links created 
  "active_template": "facebook_app_only" // name of the template to apply from the template folder


}
```

`input_file` The file as described variable of `settings.json` 

```csv
base_url,android_passive_deepview,og:imagename,platform,~campaign
company.app.link/30?,TRUE,helloworld.png,facebook cross platform,test_campaign
```


current valid template names 
```
1. facebook_app_only
2. facebook_cross_platform
3. google_cross_platform
```

To add a new template:

1. Create a new json file in the `templates` folder. 
2. add all the params you want to include on your link
3. define that template as your `active_template` in settings.json

