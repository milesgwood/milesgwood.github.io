---
layout: default
---

# Tips

Always use the `Open Windows` tab on the far left panel. The shortcuts are useless.

Make sure you view reports on a `cash` basis, not accrual. `Cash` style means you only log it when money changes hands. You don't log income when you invoice it. You log it when you get the check.  

You can see the entire history of one account (say my NFCU checking account or the Expenses to be repaid accounts.) That way you can `view all transactions for that specific account`

# K-1 payments to fix logs

Best way is to add the transactions with a real transaction from my bank account to me. That said I have so many purchases that happen outside of the Biz Bank account that I frequently need to re-emburse accounts like `Miles General Transfers` (which should be closed soon) and mainly the `reimbursed expenses account`


Need to be manually entered in a check entry `ctrl + w` where:
----

- Bank Account is where the money needs to come from. For example it could come form
  - Miles General Transfers - needs to be empty
  - NFCU Checking account
- Account under Expenses is `Miles K-1 Distributions EOY`
- Memo `FY 2017 K-1 Pass Through Distribution of profits - not subject to payroll taxes - 1040 needs a K-1 attached`
- Amount is the ordinary income on your personal k-1 after you compete your 1120s

# Chart of Accounts

I deleted the two banks that had no real data in them. That was the Suntrust and wells fargo bank accounts I opened for the purpose of simply getting a bank bonus. I had to move their transaction entries to my personal NFCU account which represents transfers that are not expenses.

# View all Expenses

There is a view of everything under reports. `Reports > Company Financial > Profit Loss`. This is the best view for finding things that you missed. You can specify the time period just make sure the use the `cash` report basis.

# View Payroll entries so far

To view the payroll entries so far this year. They should be recorded when you update the bank feeds and I should be listed as the payee.

`Reports > Memorized reports > payroll 2019`

# Journal Entry

Journal entries are NOT expenses!!! These are corrections to transfers you have made in the past.

Memorized Reports > Accountant > General Ledger

This will let you see all of the Miles General Transfer foolishness.

# K-1 Payments

 K-1 is how you pass through the biz income to your personal return. These payments are not subject to payroll taxes, just income tax.  On your personal 1040 `form 8453-s` the ordinary business income shows up in `Part 1 Line 3` Ordinary business income.

 On the `K-1 of your 1020S` the Ordinary income is in `part 3 line 1` - ordinary business income.

2018 - $8342 is accurate
2019 - $2338 - not yet paid out as of 3/24/20

The currently existing journal entries are transfers or notes of that a K-1 payment was paid. The payer account should be your business checking account. Right now it is not.

These journal entries are in error. They should be coming out of the NFCU checking account.


# Add a new expense (Write a check)

- Shortcut `Ctrl + w`
- Select the `Expenses to be reimbursed` account.
- Enter all the info and duplicate the memo on both lines. You can't use shortcuts for select all as that will open chart of accounts.
- Make sure to attach any photos to the entry before saving.
- Hit save and close.

# Find an expense

Go to chart of accounts and right click on the account you're interested in. Then hit `find` and search through the memo fields.

# Create Invoice

- Shortcut `ctrl i`
- Enter all the details of the invoice especially the `PO number` and the `vender ID`.
- Make sure to set the Item to `Build Cooper Center Websites`
- Print the invoice and save it as a PDF to send it.

Current invoice has paid out 5k of the.

PayPal invoices may deduct a fee from the total payment. Make sure to only record payment for the portion that you receive. In the payment entry (you can navigate to already saved payments through the Customer shortcut) you should set the payment to what you actually received and then select the "write off the extra amount" in the Underpayment box that appears.

# Sync with Bank account

- Go to the `bank feeds` tab to see the last date you entered transactions (8/31/2019) - cc payment made and not logged yet that day
- Login to bank account
- Filter transactions to all the ones that aren't entered into QB yet
- Download the .qbo file and click it to import it
- Review the transactions in the bank feeds tab

# Set account for Credit Card payments

In the `CC transactions` (not the checking account) set the Account to `NFCU Checking Account` as that is the account that this payment came from. We are deducting a payment that came from the NFCU checking account. Leave the Payee blank.

# Match Payment to already created invoice

- Import the transactions by downloading the transactions as described above.
- Click on the eDeposit transaction and go to `more options/details`
- In that window select the matching invoices that are paid
- If you go to income tracker now you should see the bill is no longer overdue

# How to handle PPP loan in quickbooks

[PPP Quickbooks Tutorial](https://quickbooks.intuit.com/learn-support/en-us/banking/how-do-i-enter-the-ppp-loan-into-my-deposit/00/542685)

Get PPP forgiven and [decrease the liability in QB with a journal entry](https://www.youtube.com/watch?v=2eTJBceecuM)

I transferred money from Savings to Checking. I set the account of those 3 transactions to NFCU Savings since that is the account the payment came from. Payee got left blank. It's simply logged as a tranfer from Savings to checking. The transfer to checking has PPP in the memo.
