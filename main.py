import os.path
import argparse

from scryfall_api import *
from database import *
import boto3
from PIL import Image
from mtgsdk import Card

LANGUAGES_MAPPING = {
    'fr': 'french',
    'en': 'english'
}

rekognition = boto3.client('rekognition')
comprehend = boto3.client('comprehend')


def resize_image(img):
    """
    For optimization purposes, we should resize images to acceptable sizes
    """
    img_name, img_ext = os.path.splitext(img)
    image = Image.open(img)

    image_exif = dict(image._getexif().items())

    # Image needs to be re-oriented correctly before saving
    # We hardcode 274 as the exif value for image's orientation
    if image_exif[274] == 3:
        image = image.rotate(180, expand=True)
    elif image_exif[274] == 6:
        image = image.rotate(270, expand=True)
    elif image_exif[274] == 8:
        image = image.rotate(90, expand=True)

    # We can add some more image processing here if the image is still too big
    resized_image = img_name + '_resized' + img_ext
    image.save(resized_image)
    return resized_image

    # To automatically retrieve the exif value for image's orientation
    # from PIL constants
    # for exif_id, tag in ExifTags.TAGS.items():
    #     if tag == 'Orientation':
    #         break


def detect_language(text):
    """ Use aws comprehend API to detect language in a text"""
    # Detect the dominant language of the whole text of the card
    languages_detect = comprehend.detect_dominant_language(Text=text)
    (best_language, best_score) = ('fr', 0)
    for language in languages_detect['Languages']:
        if language['Score'] > best_score:
            best_score = language['Score']
            best_language = language['LanguageCode']

    return best_language


def translate_card(card_name, language='french'):
    """ Translate an MTG card name into the english name"""
    if language == 'english':
        # Don't translate from english
        return card_name

    cards = Card.where(name=card_name).where(language=language).all()

    # TODO: Check how to handle correctly "no translation found" errors
    try:
        return cards[0].name
    except IndexError:
        return


def process_image(image_file):
    print("Resizing the image")
    usable_image = resize_image(image_file)

    # Call text recognition service
    print("Calling AWS Rekognition service for text detection")
    f = open(usable_image, 'rb')
    aws_res = rekognition.detect_text(Image={'Bytes': f.read()})
    text_detect = aws_res['TextDetections']

    # Process the text detected as you want
    first_line = ""
    full_text = ""
    for text in text_detect:
        # Also Type WORD available
        if text['Type'] == 'LINE' and text['Id'] == 0:
            # Fetch the first line of text
            first_line = text['DetectedText']

        full_text += ' ' + text['DetectedText']

    print("Calling Comprehend AWS service to detect the language")
    # Send the full text for better language detection
    card_language = detect_language(full_text)

    # Remove the last word of the first line, as it is the manacost
    card_name = ' '.join(first_line.split(' ')[:-1])

    # Translate it in english
    print("Translating the card name with mtgsdk")
    card_name_en = translate_card(card_name,
                                  language=LANGUAGES_MAPPING[card_language])

    # Check if this card already exists in our db
    if card_exists(card_name_en):
        print("Card {} already looked up, update quantity and skip".format(
              card_name_en))
        update_card_qty(card_name_en)
    else:
        # Look it up in scryfall API
        try:
            print("Finally fetching the card price from Scryfall API")
            mtg_card = search_card(card_name_en)

            price_eur = mtg_card['eur']
            price_usd = mtg_card['usd']

            print("Found {} at a price of {} EUR and {} USD".format(
                mtg_card['name'], price_eur, price_usd))

            insert_card(card_name_en, price_eur, price_usd)
        except ScryfallAPIError as e:
            print(e)

    try:
        f.close()
        os.remove(usable_image)
    except OSError as e:
        print(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-img', type=str,
                       help='The image of the MTG card to lookup')
    group.add_argument('-dir', type=str,
                       help='The folder where the images are stored')
    parser.add_argument('-export', action='store_true',
                        help='Exports the final results in csv')
    args = parser.parse_args()

    img_name = args.img
    dir_name = args.dir

    if dir_name:
        for file in os.listdir(dir_name):
            print("Now processing {}".format(file))
            process_image(dir_name + '\\' + file)
    elif img_name:
        process_image(img_name)

    if args.export:
        csv_name = 'results.csv'
        export_cards_as_csv(csv_name)
        print("Results exported into {}".format(csv_name))
