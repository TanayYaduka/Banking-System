
import streamlit as st
from Banking.account import SavingsAccount, CurrentAccount
from Banking.transaction import deposit, withdraw

# Initialize session state
if "accounts" not in st.session_state:
    st.session_state.accounts = {}

if "current_user" not in st.session_state:
    st.session_state.current_user = None


# --- Account Creation ---
def create_account_ui():
    st.subheader("📝 Create a New Account")

    name = st.text_input("👤 Enter your name:")
    acc_type = st.radio("🏦 Select account type:", ("Savings", "Current"))
    initial_deposit = st.number_input("💰 Enter initial deposit:", min_value=0.0, step=100.0)

    if st.button("Create Account"):
        if not name:
            st.error("⚠️ Please enter a name.")
            return

        if acc_type == "Savings":
            account = SavingsAccount(name, initial_deposit)
        else:
            account = CurrentAccount(name, initial_deposit)

        st.session_state.accounts[account.account_counter] = account
        st.success(f"✅ Account created successfully! Your account number is **{account.account_counter}**")


# --- Login ---
def login_ui():
    st.subheader("🔐 Login to Your Account")

    acc_number = st.number_input("🔢 Enter your account number:", min_value=1, step=1)

    if st.button("Login"):
        acc_number = int(acc_number)
        accounts = st.session_state.accounts

        if acc_number in accounts:
            st.session_state.current_user = accounts[acc_number]
            st.session_state.welcome_message = f"✅ Welcome, {accounts[acc_number].name}!"
            st.session_state.do_login_rerun = True
        else:
            st.error("❌ Invalid account number.")


# --- User Dashboard ---
def dashboard_ui():
    user = st.session_state.current_user
    st.subheader(f"👋 Hello, {user.name}")
    st.markdown(f"**Account Number:** {user.account_counter}")
    st.markdown(f"**Account Type:** {'Savings' if isinstance(user, SavingsAccount) else 'Current'}")
    st.markdown(f"**Current Balance:** ₹ {user.get_balance():.2f}")

    st.divider()

    # Show one-time message (e.g. after deposit or withdraw)
    if "action_message" in st.session_state:
        msg = st.session_state.pop("action_message")
        if msg.startswith("✅"):
            st.success(msg)
        elif msg.startswith("❌"):
            st.error(msg)
        else:
            st.info(msg)
    
    # Deposit
    deposit_amount = st.number_input("💵 Deposit Amount:", min_value=0.0, key="deposit")
    if st.button("Deposit"):
        deposit(user, deposit_amount)
        st.session_state.action_message = f"✅ Deposited ₹{deposit_amount:.2f}"
        st.rerun()
        
    # Withdraw
    withdraw_amount = st.number_input("🏧 Withdraw Amount:", min_value=0.0, key="withdraw")
    if st.button("Withdraw"):
        if withdraw(user, withdraw_amount):
            st.session_state.action_message = f"✅ Withdrawn ₹{withdraw_amount:.2f}"
        else:
            st.session_state.action_message = "❌ Insufficient balance."
        st.rerun()

    # Interest Check
    if isinstance(user, SavingsAccount):
        if st.button("📈 Calculate Interest"):
            interest = user.calculate_interest()
            st.info(f"Interest earned: ₹{interest:.2f}")

    # Logout
    if st.button("🔒 Logout"):
        st.session_state.current_user = None
        st.success("Logged out successfully.")
        st.rerun()


# --- Main App ---
def main():
    # Handle one-time rerun after login
    if st.session_state.get("do_login_rerun", False):
        st.session_state.pop("do_login_rerun")
        st.rerun()

    st.set_page_config(page_title="SIT Bank", page_icon="🏦", layout="centered")
    st.title("🏦 Welcome to SIT Bank")
    st.caption("Nagpur Branch | Simple Banking with Streamlit")

    # Display persistent welcome message after login
    if "welcome_message" in st.session_state:
        st.success(st.session_state["welcome_message"])

    # Route to dashboard or login/create account
    if st.session_state.current_user:
        dashboard_ui()
    else:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Create Account"])
        with tab1:
            login_ui()
        with tab2:
            create_account_ui()


if __name__ == "__main__":
    main()
