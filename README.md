# mtg-aws-ocr
Small python3 project to recognize Magic The Gathering (MTG) cards from pictures taken, and lookup their prices on the market.  

## APIs used
* **pillow** (image processing) : [GitHub](https://github.com/python-pillow/Pillow)
* **AWS Rekognition** (text recognition) [documentation](https://docs.aws.amazon.com/rekognition/latest/dg/getting-started.html)
* **AWS Comprehend** (language recognition) [documentation](https://docs.aws.amazon.com/comprehend/latest/dg/getting-started.html)
* **mtgsdk** (card name translation) [GitHub](https://github.com/MagicTheGathering/mtg-sdk-python)
* **Scryfall REST API** (prices lookup) [documentation](https://scryfall.com/docs/api)
