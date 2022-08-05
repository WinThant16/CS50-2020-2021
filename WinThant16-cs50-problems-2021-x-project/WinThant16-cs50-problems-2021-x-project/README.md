# Revamped C$50 Finance
#### Video Demo: <https://youtu.be/1rXRys0zUV8>
#### Description:
Improvements made to C$50 Finance.
The navigation tab, C$50 Finance is now changed to C$50 Stock Finance.
Created the option for Topping-up user's cash, and the ability for the user to view the top-up history.
Created a new tab, called C$50 Personal Finance where users can keep track of their personal payments.
The user is able to record income or expense payments under the add payment tab.
The user will also be able to view the recorded incomes or expense payments under the tab- Payment History.
I have also added footers/mini descriptions of what each tab in the website is designed to do, to make it more user-friendly.
In this way, I believe the user will have an easier and more enjoyable time navigating the website.
Most noticeably, I have spent a considerable amount of time styling up the html pages. Using different font-styles and formats for tables.
I have also ingrained the hover ability for the buttons/tabs in the website, so that they flash a different color when a cursor is hovered over them.
Some light adjustments to flash messages were made, and they were styled up a bit.
In addition, the user now has a dark navigation bar as well as colorful user input boxes.
I debated on whether to add the option of transferring a user's personal income to stocks table in order to buy more stocks, but decided not to as it might undermine the presence of the topup function that I have added.

In the templates folder, I have added multiple new html files, for the new tabs that were created in the webpage.
layout2.html is a modified copy of layout.html, used as a default layout page for C$50 Personal Finance tabs, namely personalfinance.html and pfinancetable.html
personalfinance.html is where the user can enter their personal incomes or expenses into the database.
pfinancetable.html is where the user can view the previously entered personal incomes or expenses.


apology.html displays apology messages to the user.
buy.html allows the user to buy stocks.
history.html displays the stock transaction history to the user.
index.html is the home page for the user that displays cash and current stocks owned by the user.
layout.html is the default layout page for when the website starts. I have also imported new fonts from google into this html.
layout2.html is a modified copy of layout.html, used as a default layout page for C$50 Personal Finance tabs, namely personalfinance.html and pfinancetable.html
login.html allows the user to log-in to the website and access it.
quote.html allows the user to look up stock information.
quoted.html displays the information of the stock that was looked-up.
register.html is where the user has to register his account when first creating it.
sell.html is where the user can sell the stocks that he has previously bought.
topup.html is a new html page I have created where the user can enter an amount of cash to top-up to his remaining cash.
topuphistory.html is a new html page created to display top-up history of the user.

application.py and helpers.py are python files where the code has been written to make it possible for the website to run.
finance.db is a database containing multiple tables that store information for the user.
finance.db stores five tables, namely users, users_stocks, transactions, topups and pfinance.
The tables are updated by sqlite3 commands in application.py and are responsible for displaying history, top-ups and personal finance tables.


