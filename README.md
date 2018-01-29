# About Tock blocks

A simple command line tool generate reports around user utilization using tock data. 
This command line can generate a complete csv utilization report or can print out to the console users main projects were in 5 percentage point increments. 

## Installation
```
git clone https://github.com/18F/tock-blocks.git

cd tock-blocks
```

## Running the Regular Utilization Report
1. Set TOCK_API_KEY environment variable with `export TOCK_API_KEY=<your_key>`. You can obtain an API Key by requesting one from the Tock dev team.
2. Navigate to the tock-blocks directory: `cd tock-blocks`
3. Make sure your terminal is running in Python 3. Verify by checking `pyenv local`
4. Running the command `python server.py`.  This will generate a utilization report for a list of users supplied in `users.csv` for the past year by pulling in information from tock and then output it as a `.csv` file named `utilization-summary-YYYY-MM-DD.csv`.
5. Additional options:
    * `-p tock-blocks`: run the `tock-blocks` command line summary of the application
    * `-b','--beginmonth`: choose a start date other than the default (a full year ago) but beginning month can be up to a year ago. Months must be the full name with capitalization i.e "September" or "July".
    * `'-l','--lastmonth'`: choose a start date other than the default (current month)
    * `'-f', '--file'`: a json file to process the information.
6. Upload file to google drive, outfile.csv.
7. Make sure to add a column to the right of the last month in the existing google utilization sheet. It needs to be to the right to maintain the formatting of months rather than the average column.
8. Copy and paste (only highlighting A1 in the exiting spreadsheet) from outfile.csv to existing Acqstack utilization file.


## Run the tock blocks

`python server.py -p tock-blocks -u firstName.lastName -s YYYY-MM-DD -e YYYY-MM-DD`

It will then print out an array of your major blocks of projects (rounded to the nearest 5%), as well of a list of other projects that are greater than 2.5% of your time.

### Optional Parameters
`-u` users: the user or users you would like to find tock entries for.

`-f` file: The tock file csv you would like to use. This will default to `timecards_bulk.json`.

`-s` start date: The date that you would like to look at tock entries beginning after this date.

`-e` end date: The date that you would like to look at tock entries ending before this date.

`-v` verbose: Prints additional debugging information to the command line.

`-d` display format: Display in a readable format or into markdown

`-n` no leave: remove holidays, annual and award leave from the report

`-b` begin month, for the utilization summary: which month to start at

`-l` last month: the final month for the utilization summary



## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
