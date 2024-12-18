import streamlit as st
import pandas as pd 

def load_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def detect_high_transaction_amount(df, threshold=500):
    flagged = df[df['amount'] > threshold]
    return flagged

def detect_rapid_transactions(df, time_window_seconds=120):
    df = df.sort_values(by=['user_id', 'timestamp'])
    df['time_diff'] = df.groupby('user_id')['timestamp'].diff().dt.total_seconds()
    flagged = df[df['time_diff'] <= time_window_seconds]
    return flagged

def detect_excessive_transactions(df, transaction_limit=7):
     df = df.sort_values(by=['user_id', 'timestamp'])
    
     results = []

     for user_id, group in df.groupby('user_id', group_keys=False): 
        group = group.set_index('timestamp')
        group['transaction_count'] = group.rolling('1d').count()['user_id']
        group = group.reset_index() 
        group['user_id'] = user_id 
        results.append(group)

     df = pd.concat(results)

     flagged = df[df['transaction_count'] > transaction_limit]

     return flagged

def detect_duplicate_transactions(df, time_delta_seconds=180):
    df = df.sort_values(by=['user_id', 'timestamp'])
    df['time_diff'] = df.groupby(['user_id', 'merchant_name', 'amount'])['timestamp'].diff().dt.total_seconds()
    duplicates = df[df['time_diff'].abs() <= time_delta_seconds]
    return duplicates

def detect_near_threshold_transactions(df, threshold=500, delta=30):
    lower_limit = threshold - delta
    flagged = df[(df['amount'] >= lower_limit) & (df['amount'] < threshold)]
    return flagged

def detect_frequent_merchant_transactions(df, transaction_limit=3):
    df = df.sort_values(by=['user_id', 'merchant_name', 'timestamp'])

    def calculate_merchant_count(group):
        group = group.set_index('timestamp')
        group['merchant_count'] = group.rolling('1d').count()['user_id']
        return group.reset_index()

    df = (
        df.groupby(['user_id', 'merchant_name'], group_keys=False)
          .apply(calculate_merchant_count)
    )

    flagged = df[df['merchant_count'] > transaction_limit]

    return flagged

def main():
    st.title("Fraud Detection Application")
    st.write("Upload a transaction CSV file to search for any potential fraud patterns.")

    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file:
        df = load_csv(uploaded_file)
        st.write("### Uploaded Data:")
        st.dataframe(df)

        st.write("## Flagged Transactions:")

        # Rule 1: High Transaction Amounts
        threshold = 500
        high_transactions = detect_high_transaction_amount(df, threshold)
        st.write(f"### 1. High Transaction Amounts (Threshold > ${threshold})")
        if not high_transactions.empty:
            st.dataframe(high_transactions)
        else:
            st.write("No high transaction amounts flagged.")

        # Rule 2: Rapid Transactions
        time_window = 120
        rapid_transactions = detect_rapid_transactions(df, time_window)
        st.write(f"### 2. Rapid Transactions (Time Window ≤ {time_window} seconds)")
        if not rapid_transactions.empty:
            st.dataframe(rapid_transactions)
        else:
            st.write("No rapid transactions flagged.")

        #Rule 3: Transaction limits
        transaction_limit = 10
        excessive_transactions = detect_excessive_transactions(df, transaction_limit)
        st.write(f"### 3. Excessive Transactions in 24-Hour Window (Over {transaction_limit} transactions)")
        if not excessive_transactions.empty:
            st.dataframe(excessive_transactions)
        else:
            st.write("No users flagged for excessive transactions.")
        
        #Rule 4: Detecting duplicate transactions
        duplicate_transactions = detect_duplicate_transactions(df, 180)
        st.write("### 4.Duplicate Transactions") 
        if not duplicate_transactions.empty:
            st.dataframe(duplicate_transactions)
        else:
            st.write("No users flagged for duplicate transactions")
        
        # Rule 5: Near-Threshold Transactions
        delta = 30
        near_threshold_transactions = detect_near_threshold_transactions(df, threshold, delta)
        st.write(f"### 5. Near-Threshold Transactions")
        if not near_threshold_transactions.empty:
            st.dataframe(near_threshold_transactions)
        else:
            st.write("No near-threshold transactions flagged.")

        #Bonus Rule: Detecting frequent merchant transactions
        duplicate_merchants  = detect_frequent_merchant_transactions(df, 4)
        st.write(f"### Bonus: Frequent Merchants")
        if not duplicate_merchants.empty: 
            st.dataframe(duplicate_merchants)
        else:
            st.write("No Frequent Merchants")

if __name__ == "__main__":
    main()
