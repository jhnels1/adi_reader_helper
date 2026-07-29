# adi_reader_helper

Helper script to the repo [adinstruments_sdk_python](https://github.com/JimHokanson/adinstruments_sdk_python). Takes the raw output and formats it as a single data frame containing all blocks, including global time data and comments.

### Usage Example

```
import clean_adi
df = clean_adi.df_from_file("some_labchart_file.adicht")
```

**NOTE**: Channels derived from raw channels in LabChart (e.g. Heart Rate, MAP, ...) are not load correctly. May be an issue with adinstruments_sdk_python.
