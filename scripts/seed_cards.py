#!/usr/bin/env python3

import argparse
import boto3
import sys

from botocore.exceptions import BotoCoreError, ClientError
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

class ExpansionType(Enum):
    A1 = "Genetix Apex"
    A1A = "Mythical Island"

class PackType(Enum):
    CHARIZARD = "Charizard"
    MEWTWO = "Mewtwo"
    PIKACHU = "Pikachu"
    ALL = "All"

class RarityType(Enum):
    DIAMOND_1 = "1 Diamond"
    DIAMOND_2 = "2 Diamond"
    DIAMOND_3 = "3 Diamond"
    DIAMOND_4 = "4 Diamond"
    STAR_1 = "1 Star"
    STAR_2 = "2 Star"
    STAR_3 = "3 Star"
    CROWN_1 = "1 Crown"

class CharizardRarityRates(Enum):
    DIAMOND_1 = {
        "card1To3": Decimal('0.02'),
        "card4": Decimal('0'),
        "card5": Decimal('0')
    }
    DIAMOND_2 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.02571'),
        "card5": Decimal('0.01714')
    }
    DIAMOND_3 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00357'),
        "card5": Decimal('0.01429')
    }
    DIAMOND_4 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00333'),
        "card5": Decimal('0.01333')
    }
    STAR_1 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00322'),
        "card5": Decimal('0.01286')
    }
    STAR_2 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.0005'),
        "card5": Decimal('0.002')
    }
    STAR_3 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00222'),
        "card5": Decimal('0.00888')
    }
    CROWN_1 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00013'),
        "card5": Decimal('0.00053')
    }

class MewtwoRarityRates(Enum):
    DIAMOND_1 = {
        "card1To3": Decimal('0.02'),
        "card4": Decimal('0'),
        "card5": Decimal('0')
    }
    DIAMOND_2 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.02571'),
        "card5": Decimal('0.01714')
    }
    DIAMOND_3 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00357'),
        "card5": Decimal('0.01429')
    }
    DIAMOND_4 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00333'),
        "card5": Decimal('0.01333')
    }
    STAR_1 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00322'),
        "card5": Decimal('0.01286')
    }
    STAR_2 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00056'),
        "card5": Decimal('0.00222')
    }
    STAR_3 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00222'),
        "card5": Decimal('0.00888')
    }
    CROWN_1 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00013'),
        "card5": Decimal('0.00053')
    }

class PikachuRarityRates(Enum):
    DIAMOND_1 = {
        "card1To3": Decimal('0.02'),
        "card4": Decimal('0'),
        "card5": Decimal('0')
    }
    DIAMOND_2 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.02571'),
        "card5": Decimal('0.01714')
    }
    DIAMOND_3 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00357'),
        "card5": Decimal('0.01429')
    }
    DIAMOND_4 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00333'),
        "card5": Decimal('0.01333')
    }
    STAR_1 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00322'),
        "card5": Decimal('0.01286')
    }
    STAR_2 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.0005'),
        "card5": Decimal('0.002')  
    }
    STAR_3 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00222'),
        "card5": Decimal('0.00888')
    }
    CROWN_1 = {
        "card1To3": Decimal('0'),
        "card4": Decimal('0.00013'),
        "card5": Decimal('0.00053')
    }

def validate_pack_type(value):
    try:
        return PackType(value)
    except ValueError:
        return argparse.ArgumentTypeError(
            f"Invalid pack type: {value}. Valid options are {[e.value for e in PackType]}"
        )

def validate_rarity_type(value):
    try:
        return RarityType(value)
    except ValueError:
        return argparse.ArgumentTypeError(
            f"Invalid rarity type: {value}. Valid options are {[e.value for e in RarityType]}"
        )

def main(args):
    if args.command == "add":
        add(args.card_id, args.name, args.pack, args.rarity)
    else:
        print("Unknown command. Use --help for usage details.")

def add(card_id, name, pack, rarity):
    expansion_id = card_id.split('-')[0].strip()
    current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    item = {
        "id": card_id,
        "expansion": {
            "id": expansion_id,
            "name": ExpansionType[expansion_id].value,
            "pack": pack.value,
            "rates": {
                PackType.CHARIZARD: CharizardRarityRates,
                PackType.MEWTWO: MewtwoRarityRates,
                PackType.PIKACHU: PikachuRarityRates
            }.get(pack, CharizardRarityRates)[rarity.name].value
        },
        "name": name,
        "rarity": rarity.value,
        # Required
        "createdAt": current_time,
        "updatedAt": current_time
    }

    try:
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("Cards-drk5lskwtje4zjgcchpqfybbya-NONE")
        table.put_item(Item=item)
        print(f"Successfully added {name} to the respective Deck Lab USA DynamoDB table.")
    except (BotoCoreError, ClientError) as e:
        print(f"Unsuccessfully added {name} to the respective Deck Lab USA DynamoDB table.")
        print(e)
    
    # print(item)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="A command-line tool to seed cards in the respective Deck Lab USA DynamoDB table.",
        epilog="Ex. ./seed_cards.py add --name Bulbasaur"
    )

    subparsers = parser.add_subparsers(
        title="Commands",
        dest="command",
        help="Available commands"
    )

    add_parser = subparsers.add_parser("add", help="Add the card to the respective Deck Lab USA DynamoDB table.")
    add_parser.add_argument(
        "--card-id",
        type=str,
        help="ID of the Pokemon.",
        required=True
    )
    add_parser.add_argument(
        "--name",
        type=str,
        help="Name of the Pokemon.",
        required=True
    )
    add_parser.add_argument(
        "--pack",
        type=validate_pack_type,
        help="Pack of the Pokemon.",
        required=True
    )
    add_parser.add_argument(
        "--rarity",
        type=validate_rarity_type,
        help="Rarity of the Pokemon.",
        required=True
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    main(args)
