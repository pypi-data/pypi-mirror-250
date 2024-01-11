# yabci - yet another beancount importer

**yabci** (*yet another beancount importer*) is a flexible & extensible [importer for beancount](https://beancount.github.io/docs/importing_external_data.html) (v2), aiming to replace any standard importer without the need to write custom python code.

Its goal is to support as many import formats as possible, while giving you complete control over the conversion into beancount transactions. The conversion is configured by a config, eliminating the need to write custom python code (but which can be used for complex cases)

## Motivation

There are a lot of beancount importers available. Most of them are specifically tailored for a certain format of certain banks or payment providers. And depending on the author's needs, they map import data to beancount transactions in a certain way. Any additional data from your import files is discarded. If you want to finetune beancount transactions or want to use more advanced features like tags, most of the time you are out of luck.

yabci tries to fill this gap: yabci is format-agnostic regarding input files (everything the underlying [benedict supports](https://github.com/fabiocaccamo/python-benedict), which means CSV, JSON, and [more](#todo)). On the beancount side, yabci supports all transaction properties, postings & balances (from the basic ones like date, payee, narration to tags, meta data & links).

The only thing to do for the end user is to tell yabci, which input field shall be mapped into which beancount fields. yabci takes care of the rest, like parsing dates from strings, parsing numbers with currencies, duplicate detection, etc.

**Features**:

- supports any input file format
    - a lot of formats out of the box, such as csv & json (anything that the fantastic [benedict](https://github.com/fabiocaccamo/python-benedict) supports)
    - anything else can used by implementing a custom python function to convert the input file into a nested `dict`
- complete control: you can decide specifically how your input data gets transformed into a beancount transaction
    + support for all beancount transaction properties (date, flag, payee, narration, tags, links)
    + support for all posting properties (account, amount, cost, price, flag)
    + support for transaction & post meta data
    + support for multiple postings per transaction
    + any field can be transformed while importing it, giving you total control over the output
- conversion of data types: no more custom date or number parsing
- duplication detection (optionally using existing identifiers in your input data)

## Getting started with beancount importers

*If you already know beancount importers, you can skip to [Getting started with yabci]*

To import external data into beancount, beancount uses so-called *importers*. You can install them from pip or write them on your own. If you are reading this, you probably want to use *yabci* to create one on your own.

To tell beancount about your importers, you have to create *importer config*. This is a python file (with the ending `.py`) with the necessary importer code. While example importers can become complicated very easily (see the example at [https://github.com/beancount/beancount/blob/v2/examples/ingest/office/importers/utrade/utrade_csv.py]), importers using *yabci* should look a lot simpler.

If you have your importer ready, you can run the beancount command `bean-extract` on your import files. `bean-extract` will use your importer to generate beancount transactions, which you can paste / redirect into your `*.beancount` files.

## Getting started with yabci

(if you want to see some real world code, check the repository's `examples` folder)

Say, you have the following csv from your bank, and want to import it into beancount:

*bank-foo.csv*
```csv
"ID","Datetime","Note","Type","From","To","Amount"
"2394198259925614643","2017-04-25T03:15:53","foo service","Payment","Brian Taylor","Foo company","-220"
"9571985041865770691","2017-06-05T23:25:11","by debit card-OTHPG 063441 bar service","Charge","Brian Taylor","Bar restaurant","-140"
```

Or maybe you have the data as *json* (*yabci* treats both input formats the same):

<details>
<summary>*bank-foo.json*</summary>

```json
{
    "values": [
        {
            "ID": "2394198259925614643",
            "Datetime": "2017-04-25T03:15:53",
            "Note": "foo service",
            "Type": "Payment",
            "From": "Brian Taylor",
            "To": "Foo company",
            "Amount": "-220"
        },
        {
            "ID": "9571985041865770691",
            "Datetime": "2017-06-05T23:25:11",
            "Note": "by debit card-OTHPG 063441 bar service",
            "Type": "Charge",
            "From": "Brian Taylor",
            "To": "Bar restaurant",
            "Amount": "-140"
        }
    ]
}
```
</details>

You want to import that data into beancount, with the following requirements

- transaction date shall obviously be taken from `"Datetime"`
- payee shall be taken from `"To"`
- description shall be a combination of `"Type"` and `"Note"`
- flag shall always be `*`
- transaction meta data shall contain the value of `"ID"`
- transaction shall be tagged with `#sampleimporter`
- you want one posting for the account `Assets:FooBank:Account1` containing `"Amount"` as €
- you want another posting for the account `Expenses:Misc`


With an according yabci config (see below), beancount can import & map your import data like this:
```sh
$ bean-extract config.py sample.csv

2017-04-25 * "Foo company" "(Payment): foo service" #sampleimporter
  id: "2394198259925614643"
  Assets:FooBank:Account1  -220 EUR
  Expenses:Misc

2017-06-05 * "Bar restaurant" "(Charge): by debit card-OTHPG 063441 bar service" #sampleimporter
  id: "9571985041865770691"
  Assets:FooBank:Account1  -140 EUR
  Expenses:Misc
```

Now how does this work?

Like for any beancount importer, you have to specify how the data in the bank's export files shall be mapped into beancount transactions.

Following yabci config can be used to get the results above:

*config.py*
```py
import yabci

CONFIG = [
    yabci.Importer(
        target_account="Assets:FooBank:Account1",

        # where to find the list of transactions (csv files can use "values")
        mapping_transactions="values",

        mapping_transaction={

            # regular str: use the value of "TransactionDate" in input data
            "date": "Datetime",
            "payee": "To",

            # if you want a fixed string, use type bytes (since regular strings
            # would be interpreted as dict key)
            "flag": b"*",

            # for more complex cases, you can use lambda functions. The function
            # receives the (complete) raw input dict as single argument
            "narration": lambda data: "(%s): %s" % (data.get("Type"), data.get("Note")),

            # if you pass a dict, the dict itself will be mapped again (with the
            # same logic as above)
            "meta": {
                "id": "ID",
            },

            # same goes for sets
            "tags": {b"sampleimporter"},

            # same goes for lists of dicts: each dict will be mapped again
            "postings": [
                {
                    "amount": lambda data: [data.get("Amount"), "EUR"],
                },
                {
                    "account": b"Expenses:Misc",
                },
            ],
        }
    ),
]

```

Notes:

- `"date"` only accepts `datetime.date`. If a string is passed, *yabci* tries to convert it via [dateutil.parser](https://dateutil.readthedocs.io/en/stable/parser.html)
- `"amount"` must be a 2-element list, containing numeric amount & currency

## More advanced features

### benedict arguments

If you need to pass special parameters to benedict (for example how your CSV is formatted), you can use the config entry `benedict_kwargs`. This dict gets passed to benedict and determines how you input file is parsed. See [](https://github.com/fabiocaccamo/python-benedict#io-methods) for available options.

Example for passing options about CSV format:
```py
CONFIG = [
    yabci.Importer(
        benedict_kwargs={"delimiter": ";"},
        # ...
    )
]
```

### date parsing

Transaction dates are parsed using [dateutil](https://dateutil.readthedocs.io/en/stable/parser.html#dateutil.parser.parse). If you need to pass certain options to `parse()`, you can use `        parse_date_options`:

Example for european dates (`"01.06.2023"` is parsed as "January 6th" by default, if you want it to be interpreted as `"June 1st"`, you have to pass the `dayfirst` option)
```py
CONFIG = [
    yabci.Importer(
        parse_date_options={"dayfirst": True},
        # ...
    )
]
```

## Unsupported ìnput data formats

If you want to import data from formats which are not [supported by benedict](https://github.com/fabiocaccamo/python-benedict), you can define a `prepare_data` method. This method should transform the input file into a (nested) dictionary which benedict can parse afterwards. Since you can use arbitrary python code here, you should be able to use *yabci* for really any file formats.


### `.json` inside a zip file (as found in moneywallet)

[moneywallet](https://github.com/AndreAle94/moneywallet) `.mwbx` backup files are zip files which contain a `database.json` file. You can support this format:

```python
def read_json_from_zip(filename, pattern):
    import zipfile
    import json
    import re
    with zipfile.ZipFile(filename, "r") as z:
        for filename in z.namelist():
            if re.match(pattern, filename):
                with z.open(filename) as f:
                    return json.loads(f.read())

CONFIG = [
    yabci.Importer(
        prepare_data=lambda filename: read_json_from_zip(filename, r".*database\.json"),
        # ...
    )
]
```

### CSVs with special encoding

Benedict tries to read CSVs with the system encoding (probably `utf-8`), and will choke on different encodings. If your CSV uses a different encoding, you have to read the CSV into `dict` explicitly:

```python
# https://docs.python.org/3/library/csv.html
def read_csv_windows1252(filename):
    import csv
    values = []
    with open(filename, newline='', encoding='windows-1252') as f:
        reader = csv.DictReader(f)
        for row in reader:
            values.append(row)

    return {"values": values}


CONFIG = [
    yabci.Importer(
        prepare_data=read_csv_windows1252,
        # ...
    )
]
```


## Detecting duplicate transactions

If your input data contains some form of unique id, you can use it to prevent importing the same transaction twice.

Therefore, you must import the unique id into a meta field, and let *yabci* know it should be used to identifiy duplicates. Beancount will not re-import these transactions.

*confiy.py*
```py
import yabci
from beancount.ingest.scripts_utils import ingest

yabci.Importer({
    # ...
    "duplication_key": "meta.duplication_key",

    "mapping": {
        # ...
        "transaction": {
            # ...
            "meta": {
                # use the value of "transaction_id"
                "duplication_key": "transaction_id",
            },
        },
    },
})

# beancount uses its own duplicate detection by default, which interferes with
# yabci's approach. Disable it therefore. The variable `HOOKS` is needed to
# disable it within fava as well, see
# https://github.com/beancount/fava/issues/1197 and
# https://github.com/beancount/fava/issues/1184

HOOKS = []

if __name__ == "main":
    ingest(CONFIG, hooks=[])

```

This creates transactions with meta data `duplication_key`:

```beancount
2023-01-01 * "foo transaction"
  duplication_key: "8461dd69-e9eb-4deb-9014-b5ffd082ede0"
  ...

2023-01-02 * "bar transaction"
  duplication_key: "be8595a1-c0af-496f-87ac-7ff67e6d757b"
  ...

```

The next time you try to import the same transaction, beancount will identify it
as duplicate & comment the transactions, so they will not be imported a second
time.

```beancount
; 2023-01-01 * "foo transaction"
;   duplication_key: "8461dd69-e9eb-4deb-9014-b5ffd082ede0"
;   ...

; 2023-01-02 * "bar transaction"
;   duplication_key: "be8595a1-c0af-496f-87ac-7ff67e6d757b"
;   ...

```

### Duplicate detection without suitable identifer field

If your input data contains no suitable field, you can also fallback to hashing the complete raw transaction data:

```py
"duplication_key": lambda data: yabci.utils.hash_str(data.dump())
``` 
