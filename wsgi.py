import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import ( User, Listing, Game)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    sally = User(username='sally', password='sallypass')
    rob = User(username='rob', password='robpass')
    frogger = Game(title='Frogger')
    gta = Game(title='GTA')
    apex = Game(title='Apex Legends')
    db.session.add_all([sally, rob, frogger, gta, apex])
    db.session.commit()
    print("Database initialized!")

@app.cli.command("list-game", help="lets a user list a game")
def list_game():
    games = Game.query.all()
    print(games)
    game_id = input("Enter the id of the game you want to list: ")
    users = User.query.all()
    print(users)
    user_id = input("Enter the user id performing the listing: ")

    game = Game.query.get(game_id)
    user = User.query.get(user_id)

    price = input("Enter the price you want to list the game for: ")
    condition = input("Enter the condition of the game (new, used, etc): ")

    if game and user:
        user.list_game(game, price, condition)
        print(f"Game '{game.title}' listed successfully!")
    else:
        print("Invalid game or user ID.")

@app.cli.command("get-listings", help="shows all available listings")
def get_listings():
    listings = Listing.query.filter_by(available=True).all()
    for listing in listings:
        print(f" - {listing.game.title} (Listed by: {listing.user.username}) - ${listing.price}, Condition: {listing.condition}")

@app.cli.command("change-availability", help="change the availability of a listing")
def change_availability():
    listings = Listing.query.all()
    for listing in listings:
        print(f"ID: {listing.listing_id} - {listing.game.title} (Listed by: {listing.user.username}) - ${listing.price}, Condition: {listing.condition}, Available: {listing.available}")
    listing_id = input("Enter the id of the listing you want to change: ")
    listing = Listing.query.get(listing_id)
    if listing:
        listing.available = not listing.available
        db.session.commit()
        print(f"Listing '{listing.game.title}' availability changed to {listing.available}.")
    else:
        print("Invalid listing ID.")

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)