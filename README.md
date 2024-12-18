# Fraud Detection Application

## Tech Stack
I used pandas and streamlit because it makes it easy to read the CSV, access data, and apply operations on it. Streamlit helps in creating a nice GUI to display the information and the fraud detected data. 

## Explanation of the Rules
I made 5 rules for this application, including a bonus one at the end, so technically 6. I will be explaining why I made each rule. 

1. Detecting High Transaction Amounts: I chose this rule because credit cards have limits, and all banks apply this rule. Different people have different limits, but in this case I kept the threshold to $500 for a single transaction for simplicity.
A high transaction amount detection is critical in ensuring fraudsters do not spend high amounts on your card. High transaction amounts are generally seen as suspicious and have great finanical risk for the user. 

2. Detecting Rapid Transactions: I chose this rule because normal credit card users do not immediately use their card after a transaction is already completed (within 2 mins). Fraudsters will abuse credit cards and make many transactions before a card is declined
or deemed suspicious. This is a good rule to flag a scammer who would make immediate transactions.

3. Detecting Excessive Transactions in a 24 Hour Window: I chose this rule because normal credit card holders do not make more than 7 transactions in a day. Fraudsters or scammers are likely to spend the credit card a lot and try to buy a lot of products online. It also
encourages healthy credit card usage in general. A general pattern in fraudsters or scammers is that they use the stolen card very frequently within a 24 hour window. This measure helps alert the user and the bank about the fraudulent transactions. 

4. Detecting Duplicate Transactions: I chose this rule because normal credit card holders do not buy the same exact thing more than once given a certain time frame. I put the window frame at 3 minutes. It does not make sense for a normal user to buy something and then buy
that again within 3 minutes. The time frame could be extended for a day or within some hours, but I have kept it as is to encourage good spending habits as well. 

5. Detecting transactions near threshold: I chose this rule in the case if scammers or fraudsters know the credit card limit. Since they know the threshold, they are likely to spend just below the amount to bypass rule 1. I put a delta of $30 below the threshold to throw fraudsters
off and it is something that they would not expect. This rule overlaps with rule 1, so I put another bonus rule for this application. 

Bonus Rule - Detecting Frequent Merchant Transactions: I chose this rule because a normal credit card holder doesn't buy from the same merchant more than 3 times in a day. Even for food and every day expenses, normal people do not have more than 3 transactions at the same place in a single day. This
will help flag scammers or fraudsters who abuse credit card at the same merchant, online or in person. 

Overall: These plans are solid in detecting fraud transactions. These rules cover many edge cases, and could be tweaked depending on user history, geographical information, etc. 

## Testing the Application
I provided 2 test CSVs, so that anyone can quickly test the application. For testing, make sure to have pandas and streamlit installed.
To install Pandas, use pip install pandas
To install Streamlit, use pip install streamlit.
Run the application using: streamlit run app.py
