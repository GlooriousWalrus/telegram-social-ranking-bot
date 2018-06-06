from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import logging
from base import Session, engine, Base
from users import Users

# Generate database schema
Base.metadata.create_all(engine)

# Create a new session
session = Session()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def populatetable(update):
    newuser = Users(update.message.from_user.id, 500)
    session.add(newuser)
    session.commit()
    update.message.reply_text('{name}, your profile has been created with a default score of 500'
                              .format(name=update.message.from_user.first_name))


def changescore(update, points):
    data = session.query(Users) \
        .filter(Users.telegramid == update.message.from_user.id) \
        .first()

    if data is None:
        populatetable(update)
        data = session.query(Users) \
            .filter(Users.telegramid == update.message.from_user.id) \
            .first()

    data.score = data.score + points
    session.commit()
    update.message.reply_text('{name}, your score is now {score}'.
                              format(name=update.message.from_user.first_name, score=data.score))


def queryscore(update):
    userscore = session.query(Users) \
        .filter(Users.telegramid == update.message.from_user.id) \
        .first()
    if userscore is None:
        populatetable(update)
        userscore = session.query(Users) \
            .filter(Users.telegramid == update.message.from_user.id) \
            .first()
    # print('{} recieved'.format(userscore.score))

    return userscore.score


def thottery(bot, update):
    try:
        if (update.message.text.lower().find("thot") != -1):
            update.message.reply_text('{}: Thottery detected! Social rank score reduced by 5 points!'
                                      .format(update.message.from_user.first_name))
            changescore(update, -5)


    except UnicodeEncodeError:
        update.message.reply_text(
            '{}: Unintelligeble text detected! -2 points to social score'.format(update.message.from_user.first_name))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def test(bot, update):
    update.message.reply_text('test')


def getscore(bot, update):
    update.message.reply_text(
        'PROFILE:\nFirst name: {fname}\nLast name: {lname}\nSocial ID: {sn}\nSocial Rank Score: {score}'. \
            format(fname=update.message.from_user.first_name,
                   lname=update.message.from_user.last_name,
                   sn=update.message.from_user.id,
                   score=queryscore(update)))


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("TOKEN GOES HERE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("test", test))
    dp.add_handler(CommandHandler("score", getscore))
    dp.add_handler(MessageHandler(Filters.text, thottery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
