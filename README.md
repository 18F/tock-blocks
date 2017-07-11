# About Tock blocks

A simple command line tool to see what your main projects were in 5 percentage point increments

## Installation
```
git clone https://github.com/18F/tock-blocks.git

cd tock-blocks
```

Download the Raw data in .csv from `https://tock.18f.gov/reports/` to your `tock-blocks` directory
It is easiest to do this in browser, because otherwise you will have to authenticate into tock.

## Run the tock blocks

`python server.py -u firstName.lastName -s YYYY-MM-DD -e YYYY-MM-DD`

It will then print out an array of your major blocks of projects (rounded to the nearest 5%), as well of a list of other projects that are greater than 2.5% of your time.

### Optional Parameters
`-u` users: the user or users you would like to find tock entries for.

`-f` file: The tock file csv you would like to use. This will default to `timecards_bulk.csv`.

`-s` start date: The date that you would like to look at tock entries beginning after this date.

`-e` end date: The date that you would like to look at tock entries ending before this date.

`-v` verbose: Prints additional debugging information to the command line.

'-d' display format: Display in a readable format or into markdown

'-l' exclude leave: remove holidays, annual and award leave from the report

## Public domain

This project is in the worldwide [public domain](LICENSE.md). As stated in [CONTRIBUTING](CONTRIBUTING.md):

> This project is in the public domain within the United States, and copyright and related rights in the work worldwide are waived through the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
>
> All contributions to this project will be released under the CC0 dedication. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest.
