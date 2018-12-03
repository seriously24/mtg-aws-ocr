# mtg-aws-ocr
Small python3 project to recognize Magic The Gathering (MTG) cards from pictures taken, and lookup their prices on the market.  

## APIs used
* **pillow** (image processing) : [GitHub](https://github.com/python-pillow/Pillow)
* **AWS Rekognition** (text recognition) [documentation](https://docs.aws.amazon.com/rekognition/latest/dg/getting-started.html)
* **AWS Comprehend** (language recognition) [documentation](https://docs.aws.amazon.com/comprehend/latest/dg/getting-started.html)
* **mtgsdk** (card name translation) [GitHub](https://github.com/MagicTheGathering/mtg-sdk-python)
* **Scryfall REST API** (prices lookup) [documentation](https://scryfall.com/docs/api)

## How to use it
Clone the repo
```bash
$ git clone https://github.com/seriously24/mtg-aws-ocr
$ cd mtg-aws-ocr
```
Install python dependencies
```bash
$ pip install -r requirements.txt
```
Check that aws is correctly running and configured for your AWS account
```bash
$ aws configure
AWS Access Key ID [********************]:
AWS Secret Access Key [********************]:
Default region name [eu-west-1]:
Default output format [None]:
```
Init the sqlite3 database
```bash
$ python database.py -init
```
Run the main script, either for 1 image, or for a folder containing the images
```bash
$ python main.py -img "D:\My Images\OCR\my_best_mtg_card.jpg"
$ python main.py -dir "D:\My Images\OCR"
```
All the results go into _mtg_cards.db_, that you can open with an SQLite3 browser. Or you can choose to export the results as an Excel-like CSV.
```bash
$ python main.py -img "D:\My Images\OCR\my_best_mtg_card.jpg" -export
$ python main.py -dir "D:\My Images\OCR" -export
```
If anything went wrong and you want to start all over again, you can reset the database
```bash
$ python database.py -reset
```

## About AWS
You can create a 1-year free account for AWS [here](https://portal.aws.amazon.com/billing/signup#/start). You will also need to create access tokens and IAM users with access to Rekognition and Comprehend Services. Please refer to AWS doc mentioned previously.

## Limitation
This script can only fetch prices for the last edition of the card, there is no way for it to know the actual card's edition for now.
